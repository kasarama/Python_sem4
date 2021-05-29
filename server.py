from flask import Flask
from flask import render_template
from flask import Flask, jsonify, abort, request, Response
import io
import random

from modules import facade


app = Flask(__name__)
route = "/api"

regressions=facade.prepare_regressions()


@app.route("/")
def index():
    #return render_template("public/index.html")
    return('<h>Hi there!</h>')

@app.route(route + "/estimate", methods=['POST'])
def check_price():
    print(request.json)
    if not request.json or not "model" in request.json or not "year" in request.json or not "capacity" in request.json or not "km" in request.json or not "fuel" in request.json:
        abort(400)

    att=['model','year','km','capacity',"fuel"]
    audi={}
    for a in att:
        audi[a] = request.json[a]

    #TO DO return calculated price
    price=facade.estimate_price(regressions,audi)
    
    return jsonify({'recieved': audi,'estimated_price': price})



@app.route(route + "/add_new", methods=["POST"])
def add_new():
    if not request.json or not "model" in request.json or not "year" in request.json or not "capacity" in request.json  or not "km" in request.json or not "price" in request.json:
        abort(400)

    att=['model','year','km','capacity']
    audi={}
    for a in att:
        audi[a] = request.json[a]

    # TO DO save car in DB
    
    return jsonify({'recieved': audi})


from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

if __name__ == '__main__':
    app.run(debug=True)