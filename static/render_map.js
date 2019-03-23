var map;

function drawMap(data){
    let obj = JSON.parse(data);
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: obj.lat, lng: obj.lon},
        zoom: 15
    });

    for(var i=0; i<obj.vehicles.length; i++){
        bus = obj.vehicle[i];
      var marker = new google.maps.Marker({
        position: new google.maps.LatLng(
            bus.lat, bus.lon
        ),
        title: 'My Location',
        map: map
    });
      filteredDepartures = obj.departures.filter(function (departure) {
          return departure.BlockNumber == bus.block;
      });
      marker.addListener('click', function () {
          showDirections(filteredDepartures)
      });
    }
};

function showDirections(departures){
    for(var i=0; i<departures.length; i++){
        d = departures[i];
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(
            d.lat, d.lon
        ),
        map: map
    });
      contentInfo = "Name: " + d.name + "\n DepartureText: " + d.DepartureText
      var info = new google.maps.InfoWindows({
          content: contentInfo
      });
      marker.addListener('click', function () {
          info.open(map, marker)
      })
    }
}