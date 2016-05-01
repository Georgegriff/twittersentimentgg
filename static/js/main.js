var twitterApp = (function () {
    var results = initResults(),
        total_pos = 0,
        total_neg = 0,
        POSITIVE = 1,
        NEGATIVE = 0,
        pieChart,
        self;

    function initResults() {
        return [{
            "label": "Negative",
            "value": 50
        }, {
            "label": "Positive",
            "value": 50
        }
        ];
    }


    function init() {
        self = this;
        initCountries();
        switchCountry(self.charting.getLocations().USA);
        $('#trending-drop').find('select').change(function (e) {
            var select = e.target,
                location = select.options[e.target.selectedIndex].value;
            switchCountry(location);
        });
        var drop = $('#algorithm-drop').find('select').get(0);
        getAccuracy(drop.options[drop.selectedIndex].value);
        $('#algorithm-drop').find('select').change(function (e) {
            var select = e.target,
                algorithm = select.options[e.target.selectedIndex].value;
            getAccuracy(algorithm);
        });
        self.charting.createPieChart('#pie-chart', results, function (chart) {
            pieChart = chart;
        });
        searchPressed();
        slideSide();
        drawColours(self.charting.getColors());
    }

    function drawColours(colors) {
        var $colours = $('#colors'),
            index = 0,
            text = '',
            $color = null;
        colors.forEach(function (color) {
            text = '';
            if (index === 0) {
                text = "Negative";
            } else if (index === colors.length - 1) {
                text = "Positive";
            }
            $color = $('<div class="color-block">' + text + '</div>');
            $color.css({"background": color});
            $colours.append($color);
            index++;
        });
    }

    function searchPressed() {
        $('.search').find('button').click(function () {
            self.charting.resetRegionData();
            searchQuery();

        })
    }

    function searchQuery() {
        $('.spin').show();
        var $search = $('.search'),
            val = $search.find('input').val();
        total_neg = 0;
        total_pos = 0;
        setPieResult(POSITIVE, 50);
        setPieResult(NEGATIVE, 50);
        if (val && val !== '') {
            streamResults(val)
            $('#search-title #s-val').text(val);
        }
    }


    function initCountries() {
        var options = $('#trending-drop').find('select').get(0).options,
            op, option;
        for (op in options) {
            if (options.hasOwnProperty(op)) {
                option = options[op];
                self.charting.setLocation(option.getAttribute("name"), option.getAttribute("value"));
            }
        }
    }

    function switchCountry(location) {
        showTrendingData(location);
        self.charting.switchMap(location);
    }

    function onDataReceived(data) {
        if (data) {
            total_pos += isNaN(data.positive) ? 0 : data.positive;
            total_neg += isNaN(data.negative) ? 0 : data.negative;
            setPieResult(NEGATIVE, total_neg);
            setPieResult(POSITIVE, total_pos);
            self.charting.addResultToRegion(data.positive, data.negative, data.location);
            updateInfo();

        }
    }

    function streamResults(query) {
        var codes = self.charting.getRegionCodes(),
            promises = [];
        codes.forEach(function (code) {
            promises.push(queryAPI(query, code, onDataReceived));
        });
        $.when.apply($, promises)
            .then(function () {
                $('.spin').hide();
            })

    }


    function queryAPI(query, code, onDataReceived) {
        var drop = $('#algorithm-drop').find('select').get(0),
            algorithm = drop.options[drop.selectedIndex].value,
            uri = '/' + algorithm + '?q=' + query + "&code=" + code;
        return getTweets(encodeURI(uri).replace(/#/g, "%23"), onDataReceived)
    }

    function showTrendingData(location) {
        var uri = location ? "/trending?loc=" + location : "/trending";
        return $.getJSON(uri)
            .then(function (data) {
                var trending = data && data.trending ? data.trending : [];
                $('#tags').empty();
                trending.forEach(function (hashtag) {
                    appendHashTag(hashtag);
                });
            })
    }


    function appendHashTag(hash) {
        var $trending = $('#tags'),
            $trend = $('<div class="trend"><a class="hash-link">' + hash + '</a></div>');
        $trending.append($trend);
        $trend.find('a').click(function (e) {
            $('.search').find('input').val($(e.target).text());
            self.charting.resetRegionData();
            searchQuery();

        });
    }

    function updateInfo() {
        var $resultInfo = $('#res-info');
        $resultInfo.find('.t-tweets span').html(total_neg + total_pos);
        $resultInfo.find('.p-tweets span').html(total_pos);
        $resultInfo.find('.n-tweets span').html(total_neg);
    }


    function getTweets(uri, onDataReceived) {
        return $.getJSON(uri).done(function (data) {
            if (data && data.data) {
                return onDataReceived(data.data);
            }

        });
    }

    function setPieResult(index, value) {
        results[index].value = value;
        pieChart.update();
    }


    function slideSide() {
        var $tags = $('#trending-tags');
        if ($('body').width() < 1300) {
            $tags.hide();
        }
        $(window).resize(function () {
            if ($('body').width() < 1300) {
                $tags.hide("slide", {direction: "right"}, 600);
                $('#data').css({"text-align": "center", "margin": "0 auto"});
            } else {
                $tags.show("slide", {direction: "right"}, 600);
                $('#data').css({"text-align": "left", "margin": "0"});
            }
        });
        $('#menu-btn').click(function () {
            if ($tags.is(":visible")) {
                $tags.toggle("slide", {direction: "right"}, 600);
            } else {
                $tags.toggle("slide", {direction: "right"}, 600);
            }
        });

    }

    function getAccuracy(algorithm) {
        $.getJSON('/accuracy?algorithm=' + algorithm)
            .then(function (data) {
                $('#config').find('.info .accuracy').html(data && data.accuracy ? Math.floor(data.accuracy * 100) / 100 : '');
            })
    }

    var api = {
        init: init,
        setPieResult: setPieResult
    };
    return api;


})
();