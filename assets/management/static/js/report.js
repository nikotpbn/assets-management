import { showBackdrop, hideBackdrop, showBackdropSpinner, hideBackdropSpinner } from "/static/js/backdrop.js";
import {
  getCookie,
  sendRequest,
  displayToastCustomMessage,
} from "/static/js/util.js";

const headers = {
  "Content-Type": "application/json",
  "X-CSRFToken": getCookie("csrftoken"),
};

const createReportButtons = document.querySelectorAll(".create-report-btn");
const reportContainer = document.querySelector(".report-container");

createReportButtons.forEach((element) => {
  element.addEventListener("click", (e) => {
    createReport(element.dataset.year, element.dataset.mode);
  });
});

const createReport = async (year, mode) => {
  const url = reportContainer.dataset.createReportUrl;
  const data = { year, mode };
  showBackdrop();
  showBackdropSpinner();
  const response = await sendRequest(url, "POST", headers, data);
  hideBackdropSpinner();
  hideBackdrop();
  displayToastCustomMessage(response.message, response.status);

  if (mode === "new") {
    setTimeout(() => {
      location.reload();
    }, 3000);
  }
};
