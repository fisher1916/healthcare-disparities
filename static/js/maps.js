// Function to determine marker size based on population
function markerSize(value) {
  return value * 3000;
}

function getRaceColor(race) {
  var color = "green";
  if (race === "B") {
    color = "purple";
  }
  return color;
}

d3.json("/getallmortalities").then((data) => {
  //console.log(data);

  // Define arrays to hold created measure markers
  var copdMarkers = [];
  var haMarkers = [];
  var hfMarkers = [];
  var pnMarkers = [];

  data.forEach((location) => {
    // console.log(location);
    // COPD
    if (location["Death rate for COPD patients"] != null) {
      var measure = location["Death rate for COPD patients"];
      copdMarkers.push(
        L.circle(location.coordinates, {
          stroke: false,
          fillOpacity: 0.75,
          color: getRaceColor(measure.race),
          fillColor: getRaceColor(measure.race),
          radius: markerSize(measure.score),
        })
        .bindPopup(
          "<h3>" +
        `${measure.county}, ${measure.state}`+
        "</h1> <hr> <h4>" +
        `${measure.area}`+
        "</h1> <hr> <h4>" +
        `Score: ${measure.score}`)
      );
    }
    // Heart Attack
    if (location["Death rate for heart attack patients"] != null) {
      var measure = location["Death rate for heart attack patients"];
      console.log(measure)
      haMarkers.push(
        L.circle(location.coordinates, {
          stroke: false,
          fillOpacity: 0.75,
          color: getRaceColor(measure.race),
          fillColor: getRaceColor(measure.race),
          radius: markerSize(measure.score),
        }).bindPopup(
          "<h3>" +
        `${measure.county}, ${measure.state}`+
        "</h1> <hr> <h4>" +
        `${measure.area}`+
        "</h1> <hr> <h4>" +
        `Score: ${measure.score}`)
      );
    }
    // Heart Failure
    if (location["Death rate for heart failure patients"] != null) {
      var measure = location["Death rate for heart failure patients"];
      hfMarkers.push(
        L.circle(location.coordinates, {
          stroke: false,
          fillOpacity: 0.75,
          color: getRaceColor(measure.race),
          fillColor: getRaceColor(measure.race),
          radius: markerSize(measure.score),
        })
        .bindPopup(
          "<h3>" +
        `${measure.county}, ${measure.state}`+
        "</h1> <hr> <h4>" +
        `${measure.area}`+
        "</h1> <hr> <h4>" +
        `Score: ${measure.score}`)
      );
    }
    // Pneumonia
    if (location["Death rate for pneumonia patients"] != null) {
      var measure = location["Death rate for pneumonia patients"];
      pnMarkers.push(
        L.circle(location.coordinates, {
          stroke: false,
          fillOpacity: 0.75,
          color: getRaceColor(measure.race),
          fillColor: getRaceColor(measure.race),
          radius: markerSize(measure.score),
        })
        .bindPopup(
          "<h3>" +
        `${measure.county}, ${measure.state}`+
        "</h1> <hr> <h4>" +
        `${measure.area}`+
        "</h1> <hr> <h4>" +
        `Score: ${measure.score}`)
      );
    }
  });

  // Create base layers
  // Streetmap Layer
  var streetmap = L.tileLayer(
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
  );

  var lightmap = L.tileLayer(
    "https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
    {
      attribution:
        'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: "light-v10",
      accessToken: API_KEY,
    }
  );

  // Create two separate layer groups: one for cities and one for states
  var copd = L.layerGroup(copdMarkers);
  var ha = L.layerGroup(haMarkers);
  var hf = L.layerGroup(hfMarkers);
  var pn = L.layerGroup(pnMarkers);

  // Create a baseMaps object
  var baseMaps = {
    "Light Map": lightmap,
    "Street Map": streetmap,
  };

  // Create an overlay object
  var overlayMaps = {
    COPD: copd,
    "Heart Attack": ha,
    "Heart Failure": hf,
    Pneumonia: pn,
  };

  // Define a map object
  var myMap = L.map("mapid", {
    center: [37.09, -95.71],
    zoom: 4,
    layers: [lightmap, copd],
  });

  // Pass our map layers into our layer control
  // Add the layer control to the map
  L.control
    .layers(baseMaps, overlayMaps, {
      collapsed: false,
    })
    .addTo(myMap);

    var legend = L.control({ position: "bottomright" });

    legend.onAdd = function (myMap) {
      var div = L.DomUtil.create("div", "info legend"),
        labels = ["White", "Black"];
      colors = ["green", "purple"];
      // loop through our density intervals and generate a label with a colored square for each interval
      for (var i = 0; i < labels.length; i++) {
        div.innerHTML +=
          '<i style="background:' +
          colors[i] +
          '"></i> ' +
           (labels[i] ? "" + labels[i] + "<br>" : "+");
      }
  
      return div;
    };
    legend.addTo(myMap);

});
