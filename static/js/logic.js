// local url for mortality rates
var mortalityUrl = "/mortality";
var statesURL = "/states";
var mortalitiesUrl = "/mortalities/";

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
// Detect when a new state is selected
//
function stateChange() {
  var valueSelected = this.value;
  console.log("changed state: " + valueSelected);

  d3.json(mortalitiesUrl + valueSelected).then((mortalities) => {
    console.log(mortalities);
  });
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
