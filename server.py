from flask import Flask, jsonify, abort, request, Response
import io, argparse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from modules import facade, database, classes


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
        abort(400, 'Missing input')

    att=['model','year','km','capacity',"fuel"]
    audi={}
    for a in att:
        audi[a] = request.json[a]

    (price, intercept, coefficient)=facade.estimate_price(regressions,audi)
    
    return jsonify({'recieved': audi,'estimated_price': int(price[0]), 'intercept':intercept, 'coefficient':coefficient })







@app.route( "/add", methods=["POST"])
def add_new():

    '''adds car to database with predicted price'''
    if not request.json or not "model" in request.json or not "fuel" in request.json or not "year" in request.json or not "capacity" in request.json  or not "km" in request.json or not "price" in request.json or not "user_name" in request.json :
        abort(400, 'Missing input')
    owner=request.json["user_name"]
    att=['model','year','km','capacity','fuel','price']
    audi={}
    for a in att:
        audi[a] = request.json[a]
    
    try:
        added=facade.save_car(regressions, audi, owner)
    except classes.DataBaseException as e:
        abort(400, e)
    
    return jsonify({'added': added})




#/plot?model=A1&fuel=Benzin&f1=km&f2=capacity
@app.route('/plot')
def plot_png():

    '''streams / mimics figure '''
    model=request.args.get('model')
    fuel=request.args.get('fuel')
    f1=request.args.get('f1')
    f2=request.args.get('f2')
    fig = facade._3d_figure(models, model,fuel,[f1,f2])
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')



@app.route('/register', methods=['POST'])
def register_user():
    if not request.json or not "user_name" in request.json or not "password" in request.json:
        abort(400, 'Missing input')
    user_name= request.json['user_name']
    password = request.json['password']

    pass_ok = True#validate_pass_with_regex(passw)

    if pass_ok:
        try:
            usr= database.register_user(user_name,password)[0]
            return jsonify(usr)
        except classes.DataBaseException as e:
            abort(400, e)
    else:
        abort(400, 'Wrong password format')

'''

https://stackoverflow.com/questions/5142103/regex-to-validate-password-strength

^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8}$


^                         Start anchor
(?=.*[A-Z].*[A-Z])        Ensure string has two uppercase letters.
(?=.*[!@#$&*])            Ensure string has one special case letter.
(?=.*[0-9].*[0-9])        Ensure string has two digits.
(?=.*[a-z].*[a-z].*[a-z]) Ensure string has three lowercase letters.
.{8}                      Ensure string is of length 8.
$                         End anchor.

'''


if __name__ == '__main__':
    #app.run(debug=bool(results.development))
    
    dev=False
    if results.development in  ['True', 'true', 'T', 't']:
        dev=True
    app.run(debug=dev)