from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)
global name, image, sizes
name = "No Current Product"
image = "http://via.placeholder.com/400x400?text=No%20image"
sizes = {}

@app.route('/', methods=['GET'])
def home():
	pid = request.args.get('pid')
	store = request.args.get('store')

	if pid is None:
		return render_template('index.html')
	else:
		global name, image, sizes
		name, image, sizes = get_product_info(pid, store)
		return render_template('index.html')

@app.route('/stock_results', methods=['GET'])
def stock_results():
	return render_template('stock_results.html', name=name, img=image, stock=sizes)

def get_product_info(pid, site):
	pid = str(pid).upper()

	if site == 'FP':
		api_key = '5F9D749B65CD44479C1BA2AA21991925'
		user_agent = 'FootPatrol/2.0 CFNetwork/808.3 Darwin/16.3.0'
		sitename = 'footpatrol'
	elif site == 'JD':
		api_key = '1A17CC86AC974C8D9047262E77A825A4'
		user_agent = 'JDSports/5.3.1.207 CFNetwork/808.3 Darwin/16.3.0'
		sitename = 'jdsports'
	elif site == 'SZ':
		api_key = 'EA0E72B099914EB3BA6BE90A21EA43A9'
		user_agent = 'Size-APPLEPAY/4.0 CFNetwork/808.3 Darwin/16.3.0'
		sitename = 'size'

	headers = {
		'Host': 'commerce.mesh.mx',
		'Content-Type': 'application/json',
		'X-API-Key': api_key,
		'Accept': '*/*',
		'X-Debug': '1',
		'Accept-Language': 'en-gb',
		'User-Agent': user_agent,
		'MESH-Commerce-Channel': 'iphone-app',
	}

	params = (
		('expand', 'variations,informationBlocks,customisations'),
		('channel', 'iphone-app'),
	)
	
	stock_json_raw = requests.get('https://commerce.mesh.mx/stores/' + sitename + '/products/' + pid, headers=headers, params=params).text.strip()
	stock_json = json.loads(stock_json_raw)

	try:
		product_name = str(stock_json['name'])
		product_image = str(stock_json['resizedMainImage']['originalURL'])
		product_sizes = {}
		for size in stock_json['options']:
			product_sizes[size] = stock_json['options'][size]['SKU']
	except:
		product_name = "No Product Found"
		product_image = "http://via.placeholder.com/400x400?text=No%20image"
		product_sizes = {}

	return product_name, product_image, product_sizes

if __name__ == '__main__':
	app.run(debug=True)