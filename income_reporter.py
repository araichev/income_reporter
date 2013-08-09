"""
This is a little Python 3.3 command-line program to make an HTML income 
report given a list of CSV files of income items.

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

Authors
--------
- Alex Raichev (2013-05-26)

CHANGELOG
----------
- 2013-05-26: Initial version.
- 2013-07-06: Refactored using the argparse module.
- 2013-07-08: Refactored to use a local NVD3 installation.
- 2013-08-10: Corrected Pandas frequency constant bug.

TODO
-----
- Add doctest examples
- Doctest

#*****************************************************************************
#       Copyright (C) 2013 Alex Raichev <alex@raichev.net>
#
#  Distributed under the terms of the GNU General Public License Version 3
#  (GPLv3) as published by the Free Software Foundation.
#                  http://www.gnu.org/licenses/
#*****************************************************************************
"""
# from __future__ import division, print_function
import pandas as pd
import datetime as dt

def parse_args():
    """
    Parse command line options and return an object with two attributes:
    `infiles`, a possibly empty list of input file paths, and `outfile`, 
    a list of one output file path.
    """
    import argparse
    import textwrap

    parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter, 
      description=textwrap.dedent('''\
        A littly command-line program to make an HTML income report given
        some CSV files of income items.
        
        The first (header) line/row of each given CSV file will be ignored.
        Only the first three columns of each given CSV file will be process_csv_fileed,
        and these columns should contain the following elements 
        (separated by commas) in the order listed.

        1. The date the income was received (yyyy-mm-dd)
        2. The amount of income received 
          (without currency symbols such as '$')
        3. The number of hours worked for that income

        Assumes one currency type is used throughout the files, 
        such as New Zealand dollars.
      '''))
    parser.add_argument('infiles', nargs='*', metavar='input_file',
      help='a CSV file of income items (default: randomly generated data)')
    parser.add_argument('-o', '--outfile', nargs=1, default=['income_reporter.html'], 
      metavar='output_file',
      help="path of HTML file output (default: 'income_reporter.html')")
    return parser.parse_args()

def make_data_frame(files, nweeks=100):
    """
    Given a list of CSV files of income items, convert each one into a 
    Pandas data frame object, combine the data frames into one data
    frame, remove duplicate lines, sort by date, and return the resulting
    data frame.    

    If `files` is empty, then return a data frame of `nweeks` weeks worth of
    random data.
    """
    import numpy as np

    if files:
        data = pd.concat([process_csv_file(f) for f in files])
        data = data.drop_duplicates().sort()
    else:
        # Generate test data
        dates = pd.date_range('20120101', periods=nweeks, freq='W')
        data = pd.DataFrame(index=dates, columns=['income', 'hours'])
        data['hours'] = np.random.randint(0, 25, nweeks)
        data['income'] = [h*np.random.randint(50, 100) for h in data['hours']]
    return data

def process_csv_file(csvfile):
    """
    Convert the given income CSV file into a Pandas data frame indexed by 
    date, and return that data frame.
    Ignore the first (header) line of the file and only process the first 
    three columns. 
    Assume those columns contain:
    
    1. The date the income was received (yyyy-mm-dd)
    2. The amount of income received (without currency symbols such as $)
    3. The number of hours worked for that income

    Will name these columns in the resulting data frame as 
    'date' (index column), 'income', and 'hours', respectively.
    """
    data = pd.read_csv(csvfile, header=0, usecols=[0, 1, 2], 
                       names=['date', 'income', 'hours'], index_col=0,
                       parse_dates=True)
    return data

def round_date(date, freq='M', past=True):
    """
    Suppose `freq == 'M'`.
    If `past == True`, then round the given date to the beginning 
    of its month.
    Otherwise, round the given date to the end of its month.
    Suppose `freq == 'W'`.
    If `past == True`, then round the given date to the Monday of its week.
    Otherwise, round the given date to the Sunday of its week.
    For all other values of `freq`, return the given date unchanged.
    """
    from calendar import monthrange
    from dateutil.relativedelta import relativedelta

    if freq == 'M':
        if past:
            day = 1
        else:
            day = monthrange(date.year, date.month)[1]            
        date = dt.date(date.year, date.month, day)
    elif freq == 'W':
        if past:
            date = date - dt.timedelta(date.weekday())
        else:
            date = date - dt.timedelta(date.weekday()) +\
                   dt.timedelta(days=6)
    return date

def get_slice(data, start=None, end=None, freq='M', heading=False):
    """
    Given a Pandas data frame of income items, resample it by the given
    Pandas frequency `freq`, and return the data slice between the given start
    and end dates.
    Assume `start` and `end` are date or datetime objects.
    For a list of Pandas frequency constants, see
    `https://github.com/pydata/pandas/wiki/Proposed-Frequency-Conventions`_.
    """
    data = data.resample(freq, how='sum').fillna(0)
    if start is None:
        start = data.index[0]
    if end is None:
        end = data.index[-1]
    result = data[start:end]    
    if heading != False:
        if heading == True:
            heading = '%s--%s' % (start, end)
        result = result, heading
    return result

def get_last_12_months_slice(data, freq='M', heading=False):
    """
    Given a Pandas data frame of income items, resample it by the given
    Pandas frequency `freq`, and return the data slice for the last 12 months.
    """
    from dateutil.relativedelta import relativedelta

    data = data.resample(freq, how='sum').fillna(0)
    end = round_date(dt.datetime.today(), freq='M', past=False)
    start = end + relativedelta(months=-11) 
    result = data[start:end]
    if heading != False:
        if heading == True:
            heading = 'Last 12 Months'
        result = result, heading
    return result

def get_year_slice(data, year=None, freq='M', heading=False):
    """
    Given a Pandas data frame of income items, resample it by the given
    Pandas frequency `freq`, and return the data slice for the given year.
    Default to the current year.
    """
    data = data.resample(freq, how='sum').fillna(0)
    today = round_date(dt.datetime.today(), freq='M', past=False)
    if year is None:
        year = today.year
    if year == today.year:
        start = dt.date(today.year, 1, 1)
        end = today
    else:
        start = dt.date(year, 1, 1)
        end = dt.date(year, 12, 31)        
    result = data[start:end]
    if heading != False:
        if heading == True:
            heading = 'Year %s' % year
        result = result, heading
    return result

def get_tax_year_slice(data, year=None, start_month=4, freq='M', 
                       heading=False):
    """
    Given a Pandas data frame of income items, resample it by the given
    Pandas frequency `freq`, and return the data slice for the twelve month
    period starting on the given year and month.
    Default to the current year and to the beginning of the New Zealand
    tax year, namely 1 April. 
    """
    from dateutil.relativedelta import relativedelta

    data = data.resample(freq, how='sum').fillna(0)
    if year is None:
        year = dt.datetime.today().year
    start = dt.date(year, start_month, 1)
    end = start + relativedelta(days=+364)       
    result = data[start:end]
    if heading != False:
        if heading == True:
            heading = 'Tax Year %s' % year
        result = result, heading
    return result

def get_stats(data, currency='NZD ', as_text=True):
    """
    Given a Pandas data frame of income items, return the following
    statistics: 
    (total income, start date, end date, hours worked, hours per week,
     income per month, income per week, income per hour).
    If `as_text == True`, then return the stats as a formatted text string
    using the specified currency symbol.
    """
    from dateutil.relativedelta import relativedelta

    freq = data.index.freq
    start = round_date(data.index[0].date(), freq=freq, past=True)
    end = round_date(data.index[-1].date(), freq=freq, past=False)
    delta = end - start
    total_income = data['income'].sum()
    total_hours = data['hours'].sum()
    hours_per_week = total_hours/max(1, delta.days/7)
    income_per_month = total_income/max(1, delta.days/30.4)
    income_per_week = total_income/max(1, delta.days/7)
    income_per_hour = total_income/total_hours
    result = (round(total_income, 2), 
              start,
              end, 
              total_hours, 
              round(hours_per_week, 1), 
              round(income_per_month, 2), 
              round(income_per_week, 2),
              round(income_per_hour, 2))
    if as_text:
        result = """
        Total income = $%s
        Start date = %s
        End date = %s
        Total hours = %s
        Hours per week = %s
        Income per month = $%s
        Income per week = $%s
        Income per hour = $%s
        """ % result
    result = result.replace('$', currency)
    return result
  
def plot_nvd3(data, width=700, height=400, currency='NZD ', chart_id='temp'):
    """
    Given a Pandas data frame of income items, plot the data as a 
    bar chart of the given width and height using nvd3.js.
    Use the given currency symbol.
    Return the HTML snippet containing the chart within the tags
    <div id='chard_id'></div>.
    """    
    import json

    json_data = [{'x': t.strftime('%Y-%m-%d'), 'y': float(data['income'][t])} 
                 for t in data.index]
    html = """
    <div id="chart%s"><svg style="width:%spx; height:%spx;"></svg></div>
    """ % (chart_id, width, height)
    html += """
    <script type="text/javascript">
        nv.addGraph(function() {
            var chart = nv.models.discreteBarChart()
                .margin({top: 10, right: 10, bottom: 70, left: 70});
            chart.color(d3.scale.category10().range());
            chart.xAxis
                .rotateLabels(-45);
            chart.yAxis
                .axisLabel('%s')
                .tickFormat(d3.format('.00f'));
            chart.tooltipContent(function(key, y, e, graph) {
                var x = String(graph.point.x);
                var y = String(graph.point.y);
                if(key == 'Series 1'){
                    var y =  String(graph.point.y)  + ' %s';
                }
    """ % (currency, currency)
    html += """
                tooltip_str = 'y = ' + y + '<br>x = ' + x;
                return tooltip_str;
            });
            d3.select('#chart%s svg')
                .datum(data%s)
                .transition().duration(500)
                .attr('width', %s)
                .attr('height', %s)
                .call(chart);

        return chart;
    });
    """ % (chart_id, chart_id, width, height)
    html += """
        data%s=[{"values": %s, "key": "Series 1", "yAxis": "1"}];
    </script>
    """ % (chart_id, json.dumps(json_data))
    return html


def report_nvd3(summaries, output_file, currency='NZD ', 
                css='income_reporter.css'):
    """
    Given `summaries`, a list of pairs (data, heading), where data is 
    a Pandas data frame of income items and heading is a string, 
    make a chart for each data frame via plot_nvd3() 
    (with the given currency symbol), title each chart
    with the given heading, and write the charts to the HTML file
    `output_file`.
    Use the given CSS file to style that HTML file.

    To make the charts, call upon local copies of NVD3 code, 
    which i copied from
    `http://nvd3.org/src/nv.d3.css`_, `http:/nvd3.org/lib/d3.v2.js`_,
    and `http:/nvd3.org/nv.d3.js`_.
    """
    html = """
    <head>
        <link href="%s" rel="stylesheet">
        <link media="all" href="nvd3/src/nv.d3.css" type="text/css" rel="stylesheet" />
        <script src="nvd3/lib/d3.v2.js" type="text/javascript">
        </script>
        <script src="nvd3/nv.d3.js" type="text/javascript"></script>
    </head>
    <body>
        <h1>Income Report</h1>
    """ % css
    for (i, (data, heading)) in enumerate(summaries):
        html += "\t<h2>" + heading + "</h2>\n"
        html += plot_nvd3(data, chart_id=i, currency=currency)
        text = get_stats(data, as_text=True)
        html += "\t\t<pre>" + text + "</pre>\n"
    html += """
    </body>
    </html>
    """
    fout = open(output_file, 'w')
    fout.write(html)
    fout.close()

def main():
    """
    Get command line arguments, process files, and create a report
    with four income summaries (current year, last 12 months, current
    tax year, and all data).
    """
    import webbrowser

    args = parse_args()
    data = make_data_frame(args.infiles)
    summaries = [
      get_year_slice(data, heading=True, freq='M'),
      get_last_12_months_slice(data, heading=True),
      get_tax_year_slice(data, heading=True),
      get_slice(data, heading='All Data'),
    ]
    report_nvd3(summaries, args.outfile[0])    


if __name__ == '__main__':
    main()