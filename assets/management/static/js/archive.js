import { getCookie, displayToastCustomMessage } from "/static/js/util.js";

let uploadInput;
let sendUploadModalButton;
let isUploadingHandler = false;

uploadInput = document.getElementById("file-upload");
uploadInput.addEventListener("change", displayModal, false);

sendUploadModalButton = document.querySelector(".upload-modal-save");
sendUploadModalButton.addEventListener("click", uploadFile, false);

const uploadModalElement = document.getElementById("upload-modal");
const uploadModalDescription = document.getElementById("upload-description");

const modalTitle = document.querySelector(".upload-title");
const modalUploadTitleInput = document.getElementById("upload-title");
const modalDismissButtons = document.querySelectorAll(".upload-modal-dismiss");

const uploadSpinner = document.querySelector(".upload-spinner");
const uploadSpinnerText = document.querySelector(".upload-spinner-text");

const resetUploadModalText = () => {
  modalUploadTitleInput.value = "";
  uploadModalDescription.value = "";
};

const disableDismissButtons = (handler) => {
  if (handler) {
    modalDismissButtons.forEach((element) => (element.disabled = true));
  } else {
    modalDismissButtons.forEach((element) => (element.disabled = false));
  }
};

const modalSaveButtonSpinner = (handler) => {
  if (handler) {
    uploadSpinner.hidden = false;
    uploadSpinnerText.innerHTML = "Enviando...";
  } else {
    uploadSpinner.hidden = true;
    uploadSpinnerText.innerHTML = "Adicionar";
  }
};

async function uploadFile(e) {
  e.preventDefault();
  const url = uploadInput.dataset.url;
  const formData = new FormData();
  const isValidTitle = modalUploadTitleInput.value.trim() === "" ? false : true;
  const isValidDescription =
    uploadModalDescription.value.trim() === "" ? false : true;

  if (!isValidTitle) {
    modalUploadTitleInput.classList.add("invalid");
  } else {
    modalUploadTitleInput.classList.remove("invalid");
  }

  if (!isValidDescription) {
    uploadModalDescription.classList.add("invalid");
  } else {
    uploadModalDescription.classList.remove("invalid");
  }

  if (isValidTitle && isValidDescription) {
    formData.append("asset_id", asset.value);
    formData.append("title", modalUploadTitleInput.value);
    formData.append("description", uploadModalDescription.value);
    formData.append("file", uploadInput.files[0]);

    isUploadingHandler = true;
    disableDismissButtons(isUploadingHandler);
    modalSaveButtonSpinner(isUploadingHandler);

    let response = await fetch(url, {
      method: "POST",
      body: formData,
      headers: { "X-CSRFToken": getCookie("csrftoken") },
    });

    const data = await response.json();
    displayToastCustomMessage(data.message, response.status);

    isUploadingHandler = false;
    disableDismissButtons(isUploadingHandler);
    modalSaveButtonSpinner(isUploadingHandler);

    modalDismissButtons[0].click();

    resetUploadModalText();
  }
}

function displayModal(e) {
  modalTitle.innerHTML = "Título e Descrição";
  new bootstrap.Modal(uploadModalElement).show();
}
