from flask import Flask, render_template, request, redirect

app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
    #nquestions=app_lulu.nquestions
    if request.method == 'GET':
    	return render_template('index.html')
        #return render_template('userinfo_lulu.html',num=nquestions)
    else:
        #request was a POST
        #app.vars['ticker'] = request.form['ticker']
        ticker = request.form['ticker']
        #app_lulu.vars['age'] = request.form['age_lulu']
	#LqDUrvRFHsCs1bYDLqPP
		url = https://www.quandl.com/api/v3/datasets/WIKI/%s.csv?auth_token=LqDUrvRFHsCs1bYDLqPP' % (ticker)
		session = requests.Session()
			session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
			#for url in app.fdaurls:
			#sleep(.25)
			api_url = url
			#app.responses.append(session.get(api_url))
			session.get(api_url)
		#second = app.responses

if __name__ == '__main__':
  app.run(port=33507)
