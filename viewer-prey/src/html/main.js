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
                backgroundColor: 'rgb(255,0,0)',
                pointRadius: 5
            }, {
                data: [],
                backgroundColor: 'rgb(153,50,204)',
                pointRadius: 10
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
                    min: 0,
                    max: 1000,
                    ticks: {
                        stepSize: 50
                    }
                },
                y: {
                    min: 0,
                    max: 1000,
                    ticks: {
                        stepSize: 50
                    }
                },
            },
            animation: {
                duration: 0
            }
        }
    };

    const chart = new Chart(ctx, config);
    return chart;
};

function updateChart(websocket, chart) {
    websocket.addEventListener("message", ({data}) => {
        const event = JSON.parse(data);
        const preddata = event.filter(obj => obj.type === "predator");
        const preydata = event.filter(obj => obj.type === "prey");
        chart.data.datasets[0].data = preddata;
        chart.data.datasets[1].data = preydata;
        chart.update();
        // document.getElementById("demo").innerHTML = preddata[0].type;
        // document.getElementById("demo").innerHTML = 1;
    })
} 
