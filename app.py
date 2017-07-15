from flask import Flask
from flask import request
import requests

app = Flask(__name__)

@app.route('/search')
def search_items():
	dish = request.args['dish']
	budget = int(request.args['budget'])
	cost = None
	if(budget < 500):
		cost='$'
	elif(budget < 1000):
		cost='$$'
	elif(budget < 2000):
		cost='$$$'
	else:
		cost='$$$$'

	url = 'https://www.swiggy.com/api/restaurants/search?third_party_vendor=1&lat=12.9345625&lng=77.60613179999996&str= '+dish+'&budget= '+budget
	res = requests.get(url)
	print url
	return res.text

if __name__ == '__main__':
    app.run()

    # https://www.swiggy.com/api/restaurants/search?third_party_vendor=1&str=mutton&lat=12.9345625&lng=77.60613179999996&page=