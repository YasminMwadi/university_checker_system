// doughnut_chart for overview
const cssColors = (color) => {
  return getComputedStyle(document.documentElement).getPropertyValue(color)
}

const getColor = () => {
  return window.localStorage.getItem('color') ?? 'blue'
}

const colors = {
  primary: cssColors(`--color-${getColor()}`),
  primaryLight: cssColors(`--color-${getColor()}-light`),
  primaryLighter: cssColors(`--color-${getColor()}-lighter`),
  primaryDark: cssColors(`--color-${getColor()}-dark`),
  primaryDarker: cssColors(`--color-${getColor()}-darker`),
}

const doughnutChart = new Chart(document.getElementById('doughnutChart'), {
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

const barChart = new Chart(document.getElementById('barChart'), {
  type: 'bar',
  data: {
      labels: uniqueMonthsPositive,  // Use the unique months as labels
      datasets: [
          {
              label: 'Positive Sentiment',
              data: positiveCounts,
              backgroundColor: colors.primary,
              hoverBackgroundColor: colors.primaryDark,
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
