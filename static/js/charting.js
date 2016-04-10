twitterApp.charting = (function () {
    var regionCodes = [],
        regionData = {},
        map;

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

    function calcColor(percentage) {
        var colourPalette = ['#e51e00', '#e54c00', '#e57b00', '#e5a900',
                '#e5d700', '#c4e500', '#96e500', '#67e500', '#39e500', '#0ae600'],
            totalColors = colourPalette.length,
            color = Math.floor(totalColors * percentage) - 1;
        return colourPalette[color] ||  "#AEC7E8";

    }

    function recalculateColors() {
        var colors = {},
            key, data;

        for (key in map.regions) {
            data = regionData[key];
            var percentage = data.pos / data.tot;
            colors[key] = calcColor(percentage)
        }
        return colors;
    }

    function createWorldMap() {
        var key;
        map = new jvm.Map({
            map: 'us_aea',
            container: $('#worldmap'),
            hoverOpacity: 0.7,
            series: {
                regions: [{
                    attribute: 'fill'
                }]
            },
            regionStyle: {
                initial: {
                    fill: '#AEC7E8'
                }
            }
        });
        for (key in map.regions) {
            regionData[key] = {"pos": 0, "neg": 0, "tot": 0};
            regionCodes.push(key);
        }
    }

    function addResultToRegion(result, location) {
        var region = regionData[location];
        if (region) {
            if (result === 1) {
                region.pos += 1;
            } else {
                region.neg += 1;
            }
            region.tot++;

        }
        map.series.regions[0].setValues(recalculateColors());
    }

    var api = {
        createPieChart: createPieChart,
        createWorldMap: createWorldMap,
        getRegionCodes: function () {
            return regionCodes;
        },
        addResultToRegion: addResultToRegion

    }
    return api;
})();