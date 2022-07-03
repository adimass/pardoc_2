from flask import Blueprint, render_template, request, send_file,session
import pandas as pd 
import json
import os

bp_homepage= Blueprint('bp_homepage', __name__)
@bp_homepage.route('/home')
def content_homepage():
    
    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')
        
    role = session['role']
    if role == 'user':
        return render_template('content_homepage.html')
    elif role == 'dokter':
        return render_template('content_dokter_homepage.html')
    else:
        return render_template('content_admin_homepage.html')

    


    