
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
        backgroundColor: "rgba(2,117,216,1)",
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
  let r = 0;
  let g = 0;
  let b = 0;

  graficosAlunosAtivos.forEach(element => {
    r += 15;
    g += 15;
    b += 15;
    classe.push(element.sala__nome);
    qtdAlunosClasse.push(element.total);
    cores.push(rgba(r,g,b,1));
  });

  console.log(cores);

  const grafico = new Chart(gaa, {
    type: 'bar',
    data: {
      labels: classe,
      datasets: [{
        label: "Quantidade",
        backgroundColor: "rgba(2,117,216,1)",
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
