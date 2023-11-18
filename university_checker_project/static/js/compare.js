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
 
//  university 1 Doughnut charts
  const doughnutChart = new Chart(document.getElementById('doughnutChart'), {
    type: 'doughnut',
    data: {
      labels: ['Positive', 'Negative'],
      datasets: [
        {
          data: [url_positive, url_negative],
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

//   university 2 Doughnut chart
const doughnutChart1 = new Chart(document.getElementById('doughnutChart1'), {
    type: 'doughnut',
    data: {
      labels: ['Positive', 'Negative'],
      datasets: [
        {
          data: [select_positive, select_negative],
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

//   Line chart for comparison

  const lineChart = new Chart(document.getElementById('lineChart'), {
    type: 'line',
    data: {
      labels: uniqueMonthsPositive,
      datasets: [
        {
          label: university_url,
          data: urlpositiveCounts,
          fill: false,
          borderColor: colors.primary,
          borderWidth: 2,
          pointRadius: 0,
          pointHoverRadius: 0,
        },
        {
            label: selected_university,
            data: selectpositiveCounts,
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