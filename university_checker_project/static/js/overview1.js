// your_doughnut_chart_script.js

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
