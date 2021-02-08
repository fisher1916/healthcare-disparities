var locURL = "/getallmortalities/anyjunkhere";

d3.json(locURL).then((location) => {
  console.log(location);
  L.tileLayer(
    "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
    {
      attribution:
        "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
      tileSize: 512,
      maxZoom: 18,
      zoomOffset: -1,
      id: "mapbox/streets-v11",
      accessToken: API_KEY,
    }
  ).addTo(myMap);
  
  var quakeMarker = L.geoJson(location.counties, {
    // Style each feature (in this case a neighborhood)
    pointToLayer: function (county, latlng) {
      console.log(latlng)
      return L.circleMarker(latlng);      
    },
    // Called on each feature
    // onEachFeature: function (county, layer) {
    //   // Set mouse events to change map styling
    //   layer.bindPopup(
    //     "<h1>" +
    //       county.properties.mag +
    //       "</h1> <hr> <h2>" +
    //       county.properties.place +
    //       "</h1> <hr> <h2>" +
    //       new Date(county.properties.time) +
    //       "</h2>"
    //   );
    // },
    // style: function (county) {
    //   return {
    //     color: "black",
    //     // Call the chooseColor function to decide which color to color our neighborhood (color based on borough)
    //     fillColor: chooseColor(county.geometry.coordinates[2]),
    //     fillOpacity: 0.5,
    //     radius: county.properties.mag * 4,
    //     weight: 1.5,
    //   };
    // },
  });
});
// Creating map object
var myMap = L.map("mapid", {
  center: [37.0902, -95.7129],
  zoom: 4,
});


