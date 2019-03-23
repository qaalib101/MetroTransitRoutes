var map, directionsService;
var directionsDisplay;
var request;
let markers = [];
var radius = $('#selected_route').find(":selected").val()
$(document).ready(function () {
   $("#show_button").click( function(){
      $.post(
          "/get_map",
          {radius: $("#selected_route").find(":selected").val()},
          function (data) {
             drawMap(data)
          });
   });
   $("#clear_button").click(function () {
       removeMarkersAndDirections()
       });
   $("#clear_direction").click(function () {
       removeDirections()
   })
});
function resetMap(){
    $.post(
          "/get_map",
          {radius: $("#selected_route").find(":selected").val()},
          function (data) {
              drawMap(data);
          });
}
function initMap() {
            $.get('/get_location', function (data) {
                var obj = JSON.parse(data);
                map = new google.maps.Map(document.getElementById('map'), {
                    center: {lat: obj.lat, lng: obj.lon},
                    zoom: 15,
                    mapTypeControl: true,
                    mapTypeControlOptions: {
                        style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
                    },
                    navigationControl: true,
                    mapTypeId: google.maps.MapTypeId.ROADMAP
                });
                var marker = new google.maps.Marker({
                    position: new google.maps.LatLng(
                        obj.lat, obj.lon
                    ),
                    title: 'My Location',
                    map: map
                });
            });
}
function removeDirections(){
    directionsDisplay.setMap(null);
}
function removeMarkersAndDirections() {
    directionsDisplay.setMap(null);
    if(markers.length > 0){
       for (var i = 0; i < markers.length; i++ ) {
           markers[i].setMap(null);
       }
       markers = [];
    }
}
function drawMap(data){
    let obj = JSON.parse(data);
    for(var i=0; i<obj.vehicles.length; i++){
        bus = obj.vehicles[i];
        filteredDepartures = obj.departures.filter(function (departure) {
          return departure.BlockNumber == bus.BlockNumber;
      });
        nextDeparture = filteredDepartures[0];
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(
                bus.VehicleLatitude, bus.VehicleLongitude
            ),
            icon:{
                url: "http://www.geocodezip.com/mapIcons/bus_blue.png",
                scaledSize: new google.maps.Size(15, 15),
                anchor: new google.maps.Point(5, 5)
            },
            title:"Route: "+ bus.Route+ " ID: "+ bus.BlockNumber,
            map: map
        });
        markers.push(marker);
        contentInfo = '<div id="content">'+
            '<p><b>Next Arrival: </b>'+
            ' Time: '+nextDeparture.DepartureText+
            ' Stop Location: '+ nextDeparture.name+
            '</p>' + '</div>';
        var info = new google.maps.InfoWindow({
          content: contentInfo
        });
      marker.addListener('click', function () {
          showDirections(bus,nextDeparture);
          info.open(map, marker);
      });
    }
   setInterval(resetMap(), 10000)
};

var calculateAndRenderDirections = (origin, destination) =>{
    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer();
    request = { origin: new google.maps.LatLng(origin.VehicleLatitude, origin.VehicleLongitude),
            destination: new google.maps.LatLng(destination.lat, destination.lon),
            travelMode: 'DRIVING'
        };
    directionsDisplay.setMap(map);
    directionsDisplay.setOptions({
        suppressInfoWindows: true,
        suppressMarkers: true
    });
    directionsService.route(request, (result, status)=>{
        if(status == 'OK'){
            directionsDisplay.setDirections(result)
            var marker = new google.maps.Marker({
            position: request.origin,
            icon:{
                url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
                scaledSize: new google.maps.Size(15, 15),
                anchor: new google.maps.Point(5, 5)
            },
            map: map
            });
            contentInfo = '<div id="content">'+
            '<p><b>Next Arrival: </b>'+
                'Address: '+ nextDeparture.name+
            '</p>' + '</div>';
            var info = new google.maps.InfoWindow({
                content: contentInfo
            });
            marker.addListener('click', function () {
                showDirections(bus,nextDeparture);
                info.open(map, marker);
            });
            markers.push(marker)
        }
    });
}
function showDirections(bus, departure){
    calculateAndRenderDirections(bus, departure)
}