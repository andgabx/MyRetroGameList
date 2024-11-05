document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("descriptionModal");
    const editBtn = document.getElementById("editDescriptionBtn");
    const cancelBtn = document.getElementById("cancelBtn");
    const saveBtn = document.getElementById("saveBtn");
    const userDescription = document.getElementById("userDescription");
    const descriptionInput = document.getElementById("descriptionInput");

    // Open modal
    editBtn.addEventListener("click", function (event) {
        event.preventDefault();
        modal.classList.remove("hidden");
    });

    // Close modal
    cancelBtn.addEventListener("click", function () {
        modal.classList.add("hidden");
    });
});

document.addEventListener("DOMContentLoaded", function () {
    anime({
        targets: "#usercontent",
        translateX: [-1000, 0],
        easing: "easeOutLinear",
        duration: 1000,
    });
});