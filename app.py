from flask import Flask, redirect, url_for, request, render_template, jsonify
import main
import time

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/', methods = ["GET","POST"])
def qna():
    return render_template('index.html')

@app.route('/sample', methods = ["GET","POST"])
def sample():
    return render_template('sample.html')

@app.route('/custom', methods = ["GET","POST"])
def custom():
    return render_template('custom.html')

@app.route('/img', methods = ["GET","POST"])
def img():
    return render_template('img.html')


#Worker routes
# @app.route('/kg', methods = ['GET','POST'])
# def kg():
#     main.build_graph()
#     return "Building graph"

@app.route('/model',methods = ['GET','POST'])
def model():
    data = str(request.get_json()['data'])
    file1 = open("./content/data.txt","w")
    file1.write(data)
    file1.close()
    text = main.build()
    return "Success"

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    ip_question = str(request.get_json()['question'])
    ans = main.qna_system(ip_question)
    return jsonify(ans)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)