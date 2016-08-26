import os
import sys
import csv
import datetime

metric = sys.argv[1]

def get_end_points():
	i = 0
	endpoints = []
	
	with open(metric+'-aggregated.csv', 'rb') as f:
	    reader = csv.reader(f)
	    for row in reader:
	    	i += 1
	    	if i > 1: # don't write out the header row
	        	endpoints.append(row[1])

	endpoints = list(set(endpoints))
	return endpoints

def write_chart_file(endpoints):
	target = open('memory.html', 'w')
	target.write('<html><head> <!--Load the AJAX API--> <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script> <script type="text/javascript"> google.charts.load("current", {"packages":["line"]}); google.charts.setOnLoadCallback(drawChart); function drawChart() {var data = new google.visualization.DataTable();')

	target.write('data.addColumn("string", "Date");')
	for url in endpoints:
		target.write('data.addColumn("number", "'+url+'");')

	# open csv and write data to javascript array
	target.write('data.addRows([')

	data = ''
	i = 0
	timestamp = ''
	timestamp2 = 'a'
	with open(metric+'-aggregated.csv', 'rb') as f:
	    reader = csv.reader(f)
	    for row in reader:
	    	i += 1
	    	if i > 1: # don't write out the header row
	    	# write out data as  [timestamp,  endpoint 1 value, endpoint 2 value, endpoint 3 value],
	        	#data += "['"+row[0]+"', '"+row[1]+"', "+row[2]+"],
	        	timestamp = row[0]
	        	if timestamp != timestamp2 and i == 2:
 					data += "['"+row[0]+"', "+row[2]
 					timestamp2 = timestamp
	        	elif timestamp != timestamp2 and i > 2:
	        		data += "],['"+row[0]+"', "+row[2]
	        		timestamp2 = timestamp
	        	else:
	        		data += ","+row[2]+" "


	data += "]]);"
	target.write(data)

	target.write('var options = {"title":"Percentage of Memory used", "width":1200, "lineWidth": 4, "curveType": "function", "height":800}; var chart = new google.charts.Line(document.getElementById("chart_div")); chart.draw(data, options); } </script> </head> <body> <!--Div that will hold the pie chart--> <div id="chart_div"></div> </body> </html>')
	target.close()

endpoints = get_end_points()
write_chart_file(endpoints)