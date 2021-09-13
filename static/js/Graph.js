

function viewGraph(a, b, c, d, e, f, g, h, i, j) {
    var xValues = [1,2,3,4,5,6,7,8,9,10];

new Chart("myChart", {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{ 
      data: [860,1140,1060,1060,1070,1110,1330,2210,7830,2478],
      borderColor: "red",
      fill: false
    }, { 
      data: [1600,1700,1700,1900,2000,2700,4000,5000,6000,7000],
      borderColor: "green",
      fill: false
    }, { 
      data: [300,700,2000,5000,6000,4000,2000,1000,200,100],
      borderColor: "blue",
      fill: false
    }]
  },
  options: {
    legend: {display: false},
    title: {display: true,
        text: "Green:Like / Red:Dislike / Blue:View",
        fontSize: 24
        
   }
  }
});

}








// google.charts.load('current', { packages: ['corechart'] });
// google.charts.setOnLoadCallback(drawChart);

// function drawChart() {
//     // Set Data
//     var data = google.visualization.arrayToDataTable([
//         ['Video', 'Likes'],
//         [1, 7], [2, 8], [3, 8], [4, 8], [5, 11],

//         [6, 7], [7, 8], [8, 8], [9, 8], [10, 11],
//     ]);
//     // Set Options
//     var options = {
//         title: 'Videos & Likes',
//         hAxis: { title: 'Video  (10 = Latest Videos)' },
//         vAxis: { title: 'Likes' },
//         legend: 'none'
//     };
//     // Draw
//     var chart = new google.visualization.LineChart(document.getElementById('myChart2'));
//     chart.draw(data, options);
// }
