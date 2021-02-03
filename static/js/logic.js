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
