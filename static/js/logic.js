// local url for mortality rates
var statesURL = "/states";
var mortalitiesUrl = "/mortalities/";
var racemortalitiesURL = "/racemortalities/";
var measuresURL = "/measures";
var urbanruralmortalitiesURL = "/urbanruralmortalities/";

//
// Map out the mortality abbreviations
//

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

//
// Update the state score bar chart
//

function updateStateChart(state) {
  // Default to the full state name
  var valueText = d3.select("#stateSelect option:checked").text();

  // If all states chane the title text
  if (state === "all") {
    valueText = "All States";
  }

  d3.json(mortalitiesUrl + state).then((data) => {
    var barTrace = {
      type: "bar",
      x: data.measures.map((d) => mortalityMap(d.measure)),
      y: data.measures.map((d) => d.score),
    };

    var barData = [barTrace];

    var barLayout = {
      title: valueText + " Average Mortality Rates (%)",
      yaxis: { title: "Average (%)" },
      xaxis: {
        automargin: true,
      },
    };

    Plotly.newPlot("bar1", barData, barLayout);

    var bar2Trace = {
      type: "bar",
      orientation: "h",
      x: data.demo.map((d) => d.percent),
      y: data.demo.map((d) => d.name),
    };

    var bar2Data = [bar2Trace];

    var bar2Layout = {
      title: valueText + " Demographic (%)",
      xaxis: {
        title: "Average (%)",
        automargin: true,
      },
    };

    Plotly.newPlot("bar2", bar2Data, bar2Layout);
  });
}

//
// Plot Urban vs Rural histogram
//
function updateHistogram(measure) {
  d3.json(racemortalitiesURL + measure).then((mortalities) => {
    // console.log("racemortalities");
    // console.log(mortalities);

    var x1 = mortalities["white_scores"];
    var x2 = mortalities["black_scores"];

    var x1mean = d3.mean(x1);
    var x2mean = d3.mean(x2);

    var trace1 = {
      name: "White Scores",
      x: x1,
      type: "histogram",
      opacity: 0.5,
      marker: {
        color: "green",
      },
    };
    var trace2 = {
      name: "Black Scores",
      x: x2,
      type: "histogram",
      opacity: 0.6,
      marker: {
        color: "purple",
      },
    };

    var data = [trace1, trace2];

    var layout = {
      title: mortalities["measure"],
      barmode: "overlay",
      shapes: [
        {
          type: "line",
          x0: x1mean,
          y0: 0,
          x1: x1mean,
          y1: 140,
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
          y1: 140,
          line: {
            color: "purple",
            width: 3.5,
            dash: "dot",
          },
        },
      ],
    };
    Plotly.newPlot("chart2", data, layout);
  });
}

//
// Plot Urban vs Rural histogram
//
function updateHistogram2(measure) {
  d3.json(urbanruralmortalitiesURL + measure).then((mortalities) => {
    // console.log("racemortalities");
    // console.log(mortalities);

    var x1 = mortalities["urban_scores"];
    var x2 = mortalities["rural_scores"];

    var x1mean = d3.mean(x1);
    var x2mean = d3.mean(x2);

    var trace1 = {
      name: "Urban Scores",
      x: x1,
      type: "histogram",
      opacity: 0.5,
      marker: {
        color: "yellow",
      },
    };
    var trace2 = {
      name: "Rural Scores",
      x: x2,
      type: "histogram",
      opacity: 0.6,
      marker: {
        color: "brown",
      },
    };

    var data = [trace1, trace2];

    var layout = {
      title: mortalities["measure"],
      barmode: "overlay",
      shapes: [
        {
          type: "line",
          x0: x1mean,
          y0: 0,
          x1: x1mean,
          y1: 140,
          line: {
            color: "yellow",
            width: 3.5,
            dash: "dot",
          },
        },
        {
          type: "line",
          x0: x2mean,
          y0: 0,
          x1: x2mean,
          y1: 140,
          line: {
            color: "brown",
            width: 3.5,
            dash: "dot",
          },
        },
      ],
    };
    Plotly.newPlot("urbanChart", data, layout);
  });
}

//
// Detect when a new state is selected
//
function stateChange() {
  updateStateChart(this.value);
}

//
// Detect when a new measure is selected
//
function measureChange() {
  updateHistogram(this.value);
  updateHistogram2(this.value);
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
  d3.json(statesURL).then((states) => {
    // console.log("states:");
    // console.log(states);
    populateDropdown("stateSelect", states, "state_name", "state", stateChange);
  });
  d3.json(measuresURL).then((measures) => {
    // console.log("measures:");
    // console.log(measures);

    // Create the measure selectors
    var form = d3.selectAll("form");

    labels = form
      .selectAll(null)
      .data(measures)
      .enter()
      .append("label")
      .attr("class", "radioadjust")
      .append("input")
      .attr("type", "radio")
      .attr("class", "shape")
      .attr("name", "mode")
      .attr("value", function (d) {
        return d.measure;
      })
      .property("checked", function (d) {
        return d.measure === "Death rate for COPD patients";
      })
      .on("change", measureChange);

    d3.select("form")
      .selectAll("label")
      .append("text")
      .attr("class", "radioadjust")
      .text(function (d) {
        return d.measure;
      });
  });
}

populateData();

updateStateChart("all");

updateHistogram("Death rate for COPD patients");

updateHistogram2("Death rate for COPD patients");
