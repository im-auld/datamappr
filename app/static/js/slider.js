//TODO: Fix first line when id's change
$("#1").css("opacity", 1);
$(function() {
    $("#slider").slider({
        min: 1,
        max: 12,
        step : 1,
        slide: function(event, ui) {
            var prev = ui.value - 1;
            var next = ui.value +1;
            $("#" + prev).css("opacity", 0).fadeOut("slow");
            $("#" + ui.value).css("opacity", 1).fadeIn();
            $("#" + next).css("opacity", 0).fadeOut("slow"); 
        }
    });
});