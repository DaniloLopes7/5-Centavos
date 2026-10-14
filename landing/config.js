/*
 * Endpoints da aplicação.
 * Antes do deploy, substitua os dois endereços de exemplo pelos domínios
 * públicos criados para a API e para o dashboard.
 */
(function () {
  "use strict";

  var isLocal = window.location.hostname === "localhost";

  window.API_URL = isLocal
    ? "http://localhost:8000"
    : "https://PREENCHER-COM-A-URL-DA-API";
  window.DASHBOARD_URL = isLocal
    ? "http://localhost:8501"
    : "https://PREENCHER-COM-A-URL-DO-DASHBOARD";
})();
