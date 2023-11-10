// the following code displays line and dougnut chart for a specific university

const random = (max = 100) => {
    return Math.round(Math.random() * max) + 20
  }
  
  const randomData = () => {
    return [
      random(),
      random(),
      random(),
      random(),
      random(),
      random(),
      random(),
      random(),
      random(),
      random(),
      random(),
      random(),
    ]
  }
  
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  
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
  
  const barChart = new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
      labels: months,
      datasets: [
        {
          data: randomData(),
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
              stepSize: 50,
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
        display: false,
      },
    },
  })
  
  const doughnutChart = new Chart(document.getElementById('doughnutChart'), {
    type: 'doughnut',
    data: {
      labels: ['Positive', 'Negative','Neutral'],
      datasets: [
        {
          data: [random(), random(), random()],
          backgroundColor: [colors.primary,'hsla(0, 100%, 65%, 0.793)', '#22c55e'],
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
  })


  