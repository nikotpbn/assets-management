import { getCookie, sendRequest } from "/static/js/util.js";

let selectedConsumerUnity = "W";
let selectedConsumerunityElement = null;
let asset = { id: null, unities: null };
let notEditing = true;

const headers = {
  "Content-Type": "application/json",
  "X-CSRFToken": getCookie("csrftoken"),
};

const waterButtonElement = document.getElementById("wtr");
const energyButtonElement = document.getElementById("eng");
const gasButtonElement = document.getElementById("gas");
const assetSelectElement = document.getElementById("asset");
const editUnitButtonElement = document.getElementById("edit-unit");
const editUnitButtonIcon = document.getElementById("edit-unit__icon");
const consumerUnitCardTitle = document.getElementById(
  "consumer-unit__card--title"
);
const consumerUnitCardText = document.getElementById(
  "consumer-unit__card--text"
);
const unitNumberInputElement = document.getElementById("unit-number__input");

assetSelectElement.addEventListener("change", async (event) => {
  await updateAsset();
  switch (selectedConsumerUnity) {
    case "W":
      updateWaterUnity();
      break;
    case "E":
      updateEnergyUnity();
      break;
    case "G":
      updateGasUnity();
      break;
  }
});

const resetUnitButtonElements = () => {
  const buttons = [
    waterButtonElement,
    energyButtonElement,
    gasButtonElement,
    editUnitButtonElement,
  ];
  buttons.forEach((element) => {
    element.classList.remove("active");
  });
  stopEditing();
};

const startEditing = () => {
  editUnitButtonIcon.classList.remove("bi-pencil-square");
  editUnitButtonIcon.classList.add("bi-check-square");
  unitNumberInputElement.disabled = false;
  notEditing = false;
  addOrRemoveActiveClass(editUnitButtonElement, "add");
  unitNumberInputElement.focus();
};

const stopEditing = () => {
  editUnitButtonIcon.classList.remove("bi-check-square");
  editUnitButtonIcon.classList.add("bi-pencil-square");
  unitNumberInputElement.disabled = true;
  notEditing = true;
  addOrRemoveActiveClass(editUnitButtonElement, "remove");
};

const editButtonIconHandler = async () => {
  if (notEditing) {
    startEditing();
  } else {
    stopEditing();
    let unitySymbol = consumerUnitCardTitle.innerHTML;
    let newUnityNumber = unitNumberInputElement.value;

    const unityElement = asset.unities.find(
      (element) => element.source === selectedConsumerUnity
    );

    if (unityElement.number != newUnityNumber) {

      try {
        let response = await sendRequest(
          editUnitButtonElement.dataset.url,
          "POST",
          headers,
          {
            asset_id: assetSelectElement.value,
            source: selectedConsumerUnity,
            number: newUnityNumber,
          }
        );

        unityElement.number = newUnityNumber;


      } catch (error) {
        console.log(error.message);
      }
    }
  }
};

editUnitButtonElement.addEventListener("click", (event) => {
  editButtonIconHandler();
});

waterButtonElement.addEventListener("click", (event) => {
  resetUnitButtonElements();
  selectedConsumerUnity = "W";
  updateWaterUnity();

  selectedConsumerunityElement = waterButtonElement;
  addOrRemoveActiveClass(selectedConsumerunityElement, "add");
});

energyButtonElement.addEventListener("click", (event) => {
  resetUnitButtonElements();
  selectedConsumerUnity = "E";
  updateEnergyUnity();

  selectedConsumerunityElement = energyButtonElement;
  addOrRemoveActiveClass(selectedConsumerunityElement, "add");
});

gasButtonElement.addEventListener("click", (event) => {
  resetUnitButtonElements();
  selectedConsumerUnity = "G";
  updateGasUnity();

  selectedConsumerunityElement = gasButtonElement;
  addOrRemoveActiveClass(selectedConsumerunityElement, "add");
});

const updateAsset = async () => {
  try {
    let response = await sendRequest(
      assetSelectElement.dataset.url,
      "POST",
      headers,
      { asset_id: assetSelectElement.value }
    );
    let unities = await JSON.parse(response.unities);
    asset.id = assetSelectElement.value;
    asset.unities = unities;
  } catch (error) {
    console.log(error.message);
  }
};

const updateWaterUnity = () => {
  let unity = asset.unities.find((el) => el.source === "W");
  let unityNumber = unity == null ? "" : unity.number;
  consumerUnitCardChangeContent("Água", unityNumber);
};

const updateEnergyUnity = () => {
  let unity = asset.unities.find((el) => el.source === "E");
  let unityNumber = unity == null ? "" : unity.number;
  consumerUnitCardChangeContent("Eletrecidade", unityNumber);
};

const updateGasUnity = () => {
  let unity = asset.unities.find((el) => el.source === "G");
  let unityNumber = unity == null ? "" : unity.number;
  consumerUnitCardChangeContent("Gás", unityNumber);
};

const consumerUnitCardChangeContent = (title, text) => {
  consumerUnitCardTitle.innerHTML = title;
  //   consumerUnitCardText.innerHTML = text;
  unitNumberInputElement.value = text;
};

const addOrRemoveActiveClass = (element, action) => {
  if (action === "add") {
    element.classList.add("active");
  } else {
    element.classList.remove("active");
  }
};

window.addEventListener("load", async () => {
  await updateAsset();
  selectedConsumerunityElement = waterButtonElement;
  waterButtonElement.click();
  waterButtonElement.focus();
});
