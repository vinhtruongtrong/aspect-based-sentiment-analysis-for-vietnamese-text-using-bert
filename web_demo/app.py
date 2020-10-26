from flask import Flask, request, jsonify, abort
from flask import make_response
from flask import render_template
from predictor import Predictor
from flask_cors import CORS, cross_origin


predictor = Predictor()
app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route("/")
def hello():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route("/api/predict", methods=["POST"])
def predict_sentence():
    sentence = request.json['sentence']
    if(sentence == None or len(sentence) == 0):
        return jsonify({'status_code' : 400, 'message':'Your sentence is empty'})
    result = predictor.predict(sentence)
    result = predictor.multiple_output_post_processing(result)
    return jsonify({'status_code': 200, 'result': result})


if __name__ == "__main__":
    app.run(debug=True, port=1203)