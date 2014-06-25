//TODO: Fix first line when id's change
$(function() {
    $("#time-slider").slider({
        min: 1,
        max: 12,
        step : 1,
        slide: function(event, ui) {
            $.ajax("/mock-ajax", {
                type : 'GET',
                success : function(response){
                    var newData = {max : response.max_val, data : response.data};
                    heatmap.setDataSet(newData);
                }
            });
        }
    });
});

//TODO: Fix first line when id's change