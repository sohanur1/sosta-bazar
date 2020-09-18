from flask import Flask,request,Response
from flask import render_template
from shwapno import Shwapno
from chaldal import Chaldal
from flask_cors import CORS
import json
app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def hello_world():
    return 'Hello World! <a href="/search_products">Search</a>'


@app.route('/search_products')
def search_products_func():
   return render_template('search_products.html')

@app.route('/find_products')
def find_products_func():
    pname = request.args.get('pname')
    swapno_app = Shwapno(pname, 'Uttara')
    list = swapno_app.prod_list
    return render_template('results.html',result = list)

@app.route('/api/products/search/<key>', methods=['GET'])
def api_all(key):
    pname = key
    swapno_app = Shwapno(pname, 'Uttara')
    chaldal_app = Chaldal(pname,'Uttara')
    list = swapno_app.prod_list
    list2 = chaldal_app.prod_list
    res = list+list2
    arr = [{"name": p.name, "shop": p.shop,
                     "price": p.price, "link": p.link,"img":p.img}
                    for p in res]
    #print(json.dumps({"data": arr}, indent=3))
    return Response(json.dumps(arr, indent=3),  mimetype='application/json')



if __name__ == '__main__':
    app.run()
