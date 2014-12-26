
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
    $("#id_query").val("");

    return false;
}

function filterClubMatches() {
    var form_data = $("#club-match-filter").serialize();

    $.get("?", form_data, function(data) {
        $("#macth-list").html(data);
    });

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
                            id: item.pk,
                            url: "/data/players/" + item.pk + "/"
                        };
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

function makeSelect2Club(sel) {
    sel.select2({
        minimumInputLength: 3,
        ajax: {
            url: "/data/api/club_search/",
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
                            text: item.fields.name,
                            id: item.pk,
                            url: "/data/clubs/" + item.pk + "/"
                        };
                    })
                };
            }
        },
        initSelection : function (element, callback) {
            var id=$(element).val();
            if (id!=="") {
                $.ajax("/data/api/club/" + id +"/", {
                    dataType: "json"
                }).done(function (data) {
                    callback({
                        id: data[0].pk,
                        text: data[0].fields.name
                    });
                });
            }
        }
    });
}

function makeSelect2Search(sel) {
    sel.select2({
        minimumInputLength: 3,
        ajax: {
            url: "/data/api/search_all/",
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
                        var model = item.model;
                        var url = (model == "data.club" ? "/data/clubs/" : "/data/players/");
                        var name = (model == "data.club" ? item.fields.name : item.fields.first_name + ' ' + item.fields.last_name);
                        return {
                            text: name,
                            id: item.pk,
                            url: url + item.pk + "/",
                            type: model
                        };
                    })
                };
            }
        },
        formatResult : function(item) {
            var css_class = "";
            if (item.type == "data.club") {
                css_class = "fa-group";
            } else {
                css_class = "fa-user";
            }
            return '<i class="fa ' + css_class + '"></i> ' + item.text
        },
    });
}

function makeSelect2(sel) {
    sel.select2({
        minimumResultsForSearch: 10
    });
}

function centerModal() {
    $(this).css('display', 'block');
    var $dialog = $(this).find(".modal-dialog");
    var offset = ($(window).height() - $dialog.height()) / 2;
    // Make sure you don't hide the top part of the modal w/ 
    // a negative margin if it's longer than the screen height,
    // and keep the margin equal to the bottom margin of the modal
    var bottomMargin = $dialog.css('marginBottom');
    bottomMargin = parseInt(bottomMargin);
    if(offset < bottomMargin) offset = bottomMargin;
    $dialog.css("margin-top", offset);
}

function genericUnfollow() {
    var btn = $(this);
    $.ajax({
        type: 'POST',
        url: '/data/unfollow/',
        data: btn.data(),
        success: function(data) {
            btn.closest('li').remove();
        },
        error: function(data) {
            if (data.status == 401) {
                window.location.href = data.responseText + '?next=' + window.location.pathname;
            } else {
                alert("Something went wrong!");
            }
        }
    });
}

var main = function() {

    $("#search-form").submit(search_submit);
    $("#club-match-filter").submit(filterClubMatches);

    $("#follow").click(function(e) {
        e.preventDefault();
    });

    $(".list_follow").submit(follow);
    $("#follow_form").submit(follow);
    $(".user-unfollow").click(genericUnfollow);

    $("select").addClass("th-selectable");
    makeSelect2Player($(".select-player"));
    makeSelect2Club($(".select-club"));
    makeSelect2Search($(".select-search"));
    makeSelect2($(".th-selectable"));

    $('.th-search-go').on("change", function() {
        var x = $(this).select2('data');
        window.location.href = x.url;
    });

    $(".dateinput").datepicker({
        format: 'dd/mm/yyyy',
        autoclose: true,
        weekStart: 1
    });

    $(".th-toggler").click(function() {
        $(this).children("i").toggleClass("fa-chevron-up fa-chevron-down");
    });

    $('.modal').on('show.bs.modal', centerModal);
    $(window).on("resize", function () {
        $('.modal:visible').each(centerModal);
    });
};

$(document).ready(main);
