// Função para enviar formulários sem recarregar a página
// Toast simples
function showToast(msg, type = "success") {
    let toast = document.createElement('div');
    toast.className = `toast-message bg-${type} text-white px-3 py-2 rounded position-fixed`;
    toast.style.top = "20px";
    toast.style.right = "20px";
    toast.style.zIndex = 9999;
    toast.innerText = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
}

// Adiciona tarefa/hábito sem reload
function ajaxForm(formSelector, listSelector, urlRedirect) {
    const form = document.querySelector(formSelector);
    if (!form) return;

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
                atualizarGraficoProgresso(); // Atualiza o gráfico
                setTimeout(() => window.location.href = urlRedirect, 800);
            });
    });
}


// Concluir/remover sem reload e com animação
function ajaxAction(linkSelector, urlRedirect, actionMsg) {
    document.querySelectorAll(linkSelector).forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const li = link.closest('li');
            fetch(link.href)
                .then(response => response.text())
                .then(() => {
                    if (li) {
                        li.style.transition = "opacity 0.5s";
                        li.style.opacity = 0.3;
                        setTimeout(() => {
                            li.remove();
                            showToast(actionMsg);
                            atualizarGraficoProgresso(); // Atualiza o gráfico
                            setTimeout(() => window.location.href = urlRedirect, 500);
                        }, 400);
                    } else {
                        showToast(actionMsg);
                        atualizarGraficoProgresso(); // Atualiza o gráfico
                        setTimeout(() => window.location.href = urlRedirect, 500);
                    }
                });
        });
    });
}

// Inicialização ao carregar a página
document.addEventListener('DOMContentLoaded', function () {
    // Tarefas
    ajaxForm('form[action*="adicionar_tarefa"]', '.list-group', '/tarefas');
    ajaxAction('a[href*="concluir_tarefa"]', '/tarefas', "Tarefa concluída!");
    ajaxAction('a[href*="remover_tarefa"]', '/tarefas', "Tarefa removida!");

    // Hábitos
    ajaxForm('form[action*="adicionar_habito"]', '.list-group', '/habitos');
    ajaxAction('a[href*="concluir_habito"]', '/habitos', "Hábito concluído!");
    ajaxAction('a[href*="remover_habito"]', '/habitos', "Hábito removido!");
});

// Toast CSS (adicione no seu style.css se quiser)
const style = document.createElement('style');
style.innerHTML = `
.toast-message {
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  opacity: 0.95;
  font-size: 1rem;
  pointer-events: none;
}
.bg-success { background: #198754 !important; }
.bg-danger { background: #dc3545 !important; }
`;
document.head.appendChild(style);

console.log("JS carregado!");