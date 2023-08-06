
var endpoint = '/api/cont/pos/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        const dt = {
            labels: data.label,
            datasets: [{
                label: 'Pojisaun',
                data: data.obj,
                backgroundColor: 'rgba(229, 230, 126, 0.75)',
                borderWidth: 1
            }]
        };
        
        const config_contpos = {
            type: 'bar',
            data: dt,
            options: myoption
        };
        const contposChart_data = new Chart(
            document.getElementById('contposChart_data'),
            config_contpos
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
