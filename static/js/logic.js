// local url for mortality rates
var mortalityUrl = "/mortality";
var statesURL = "/states";
var mortalitiesUrl = "/mortalities/";

function mortalityMap(mortality) {
  var myMortality = "Unknown";
  switch (mortality) {
    case "Death rate for COPD patients":
      myMortality = "COPD";
      break;
    case "Death rate for heart attack patients":
      myMortality = "Heart Attack";
      break;
    case "Death rate for heart failure patients":
      myMortality = "Heart Failure";
      break;
    case "Death rate for pneumonia patients":
      myMortality = "Pneumonia";
      break;
    default:
      console.log("Unkown Mortality");
  }
  return myMortality;
}

//
// Given the data passed find the unique elements by the object key and also sort
// the resultant array by the object key specified in acsending order
//
function getSortedElementsByKey(targetData, key) {
  var returnArray = [
    ...new Map(targetData.map((item) => [item[key], item])).values(),
  ];
  return returnArray.sort((a, b) => (a[key] > b[key] ? 1 : -1));
}

function updateStateChart(state) {
  // Default to the full state name
  var valueText = d3.select("#stateSelect option:checked").text();

  // If all states chane the title text
  if (state === "all") {
    valueText = "All States";
  }

  d3.json(mortalitiesUrl + state).then((mortalities) => {
    console.log(mortalities);

    var barTrace = {
      type: "bar",
      x: mortalities.map((d) => mortalityMap(d.measure)),
      y: mortalities.map((d) => d.score),
    };

    var barData = [barTrace];

    var barLayout = {
      title: valueText + " Average Mortality Rates (%)",
      yaxis: { title: "Average (%)" },
      xaxis: {
        automargin: true,
      },
    };

    Plotly.newPlot("chart1", barData, barLayout);
  });
}

function updateHistogram() {
  var x1 = [];
  var x2 = [];
  for (var i = 1; i < 500; i++) {
    k = Math.random();
    x1.push(Math.random() + 1);
    x2.push(Math.random() + 1.1);
  }

  var x1mean = d3.mean(x1);
  var x2mean = d3.mean(x2);

  var trace1 = {
    x: x1,
    type: "histogram",
    opacity: 0.5,
    marker: {
      color: "green",
    },
  };
  var trace2 = {
    x: x2,
    type: "histogram",
    opacity: 0.6,
    marker: {
      color: "red",
    },
  };

  var data = [trace1, trace2];

  var layout = {
    barmode: "overlay",
    shapes: [
      {
        type: "line",
        x0: x1mean,
        y0: 0,
        x1: x1mean,
        y1: 40,
        line: {
          color: "green",
          width: 3.5,
          dash: "dot",
        },
      },
      {
        type: "line",
        x0: x2mean,
        y0: 0,
        x1: x2mean,
        y1: 40,
        line: {
          color: "red",
          width: 3.5,
          dash: "dot",
        },
      },
    ],
  };
  Plotly.newPlot("chart2", data, layout);
}
//
// Detect when a new state is selected
//
function stateChange() {
  updateStateChart(this.value);
}

//
// Populate the select dropdown by name id and data values passing the object
// keys for option and value, if needed pass the function you wanted called
// on a change event
//
function populateDropdown(
  elementName,
  values,
  optionKey,
  valueKey,
  onChangeFunc = null
) {
  // select the dropdown
  var dropDown = d3.select(`#${elementName}`);

  // populate the options for the select list
  var options = dropDown
    .selectAll(null)
    .data(values)
    .enter()
    .append("option")
    .text((d) => d[optionKey])
    .attr("value", (d) => d[valueKey]);

  if (onChangeFunc != null) {
    dropDown.on("change", onChangeFunc);
  }
}

function populateData() {
  // load the data into the data variable
  d3.json(mortalityUrl).then((data) => {
    console.log("records read:" + data.length);
    console.log(data);
    // populate the state drop down
    d3.json(statesURL).then((states) => {
      console.log("states:");
      console.log(states);
      populateDropdown(
        "stateSelect",
        states,
        "state_name",
        "state",
        stateChange
      );
    });
  });
}

populateData();

updateStateChart("all");

updateHistogram();
