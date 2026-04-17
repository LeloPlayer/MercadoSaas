from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime, timedelta
import os
import random

app = Flask(__name__, static_folder='static')
CORS(app)

DB_PATH = 'mercado.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

