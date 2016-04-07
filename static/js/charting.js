twitterApp.charting = (function () {

    function createPieChart(elementSelector, results, listener) {
        var chart;
        nv.addGraph(function () {
            var width = 600,
                height = 400;
            chart = nv.models.pieChart()
                .x(function (d) {
                    return d.label
                })
                .y(function (d) {
                    return d.value
                })
                .showLabels(true)     //Display pie labels
                .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
                .labelType("percent")
                .width(width)
                .height(height)
            d3.select(elementSelector)
                .datum(results)
                .transition().duration(350)
                .call(chart)
                .style({'width': width, 'height': height});
            nv.utils.windowResize(chart.update);

            listener(chart);

            return chart;
        });
    }

    var api = {
        createPieChart: createPieChart

    }
    return api;
})();