const sidebarToggle = document.getElementById("sidebarToggle");
const closeSidebar = document.getElementById("closeSidebar");
const sidebar = document.getElementById("sidebar");
const mainContent = document.getElementById("mainContent");
const toggleIcon = document.getElementById("toggleIcon");

function toggleSidebar() {
  sidebar.classList.toggle("-translate-x-full");
  mainContent.classList.toggle("lg:ml-64");
  sidebarToggle.classList.toggle("left-64");

  // Mudando icone quando abre ou fecha
  if (sidebar.classList.contains("-translate-x-full")) {
    toggleIcon.classList.remove("bi-chevron-left");
    toggleIcon.classList.add("bi-chevron-right");
  } else {
    toggleIcon.classList.remove("bi-chevron-right");
    toggleIcon.classList.add("bi-chevron-left");
  }
}

sidebarToggle.addEventListener("click", toggleSidebar);
closeSidebar.addEventListener("click", toggleSidebar);

// FUNCAO AJAX TESTE

document.addEventListener('DOMContentLoaded', function () {
  // Seleciona todos os botões com a classe "manage-game"
  const manageGameButtons = document.querySelectorAll('.manage-game');

  manageGameButtons.forEach(button => {
    button.addEventListener('click', function (event) {
      event.preventDefault();

      // Obtém os dados do botão
      const gameId = this.getAttribute('data-game-id');
      const action = this.getAttribute('data-action');
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

      // Cria a requisição AJAX
      fetch(`/game/${action}/${gameId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken, // Token CSRF para proteger a requisição
        },
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert(data.message);
        } else {
          alert('Erro: ' + data.message);
        }
      })
      .catch(error => {
        console.error('Erro ao processar a requisição:', error);
      });
    });
  });
});
