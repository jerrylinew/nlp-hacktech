window.onload = function()
{
    //updateWidth();
    chart = document.getElementById("myChart");
    var ctx = chart.getContext("2d");
    var data = {
        labels: ["12:00 AM", "02:00 AM", "04:00 AM", "06:00 AM", "08:00 AM", "10:00 AM", "12:00 PM", "02:00 PM", "04:00 PM", "06:00 PM", "08:00 PM", "10:00 PM", "12:00 AM"],
        datasets: 
            [{
                label: "Number of Red Flagged Messages",
                fillColor: "rgba(0,85,186,0.5)",
                strokeColor: "rgba(220,220,220,0.8)",
                highlightFill: "rgba(0,165,229,0.75)",
                highlightStroke: "rgba(220,220,220,1)",
                data: [0, 0, 0, 0, 0, 5, 5, 6, 8, 5, 3, 1, 0]
            }],
        options: {
            title: {
                display: true,
                position: 'top',
                text: 'Number of Red Flagged Messages'
            }
        }
    };
    myNewChart = new Chart(ctx).Line(data, {barShowStroke: false});

    $('.select').on('click', function(){
        $('.toggle').hide();
        id = $(this).attr('id');
        $('.u' + id).show();
    });
}
