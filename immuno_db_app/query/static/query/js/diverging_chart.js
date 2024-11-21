// Adapted from: https://github.com/wpoely86/D3.js-Diverging-Stacked-Bar-Chart
// Author: wpoely86 (https://github.com/wpoely86)
// Originally published under the Apache License Version 2.0

var margin = {top: 50, right: 20, bottom: 10, left: 205},
  width = 900 - margin.left - margin.right,
  height = 1000 - margin.top - margin.bottom;

var y = d3.scaleBand()
  .rangeRound([0, height])
  .padding(0.3);

var x = d3.scaleLinear()
  .rangeRound([0, width]);

var color = d3.scaleOrdinal()
  .range(["#D5665D", "#F19B5D", "#cccccc", "#92c6db", "#086fad"]);

var xAxis = d3.axisTop(x)
  .tickFormat(function(d) { return Math.abs(d); }); // Display absolute values

var yAxis = d3.axisLeft(y);

var svg = d3
  .select("#figure_diverging_chart")
  .append("div") // Change from svg to div
  .style("overflow-x", "auto") // Add style to make it scrollable
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .attr("id", "d3-plot")
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

color.domain(["HLA I", "HLA II"]);// benign", "HLA I malignant", "HLA II malignant", "HLA II benign"]);

d3.csv("/static/query/data/malignant_diseases_counts_div_default.csv", function(error, data) {

  data.forEach(function(d) {
  // calc percentages
  d["HLA I"] = +d["HLA I"];
  d["HLA II"] = +d["HLA II"];

  var x0 = -1*(d["HLA I"]);
  var idx = 0;
  d.boxes = color.domain().map(function(name) { return {name: name, x0: x0, x1: x0 += +d[name], n: d[name], link: d[name + " link"], disease: d['Disease']}; });
  });

  var maxAbsVal = d3.max(data, function(d) {
      return d3.max(d.boxes, function(box) {
          return Math.abs(box.x0);
      });
  });

  // Set the domain of x to be symmetric around zero
  x.domain([-maxAbsVal, maxAbsVal]).nice();
  y.domain(data.map(function(d) { return d.Disease; }));

  svg.append("g")
    .attr("class", "x axis")
    .call(xAxis);

  svg.append("g")
    .attr("class", "y axis")
    .call(yAxis);

  var my_boxes = svg.selectAll(".disease")
    .data(data)
  .enter().append("g")
    .attr("class", "bar")
    .attr("transform", function(d) { return "translate(0," + y(d.Disease) + ")"; });

  var bars = my_boxes.selectAll(".subbar")
    .data(function(d) { return d.boxes; })
  .enter().append("g").attr("class", "subbar");

  bars.append("rect")
  .attr("height", y.bandwidth())
  .attr("x", function(d) { return x(d.x0); })
  .attr("width", function(d) { return x(d.x1) - x(d.x0); })
  .style("fill", function(d) { return color(d.name); })
  .on("click", function(d) {
    console.log(d)
    // Extract the link corresponding to the clicked bar
    var linkIndex = color.domain().indexOf(d.name);
    var link = data[0][d.link]; // Assuming the links are in the first row

    // Navigate to the page
    window.location.href = d.link;
  })
  .on("mouseover", function(d) {
    // Show count and disease on hover
    var tooltipText = "Disease: " + d.disease + " <br>  Peptides: " + d.n + " <br>  MHC class: " + d.name;
    console.log(d)
    // Calculate tooltip position based on cursor position
    var tooltipX = d3.event.pageX + 10;
    var tooltipY = d3.event.pageY + 10; // Adjusted to be below the cursor
  
    d3.select("#tooltip")
      .html(tooltipText)
      .style("display", "block")
      .style("left", tooltipX + "px")
      .style("top", tooltipY + "px")
      .style("pointer-events", "none"); // Make the tooltip "transparent" to mouse events
  
    // Highlight the bar on hover
    d3.select(this).style("fill", "orange");
  })
  .on("mouseout", function() {
    // Hide count on mouseout
    d3.select("#tooltip").style("display", "none");
  
    // Revert the bar color on mouseout
    d3.select(this).style("fill", function(d) { return color(d.name); });
  });

    my_boxes.insert("rect",":first-child")
    .attr("height", y.bandwidth())
    .attr("x", "1")
    .attr("width", width)
    .attr("fill-opacity", "0.5")
    .style("fill", "#F5F5F5")
    .attr("class", function(d,index) { return index%2==0 ? "even" : "uneven"; });

  svg.append("g")
    .attr("class", "y axis")
  .append("line")
    .attr("x1", x(0))
    .attr("x2", x(0))
    .attr("y2", height);

  var startp = svg.append("g").attr("class", "legendbox").attr("id", "mylegendbox");
  // this is not nice, we should calculate the bounding box and use that
  var legend_tabs = [0, 140, 280, 420];
  
  
  var legendSelection = {};
  
  var legend = startp.selectAll(".legend")
  .data(color.domain().slice())
  .enter().append("g")
  .attr("class", "legend")
  .attr("transform", function(d, i) {
    return "translate(" + legend_tabs[i] + ",-45)";
  });

legend.append("rect")
  .attr("x", 0)
  .attr("width", 18)
  .attr("height", 18)
  .style("fill", color);

legend.append("text")
  .attr("x", 22)
  .attr("y", 9)
  .attr("dy", ".35em")
  .style("text-anchor", "begin")
  .style("font", "10px sans-serif")
  .text(function(d) { return d; });

var zeroPosition = x(0);

// Append x-axis label
svg.append("text")
  .attr("class", "x label")
  .attr("text-anchor", "middle")
  .attr("x", zeroPosition)
  .attr("y", -margin.top / 2)
  .text("Peptide count");

});