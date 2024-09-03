const csrftoken = getCookie("csrftoken");

const currentYear =
  document.getElementById("monthly-income").dataset.currentYear;

const annualIncomeUrl = document.getElementById("annual-income").dataset.url;
const annualIncomeCanvas = document.getElementById("annual-income-canvas");

let monthlyIncomeChart;
const monthlyIncomeUrl = document.getElementById("monthly-income").dataset.url;
const monthlyIncomeCanvas = document.getElementById("monthly-income-canvas");
const monthlyIncomeSelect = document.getElementById("monthly-income-select");
monthlyIncomeSelect.addEventListener("change", monthlyIncomeChartHandler);

updateAnnualIncomeChart();
updateMonthlyIncomeChart(currentYear);

async function updateAnnualIncomeChart() {
  const response = await fetch(annualIncomeUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
  });
  const data = await response.json();
  new Chart(annualIncomeCanvas, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Entrada em R$",
          backgroundColor: "rgba(255,255,255,0.5)",
          borderColor: "rgba(255,255,255,1)",
          borderWidth: 2,
          hoverBackgroundColor: "rgba(255,255,255,0.7)",
          hoverBorderColor: "rgba(255,255,255,1)",
          data: data.values,
          borderWidth: 1,
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          stacked: true,
          grid: {
            display: true,
            color: "rgba(255,255,255,0.2)",
          },
        },
        x: {
          grid: {
            display: false,
          },
        },
      },
    },
  });
}

function monthlyIncomeChartHandler() {
  monthlyIncomeChart.destroy();
  monthlyIncomeChart = null;
  updateMonthlyIncomeChart(this.value);
}

async function updateMonthlyIncomeChart(year) {
  const response = await fetch(monthlyIncomeUrl, {
    method: "POST",
    body: JSON.stringify({ year }),
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
  });

  const data = await response.json();

  monthlyIncomeChart = new Chart(monthlyIncomeCanvas, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Entrada em R$",
          backgroundColor: "rgba(255,255,255,0.5)",
          borderColor: "rgba(255,255,255,1)",
          borderWidth: 2,
          hoverBackgroundColor: "rgba(255,255,255,0.7)",
          hoverBorderColor: "rgba(255,255,255,1)",
          data: data.values,
          borderWidth: 1,
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          stacked: true,
          grid: {
            display: true,
            color: "rgba(255,255,255,0.2)",
          },
        },
        x: {
          grid: {
            display: false,
          },
        },
      },
    },
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
