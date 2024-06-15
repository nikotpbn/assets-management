const labels = document.querySelector(".annual-income").dataset.labels;
const data = document.querySelector(".annual-income").dataset.data;
const ctx = document.getElementById("myChart");

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
