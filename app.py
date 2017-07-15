from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import requests
import LatLon
import psycopg2

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

conn = psycopg2.connect(
	dbname="dq82dh5e9an5",
    user="jjmfzenixiiqri",
    password="5838f7538a792efcf4b8fd7e263ec720fcca4870d06fa86427d5c629ca508af7",
    host="ec2-50-19-83-146.compute-1.amazonaws.com",
    port="5432"
    )

@app.route('/search')
@cross_origin()
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

	url = 'https://www.swiggy.com/api/restaurants/search?third_party_vendor=1&lat=12.9345625&lng=77.60613179999996&page=ITEM&str= '+dish
	res = requests.get(url)
	print url
	return res.text

def insert_into_table(user,lat,lon):
	# Connect to an existing database
	lat = float(lat)
	lon = float(lon)

	# Open a cursor to perform database operations
	cur = conn.cursor()

	# Execute a command: this creates a new table
	cur.execute("CREATE TABLE location IF NOT EXISTS (id serial PRIMARY KEY, lat decimal, lon decimal);")

	# Pass data to fill a query placeholders and let Psycopg perform
	# the correct conversion (no more SQL injections!)
	cur.execute("INSERT INTO location (id, lat, lon) VALUES (%d, %f, %f)",(user, lat, lon))

	# Make the changes to the database persistent
	conn.commit()

	# Close communication with the database
	cur.close()


def query_from_table(lat,lon):
	# Connect to an existing database
	lat = float(lat)
	lon = float(lon)

	currentPos = LatLon(lat, lon)
	offsetTop = currentPos.offset(90, 1)
	offsetBottom = currentPos.offset(275, 1)

	offsetRight = currentPos.offset(0, 1)
	offsetLeft = currentPos.offset(270, 1)
	# Open a cursor to perform database operations
	cur = conn.cursor()

	cur.execute("SELECT * from location WHERE lat in between "+offsetTop+" and "+offsetBottom +"and lon in between "+offsetRight+" and "+offsetLeft)
	rows = cur.fetchall()
	for row in rows:
		print "   ", row[1][1]
	# Close communication with the database
	cur.close()


@app.route('/setlocation', methods=['POST'])
def set_location():
	lat = request.args['lat']
	lon = int(request.args['lon'])
	insert_into_table(user,lat,lon)
	return "Your location has been successfully set"

if __name__ == '__main__':
    app.run()

 