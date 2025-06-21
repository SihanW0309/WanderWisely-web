
function initMap() {

    const locations = JSON.parse(document.getElementById('locations').getAttribute("locations"))
    var directionsService = new google.maps.DirectionsService();
    var directionsRenderer = new google.maps.DirectionsRenderer();
    // convert locations[list of list] to list of dict
    const laglngs = []

    locations.map((position, i) => {
        laglngs.push({ lat: position[0], lng: position[1] })
    });

    // const location_names = JSON.parse(document.getElementById('location_names').getAttribute("location_names"));


    const startLatLng = laglngs[0];

    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 11,
        center: startLatLng,
        gestureHandling: "greedy",
        mapId:'d5a1921b1f1eed54'
    });


    const svgMarker = {
        path: "M22,9.81a1,1,0,0,0-.83-.69l-5.7-.78L12.88,3.53a1,1,0,0,0-1.76,0L8.57,8.34l-5.7.78a1,1,0,0,0-.82.69,1,1,0,0,0,.28,1l4.09,3.73-1,5.24A1,1,0,0,0,6.88,20.9L12,18.38l5.12,2.52a1,1,0,0,0,.44.1,1,1,0,0,0,1-1.18l-1-5.24,4.09-3.73A1,1,0,0,0,22,9.81Z",
        fillColor: "#00468b",
        fillOpacity: 1,
        strokeWeight: 0,
        rotation: 0,
        scale: 0.5,
        anchor: new google.maps.Point(0, 20),
    };

    laglngs.map((laglng, i) => {
        let num = i
        new google.maps.Marker({
            position: laglng,
            map: map,
            icon: svgMarker,
            //label: num.toString(),
            animation: google.maps.Animation.DROP,
            // title: location_names[i].replaceAll("_"," "),
        })

    });



    directionsRenderer.setMap(map)
    calcRoute(directionsService, directionsRenderer, locations)
    }
    function calcRoute(directionsService, directionsRenderer, locations) {
      const waypts = [];

      for (let i = 1; i < locations.length-1; i++) {
          waypts.push({
            location: new google.maps.LatLng(locations[i][0], locations[i][1]),
            stopover: true,
          });
      }
      directionsService
        .route({
          origin: new google.maps.LatLng(locations[0][0], locations[0][1]),
          destination: new google.maps.LatLng(locations[locations.length-1][0], locations[locations.length-1][1]),
          waypoints: waypts,
          optimizeWaypoints: true,
          travelMode: google.maps.TravelMode.WALKING,
        })
        .then((response) => {
          directionsRenderer.setDirections(response);
    })
}

window.initMap = initMap;

