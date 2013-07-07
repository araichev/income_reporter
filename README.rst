Income Reporter
=================
This is a little Python 2.7 command-line program to make an HTML income 
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

Todo
-----
- Add doctest examples
- Doctest

Example
--------
The file `income_reporter.html` contains an example of a report made from randomly generated data and can be viewed live via rawgithub.com `here <https://rawgithub.com/araichev/income_reporter/master/income_reporter.html>`_.

Dependencies
-------------
Pandas.

Authors
--------
- Alex Raichev (2013-05-26)

License
--------
GPLv3.  See `COPYING.txt`.
