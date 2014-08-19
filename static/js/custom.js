
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

function makeSelect2Player(sel) {
    sel.select2({
        minimumInputLength: 2,
        ajax: {
            url: "/data/api/player_search/",
            dataType: 'json',
            type: "GET",
            quietMillis: 50,
            data: function (term) {
                return {
                    q: term
                };
            },
            results: function (data) {
                return {
                    results: $.map(data, function (item) {
                        return {
                            text: item.fields.first_name + ' ' + item.fields.last_name ,
                            id: item.pk
                        }
                    })
                };
            }
        },
        initSelection : function (element, callback) {
            var id=$(element).val();
            if (id!=="") {
                $.ajax("/data/api/player/" + id +"/", {
                    dataType: "json"
                }).done(function (data) {
                    callback({
                        id: data[0].pk,
                        text: data[0].fields.first_name + ' ' + data[0].fields.last_name
                    });
                });
            }
        }
    });
}

var main = function() {

    $("#search-form").submit(search_submit);

    $("#follow").click(function(e) {
        e.preventDefault();
    });

    $(".list_follow").submit(follow);
    $("#follow_form").submit(follow);

    makeSelect2Player($(".select-player"));

    // $(".select2-player").select2({
    //     minimumInputLength: 2,
    //     ajax: {
    //         url: "/data/api/player_search/",
    //         dataType: 'json',
    //         type: "GET",
    //         quietMillis: 50,
    //         data: function (term) {
    //             return {
    //                 q: term
    //             };
    //         },
    //         results: function (data) {
    //             return {
    //                 results: $.map(data, function (item) {
    //                     return {
    //                         text: item.fields.first_name + ' ' + item.fields.last_name ,
    //                         id: item.pk
    //                     }
    //                 })
    //             };
    //         }
    //     },
    //     initSelection : function (element, callback) {
    //         var id=$(element).val();
    //         if (id!=="") {
    //             $.ajax("/data/api/player/" + id +"/", {
    //                 dataType: "json"
    //             }).done(function (data) {
    //                 callback({
    //                     id: data[0].pk,
    //                     text: data[0].fields.first_name + ' ' + data[0].fields.last_name
    //                 });
    //             });
    //         }
    //     }
    // });

    $(".selectable").select2();

};

$(document).ready(main);
