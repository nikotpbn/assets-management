import {
  getCookie,
  sendRequest,
  displayToastCustomMessage,
} from "/static/js/util.js";

const headers = {
  "Content-Type": "application/json",
  "X-CSRFToken": getCookie("csrftoken"),
};

const assetForm = document.querySelector("#asset-form");

const deleteModal = document.querySelector(".delete-modal");
const deleteButtons = document.querySelectorAll(".delete-form-button");
const modalBody = document.querySelector(".modal-body");
const modalSubmitButton = document.querySelector(".modal-submit");
const deleteForm = document.querySelector("#delete-form");

const closeDeleteModalButton = document.querySelector(".delete-modal-close");
const flowTable = document.querySelector(".flow-table");

let data;
let url;

assetForm.addEventListener("change", function (event) {
  this.submit();
});

modalSubmitButton.addEventListener("click", async () => {
  deleteForm.submit();
});

deleteButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    event.preventDefault();

    const value = button.dataset.value;
    const date = button.dataset.date;
    const flow_type = button.dataset.flow;
    const flow = flow_type === "Income" ? "Entrada" : "Saída";
    data = { value, date, flow };
    displayModal(flow, date, value);
  });
});

const displayModal = (flow, date, value) => {
  modalBody.innerHTML = `Deseja mesmo remover o ${flow} do dia ${date} no valor de R$${value}`;
  new bootstrap.Modal(deleteModal).show();
};

window.addEventListener("load", (event) => {
  const message = document.querySelector(".message").dataset.message;
  if (message !== "None") {
    displayToastCustomMessage(message, 200);
  }
});
