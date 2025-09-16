
// Bar Chart Example
var gsa = document.getElementById("graficosStatusAlunos");
if (gsa) {
  let status = [];
  let qtdAlunos = [];

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
        label: "Quantidade",
        backgroundColor: ["rgba(2,117,216,1)", "rgba(216, 216, 2, 1)", "rgba(216, 2, 2, 1)"],
        borderColor: "rgba(2,117,216,1)",
        data: qtdAlunos,
      }],
    },
    options: {
        scales: {
           y: {
            beginAtZero: true,
           }
        }
    }
  });
}

var gaa = document.getElementById("graficosAlunosAtivosPorSala");
if (gaa) {
  let classe = [];
  let qtdAlunosClasse = [];
  let cores = []

  function corAleatoria(alpha = 1) {
    const r = Math.floor(Math.random() * 256); // 0–255
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }

  graficosAlunosAtivos.forEach(element => {
    classe.push(element.sala__nome);
    qtdAlunosClasse.push(element.total);
    cores.push(corAleatoria());
  });

  const grafico = new Chart(gaa, {
    type: 'bar',
    data: {
      labels: classe,
      datasets: [{
        label: "Quantidade",
        backgroundColor: cores,
        borderColor: "rgba(2,117,216,1)",
        data: qtdAlunosClasse,
      }],
    },
    options: {
        scales: {
           y: {
            beginAtZero: true,
           }
        }
    }
  });
}
