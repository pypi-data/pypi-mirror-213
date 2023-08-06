
var endpoint = '/api/cont/type/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        obj = data.obj
        legend = 'DISTRIBUISAUN FUNSIONARIO TUIR TIPU KONTRATO'
        categories = data.label
        setContType()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function setContType(){
    const chart = new Highcharts.Chart({
        chart: {
            renderTo: 'contcatTypeChart_data',
            type: 'column',
            options3d: {
                enabled: true,
                alpha: 15,
                beta: 15,
                depth: 50,
                viewDistance: 25
            }
        },
        xAxis: {
            categories: categories
        },
        yAxis: {
            title: {
                enabled: false
            }
        },
        tooltip: {
            headerFormat: '<b>{point.key}</b><br>',
            pointFormat: 'Total Funsionario: {point.y}'
        },
        title: {
            text: legend
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    format: '{point.y}'
                }
            }
        },
        credits: {
            enabled: false
      },
        series: [{
            data: obj,
            colorByPoint: true
        }]
    });
    


}




