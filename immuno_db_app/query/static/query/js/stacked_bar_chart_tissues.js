// Adapted from: https://github.com/holtzy/D3-graph-gallery/
// Author: Holtz Yan (https://github.com/holtzy)
// Originally published under the MIT license

// Set the dimensions and margins of the graph
var margin_var = {top: 10, right: 5, bottom: 140, left: 80},
    width_var = 1000 - margin_var.left - margin_var.right,
    height_var = 700 - margin_var.top - margin_var.bottom;

// Append the svg object to the body of the page
var svg_var = d3.select("#my_dataviz")
  .append("div")
    .style("overflow-x", "auto")  // Enable horizontal scrolling
    .append("svg")
    .attr("width", width_var + margin_var.left + margin_var.right)
    .attr("height", height_var + margin_var.top + margin_var.bottom)
  .append("g")
    .attr("transform", "translate(" + margin_var.left + "," + margin_var.top + ")");

async function loadCSV(path) {
    const response = await fetch(path);
    const csvData = await response.text();
    return csvToObject(csvData);
}

function csvToObject(csv) {
    var lines = csv.split("\n");
    var result = {};
    lines.forEach(function(line) {
        var parts = line.split(",");
        if (parts.length === 2) {
            result[parts[0]] = parts[1];
        }
    });
    return result;
}

// Parse the Data
d3.csv("/static/query/data/tissue_db_webapp_in_default_30-10-24.csv", function(data_var) {

    loadCSV("/static/query/data/tissue_db_webapp_in_links_default_30-10-24.csv").then(dataObject => {


  // List of subgroups = header of the csv files = soil condition here
  var subgroups_var = data_var.columns.slice(1)

  // List of groups = species here = value of the first column called group -> I show them on the X axis
  var groups_var = d3.map(data_var, function(d){return(d.group)}).keys()

  // Add X axis
  var x_var = d3.scaleBand()
      .domain(groups_var)
      .range([0, width_var])
      .padding([0.2])
svg_var.append("g")
    .attr("transform", "translate(0," + height_var + ")")
    .call(d3.axisBottom(x_var).tickSizeOuter(0))
    .selectAll("text")  // select all the text elements for the x-axis
    .style("text-anchor", "end")
    .attr("dx", "-.8em")
    .attr("dy", ".15em")
    .attr("transform", "rotate(-45)"); // rotate the text

  // Calculate the maximum stack value
    var maxStackValue_var = d3.max(data_var, function(d) {
      var sum = 0;
      for (var i = 0; i < subgroups_var.length; i++) {
        sum += +d[subgroups_var[i]];
      }
      return sum;
    });

  // Add Y axis
  var y_var = d3.scaleLinear()
    .domain([0, maxStackValue_var])
    .range([ height_var, 0 ]);
  svg_var.append("g")
    .call(d3.axisLeft(y_var));

// Color palette = one color per subgroup
var color_var = d3.scaleOrdinal()
    .domain(subgroups_var)
    .range(["#D5665D", "#F19B5D", "#777777", "#BBBBBB"]);

  console.log(data_var)

  // Stack the data? --> stack per subgroup
  var stackedData_var = d3.stack()
    .keys(subgroups_var)
    (data_var)

  console.log(stackedData_var)

  // Highlight a specific subgroup when hovered
  var mouseover_var = function(d) {
    // What subgroup are we hovering?
    var subgroupName_var = d3.select(this.parentNode).datum().key; // This was the tricky part
    var subgroupValue_var = d.data[subgroupName_var];

    var tooltipText = subgroupName_var + "<br>" + d.data.group + "<br>" + subgroupValue_var;
    // Calculate tooltip position based on cursor position
    var tooltipX = d3.event.pageX + 10;
    var tooltipY = d3.event.pageY + 10;


    // Reduce opacity of all rects to 0.2
    d3.selectAll(".myRect").style("opacity", 0.2)
    // Highlight all rects of this subgroup with opacity 0.8. It is possible to select them since they have a specific class = their name.
    d3.selectAll("."+subgroupName_var)
      .style("opacity", 1.0);
    d3.select(this)
      .style("opacity", 1)
      .style("stroke", "black")
      .style("stroke-width", "2px");
    d3.select("#tooltip")
      .html(tooltipText)
      .style("display", "block")
      .style("left", tooltipX + "px")
      .style("top", tooltipY + "px")
      .style("pointer-events", "none");
    }



  // When user does not hover anymore
  var mouseleave_var = function(d) {
    // Back to normal opacity: 0.8
    d3.selectAll(".myRect")
      .style("opacity",1.0)
      d3.select(this)
      .style("stroke", "none")
      .style("stroke-width", "0px");
    d3.select("#tooltip").style("display", "none");
    }

  // Show the bars
  svg_var.append("g")
    .selectAll("g")
    // Enter in the stack data = loop key per key = group per group
    .data(stackedData_var)
    .enter().append("g")
      .attr("fill", function(d) { return color_var(d.key); })
      .attr("class", function(d){ return "myRect " + d.key }) // Add a class to each subgroup: their name
      .selectAll("rect")
      // Enter a second time = loop subgroup per subgroup to add all rectangles
      .data(function(d) { return d; })
      .enter().append("rect")
        .attr("x", function(d) { return x_var(d.data.group); })
        .attr("y", function(d) { return y_var(d[1]); })
        .attr("height", function(d) { return y_var(d[0]) - y_var(d[1]); })
        .attr("width",x_var.bandwidth())
        .style("opacity", 1)
        .on("mouseover", mouseover_var)
        .on("mouseleave", mouseleave_var)
        .on("click", function(d) {
            var subgroupName_var = d3.select(this.parentNode).datum().key;
            console.log(subgroupName_var)
            console.log()
            var url = d.data[subgroupName_var + "_url"]; // Construct the URL field name
            if(url) window.open(url, "_blank"); // Open the URL in a new tab
            console.log(dataObject[d.data.group + "_" + subgroupName_var])
            window.location.href = dataObject[d.data.group + "_" + subgroupName_var];
        });

var legend_tabs = [20, 160, 300, 440];

// Select the existing svg and add legend group
var legend = svg_var.selectAll(".legend")
  .data(subgroups_var)
  .enter().append("g")
    .attr("class", "legend")
    .attr("transform", function(d, i) { return "translate(" + (width_var - margin_var.right - 200) + "," + (i * 20) + ")"; });

// Add colored rectangles to the legend
legend.append("rect")
  .attr("x", 0)
  .attr("width", 18)
  .attr("height", 18)
  .style("fill", function(d) { return color_var(d); });

// Add text labels to the legend
legend.append("text")
  .attr("x", 22)
  .attr("y", 9)
  .attr("dy", ".35em")
  .style("text-anchor", "begin")
  .style("font", "10px sans-serif")
  .text(function(d) { return d; });

    })
})
