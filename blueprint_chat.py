from flask import Blueprint, render_template, redirect, url_for, send_file,session, abort, redirect, request
import requests
import json
import database as db
from flask_socketio import SocketIO, send

bp_chat = Blueprint("bp_chat",__name__)



@bp_chat.route('/chat')
def content_chat():



    return render_template('content_chat.html')