document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".varietal-button");
    const unlocked = new Set(progress);
    const varietalIndex = varietalOrder.findIndex(v => !unlocked.has(v));
    const maxUnlockedIndex = varietalIndex === -1 ? varietalOrder.length : varietalIndex;

    buttons.forEach(button => {
        const varietal = button.dataset.varietal;
        const index = varietalOrder.indexOf(varietal);
        button.disabled = index > maxUnlockedIndex;
    });

    // Show buttons only after logic is applied
    const container = document.getElementById("map-buttons");
    container.style.visibility = "visible";
});

document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".varietal-button");
    const unlocked = new Set(progress);
    const varietalIndex = varietalOrder.findIndex(v => !unlocked.has(v));
    const maxUnlockedIndex = varietalIndex === -1 ? varietalOrder.length : varietalIndex;

    buttons.forEach(button => {
        const varietal = button.dataset.varietal;
        const index = varietalOrder.indexOf(varietal);
        button.disabled = index > maxUnlockedIndex;
    });

    // Show buttons only after logic is applied
    document.getElementById("loader").style.display = "none";
    const container = document.getElementById("map-buttons");
    container.style.visibility = "visible";
});