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
            if (data.status == 401) {
                window.location.href = data.responseText + '?next=' + window.location.pathname;
            } else {
                alert("Something went wrong!");
            }
        }
    });
    return false;
});
