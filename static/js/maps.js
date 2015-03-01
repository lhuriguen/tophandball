function initialize() {

    var pathname = window.location.pathname;
    var mapUrl = pathname.replace("teams", "map");

    var locations = [];
    $.getJSON(mapUrl, function(json) {

        $.each(json, function(key) {
            locations.push(json[key].fields);
        });

        drawLocations();
    });

    function drawLocations() {

        window.map = new google.maps.Map(document.getElementById('map'), {
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        var infowindow = new google.maps.InfoWindow();
        var bounds = new google.maps.LatLngBounds();

        for (i = 0; i < locations.length; i++) {
            if (locations[i]['latitude'] == 0) {
                continue;
            };
            marker = new google.maps.Marker({
                position: new google.maps.LatLng(locations[i]['latitude'], locations[i]['longitude']),
                map: map
            });

            bounds.extend(marker.position);

            google.maps.event.addListener(marker, 'click', (function(marker, i) {
                return function() {
                    infowindow.setContent(locations[i]['name']);
                    infowindow.open(map, marker);
                }
            })(marker, i));
        }

        map.fitBounds(bounds);

    }
}

function loadScript() {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp' +
        '&signed_in=true&callback=initialize';
    document.body.appendChild(script);
}

window.onload = loadScript;
