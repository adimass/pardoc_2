from flask import Blueprint, render_template, redirect, url_for, send_file,session, abort, redirect, request
import requests
import json
import database as db
import pandas as pd
from flask_paginate import Pagination, get_page_parameter

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


@bp_profile.route('/list_user', methods=['POST',"GET"])
def list_users():

    query = '''
    select *
    from users
    where role like 'user'
    '''
    all_user = db.df_query(query)
    list_user = all_user.values.tolist()
    return render_template('content_admin_list_user.html',list_user=list_user)


@bp_profile.route('/delete_list_user', methods=['POST',"GET"])
def delete_list_users():

    userId = request.args.get("userId")
    print(userId)

    query = """
    delete from users
    where userId like '%s'
    """%(userId)

    db.execute_query(query)

    return redirect("/list_user")

@bp_profile.route('/list_penyakit', methods=['POST',"GET"])
def list_penyakit():

    # page = request.args.get('page', 1, type=int)

    # query = '''
    # select *
    # from penyakit
    # '''
    # all_penyakit = db.df_query(query)
    # list_penyakit = all_penyakit.values.tolist()
    # list_penyakit = list_penyakit.paginate(page=page, per_page=5)

    # print(list_penyakit)



    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)

    query = '''
    select *
    from penyakit
    '''
    all_penyakit = db.df_query(query)
    list_penyakit = all_penyakit.values.tolist()

    i=(page-1)*5
    penyakit_page = list_penyakit[i:i+5]


    # pagination = Pagination(page=page, total=len(list_penyakit), record_name='list_penyakit')
    pagination = Pagination(page=page,per_page=5, total=len(list_penyakit), search=search, record_name='List')

    return render_template('content_admin_list_penyakit.html',penyakit = penyakit_page, pagination=pagination,show_single_page=True)

@bp_profile.route('/list_gejala', methods=['POST',"GET"])
def list_gejala():

    query = '''
    select *
    from gejala
    '''
    all_gejala = db.df_query(query)
    list_gejala = all_gejala.values.tolist()

    print(list_gejala)

    return render_template('content_admin_list_gejala.html',gejala = list_gejala)

@bp_profile.route('/list_drug', methods=['POST',"GET"])
def list_drug():



    return render_template('content_admin_list_drug.html')


# for i in hasil.items():
#     if len(i[1][0]) > 0 :
#         if i[1][0].isnumeric():
#             qry = str(i[0])+" = %s,"%(i[1][0])
#         else:
#             qry = str(i[0])+" = '%s',"%(i[1][0])
#         print(qry)
#         string = string+qry
