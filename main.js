window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://localhost:8001");
    let event = {type: "viewer"};
    websocket.onopen = () => websocket.send(JSON.stringify(event));
    var chart = setupChart();
    updateChart(websocket, chart);
});

function setupChart() {
    const ctx = document.getElementById('sim-chart');

    const config = {
        type: 'scatter',
        data: {
            datasets: [{
                data: [],
                backgroundColor: 'rgb(255,0,0)'
            }],
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    min: 1,
                    max: 20,
                    ticks: {
                        stepSize: 1
                    }
                },
                y: {
                    min: 1,
                    max: 20,
                    ticks: {
                        stepSize: 1
                    }
                },
            }
        }
    };

    const chart = new Chart(ctx, config);
    return chart;
};

function updateChart(websocket, chart) {
    websocket.addEventListener("message", ({data}) => {
        const event = JSON.parse(data);
        chart.data.datasets[0].data = event;
        chart.update();
    })
}