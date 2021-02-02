// local url for mortality rates
var url = "/mortality";

function getSortedElementsByKey(targetData, key) {
  var returnArray = [
    ...new Map(targetData.map((item) => [item[key], item])).values(),
  ];
  return returnArray.sort((a, b) => (a[key] > b[key] ? 1 : -1));
}
// load the data into the data variable
d3.json(url).then((data) => {
  console.log("records read:" + data.length);
  console.log(data);

  const uniqueStates = getSortedElementsByKey(data, "state_name");
  const uniqueMeasures = getSortedElementsByKey(data, "measure");
  console.log(uniqueStates);
  console.log(uniqueMeasures);
});
