from flask import Flask, request, jsonify
# from speechtext import record

app = Flask(__name__)

command = []

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/listen/send", methods=["POST", "GET"])
def listenFunc():
    content = request.json
    if content != None:
        command.append(content)
        print(content)
        return jsonify({"OK": 1})
    else:
        return jsonify({"OK": 0})

@app.route("/check", methods=["GET"])
def checkNewCommand():
    if len(command) == 0:
        json = {
            "piece": None,
            "y": None,
            "x": None
        }
        return json
    else:
        temp = command[0]
        command.pop(0)
        return jsonify(temp)

if __name__ == "__main__":
    app.run(debug=True)