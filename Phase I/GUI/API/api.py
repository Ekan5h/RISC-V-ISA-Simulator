import flask
from flask import request, jsonify
from flask_cors import CORS
from ASM2MC import parse

mc = [
    {
        'error':False,
        'error_msg':'',
        'original':[0,1,2,3,4],
        'basic':[0,1,2,3,4],
        'machine':[0,1,2,3,4],
        'data':{
            '0x000000':0
        }
    }
]

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/api/machine-code/', methods=['POST'])
def api():
    print(str(request))
    try:
        Original, Basic, Machine, data = parse(request.form['code'])
        return jsonify({
                'error':False,
                'original':Original,
                'basic':Basic,
                'machine':Machine,
                'data':data
            })
    except Exception as e:
        return jsonify(
            {
                'error':True,
                'errormsg':str(e)
            }
        )
app.run()
