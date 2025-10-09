
// Bar Chart Example
var gsa = document.getElementById("graficosStatusAlunos");
if (gsa) {
  let status = [];
  let qtdAlunos = [];
  let coresGsa = ["rgba(2,117,216,0.5)", "rgba(255, 255, 5, 0.5)", "rgba(216, 2, 2, 0.5)"];

  if (graficoStatus) {
    graficoStatus.forEach(element => {
      status.push(element.status);
      qtdAlunos.push(element.total);
    });
  }

  const grafico = new Chart(gsa, {
    type: 'bar',
    data: {
      labels: status,
      datasets: [{
        label: "Quantidades",
        backgroundColor: coresGsa,
        borderColor: "rgba(2,117,216,1)",
        data: qtdAlunos,
      }],
    },
    options: {
      plugins: {
        legend: {
          display: true,
          labels: {
            generateLabels: function (grafico) {
              let legendasGsa = [];
              status.forEach((label, i) => {
                legendasGsa.push({
                  text: label,
                  fillStyle: coresGsa[i],
                  strokesStyle: coresGsa[i],
                  hidden: false,
                });
              });
              return legendasGsa;
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
        }
      },
      responsive: true,
    }
  });
}

var gaa = document.getElementById("graficosAlunosAtivosPorSala");
if (gaa) {
  let cores = []

  function corAleatoria(alpha = 0.5) {
    const r = Math.floor(Math.random() * 256); // 0–255
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }

  salasAtivos.forEach(element => {
    cores.push(corAleatoria());
  });

  const grafico = new Chart(gaa, {
    type: 'bar',
    data: {
      labels: salasAtivos,
      datasets: [{
        label: "Salas",
        backgroundColor: cores,
        borderColor: "rgba(2,117,216,1)",
        data: qtdAtivos,
      }],
    },
    options: {
      plugins: {
        legend: {
          display: true,
          labels: {
            generateLabels: function (grafico) {
              let legendas = [];
              salasAtivos.forEach((label, i) => {
                legendas.push({
                  text: label,
                  fillStyle: cores[i],
                  strokesStyle: cores[i],
                  hidden: false,
                });
              });
              return legendas;
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
        }
      },
      responsive: true,
    }
  });

}
