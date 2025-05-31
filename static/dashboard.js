// Toast simples com fade e timeout
function showToast(msg, type = "success") {
  let toast = document.createElement('div');
  toast.className = `toast-message bg-${type} text-white px-3 py-2 rounded position-fixed`;
  toast.style.top = "20px";
  toast.style.right = "20px";
  toast.style.zIndex = 9999;
  toast.style.opacity = 1;
  toast.innerText = msg;
  document.body.appendChild(toast);

  // Fade-out antes de remover
  setTimeout(() => {
    toast.style.transition = "opacity 0.5s ease";
    toast.style.opacity = 0;
    setTimeout(() => toast.remove(), 500);
  }, 1800);
}

// Envio de formulários via AJAX
function ajaxForm(formSelector, urlRedirect) {
  const form = document.querySelector(formSelector);
  if (!form) {
    console.warn("Formulário não encontrado:", formSelector);
    return;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(form);

    fetch(form.action, {
      method: 'POST',
      body: formData
    })
      .then(response => response.text())
      .then(() => {
        showToast("Adicionado com sucesso!");
        setTimeout(() => window.location.href = urlRedirect, 800);
      })
      .catch(err => {
        console.error("Erro ao enviar formulário:", err);
        showToast("Erro ao adicionar", "danger");
      });
  });
}

// Ação AJAX para concluir/remover com animação
function ajaxAction(linkSelector, urlRedirect, actionMsg) {
  const links = document.querySelectorAll(linkSelector);
  if (!links.length) {
    console.warn("Nenhum link encontrado para:", linkSelector);
    return;
  }

  links.forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      const li = link.closest('li');

      fetch(link.href)
        .then(response => response.text())
        .then(() => {
          if (li) {
            li.style.transition = "opacity 0.5s ease";
            li.style.opacity = 0.3;
            setTimeout(() => {
              li.remove();
              showToast(actionMsg);
              setTimeout(() => window.location.href = urlRedirect, 500);
            }, 400);
          } else {
            showToast(actionMsg);
            setTimeout(() => window.location.href = urlRedirect, 500);
          }
        })
        .catch(err => {
          console.error("Erro ao executar ação AJAX:", err);
          showToast("Erro na ação", "danger");
        });
    });
  });
}

// Executa ao carregar a página
document.addEventListener('DOMContentLoaded', function () {
  console.log("JS VidaXP carregado!");

  // Tarefas
  ajaxForm('form[action*="adicionar_tarefa"]', '/tarefas');
  ajaxAction('a[href*="concluir_tarefa"]', '/tarefas', "Tarefa concluída!");
  ajaxAction('a[href*="remover_tarefa"]', '/tarefas', "Tarefa removida!");

  // Hábitos
  ajaxForm('form[action*="adicionar_habito"]', '/habitos');
  ajaxAction('a[href*="concluir_habito"]', '/habitos', "Hábito concluído!");
  ajaxAction('a[href*="remover_habito"]', '/habitos', "Hábito removido!");
  if (typeof atualizarGrafico === 'function') atualizarGrafico();
});

// Toast estilo CSS injetado
const style = document.createElement('style');
style.innerHTML = `
.toast-message {
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  opacity: 0.95;
  font-size: 1rem;
  pointer-events: none;
  transition: opacity 0.5s ease;
}
.bg-success { background: #198754 !important; }
.bg-danger { background: #dc3545 !important; }
`;
document.head.appendChild(style);
