"""ETL — carga inicial de dados a partir dos CSVs em ``data/`` (RF14, CU13).

Regras aplicadas (docs/regras-de-negocio.md §8):

* Registros inválidos são descartados e contabilizados no relatório final;
* Datas devem estar no formato ISO (YYYY-MM-DD);
* Categorias/transações devem respeitar a compatibilidade de tipos.

Uso::

    python -m cinco_centavos.etl.load_data
    RUN_ETL=true (executa automaticamente no startup da API)
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from cinco_centavos.core.database import SessionLocal, init_db
from cinco_centavos.core.logging import get_logger
from cinco_centavos.models import (
    Account,
    AccountType,
    Category,
    CategoryType,
    Goal,
    Transaction,
    TransactionType,
)
from cinco_centavos.repositories import UserRepository
from cinco_centavos.services import UserService
from cinco_centavos.services.exceptions import ConflictError
from cinco_centavos.schemas.auth import UserRegister

logger = get_logger(__name__)

DATA_DIR = Path(__file__).resolve().parents[3] / "data"


@dataclass
class EtlReport:
    """Relatório de carga: criados x descartados por entidade."""

    created: dict[str, int] = field(default_factory=dict)
    skipped: dict[str, int] = field(default_factory=dict)

    def add_created(self, entity: str, qty: int = 1) -> None:
        self.created[entity] = self.created.get(entity, 0) + qty

    def add_skipped(self, entity: str, qty: int = 1) -> None:
        self.skipped[entity] = self.skipped.get(entity, 0) + qty


def _read_csv(name: str) -> list[dict[str, str]]:
    path = DATA_DIR / name
    if not path.exists():
        logger.warning("etl.file_missing", file=name)
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _parse_decimal(raw: str) -> Decimal:
    try:
        value = Decimal(str(raw).replace(",", "."))
    except InvalidOperation as exc:
        raise ValueError(f"valor monetário inválido: {raw!r}") from exc
    if value <= 0:
        raise ValueError(f"valor deve ser positivo: {raw!r}")
    return value


def _parse_date(raw: str) -> date:
    return date.fromisoformat(raw.strip())


def _load_users(db: Session, report: EtlReport) -> dict[str, int]:
    mapping: dict[str, int] = {}
    service = UserService(db)
    users_repo = UserRepository(db)
    for row in _read_csv("usuarios.csv"):
        email = row.get("email", "").strip()
        try:
            data = UserRegister(
                name=row["name"], email=email, password=row.get("password", "123456")
            )
            user = service.register(data)
            report.add_created("usuarios")
        except ConflictError:
            # Já existe (idempotência): reutiliza sem contar como criado.
            user = users_repo.get_by_email(email)
        except Exception:  # noqa: BLE001 — linha inválida é descartada
            report.add_skipped("usuarios")
            continue
        if user is not None:
            mapping[email] = user.id
    return mapping


def _load_accounts(db: Session, report: EtlReport, users: dict[str, int]) -> None:
    for row in _read_csv("contas.csv"):
        try:
            user_id = users[row["user_email"].strip()]
            name = row["name"].strip()
            exists = db.scalars(
                select(func.count(Account.id)).where(
                    Account.user_id == user_id, Account.name == name
                )
            ).one()
            if exists:
                continue
            db.add(
                Account(
                    user_id=user_id,
                    name=name,
                    type=AccountType[row["type"].strip().upper()],
                    initial_balance=Decimal(row["initial_balance"]),
                )
            )
            report.add_created("contas")
        except (KeyError, ValueError):
            report.add_skipped("contas")
    db.commit()


def _load_categories(db: Session, report: EtlReport, users: dict[str, int]) -> None:
    for row in _read_csv("categorias.csv"):
        try:
            user_id = users[row["user_email"].strip()]
            name = row["name"].strip()
            type_ = CategoryType[row["type"].strip().upper()]
            exists = db.scalars(
                select(func.count(Category.id)).where(
                    Category.user_id == user_id,
                    Category.name == name,
                    Category.type == type_,
                )
            ).one()
            if exists:  # já existe (ex.: categoria padrão criada no registro)
                continue
            db.add(Category(user_id=user_id, name=name, type=type_))
            report.add_created("categorias")
        except (KeyError, ValueError):
            report.add_skipped("categorias")
    db.commit()


def _load_transactions(db: Session, report: EtlReport, users: dict[str, int]) -> None:
    for row in _read_csv("transacoes.csv"):
        try:
            user_id = users[row["user_email"].strip()]
            account = db.scalars(
                select(Account).where(
                    Account.user_id == user_id,
                    Account.name == row["account_name"].strip(),
                )
            ).one()
            category = db.scalars(
                select(Category).where(
                    Category.user_id == user_id,
                    Category.name == row["category_name"].strip(),
                )
            ).one()
            type_ = TransactionType[row["type"].strip().upper()]
            if category.type.value != type_.value:
                raise ValueError("categoria incompatível com o tipo da transação")
            parsed_date = _parse_date(row["date"])
            exists = db.scalars(
                select(func.count(Transaction.id)).where(
                    Transaction.account_id == account.id,
                    Transaction.description == row["description"].strip(),
                    Transaction.date == parsed_date,
                )
            ).one()
            if exists:
                continue
            db.add(
                Transaction(
                    account_id=account.id,
                    category_id=category.id,
                    description=row["description"].strip(),
                    amount=_parse_decimal(row["amount"]),
                    type=type_,
                    date=parsed_date,
                )
            )
            report.add_created("transacoes")
        except (KeyError, ValueError, NoResultFound):
            # Nada foi adicionado nesta linha; apenas contamos o descarte.
            report.add_skipped("transacoes")
    db.commit()


def _load_goals(db: Session, report: EtlReport, users: dict[str, int]) -> None:
    for row in _read_csv("metas.csv"):
        try:
            user_id = users[row["user_email"].strip()]
            name = row["name"].strip()
            exists = db.scalars(
                select(func.count(Goal.id)).where(
                    Goal.user_id == user_id, Goal.name == name
                )
            ).one()
            if exists:
                continue
            db.add(
                Goal(
                    user_id=user_id,
                    name=name,
                    target_amount=_parse_decimal(row["target_amount"]),
                    current_amount=Decimal(row.get("current_amount", "0") or "0"),
                    deadline=_parse_date(row["deadline"]) if row.get("deadline") else None,
                )
            )
            report.add_created("metas")
        except (KeyError, ValueError):
            report.add_skipped("metas")
    db.commit()


def run(data_dir: Path | None = None) -> EtlReport:
    """Executa a carga completa. Idempotente: usuários existentes são reutilizados."""
    global DATA_DIR
    if data_dir is not None:
        DATA_DIR = data_dir

    init_db()
    report = EtlReport()
    db = SessionLocal()
    try:
        users = _load_users(db, report)
        _load_accounts(db, report, users)
        _load_categories(db, report, users)
        _load_transactions(db, report, users)
        _load_goals(db, report, users)
        logger.info("etl.steps_done")
    finally:
        db.close()

    logger.info("etl.done", created=report.created, skipped=report.skipped)
    print(f"ETL concluído — criados: {report.created} | descartados: {report.skipped}")
    return report


if __name__ == "__main__":
    run()
