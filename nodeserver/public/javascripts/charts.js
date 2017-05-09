function makeBarGraph(data) {
  var height = 200, barWidth = 40;
  var x = d3.scaleLinear()
    .domain([0, d3.max(data)])
    .range([0, height]);

  var chart = d3.select("#chart")
    .attr("width", barWidth * data.length)
    .attr("height", height);

  var bar = chart.selectAll("g").data(data)
    .enter().append("g")
    .attr("transform", function(d, i) { return "translate("+i*barWidth+",0)"; });

  bar.append("rect")
    .attr("width", barWidth)
    .attr("height", x)
    .attr("transform", function(d, i) { return "translate(0,"+(height-x(d))+")"});

  bar.append("text")
    .attr("x", 0)
    .attr("y", function(d) {
      var offset = -5;
      if (x(d) > (height/2)) offset = 24;
      return height - x(d) + offset; 
    })
    .attr("dx", ".35em")
    .text(function(d) { return d; });

  return "Bar Graph";
}
