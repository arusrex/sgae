
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
