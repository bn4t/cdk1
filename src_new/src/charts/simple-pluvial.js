import {Data} from "../data";
import 'https://www.gstatic.com/charts/loader.js'

let data = new Data()

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    let pluvial_data = data.pluvial_data
    let data = new google.visualization.DataTable();
    data.addColumn('string', 'Date');
    data.addColumn('number', 'Rainfall');
    pluvial_data.forEach((row) => {
        data.addRow([row['date'], parseFloat(row['rainfall'])]);
    });

    let options = {
        title: 'Rainfall in the last 30 days',
        curveType: 'function',
        legend: { position: 'bottom' }
    };

    let chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, options);
}
