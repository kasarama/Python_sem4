from flask import Flask, jsonify, abort, request, Response
import io, argparse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
 
from modules import facade, database
#from modules import facade


parser = argparse.ArgumentParser()
parser.add_argument('-r', '--restore', action ='store', dest='restore_db', default=False, help='Defines if the database should be restored')
parser.add_argument('-d', '--development', action ='store', dest='development', default=False, help='Set to False if run in production mode')
results=parser.parse_args()

def setup_db():
    if results.restore_db in ['True', 'true', 'T', 't']:
        
        database.setup_db()

setup_db()




app = Flask(__name__)

#return calculated regressions for all the models, return all the models
regressions, models=facade.prepare_regressions()

@app.route("/")
def index():
    return('<h>Hi there!</h>')


@app.route( "/estimate", methods=['POST'])
def check_price():
    '''Calculates price with linerar regression'''

    print(request.json)
    if not request.json or not "model" in request.json or not "year" in request.json or not "capacity" in request.json or not "km" in request.json or not "fuel" in request.json:
        abort(400)

    att=['model','year','km','capacity',"fuel"]
    audi={}
    for a in att:
        audi[a] = request.json[a]

    (price, intercept, coefficient)=facade.estimate_price(regressions,audi)
    
    return jsonify({'recieved': audi,'estimated_price': int(price[0]), 'intercept':intercept, 'coefficient':coefficient })







@app.route( "/add", methods=["POST"])
def add_new():

    '''adds car to database with predicted price'''
    if not request.json or not "model" in request.json or not "fuel" in request.json or not "year" in request.json or not "capacity" in request.json  or not "km" in request.json or not "price" in request.json:
        abort(400)

    att=['model','year','km','capacity','fuel','price']
    audi={}
    for a in att:
        audi[a] = request.json[a]

    # TO DO save car in DB
    added=facade.save_car(regressions, audi)
    
    return jsonify({'added': added})




#/plot?model=A1&fuel=Benzin&f1=km&f2=capacity
@app.route('/plot')
def plot_png():
    model=request.args.get('model')
    fuel=request.args.get('fuel')
    f1=request.args.get('f1')
    f2=request.args.get('f2')
    fig = _3d_figure(models, model,fuel,[f1,f2])
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def _3d_figure(models,model,fuel,features):
    request_model=models[fuel][model]   

    xs=list(request_model[features[0]])
    ys=list(request_model[features[1]])
    zs=list(request_model['price'])
    fig = Figure()    
    ax = fig.add_subplot(111, projection='3d')
  
    ax.scatter(xs, ys, zs, cmap="Blues", marker='o')

    ax.set_xlabel(features[0])
    ax.set_ylabel(features[1])
    ax.set_zlabel('Price')
    return fig



if __name__ == '__main__':
    #app.run(debug=bool(results.development))
    
    dev=False
    if results.development in  ['True', 'true', 'T', 't']:
        dev=True
    app.run(debug=dev)