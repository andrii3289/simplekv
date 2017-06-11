import os
import flask
import token_check
import token_create

app = flask.Flask(__name__)


#default welcome page
@app.route("/")
def default():
    return flask.jsonify({"status":"ok"})


#creating storage with inputs
@app.route("/<namespace>/<key>/<value>", methods=['POST'])
def add_key(namespace,key,value):
    try:
        token = flask.request.headers['token']
        if token_check.check(token):
            #creating directory if not exists
            if not os.path.exists(token):
                try:
                    os.makedirs(token)
                except Exception as e:
                    return flask.jsonify({"error":"{}".format(str(e))})
            #creating namespace if not exists
            if not os.path.exists('{}/{}'.format(token,namespace)):
                try:
                    with open('{}/{}'.format(token,namespace),'w') as empty_namespace:
                        empty_namespace.write("{}")
                except Exception as e:
                    return flask.jsonify({"error":"{}".format(str(e))})
                try:
                    #creating json from inputs
                    with open('{}/{}'.format(token,namespace)) as f:
                        data = flask.json.load(f)
                        data[key] = value
                    with open('{}/{}'.format(token,namespace),'w') as outnamespace:
                        flask.json.dump(data,outnamespace,indent=4)
                    return flask.jsonify({"namespace":"{}".format(namespace),"created":"true"})
                except Exception as e:
                    return flask.jsonify({"error":"{}".format(str(e))})
    except:
        return flask.jsonify({"error":"token is invalid"})


#flask.request whole namespace
@app.route("/<namespace>")
def whole_namespace(namespace):
    try:
        token = flask.request.headers['token']
        with open('{}/{}'.format(token,namespace)) as response:
            loaded_response = flask.json.load(response)
        return flask.jsonify(loaded_response)
    except Exception as e:
        return flask.jsonify({"error":"{}".format(str(e))})


#flask.request value of certain key
@app.route("/<namespace>/<key>")
def certain_key(namespace,key):
    try:
        token = flask.request.headers['token']
        with open('{}/{}'.format(token,namespace)) as response:
            loaded_response = flask.json.load(response)
        return loaded_response[key] + "\n" 
    except Exception as e:
        return flask.jsonify({"error":"{}".format(str(e))})


#delete certain key
@app.route("/<namespace>/<key>", methods=['DELETE'])
def del_key(namespace,key):
    try:
        token = flask.request.headers['token']
        with open('{}/{}'.format(token,namespace)) as changing_namespace:
            changing_data = flask.json.load(changing_namespace)
            if key in  changing_data:
                changing_data.pop(key,None)
            else:
                return "key is invalid"
        with open('{}/{}'.format(token,namespace),'w') as result:
            flask.json.dump(changing_data,result)
        return flask.jsonify({"key":"{}".format(key),"deleted":"true"})
    except Exception as e:
        return flask.jsonify({"error":"{}".format(str(e))})


#delete whole namespace
@app.route("/<namespace>", methods=['DELETE'])
def del_whole_namespace(namespace):
    try:
        token = flask.request.headers['token']
        os.remove('{}/{}'.format(token,namespace))
    except Exception as e:
        return flask.jsonify({"error":"{}".format(str(e))})
    return flask.jsonify({"namespace":"{}".format(namespace),"deleted":"true"})


#token flask.request page
@app.route("/token")
def token_request():
    token = token_create.create()
    try:
        with open('tokens_base','a') as f:
            f.write(token+"\n")
        return flask.jsonify({"token_request":"ok","token":"{}".format(token)})
    except Exception as e:
        return flask.jsonify({"error":"{}".format(str(e))})


if __name__ == "__main__":
    app.run(port=8080,debug=True)
