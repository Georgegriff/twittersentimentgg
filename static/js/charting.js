twitterApp.charting = (function () {
    var regionCodes = [],
        regionData = {},
        locations = {},
        map,
        colourPalette = ['#e51e00', '#e54c00', '#e57b00', '#e5a900',
            '#e5d700', '#c4e500', '#96e500', '#67e500', '#0ae600'];

    function createPieChart(elementSelector, results, listener) {
        var chart;
        nv.addGraph(function () {
            var myColors = [colourPalette[0], colourPalette[colourPalette.length -1]];
            d3.scale.myColors = function () {
                return d3.scale.ordinal().range(myColors);
            };
            var width = 600,
                height = 400;
            chart = nv.models.pieChart()
                .x(function (d) {
                    return d.label
                })
                .y(function (d) {
                    return d.value
                })
                .showLabels(true).color(d3.scale.myColors().range())
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

        var totalColors = colourPalette.length,
            color = Math.floor(totalColors * percentage) - 1;
        if (color < 0) {
            color = 0;
        }
        return colourPalette[color] || "#1da1f2";

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

    function createMap(mapName) {
        var key;
        map = new jvm.Map({
            map: mapName,
            container: $('#map'),
            hoverOpacity: 0.7,
            series: {
                regions: [{
                    attribute: 'fill'
                }]
            },
            regionStyle: {
                initial: {
                    fill: '#1da1f2'
                }
            },
            onRegionTipShow: function (e, el, code) {
                if (regionData && regionData[code]) {
                    el.html(el.html() + (', Total:' + regionData[code].tot || ''));
                }
            }
        });
        for (key in map.regions) {
            regionData[key] = {"pos": 0, "neg": 0, "tot": 0};
            regionCodes.push(key);
        }
    }

    function addResultToRegion(pos, neg, location) {
        var region = regionData[location];
        if (region) {
            region.pos += pos;
            region.neg += neg;
            region.tot = region.pos + region.neg;

        }
        map.series.regions[0].setValues(recalculateColors());
    }

    function switchMap(location) {
        $('#map').empty();
        regionCodes = [];
        regionData = {};
        switch (location) {

            case locations.USA:
                createMap('us_aea');
                break;
            case locations.UK:
                createMap('uk_countries_mill');
                break;

            default:
                break;
        }
    }

    var api = {
        createPieChart: createPieChart,
        createMap: createMap,
        getRegionCodes: function () {
            return regionCodes;
        },
        resetRegionData: function resetRegionData() {
            for (var key in map.regions) {
                regionData[key] = {"pos": 0, "neg": 0, "tot": 0};
            }
        },
        addResultToRegion: addResultToRegion,
        switchMap: switchMap,
        setLocation: function (name, value) {
            locations[name] = value;
        },
        getLocations: function () {
            return locations;
        },
        getColors: function () {
            return colourPalette;
        }

    }
    return api;
})();