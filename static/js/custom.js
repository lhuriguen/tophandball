$(document).on('submit', '#follow_form', function() {
    var frm = $('#follow_form');
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        success: function(data) {
            $(".top-button-bar").html(data);
        },
        error: function(data) {
            alert("Something went wrong! Are you logged in?");
        }
    });
    return false;
});
