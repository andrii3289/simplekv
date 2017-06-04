import os
from socket import gethostbyname
from flask import Flask,json,jsonify,request,render_template
from token_create import token_create
from token_check import token_check


app = Flask(__name__)


#default welcome page
@app.route("/")
def default():
    return render_template('index.html',name=request.remote_addr,host=gethostbyname('localhost'))


#creating storage with inputs
@app.route("/<filename>/<key>/<value>", methods=['POST'])
def add_key(filename,key,value):
    token = request.headers['token']
    if token_check(token):
        #creating directory if not exists
        if not os.path.exists(token):
            try:
                os.makedirs(token)
            except Exception as e:
                return jsonify({"error":"{}".format(str(e))})
        #creating file if not exists
        if not os.path.exists('{}/{}'.format(token,filename)):
            try:
                with open('{}/{}'.format(token,filename),'w') as empty_file:
                    empty_file.write("{}")
            except Exception as e:
                return jsonify({"error":"{}".format(str(e))})
            try:
                #creating json from inputs
                with open('{}/{}'.format(token,filename)) as f:
                    data = json.load(f)
                    dict_new = {key: value}
                    data.update(dict_new)
                with open('{}/{}'.format(token,filename),'w') as outfile:
                    json.dump(data,outfile,indent=4)
                return jsonify({"file":"{}".format(filename),"created":"true"})
            except Exception as e:
                return jsonify({"error":"{}".format(str(e))})
    else:
        return "token is invalid\n"


#request whole file
@app.route("/<filename>")
def whole_file(filename):
    token = request.headers['token']
    try:
        with open('{}/{}'.format(token,filename)) as response:
            loaded_response = json.load(response)
        return jsonify(loaded_response)
    except Exception as e:
        return jsonify({"error":"{}".format(str(e))})


#request value of certain key
@app.route("/<filename>/<key>")
def certain_key(filename,key):
    token = request.headers['token']
    with open('{}/{}'.format(token,filename)) as response:
            loaded_response = json.load(response)
    return loaded_response[key] + "\n" 


#delete certain key
@app.route("/<filename>/<key>", methods=['DELETE'])
def del_key(filename,key):
    token = request.headers['token']
    try:
        with open('{}/{}'.format(token,filename)) as changing_file:
            changing_data = json.load(changing_file)
            if key in  changing_data:
                changing_data.pop(key,None)
            else:
                return "key is invalid"
        with open('{}/{}'.format(token,filename),'w') as result:
            json.dump(changing_data,result)
        return jsonify({"key":"{}".format(key),"deleted":"true"})
    except Exception as e:
        return jsonify({"error":"{}".format(str(e))})


#delete whole file
@app.route("/<filename>", methods=['DELETE'])
def del_whole_file(filename):
    token = request.headers['token']
    try:
        os.remove('{}/{}'.format(token,filename))
    except Exception as e:
        return jsonify({"error":"{}".format(str(e))})
    return jsonify({"filename":"{}".format(filename),"deleted":"true"})


#token request page
@app.route("/token")
def token_request():
    token = token_create()
    try:
        with open('tokens_base','a') as f:
            f.write(token+"\n")
        return render_template('token.html',token=token)
    except Exception as e:
        return jsonify({"error":"{}".format(str(e))})


if __name__ == "__main__":
    app.run(port=8080,debug=True)
