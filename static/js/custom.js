
var follow = function() {
    var frm = $(this);
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        success: function(data) {
            //alert("Something went OK!");
            frm.html(data);
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
};

function search_submit() {
    var query = $("#id_query").val();

    $("#search-results").load(
        "?name=" + encodeURIComponent(query)
    );
    $("#id_query").val("")

    return false;
}

var main = function() {

    $("#search-form").submit(search_submit);

    $("#follow").click(function(e) {
        e.preventDefault();
    });

    $(".list_follow").submit(follow);
    $("#follow_form").submit(follow);

    $(".selectable").select2({
        placeholder: "Select an item",
        minimumInputLength: 2
    });

};

$(document).ready(main);
