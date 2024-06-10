import { getCookie, sendRequest } from "/static/js/util.js";

const headers = {
  "Content-Type": "application/json",
  "X-CSRFToken": getCookie("csrftoken"),
};

let currentYear = null;

const incomeButtonElement = document.getElementById("income-button");
const expenseButtonElement = document.getElementById("expense-button");
const incomeExpenseModalElement = document.getElementById("flow-modal");

const flowDateInputElement = document.getElementById("flow-date-input");
const flowValueInputElement = document.getElementById("flow-value-input");

const toastTrigger = document.getElementById("liveToastBtn");
const toastLiveExample = document.getElementById("liveToast");
const toastLiveBody = document.querySelector(".toast-body");

const modalTitle = document.querySelector(".modal-title");
const modalBodyText = document.querySelector(".modal-body-text");
const modalBodyTextAreaInput = document.querySelector(".modal-body-textarea");
const modalSaveButton = document.querySelector(".modal-save");
const modalDismissButtons = document.querySelectorAll(".modal-dismiss");

let addIncome = false;
let addExpense = false;
let initialDate = null;
let data = {};
let url = "";

const saveFlow = async () => {
  let response = await sendRequest(url, "POST", headers, data);
  displayToastCustomMessage(response.message, response.status);
};

modalSaveButton.addEventListener("click", () => {
  if (data.flow === "expense") {
    data.description = modalBodyTextAreaInput.value;
  }
  saveFlow();
  modalDismissButtons[0].click();
});

modalDismissButtons.forEach((element) =>
  element.addEventListener("click", (event) => {
    resetFlowButtons();
  })
);

const resetFlowButtons = () => {
  const buttons = [incomeButtonElement, expenseButtonElement];
  buttons.forEach((element) => {
    element.classList.remove("active");
  });
};

const resetUnitButtonElements = () => {
  const buttons = [incomeButtonElement, expenseButtonElement];
  buttons.forEach((element) => {
    element.classList.remove("active");
    addIncome = false;
    addExpense = false;
  });
};

const getFormData = (flow) => {
  const date = flowDateInputElement.value;
  const value = flowValueInputElement.value;

  try {
    let insertedDateYear = Number.parseInt(date.slice(0, 4));
    let insertedValue = Number.parseFloat(
      value.replace(".", "").replace(",", ".")
    );

    data.asset_id = asset.value;

    if (flow === "entrada") {
      data.flow = "income";
      url = incomeButtonElement.dataset.url;
    } else {
      data.flow = "expense";
      url = expenseButtonElement.dataset.url;
    }

    if (insertedDateYear <= currentYear) {
      data.date = date;
    } else {
      throw new Error("O ano não pode ser maior que o ano atual.");
    }

    if (insertedValue > 0) {
      data.value = value;
    } else {
      throw new Error("O valor não pode ser 0.");
    }

    displayModal(data, flow);
  } catch (error) {
    displayToastCustomMessage(error.message);
    resetFlowButtons();
  }
  if (flow === "entrada") {
    modalSaveButton.classList.remove("btn-danger");
    modalSaveButton.classList.add("btn-success");
  } else {
    modalSaveButton.classList.remove("btn-success");
    modalSaveButton.classList.add("btn-danger");
  }
  return data;
};

const displayModal = (data, flow) => {
  let message = `Deseja mesmo criar uma ${flow} no valor de R$ ${data.value}`;
  modalBodyText.innerHTML = message;
  modalTitle.innerHTML = `Criar ${flow}`;

  if (flow === 'saida') {
    modalBodyTextAreaInput.style.display = "block";
  } else {
    modalBodyTextAreaInput.style.display = "none";
  }
  new bootstrap.Modal(incomeExpenseModalElement).show();
};

incomeButtonElement.addEventListener("click", (event) => {
  event.preventDefault();
  resetUnitButtonElements();
  if (addIncome) {
    incomeButtonElement.classList.remove("active");
  } else {
    incomeButtonElement.classList.add("active");
  }
  addIncome = !addIncome;
  getFormData("entrada");
});

expenseButtonElement.addEventListener("click", (event) => {
  event.preventDefault();
  resetUnitButtonElements();
  if (addExpense) {
    expenseButtonElement.classList.remove("active");
    addExpense = false;
  } else {
    expenseButtonElement.classList.add("active");
  }
  addExpense = !addExpense;
  getFormData("saida");

});

const moneyMask = (value) => {
  value = value.replace(".", "").replace(",", "").replace(/\D/g, "");

  const options = { minimumFractionDigits: 2 };
  const result = new Intl.NumberFormat("pt-BR", options).format(
    parseFloat(value) / 100
  );

  return value === "" ? "0,00" : result;
};

flowValueInputElement.addEventListener("input", (event) => {
  flowValueInputElement.value = moneyMask(event.target.value);
});

const formatDate = (year, month, day) => {
  if (month < 10) {
    month = `0${month}`;
  }
  if (day < 10) {
    day = `0${day}`;
  }
  return `${year}-${month}-${day}`;
};

export const displayToastCustomMessage = (message, status) => {
  if (status === 200) {
    toastLiveExample.classList.remove("text-bg-danger");
    toastLiveExample.classList.add("text-bg-success");
  } else {
    toastLiveExample.classList.remove("text-bg-success");
    toastLiveExample.classList.add("text-bg-danger");
  }
  toastLiveBody.innerHTML = message;
  const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample);
  toastBootstrap.show();
};

window.addEventListener("load", async () => {
  let timestamp = Date.now();
  initialDate = new Date(timestamp);

  currentYear = initialDate.getFullYear();
  flowDateInputElement.value = formatDate(
    initialDate.getFullYear(),
    initialDate.getMonth(),
    initialDate.getDate()
  );
});
