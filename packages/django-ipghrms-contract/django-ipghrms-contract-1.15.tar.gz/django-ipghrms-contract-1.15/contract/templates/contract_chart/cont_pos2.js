
var endpoint = '/api/cont/pos/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        obj = data.obj
        legend = 'DISTRIBUISAUN FUNSIONARIO TUIR EKIPA'
        categories = data.label
        contPostChart()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function contPostChart(){
    Highcharts.chart('contposChart_data', {
        chart: {
            type: 'bar'
        },
        title: {
            align: 'center',
            text: legend
        },
        subtitle: {
        },
        accessibility: {
            announceNewData: {
                enabled: true
            }
        },
        xAxis: {
            categories: categories,
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total Staff',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
    
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
    
        tooltip: {
            formatter: function () {
                return this.point.name + ': ' + this.y;
            }
        },
    
        series: [
            {
                name: "Ekipa",
                colorByPoint: true,
                data:obj
            }
        ],
        drilldown: {
            breadcrumbs: {
                position: {
                    align: 'right'
                }
            },
            series: [
            ]
        }
    });


}




