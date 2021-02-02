// local url for mortality rates
var url = "/mortality";

// load the data into the data variable
d3.json(url).then((data) => {
  console.log("records read:" + data.length);
  console.log(data);
});
