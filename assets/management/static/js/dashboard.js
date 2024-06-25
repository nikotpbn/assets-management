const csrftoken = getCookie("csrftoken");

const labels = document.querySelector(".annual-income").dataset.labels;
const data = document.querySelector(".annual-income").dataset.data;
const ctx = document.getElementById("myChart");

const currentYear = document.getElementById("monthly-income").dataset.currentYear;

const monthlyIncomeUrl = document.getElementById("monthly-income").dataset.url;
const monthlyIncomeCanvas = document.getElementById("monthly-income-canvas");
const monthlyIncomeSelect = document.getElementById("monthly-income-select");
let monthlyIncomeChart;

monthlyIncomeSelect.addEventListener("change", chartHandler);

function chartHandler() {
  monthlyIncomeChart.destroy();
  monthlyIncomeChart = null;
  updateMonthlyIncomeChart(this.value);
};

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
          data: data.values,
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}
updateMonthlyIncomeChart(currentYear);

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

new Chart(ctx, {
  type: "bar",
  data: {
    labels: JSON.parse(labels),
    datasets: [
      {
        label: "Entrada em R$",
        data: JSON.parse(data),
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});
