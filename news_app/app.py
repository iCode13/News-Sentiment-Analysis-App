from flask import Flask, jsonify, render_template, request, make_response
import requests

# from news_app.sentiment import get_scores


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")