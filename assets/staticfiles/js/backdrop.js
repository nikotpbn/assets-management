const backdrop = document.querySelector(".backdrop");

export function showBackdrop() {
    backdrop.style.display = "flex";
}

export function hideBackdrop() {
    backdrop.style.display = "none";
}