import os
from database import (
    ensure_database_exists,
    get_user_by_id,
    get_user_by_email,
    check_password,
    create_user,
    get_accounts_by_user,
    calculate_balance,
    add_transaction,
    get_transactions_by_account,
    get_categories_by_user,
    create_category,
    create_default_categories,
    get_goals_by_user,
    create_goal,
    update_goal_progress,
    create_account
)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    print("\n" + "="*40)
    print(f"{text:^40}")
    print("="*40)

def main_menu():
    while True:
        clear_screen()
        print_header("5 CENTAVOS - V0.3.0")
        print("1. Login")
        print("2. Criar Conta (Cadastro)")
        print("3. Sair")

        choice = input("\nEscolha uma opção: ")

        if choice == '1':
            login_screen()
        elif choice == '2':
            register_screen()
        elif choice == '3':
            print("Saindo... Até logo!")
            break
        else:
            input("Opção inválida! Pressione Enter para tentar novamente.")

def register_screen():
    clear_screen()
    print_header("CADASTRAR USUÁRIO")
    name = input("Nome completo: ")
    email = input("E-mail: ")
    password = input("Senha: ")

    if create_user(name, email, password):
        user = get_user_by_email(email)
        if user:
            create_default_categories(user['id'])
        print("\n✅ Conta criada com sucesso! Categorias padrão foram adicionadas.")
    else:
        print("\n❌ Erro ao criar conta. O e-mail pode já estar em uso.")

    input("\nPressione Enter para voltar.")

def login_screen():
    clear_screen()
    print_header("LOGIN")
    email = input("E-mail: ")
    password = input("Senha: ")

    user = get_user_by_email(email)
    if user and user.get('id') is not None and check_password(password, user['password_hash']):
        print("\n✅ Login realizado com sucesso!")
        account_menu(user)
    else:
        print("\n❌ E-mail ou senha incorretos, ou usuário sem ID válido.")

    input("\nPressione Enter para voltar.")

def account_menu(user):
    while True:
        clear_screen()
        print_header(f"Olá, {user['name']}!")

        accounts = get_accounts_by_user(user['id'])
        if not accounts:
            print("Você não possui carteiras cadastradas.")
            print("Crie uma carteira para começar a gerenciar seu dinheiro.")
        else:
            print("Suas Carteiras:")
            for acc in accounts:
                balance = calculate_balance(acc['id'])
                print(f"ID: {acc['id']} | {acc['name']} ({acc['type']}) - Saldo: R$ {balance:.2f}")

        print("\n--- Menu de Ações ---")
        print("1. Ver Meu Extrato")
        print("2. Adicionar Transação (Receita/Despesa)")
        print("3. Gerenciar Metas")
        print("4. Criar Nova Carteira")
        print("5. Criar Nova Categoria")
        print("6. Voltar ao Login")

        choice = input("\nEscolha uma opção: ")

        if choice == '1':
            extract_menu(user)
        elif choice == '2':
            transaction_menu(user)
        elif choice == '3':
            goals_menu(user)
        elif choice == '4':
            create_account_menu(user)
        elif choice == '5':
            category_menu(user)
        elif choice == '6':
            break
        else:
            input("Opção inválida! Pressione Enter.")

def extract_menu(user):
    clear_screen()
    print_header("MEU EXTRATO")

    accounts = get_accounts_by_user(user['id'])
    if not accounts:
        print("Você não possui carteiras para visualizar o extrato.")
        input("\nPressione Enter para voltar.")
        return

    print("Selecione a carteira:")
    for i, acc in enumerate(accounts, 1):
        print(f"{i}. {acc['name']} ({acc['type']})")

    try:
        choice = int(input("\nOpção: "))
        if 1 <= choice <= len(accounts):
            selected_acc = accounts[choice - 1]
            acc_id = selected_acc['id']

            transactions = get_transactions_by_account(acc_id)
            if not transactions:
                print("\nNenhuma transação encontrada para esta carteira.")
            else:
                print(f"\nExtrato de: {selected_acc['name']}")
                print(f"{'Data':<12} | {'Descrição':<20} | {'Valor':<10} | {'Tipo':<10}")
                print("-" * 55)
                for t in transactions:
                    print(f"{t['date']:<12} | {t['description']:<20} | {t['amount']:<10.2f} | {t['type']:<10}")
        else:
            print("\n❌ Opção inválida.")
    except ValueError:
        print("\n❌ Erro: Por favor, digite um número válido.")

    input("\nPressione Enter para voltar.")

def transaction_menu(user):
    clear_screen()
    print_header("NOVA TRANSAÇÃO")

    try:
        accounts = get_accounts_by_user(user['id'])
        if not accounts:
            print("\n❌ Você não possui carteiras. Crie uma carteira primeiro!")
            input("Pressione Enter para voltar.")
            return

        print("Selecione a carteira:")
        for i, acc in enumerate(accounts, 1):
            print(f"{i}. {acc['name']}")

        acc_choice = int(input("\nOpção: "))
        if not (1 <= acc_choice <= len(accounts)):
            print("\n❌ Opção inválida.")
            input("Pressione Enter para voltar.")
            return
        acc_id = accounts[acc_choice - 1]['id']

        categories = get_categories_by_user(user['id'])
        if not categories:
            print("\n❌ Você não tem categorias. Crie uma categoria primeiro!")
            input("Pressione Enter para voltar.")
            return

        print("\nSelecione a categoria:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat['name']} ({cat['type']})")

        cat_choice = int(input("\nOpção: "))
        if not (1 <= cat_choice <= len(categories)):
            print("\n❌ Opção inválida.")
            input("Pressione Enter para voltar.")
            return
        cat_id = categories[cat_choice - 1]['id']
        trans_type = categories[cat_choice - 1]['type']

        description = input("Descrição: ")
        amount = float(input("Valor: "))
        date = input("Data (AAAA-MM-DD): ")

        if add_transaction(acc_id, cat_id, description, amount, trans_type, date):
            print("\n✅ Transação registrada com sucesso!")
        else:
            print("\n❌ Erro ao registrar transação.")

    except ValueError:
        print("\n❌ Erro: Entrada inválida.")

    input("\nPressione Enter para voltar.")

def goals_menu(user):
    while True:
        clear_screen()
        print_header("METAS FINANCEIRAS")
        goals = get_goals_by_user(user['id'])

        if not goals:
            print("Você ainda não tem metas definidas.")
        else:
            for g in goals:
                progresso = (g['current_amount'] / g['target_amount']) * 100 if g['target_amount'] > 0 else 0
                print(f"ID: {g['id']} | Meta: {g['name']}")
                print(f"Progresso: R$ {g['current_amount']:.2f} / R$ {g['target_amount']:.2f} ({progresso:.1f}%)")
                print(f"Prazo: {g['deadline'] if g['deadline'] else 'Sem prazo'}")
                print("-" * 30)

        print("\n1. Criar Nova Meta")
        print("2. Adicionar Valor a uma Meta")
        print("3. Voltar")

        choice = input("\nEscolha uma opção: ")

        if choice == '1':
            name = input("Nome da meta: ")
            target = float(input("Valor alvo: "))
            deadline = input("Prazo (AAAA-MM-DD) [Opcional]: ") or None
            if create_goal(user['id'], name, target, deadline):
                print("\n✅ Meta criada com sucesso!")
            input("\nPressione Enter.")
        elif choice == '2':
            try:
                if not goals:
                    print("\n❌ Você não tem metas para atualizar.")
                    input("Pressione Enter.")
                    continue

                print("\nSelecione a meta:")
                for i, g in enumerate(goals, 1):
                    print(f"{i}. {g['name']}")

                g_choice = int(input("\nOpção: "))
                if 1 <= g_choice <= len(goals):
                    g_id = goals[g_choice - 1]['id']
                    val = float(input("Valor para adicionar: "))
                    if update_goal_progress(g_id, val):
                        print("\n✅ Progresso atualizado!")
                    else:
                        print("\n❌ Erro ao atualizar meta.")
                else:
                    print("\n❌ Opção inválida.")
            except ValueError:
                print("\n❌ Entrada inválida.")
            input("\nPressione Enter.")
        elif choice == '3':
            break

def create_account_menu(user):
    clear_screen()
    print_header("CRIAR NOVA CARTEIRA")
    try:
        name = input("Nome da carteira (ex: NuConta, Carteira): ")
        acc_type = input("Tipo (ex: Corrente, Poupança, Espécie): ")
        initial_bal = float(input("Saldo Inicial: "))
        if create_account(user['id'], name, acc_type, initial_bal):
            print("\n✅ Carteira criada com sucesso!")
    except ValueError:
        print("\n❌ Erro: Valor de saldo inválido.")
    input("\nPressione Enter.")

def category_menu(user):
    clear_screen()
    print_header("CRIAR NOVA CATEGORIA")
    try:
        name = input("Nome da categoria (ex: Lazer, Educação): ")
        cat_type = input("Tipo (RECEITA ou DESPESA): ").upper()
        if create_category(user['id'], name, cat_type):
            print("\n✅ Categoria criada com sucesso!")
    except ValueError:
        print("\n❌ Erro ao criar categoria.")
    input("\nPressione Enter.")

if __name__ == "__main__":
    ensure_database_exists()
    main_menu()
