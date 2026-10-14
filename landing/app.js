/* ============================================================
   5 CENTAVOS — LANDING PAGE · INTERAÇÕES
   Validação do cadastro, integração com API real (com fallback),
   animações de scroll, contadores, FAQ, demo e navegação.
   ============================================================ */

(function () {
  "use strict";

  /* URLs centralizadas em config.js (local ou produção). */
  var API_BASE_URL = window.API_URL.replace(/\/+$/, "") + "/api/v1";
  var DASHBOARD_URL = window.DASHBOARD_URL.replace(/\/+$/, "");

  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ================= NAV MOBILE ================= */
  var navToggle = document.getElementById("nav-toggle");
  var navLinks = document.getElementById("nav-links");

  if (navToggle && navLinks) {
    navToggle.addEventListener("click", function () {
      var isOpen = navLinks.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
      navToggle.innerHTML = isOpen
        ? '<i class="ph ph-x" aria-hidden="true"></i>'
        : '<i class="ph ph-list" aria-hidden="true"></i>';
    });

    navLinks.addEventListener("click", function (event) {
      if (event.target.tagName === "A" && navLinks.classList.contains("is-open")) {
        navLinks.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
        navToggle.innerHTML = '<i class="ph ph-list" aria-hidden="true"></i>';
      }
    });
  }

  /* ================= FORMULÁRIO DE CADASTRO / LOGIN ================= */
  var form = document.getElementById("signup-form");
  var emailInput = document.getElementById("email");
  var passwordInput = document.getElementById("password");
  var submitButton = document.getElementById("signup-submit");
  var submitLabel = submitButton ? submitButton.querySelector(".btn__label") : null;
  var messageBox = document.getElementById("signup-message");
  var microcopy = document.getElementById("signup-microcopy");
  var googleButton = document.getElementById("google-btn");
  var modeButtons = document.querySelectorAll(".signup__mode-btn");

  var EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var mode = "signup"; /* "signup" | "login" — widget do formulário dual */

  var MODE_TEXT = {
    signup: {
      cta: "Começar grátis",
      passwordPh: "Crie uma senha (mín. 6 caracteres)",
      micro: "Sem cartão de crédito · Leva 30 segundos",
      autocomplete: "new-password"
    },
    login: {
      cta: "Entrar",
      passwordPh: "Sua senha",
      micro: "Bem-vindo de volta! Seus dados seguem seguros.",
      autocomplete: "current-password"
    }
  };

  function setMode(next) {
    mode = next;
    modeButtons.forEach(function (btn) {
      var active = btn.getAttribute("data-mode") === next;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-selected", String(active));
    });
    submitLabel.textContent = MODE_TEXT[next].cta;
    passwordInput.placeholder = MODE_TEXT[next].passwordPh;
    passwordInput.setAttribute("autocomplete", MODE_TEXT[next].autocomplete);
    microcopy.textContent = MODE_TEXT[next].micro;
    hideMessage();
  }

  modeButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      setMode(btn.getAttribute("data-mode"));
    });
  });

  /* Botões/âncoras "Entrar" da página abrem o form já em modo login. */
  document.querySelectorAll('a[href="#cadastro"]').forEach(function (link) {
    if (link.textContent.trim().toLowerCase() === "entrar") {
      link.addEventListener("click", function () { setMode("login"); });
    }
  });

  function setFieldState(input, errorId, message) {
    var field = input.closest(".field");
    var errorEl = document.getElementById(errorId);
    if (message) {
      field.classList.add("field--invalid");
      errorEl.textContent = message;
      input.setAttribute("aria-invalid", "true");
      return false;
    }
    field.classList.remove("field--invalid");
    errorEl.textContent = "";
    input.removeAttribute("aria-invalid");
    return true;
  }

  function validateEmail() {
    var value = emailInput.value.trim();
    if (!value) return setFieldState(emailInput, "email-error", "Informe seu e-mail");
    if (!EMAIL_REGEX.test(value)) return setFieldState(emailInput, "email-error", "Hmm, esse e-mail não parece válido");
    return true;
  }

  function validatePassword() {
    var value = passwordInput.value;
    if (!value) return setFieldState(passwordInput, "password-error", mode === "login" ? "Informe sua senha" : "Crie uma senha");
    if (mode === "signup" && value.length < 6) {
      return setFieldState(passwordInput, "password-error", "A senha precisa de pelo menos 6 caracteres");
    }
    return true;
  }

  function showMessage(type, html) {
    messageBox.className = "signup__message signup__message--" + type;
    messageBox.innerHTML = html;
  }

  function hideMessage() {
    messageBox.className = "signup__message";
    messageBox.textContent = "";
  }

  function setLoading(isLoading) {
    submitButton.classList.toggle("is-loading", isLoading);
    submitButton.disabled = isLoading;
  }

  /* Deriva o nome do e-mail (a API exige `name`, mas o form segue o
     plano com apenas 2 campos). Ex.: "maria.silva@" → "Maria Silva". */
  function deriveNameFromEmail(email) {
    var local = email.split("@")[0];
    var cleaned = local.replace(/[._\-+]+/g, " ").trim();
    if (!cleaned) return "Usuário 5C";
    return cleaned
      .split(" ")
      .map(function (w) { return w.charAt(0).toUpperCase() + w.slice(1); })
      .join(" ")
      .slice(0, 120);
  }

  function goToDashboard(token) {
    showMessage("success", "✨ Tudo certo! Abrindo seu painel…");
    setTimeout(function () {
      window.location.href = DASHBOARD_URL + "/?token=" + encodeURIComponent(token);
    }, 700);
  }

  function requestToken(email, password) {
    return fetch(API_BASE_URL + "/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email, password: password })
    }).then(function (response) {
      if (response.ok) {
        return response.json().then(function (body) { return body.access_token; });
      }
      var err = new Error("login-failed");
      err.status = response.status;
      throw err;
    });
  }

  function handleLoginError(status) {
    if (status === 401) {
      showMessage("error", "E-mail ou senha incorretos. Tente novamente.");
      return;
    }
    if (status === 429) {
      showMessage("error", "Muitas tentativas seguidas. Aguarde um minuto e tente novamente.");
      return;
    }
    showMessage("error", "Não foi possível entrar. Tente novamente em instantes.");
  }

  function handleRegisterError(status, body) {
    if (status === 409) {
      showMessage(
        "error",
        'Este e-mail já está cadastrado. <a href="#cadastro" id="go-login">Clique aqui para entrar</a>.'
      );
      var goLogin = document.getElementById("go-login");
      if (goLogin) {
        goLogin.addEventListener("click", function () { setMode("login"); });
      }
      return;
    }
    if (status === 429) {
      showMessage("error", "Muitas tentativas seguidas. Aguarde um minuto e tente novamente.");
      return;
    }
    var detail = body && body.detail ? body.detail : "Não foi possível criar sua conta. Tente novamente.";
    showMessage("error", detail);
  }

  if (form) {
    emailInput.addEventListener("blur", validateEmail);
    passwordInput.addEventListener("blur", validatePassword);
    emailInput.addEventListener("input", function () { validateEmail(); hideMessage(); });
    passwordInput.addEventListener("input", function () { validatePassword(); hideMessage(); });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      hideMessage();

      var okEmail = validateEmail();
      var okPassword = validatePassword();
      if (!okEmail || !okPassword) {
        var firstInvalid = form.querySelector(".field--invalid input");
        if (firstInvalid) firstInvalid.focus();
        return;
      }

      setLoading(true);
      var email = emailInput.value.trim();
      var password = passwordInput.value;

      if (mode === "login") {
        /* ---------- FLUXO: ENTRAR ---------- */
        requestToken(email, password)
          .then(function (token) {
            setLoading(false);
            goToDashboard(token);
          })
          .catch(function (err) {
            setLoading(false);
            if (err && err.status) {
              handleLoginError(err.status);
            } else {
              /* API offline */
              showMessage(
                "error",
                "Não foi possível conectar ao servidor. Verifique se a API está no ar e tente novamente."
              );
            }
          });
        return;
      }

      /* ---------- FLUXO: CRIAR CONTA (register → auto-login → dashboard) ---------- */
      var payload = {
        name: deriveNameFromEmail(email),
        email: email,
        password: password
      };

      fetch(API_BASE_URL + "/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      })
        .then(function (response) {
          if (response.status === 201) {
            /* Cadastro ok → login automático → redireciona ao painel */
            return requestToken(email, password).then(function (token) {
              setLoading(false);
              goToDashboard(token);
            });
          }
          return response.json().then(function (body) {
            setLoading(false);
            handleRegisterError(response.status, body);
          }).catch(function () {
            setLoading(false);
            handleRegisterError(response.status, null);
          });
        })
        .catch(function () {
          /* Fallback: API offline ou CORS não configurado — mostra
             estado de sucesso simulado para fins de demonstração. */
          setLoading(false);
          showMessage(
            "demo",
            "✨ Cadastro simulado com sucesso! <small>(A API está offline — esta é uma demonstração. Num ambiente real, sua conta seria criada agora.)</small>"
          );
          form.reset();
        });
    });
  }

  /* Botão Google: o backend ainda não suporta OAuth — estado honesto. */
  if (googleButton) {
    googleButton.addEventListener("click", function () {
      showMessage(
        "demo",
        "O login com Google chega em breve. Por enquanto, cadastre-se com seu e-mail — leva 30 segundos."
      );
      emailInput.focus();
    });
  }

  /* ================= STICKY CTA (mobile) ================= */
  var stickyCta = document.getElementById("sticky-cta");
  var heroSection = document.querySelector(".hero");

  if (stickyCta && heroSection) {
    var ctaObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          stickyCta.classList.toggle("is-visible", !entry.isIntersecting);
          stickyCta.setAttribute("aria-hidden", String(entry.isIntersecting));
        });
      },
      { rootMargin: "-80px 0px 0px 0px" }
    );
    ctaObserver.observe(heroSection);
  }

  /* ================= ANIMAÇÃO DE ENTRADA (.reveal) ================= */
  var revealEls = document.querySelectorAll(".reveal");
  if (prefersReducedMotion) {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  } else {
    var revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach(function (el) { revealObserver.observe(el); });
  }

  /* ================= CONTADORES ANIMADOS ================= */
  var counters = document.querySelectorAll("[data-count]");

  function animateCounter(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    if (isNaN(target)) return;
    var duration = 1400;
    var start = null;

    function step(timestamp) {
      if (!start) start = timestamp;
      var progress = Math.min((timestamp - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(target * eased).toLocaleString("pt-BR");
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  if (prefersReducedMotion) {
    counters.forEach(function (el) {
      el.textContent = parseInt(el.getAttribute("data-count"), 10).toLocaleString("pt-BR");
    });
  } else {
    var counterObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            counterObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.6 }
    );
    counters.forEach(function (el) { counterObserver.observe(el); });
  }

  /* ================= DEMO: TABS ================= */
  var demoTabs = document.querySelectorAll(".demo__tab");
  var demoPanels = document.querySelectorAll(".demo__panel");

  demoTabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      var target = tab.getAttribute("data-tab");

      demoTabs.forEach(function (t) {
        t.classList.toggle("is-active", t === tab);
        t.setAttribute("aria-selected", String(t === tab));
      });

      demoPanels.forEach(function (panel) {
        panel.hidden = panel.getAttribute("data-panel") !== target;
      });
    });
  });

  /* ================= FAQ (acordeão) ================= */
  var faqQuestions = document.querySelectorAll(".faq__question");

  faqQuestions.forEach(function (question) {
    question.addEventListener("click", function () {
      var isOpen = question.getAttribute("aria-expanded") === "true";
      var answer = question.parentElement.querySelector(".faq__answer");

      /* Fecha os demais para foco em uma objeção por vez */
      faqQuestions.forEach(function (q) {
        q.setAttribute("aria-expanded", "false");
        var a = q.parentElement.querySelector(".faq__answer");
        if (a) a.hidden = true;
      });

      if (!isOpen) {
        question.setAttribute("aria-expanded", "true");
        if (answer) answer.hidden = false;
      }
    });
  });

  /* ================= PARALLAX NOS CARDS DE VIDRO ================= */
  if (!prefersReducedMotion) {
    var parent = document.querySelector("[data-parallax-parent]");
    if (parent && window.matchMedia("(pointer: fine)").matches) {
      parent.addEventListener("mousemove", function (event) {
        var rect = parent.getBoundingClientRect();
        var x = (event.clientX - rect.left) / rect.width - 0.5;
        var y = (event.clientY - rect.top) / rect.height - 0.5;

        parent.querySelectorAll("[data-parallax]").forEach(function (el) {
          var depth = parseFloat(el.getAttribute("data-parallax")) || 1;
          el.style.transform =
            "translate(" + (x * depth * 8).toFixed(1) + "px," + (y * depth * 8).toFixed(1) + "px)";
        });
      });

      parent.addEventListener("mouseleave", function () {
        parent.querySelectorAll("[data-parallax]").forEach(function (el) {
          el.style.transform = "";
        });
      });
    }
  }
})();
