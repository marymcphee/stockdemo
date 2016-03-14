from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import numpy as np
import bokeh
from bokeh.embed import components
from bokeh.plotting import figure, show, output_server
from datetime import datetime
#from werkzeug.contrib.cache import SimpleCache

#cache = SimpleCache()


app = Flask(__name__)

app.vars={}
app.df = pd.DataFrame()


@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():

	if request.method == 'GET':
		return render_template('/index.html')

	else:

		app.vars['ticker'] = request.form['ticker']
		url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json?auth_token=LqDUrvRFHsCs1bYDLqPP' % (app.vars['ticker'])
		session = requests.Session()
		session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
		sesh = session.get(url)
		injson=sesh.json()
		app.df=pd.DataFrame(injson['dataset']['data'])
		app.df.columns=injson['dataset']['column_names']
		return redirect('/graph')


@app.route('/graph', methods=['GET', 'POST'])
def this_graph():

	data = app.df
	ticker =app.vars['ticker']

	def makedate(x):
		return np.array(x, dtype=np.datetime64)


	
	if request.method == 'GET':
		thismax = max(data['Date'])
		thismin = min(data['Date'])
		app.maxdate = datetime.strptime(thismax, '%Y-%m-%d').strftime("%m/%d/%Y")
		app.mindate = datetime.strptime(thismin, '%Y-%m-%d').strftime("%m/%d/%Y")


		p1 = figure(x_axis_type = "datetime")
		p1.title = "Adjusted Closing Price"
		p1.grid.grid_line_alpha=0.3
		p1.xaxis.axis_label = 'Date'
		p1.yaxis.axis_label = 'Price'

		p1.line(makedate(data['Date']), data['Adj. Close'],  color='#A6CEE3', legend=ticker)

		show(p1)
	else:
		low = request.form['low']
		high = request.form['high']
		data['Date'] = makedate(data['Date'])
		toplot = data[(data['Date']<=high) & (data['Date']>=low)]
			#&data['Date']<high)]

		p1 = figure(x_axis_type = "datetime")
		p1.title = "Adjusted Closing Price"
		p1.grid.grid_line_alpha=0.3
		p1.xaxis.axis_label = 'Date'
		p1.yaxis.axis_label = 'Price'

		p1.line(toplot['Date'], toplot['Adj. Close'],  color='#A6CEE3', legend=ticker)

		show(p1)


	script, div = components(p1)
	return render_template('graph.html', thismin=app.mindate, thismax=app.maxdate, script=script, div=div, ticker=ticker)



##REMOVE DEBUG BEFORE DEPLOYING
if __name__ == '__main__':
  app.run(port=33507)
