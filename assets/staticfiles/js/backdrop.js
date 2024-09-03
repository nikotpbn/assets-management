const backdrop = document.querySelector(".backdrop");
const modalBackdrop = document.querySelector(".modal-backdrop");
const backdropSpinner = document.querySelector(".backdrop-spinner");

export function showBackdrop() {
    backdrop.style.display = "flex";
}

export function hideBackdrop() {
    backdrop.style.display = "none";
}

export function showBackdropSpinner() {
    backdropSpinner.style.display = "flex";
}

export function hideBackdropSpinner() {
    backdropSpinner.style.display = "none";
}

export function showModalBackdrop() {
    modalBackdrop.style.display = "flex";
}

export function hideModalBackdrop() {
    modalBackdrop.style.display = "none";
}