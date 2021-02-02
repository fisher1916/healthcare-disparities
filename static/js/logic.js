// local url for mortality rates
var url = "/mortality";

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
    .selectAll("option")
    .data(values)
    .enter()
    .append("option")
    .text((d) => d[optionKey])
    .attr("value", (d) => d[valueKey]);

  if (onChangeFunc != null) {
    dropDown.on("change", onChangeFunc);
  }
}

// load the data into the data variable
d3.json(url).then((data) => {
  console.log("records read:" + data.length);
  console.log(data);

  // grab unique sorted values
  const uniqueStates = getSortedElementsByKey(data, "state_name");
  const uniqueMeasures = getSortedElementsByKey(data, "measure");

  // populate the state drop down
  populateDropdown(
    "stateSelect",
    uniqueStates,
    "state_name",
    "state",
    stateChange
  );
});
