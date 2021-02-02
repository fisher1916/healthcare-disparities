// local url for mortality rates
var url = "/mortality";

function getSortedUniqueObjectValues(target_data, key) {
  const uniqueElements = [
    ...new Map(target_data.map((item) => [item[key], item])).values(),
  ];

  return uniqueElements.sort((a, b) => (a[key] > b[key] ? 1 : -1));
}
// load the data into the data variable
d3.json(url).then((data) => {
  console.log("records read:" + data.length);
  console.log(data);

  const uniqueMeasures = getSortedUniqueObjectValues(data, "measure");

  console.log(uniqueMeasures);

  const uniqueStates = getSortedUniqueObjectValues(data, "state_name");

  console.log(uniqueStates);
});
