import {
  getCookie,
  sendRequest,
  displayToastCustomMessage,
} from "/static/js/util.js";

const headers = {
  "Content-Type": "application/json",
  "X-CSRFToken": getCookie("csrftoken"),
};

const deleteModal = document.querySelector(".delete-modal");
const deleteButtons = document.querySelectorAll(".delete-button");
const modalBody = document.querySelector(".modal-body");
const modalSubmitButton = document.querySelector(".modal-submit");
let data;

modalSubmitButton.addEventListener("click", () => {
  console.log(data);
});

deleteButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const value = button.dataset.value;
    const date = button.dataset.date;
    const flow_type = button.dataset.flow;
    const flow = flow_type === "Income" ? "Entrada" : "Saída";
    data = { value, date, flow };
    displayModal(data);
  });
});

const displayModal = (data) => {
  modalBody.innerHTML = `Deseja mesmo remover o ${data.flow} do dia ${data.date} no valor de R$${data.value}`;
  new bootstrap.Modal(deleteModal).show();
};
