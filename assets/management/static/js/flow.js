import {
  getCookie,
  sendRequest,
  displayToastCustomMessage,
} from "/static/js/util.js";

const headers = {
  "X-CSRFToken": getCookie("csrftoken"),
};

let currentYear = null;

const incomeButtonElement = document.getElementById("income-button");
const expenseButtonElement = document.getElementById("expense-button");
const incomeExpenseModalElement = document.getElementById("flow-modal");

const flowDateInputElement = document.getElementById("flow-date-input");
const flowValueInputElement = document.getElementById("flow-value-input");

const modalTitle = document.querySelector(".modal-title");
const modalBodyText = document.querySelector(".modal-body-text");
const modalBodyTextAreaInput = document.querySelector(".modal-body-textarea");
const modalFileInput = document.querySelector("#modal-file-upload");
const modalFileLabel = document.querySelector(".selected-file");
const modalSaveButton = document.querySelector(".modal-save");
const modalDismissButtons = document.querySelectorAll(".modal-dismiss");

let addIncome = false;
let addExpense = false;
let initialDate = null;
let data = {};
let url = "";

const saveFlow = async () => {
  const formData = new FormData();
  const file = modalFileInput.files[0];

  if (file) {
    formData.append("document", file);
  }
  for (const key in data) {
    formData.append(key, data[key]);
  }

  try {
    const response = await fetch(url, {
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    displayToastCustomMessage(data.message, response.status);
  } catch (error) {
    console.log(error.message);
  }
};

modalFileInput.addEventListener("change", (event) => {
  const file = event.target.files[0];
  const [name, ext] = file.name.split(".");
  modalFileLabel.innerHTML = name;
});

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
    let insertedValue = Number.parseFloat(
      value.replace(".", "").replace(",", ".")
    );

    data.asset_id = asset.value;
    data.date = date;

    if (flow === "entrada") {
      data.flow = "income";
      url = incomeButtonElement.dataset.url;
    } else {
      data.flow = "expense";
      url = expenseButtonElement.dataset.url;
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

const displayModal = (data, flow) => {
  let message = `Deseja mesmo criar uma ${flow} no valor de R$ ${data.value}`;
  modalBodyText.innerHTML = message;
  modalTitle.innerHTML = `Criar ${flow}`;

  if (flow === "saida") {
    modalBodyTextAreaInput.style.display = "block";
  } else {
    modalBodyTextAreaInput.style.display = "none";
  }
  new bootstrap.Modal(incomeExpenseModalElement).show();
};

flowValueInputElement.addEventListener("input", (event) => {
  flowValueInputElement.value = moneyMask(event.target.value);
});
