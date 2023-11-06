// All javascript code in this project for now is just for demo DON'T RELY ON IT

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
  
  const doughnutChart = new Chart(document.getElementById('doughnutChart'), {
    type: 'doughnut',
    data: {
      labels: ['Positive', 'Negative'],
      datasets: [
        {
          data: [random(), random()],
          backgroundColor: [colors.primary,'hsla(0, 100%, 65%, 0.793)'],
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

//   comparison chart
const doughnutChart1 = new Chart(document.getElementById('doughnutChart1'), {
    type: 'doughnut',
    data: {
      labels: ['Positive', 'Negative'],
      datasets: [
        {
          data: [random(), random()],
          backgroundColor: [colors.primary,'hsla(0, 100%, 65%, 0.793)'],
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
//   end donut

  const lineChart = new Chart(document.getElementById('lineChart'), {
    type: 'line',
    data: {
      labels: months,
      datasets: [
        {
          label: 'University 1',
          data: randomData(),
          fill: false,
          borderColor: colors.primary,
          borderWidth: 2,
          pointRadius: 0,
          pointHoverRadius: 0,
        },
        {
            label: 'University 2',
            data: randomData(),
            fill: false,
            borderColor: 'hsla(0, 100%, 65%, 0.793)',
            borderWidth: 2,
            pointRadius: 0,
            pointHoverRadius: 0,
          },
      ],
    },
    options: {
      responsive: true,
      scales: {
        yAxes: [
          {
            gridLines: false,
            ticks: {
              beginAtZero: false,
              stepSize: 50,
              fontSize: 12,
              fontColor: '#97a4af',
              fontFamily: 'Open Sans, sans-serif',
              padding: 20,
            },
          },
        ],
        xAxes: [
          {
            gridLines: false,
          },
        ],
      },
      maintainAspectRatio: false,
      legend: {
        display: false,
      },
      tooltips: {
        hasIndicator: true,
        intersect: false,
      },
    },
  })

//   test


  