plotter = {};
plotter.filters = [];
plotter.data = [];
plotter.date = [];
plotter.names = [];

function loadPinch(names, data, date){
    plotter.data = data;
    plotter.date = date;
    plotter.names = names;
    y = makeY(names);
    ser = makeSeries(names, data, date);
    console.log(y);
    console.log(ser);
    $('#charts').highcharts({
        chart: {
            zoomType: 'x',
            spacingRight: 20
        },
        title: {text: 'Data'},
        subtitle: {
            text: document.ontouchstart === undefined ?
                'Click and drag in the plot area to zoom in' :
                'Pinch the chart to zoom in'
        },
        xAxis: {
            type: 'datetime',
            maxZoom: 10 * 24 * 3600000,
            title: 'Time'
        },
        yAxis: y,
        tooltip: {shared: true},
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 70,
            verticalAlign: 'top',
            y: 10,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: ser 
    });
};

function makeY(names){
    var y = [];
    for(var i = 0; i < names.length; i++){
        y.push({ title: {
                            text: names[i],
                            style: {
                                color: Highcharts.getOptions().colors[i]
                            }
                        }});
    }
    return y;
}

function makeSeries(names, data, date){
    var ser = [];
    var plot = names.length > 1 ? 'line' : 'area';
    for(var i = 0; i < names.length; i++){
        ser.push({
                type: plot,
                name: names[i],
                yAxis: i,
                data: data[i],
                pointInterval: 48 * 7200 * 100000,
                pointStart: Date.UTC(date[0], date[1], date[2])
            });
    }
    return ser;
}

function addFilter(name){
    plotter.filters.push(name);
    renderFilters(name);
}

function renderFilters(name){
    $('filters').appendTo('<option>' + name + '</option>');
    alert($('filters').children().text());
}
