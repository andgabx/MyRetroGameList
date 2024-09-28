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