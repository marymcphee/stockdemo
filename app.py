from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
	#nquestions=app_lulu.nquestions
	if request.method == 'GET':
		return render_template('/index.html')
		#return render_template('userinfo_lulu.html',num=nquestions)
	else:
		#app.vars['ticker'] = request.form['ticker']
		ticker = request.form['ticker']
		url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.csv?auth_token=LqDUrvRFHsCs1bYDLqPP' % (ticker)
		session = requests.Session()
		session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
			#for url in app.fdaurls:
			#sleep(.25)
		api_url = url
			#app.responses.append(session.get(api_url))
		sesh = session.get(api_url)
			
		#second = app.responses
		pony=sesh.json()
		pony['dataset']
		pony2=pd.DataFrame(pony['dataset']['data'])
		pony2.columns=pony['dataset']['column_names']
		cache.set('data', pony2, timeout=5 * 60)

		return render_template('/index.html', sesh=sesh)

@app.route('/graph')
def this_graph():
	script, div = components(plot)
	return render_template('graph.html',script=script, div=div)


if __name__ == '__main__':
  app.run(port=33507)
