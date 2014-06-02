//And again, the global namespace is spared.
var d3Setup = {};
d3Setup.xScale = d3.scale.linear();
d3Setup.yScale = d3.scale.linear();
d3Setup.xAxis = d3.svg.axis();
d3Setup.yAxis = d3.svg.axis();
d3Setup.padding = 0;

//Sets up a scatter plot with d3
function setupVisuals(data, pad, mono){
    d3Setup.padding = pad;
    if(mono){
        h = d3.max(data, function(d){return d;});
        d3Setup.yScale.domain([pad, h - pad)]);
        d3Setup.yAxis.domain(d3Setup.yScale)
            .orient("bottom");
        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(0, " + h - pad + ")")
            .call(d3Setup.yAxis);
    } else{
        w = d3.max(data, function(d){return d[0];});
        h = d3.max(data, function(d){return d[1];});
        d3Setup.xScale.domain([pad, w - pad]);
        d3Setup.yScale.domain([pad, h - pad]);
        d3Setup.xAxis.domain(d3Setup.xScale)
            .orient("left");
        d3Setup.yAxis.domain(d3Setup.yScale)
            .orient("bottom");
        svg.append("g")
            .attr("class", "axis")
            .call(d3Setup.xAxis);
        svg.append("g")
            .attr("class", "axis")
            .call(d3Setup.yAxis);
    }
};
