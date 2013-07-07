README
=======
This is a little Python 2.7 command-line program to make HTML income 
reports given a list of CSV files of income items.

The first (header) row of each given CSV file will be ignored.
Only the first three columns of each given CSV file will be processed
(extra columns will be ignored),
and these columns should contain the following elements 
(separated by commas) in the order listed.

1. The date the income was received (yyyy-mm-dd)
2. The amount of income received (without currency symbols such as '$')
3. The number of hours worked for that income

Assumes one currency type is used throughout the files, such as New Zealand
dollars.

Uses Pandas for data manipulation and a local copy of NVD3 
for Javascript charts.

AUTHORS
--------
- Alex Raichev (2013-05-26)

CHANGELOG
----------
- 2013-05-26: Initial version.
- 2013-07-06: Refactored using argparse module.
- 2013-07-08: Refactored to use local NVD3 installation.

TODO
-----
- Add doctest examples
- Doctest

.. raw:: html


    <head>
        <link href="income_reporter.css" rel="stylesheet">
        <link media="all" href="nvd3/src/nv.d3.css" type="text/css" rel="stylesheet" />
        <script src="nvd3/lib/d3.v2.js" type="text/javascript">
        </script>
        <script src="nvd3/nv.d3.js" type="text/javascript"></script>
    </head>
    <body>
        <h1>Income Report</h1>
        <h2>Year 2013</h2>

    <div id="chart0"><svg style="width:700px; height:400px;"></svg></div>
    
    <script type="text/javascript">
        nv.addGraph(function() {
            var chart = nv.models.discreteBarChart()
                .margin({top: 10, right: 10, bottom: 70, left: 70});
            chart.color(d3.scale.category10().range());
            chart.xAxis
                .rotateLabels(-45);
            chart.yAxis
                .axisLabel('NZD ')
                .tickFormat(d3.format('.00f'));
            chart.tooltipContent(function(key, y, e, graph) {
                var x = String(graph.point.x);
                var y = String(graph.point.y);
                if(key == 'Series 1'){
                    var y =  String(graph.point.y)  + ' NZD ';
                }
    
                tooltip_str = 'y = ' + y + '<br>x = ' + x;
                return tooltip_str;
            });
            d3.select('#chart0 svg')
                .datum(data0)
                .transition().duration(500)
                .attr('width', 700)
                .attr('height', 400)
                .call(chart);

        return chart;
    });
    
        data0=[{"values": [{"y": 2182.0, "x": "2013-01-31"}, {"y": 3895.0, "x": "2013-02-28"}, {"y": 2157.0, "x": "2013-03-31"}, {"y": 4517.0, "x": "2013-04-30"}, {"y": 4294.0, "x": "2013-05-31"}, {"y": 2868.0, "x": "2013-06-30"}], "key": "Series 1", "yAxis": "1"}];
    </script>
            <pre>
        Total income = NZD 19913.0
        Start date = 2013-01-01
        End date = 2013-06-30
        Total hours = 292
        Hours per week = 11.4
        Income per month = NZD 3363.08
        Income per week = NZD 774.39
        Income per hour = NZD 68.2
        </pre>
    <h2>Last 12 Months</h2>

    <div id="chart1"><svg style="width:700px; height:400px;"></svg></div>
    
    <script type="text/javascript">
        nv.addGraph(function() {
            var chart = nv.models.discreteBarChart()
                .margin({top: 10, right: 10, bottom: 70, left: 70});
            chart.color(d3.scale.category10().range());
            chart.xAxis
                .rotateLabels(-45);
            chart.yAxis
                .axisLabel('NZD ')
                .tickFormat(d3.format('.00f'));
            chart.tooltipContent(function(key, y, e, graph) {
                var x = String(graph.point.x);
                var y = String(graph.point.y);
                if(key == 'Series 1'){
                    var y =  String(graph.point.y)  + ' NZD ';
                }
    
                tooltip_str = 'y = ' + y + '<br>x = ' + x;
                return tooltip_str;
            });
            d3.select('#chart1 svg')
                .datum(data1)
                .transition().duration(500)
                .attr('width', 700)
                .attr('height', 400)
                .call(chart);

        return chart;
    });
    
        data1=[{"values": [{"y": 4034.0, "x": "2012-08-31"}, {"y": 4613.0, "x": "2012-09-30"}, {"y": 4536.0, "x": "2012-10-31"}, {"y": 3818.0, "x": "2012-11-30"}, {"y": 3230.0, "x": "2012-12-31"}, {"y": 2182.0, "x": "2013-01-31"}, {"y": 3895.0, "x": "2013-02-28"}, {"y": 2157.0, "x": "2013-03-31"}, {"y": 4517.0, "x": "2013-04-30"}, {"y": 4294.0, "x": "2013-05-31"}, {"y": 2868.0, "x": "2013-06-30"}], "key": "Series 1", "yAxis": "1"}];
    </script>
            <pre>
        Total income = NZD 40144.0
        Start date = 2012-08-01
        End date = 2013-06-30
        Total hours = 583
        Hours per week = 12.3
        Income per month = NZD 3664.8
        Income per week = NZD 843.87
        Income per hour = NZD 68.86
        </pre>
    <h2>Tax Year 2013</h2>

    <div id="chart2"><svg style="width:700px; height:400px;"></svg></div>
    
    <script type="text/javascript">
        nv.addGraph(function() {
            var chart = nv.models.discreteBarChart()
                .margin({top: 10, right: 10, bottom: 70, left: 70});
            chart.color(d3.scale.category10().range());
            chart.xAxis
                .rotateLabels(-45);
            chart.yAxis
                .axisLabel('NZD ')
                .tickFormat(d3.format('.00f'));
            chart.tooltipContent(function(key, y, e, graph) {
                var x = String(graph.point.x);
                var y = String(graph.point.y);
                if(key == 'Series 1'){
                    var y =  String(graph.point.y)  + ' NZD ';
                }
    
                tooltip_str = 'y = ' + y + '<br>x = ' + x;
                return tooltip_str;
            });
            d3.select('#chart2 svg')
                .datum(data2)
                .transition().duration(500)
                .attr('width', 700)
                .attr('height', 400)
                .call(chart);

        return chart;
    });
    
        data2=[{"values": [{"y": 4517.0, "x": "2013-04-30"}, {"y": 4294.0, "x": "2013-05-31"}, {"y": 2868.0, "x": "2013-06-30"}, {"y": 2959.0, "x": "2013-07-31"}, {"y": 3132.0, "x": "2013-08-31"}, {"y": 3034.0, "x": "2013-09-30"}, {"y": 2518.0, "x": "2013-10-31"}, {"y": 1824.0, "x": "2013-11-30"}], "key": "Series 1", "yAxis": "1"}];
    </script>
            <pre>
        Total income = NZD 25146.0
        Start date = 2013-04-01
        End date = 2013-11-30
        Total hours = 381
        Hours per week = 11.0
        Income per month = NZD 3145.84
        Income per week = NZD 724.37
        Income per hour = NZD 66.0
        </pre>
    <h2>All Data</h2>

    <div id="chart3"><svg style="width:700px; height:400px;"></svg></div>
    
    <script type="text/javascript">
        nv.addGraph(function() {
            var chart = nv.models.discreteBarChart()
                .margin({top: 10, right: 10, bottom: 70, left: 70});
            chart.color(d3.scale.category10().range());
            chart.xAxis
                .rotateLabels(-45);
            chart.yAxis
                .axisLabel('NZD ')
                .tickFormat(d3.format('.00f'));
            chart.tooltipContent(function(key, y, e, graph) {
                var x = String(graph.point.x);
                var y = String(graph.point.y);
                if(key == 'Series 1'){
                    var y =  String(graph.point.y)  + ' NZD ';
                }
    
                tooltip_str = 'y = ' + y + '<br>x = ' + x;
                return tooltip_str;
            });
            d3.select('#chart3 svg')
                .datum(data3)
                .transition().duration(500)
                .attr('width', 700)
                .attr('height', 400)
                .call(chart);

        return chart;
    });
    
        data3=[{"values": [{"y": 4469.0, "x": "2012-01-31"}, {"y": 4145.0, "x": "2012-02-29"}, {"y": 4395.0, "x": "2012-03-31"}, {"y": 5739.0, "x": "2012-04-30"}, {"y": 2168.0, "x": "2012-05-31"}, {"y": 2654.0, "x": "2012-06-30"}, {"y": 2974.0, "x": "2012-07-31"}, {"y": 4034.0, "x": "2012-08-31"}, {"y": 4613.0, "x": "2012-09-30"}, {"y": 4536.0, "x": "2012-10-31"}, {"y": 3818.0, "x": "2012-11-30"}, {"y": 3230.0, "x": "2012-12-31"}, {"y": 2182.0, "x": "2013-01-31"}, {"y": 3895.0, "x": "2013-02-28"}, {"y": 2157.0, "x": "2013-03-31"}, {"y": 4517.0, "x": "2013-04-30"}, {"y": 4294.0, "x": "2013-05-31"}, {"y": 2868.0, "x": "2013-06-30"}, {"y": 2959.0, "x": "2013-07-31"}, {"y": 3132.0, "x": "2013-08-31"}, {"y": 3034.0, "x": "2013-09-30"}, {"y": 2518.0, "x": "2013-10-31"}, {"y": 1824.0, "x": "2013-11-30"}], "key": "Series 1", "yAxis": "1"}];
    </script>
            <pre>
        Total income = NZD 80155.0
        Start date = 2012-01-01
        End date = 2013-11-30
        Total hours = 1182
        Hours per week = 11.8
        Income per month = NZD 3486.0
        Income per week = NZD 802.7
        Income per hour = NZD 67.81
        </pre>

    </body>
    </html>