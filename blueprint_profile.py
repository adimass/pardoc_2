from flask import Blueprint, render_template, redirect, url_for, send_file,session, abort, redirect, request
import requests
import json
import database as db
import pandas as pd

bp_profile = Blueprint("bp_profile",__name__)

@bp_profile.route("/user-profile",methods=["POST","GET"])
def user_profile():

    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')

    userId = session['userId']
    query = '''
    
    select *
    from users
    where userId like '%s'
    
    '''%(str(userId))
    user = db.df_query(query)
    parsed = user.to_json(orient="records")
    user_json = json.loads(parsed)

    return render_template('content_user_profile.html',user = user_json[0])

@bp_profile.route('/update-users', methods=['POST',"GET"])
def update_users():

    hasil = request.form.to_dict(flat=False)
    string = ""
    for i in hasil.items():
        if len(i[1][0]) > 0 :
            qry = str(i[0])+" = '%s',"%(i[1][0])
            string = string+qry

    userId = session['userId']
    query = """
    UPDATE users
    SET %s
    WHERE userId = '%s'
    """%(string[:-1],userId)
    db.execute_query(query)
    return redirect("/user-profile")


# for i in hasil.items():
#     if len(i[1][0]) > 0 :
#         if i[1][0].isnumeric():
#             qry = str(i[0])+" = %s,"%(i[1][0])
#         else:
#             qry = str(i[0])+" = '%s',"%(i[1][0])
#         print(qry)
#         string = string+qry
