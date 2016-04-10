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


    function init(options) {
        self = this;
        showTrendingData();
        self.charting.createPieChart('#pie-chart', results, function (chart) {
            pieChart = chart;
        });
        searchPressed();
        self.charting.createWorldMap();
    }


    function searchPressed() {
        $('.search').find('button').click(function () {
            self.charting.resetRegionData();
            searchQuery();

        })
    }

    function searchQuery() {
        var $search = $('.search'),
            val = $search.find('input').val();
        total_neg = 0;
        total_pos = 0;
        setPieResult(POSITIVE, 50);
        setPieResult(NEGATIVE, 50);
        if (val && val !== '') {
            streamResults(val)
            $('#search-title').append(val);
        }
    }


    function onDataReceived(datas) {
        if (datas) {
            console.log(datas);
            datas.forEach(function (value) {
                var data = value.data,
                    result = data.result;
                if (result === 1) {
                    total_pos++;
                    setPieResult(POSITIVE, total_pos);
                } else {
                    total_neg++;
                    setPieResult(NEGATIVE, total_neg);
                }
                self.charting.addResultToRegion(data.result, data.location);


            });

        }
    }

    function streamResults(query) {
        var codes = self.charting.getRegionCodes();
        codes.forEach(function (code) {
            queryAPI(query, code, onDataReceived);
        })

    }


    function queryAPI(query, code, onDataReceived) {
        var uri = '/linearsvc?q=' + query + "&code=" + code;
        return ajax_stream(uri, onDataReceived)
    }

    function showTrendingData() {
        return $.getJSON('/trending')
            .then(function (data) {
                var trending = data && data.trending ? data.trending : [];
                trending.forEach(function (hashtag) {
                    appendHashTag(hashtag);
                });

            })
    }


    function appendHashTag(hash) {
        var $trending = $('#trending-tags');
        $trending.append('<div class="trend">' + hash + '</div>');
    }


    function ajax_stream(uri, onDataReceived) {
        try {
            var xhr = new XMLHttpRequest();
            xhr.previous_text = '';

            xhr.onerror = function () {
                console.log("XHR Error");
            };
            xhr.onreadystatechange = function () {
                try {
                    if (xhr.readyState > 2) {
                        var response = xhr.responseText.substring(xhr.previous_text.length);
                        if (response.endsWith(",")) {
                            response = response.slice(0, -1);
                        }
                        if (response.startsWith(",")) {
                            response = response.slice(1);
                        }
                        var result = JSON.parse("[" + response + "]");
                        onDataReceived(result);
                        xhr.previous_text = xhr.responseText;
                    }
                }
                catch (e) {
                    console.log(e);
                }


            };
            xhr.open("GET", uri, true);
            xhr.send("Making request...");
        }
        catch (e) {
            log_message("<b>[XHR] Exception: " + e + "</b>");
        }
    }

    function setPieResult(index, value) {
        results[index].value = value
        pieChart.update();
    }

    var api = {
        init: init,
        setPieResult: setPieResult
    };
    return api;


})();