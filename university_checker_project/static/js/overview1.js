// doughnut_chart for overview

const doughnutChart1 = new Chart(document.getElementById('doughnutChart1'), {
    type: 'doughnut',
    data: {
        labels: ['Positive', 'Negative', 'Neutral'],
        datasets: [
            {
                data: [positiveCount, negativeCount, neutralCount],
                backgroundColor: [colors.primary, 'hsla(0, 100%, 65%, 0.793)', '#22c55e'],
                borderWidth: 0,
                weight: 0.5,
            },
        ],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
            position: 'bottom',
        },
        title: {
            display: false,
        },
        animation: {
            animateScale: true,
            animateRotate: true,
        },
    },
});


const barChart1 = new Chart(document.getElementById('barChart1'), {
    type: 'bar',
    data: {
      labels: uniqueMonthsPositive,  // Use the unique months as labels
      datasets: [
        {
          label: 'Positive Sentiment',
          data: positiveCounts,
          backgroundColor: colors.positive,
          hoverBackgroundColor: colors.positiveDark,
        },
      ],
    },
    options: {
      scales: {
        yAxes: [
          {
            gridLines: false,
            ticks: {
              beginAtZero: true,
              stepSize: 1,  // Assuming counts are integers
              fontSize: 12,
              fontColor: '#97a4af',
              fontFamily: 'Open Sans, sans-serif',
              padding: 10,
            },
          },
        ],
        xAxes: [
          {
            gridLines: false,
            ticks: {
              fontSize: 12,
              fontColor: '#97a4af',
              fontFamily: 'Open Sans, sans-serif',
              padding: 5,
            },
            categoryPercentage: 0.5,
            maxBarThickness: '10',
          },
        ],
      },
      cornerRadius: 2,
      maintainAspectRatio: false,
      legend: {
        display: true,
      },
    },
  });
  
  
  
