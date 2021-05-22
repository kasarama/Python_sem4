from flask import Flask
from flask import render_template
from flask import Flask, jsonify, abort, request

app = Flask(__name__)
route = 'api'