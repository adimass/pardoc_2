from flask import Blueprint, render_template, redirect, url_for, send_file,session, abort, redirect, request
import requests
import json
import database as db

bp_self_diagnose = Blueprint('bp_self_diagnose', __name__)

@bp_self_diagnose.route('/self_diagnose')
def self_diagnose():

    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')


    if "flag" not in session:
        query ='''
        select *
        from gejala
        where gejalaId = 'G1'
        '''

    else:
        query ='''
        select *
        from gejala
        where gejalaId = 'G1'
        '''
    gejala = db.df_query(query)

    gejalaId = gejala.iloc[0]['gejalaId']
    pertanyaan = gejala.iloc[0]['pertanyaan']

    print(pertanyaan)
    print(gejala)

    return render_template('content_user_self_diagnose.html',pertanyaan = pertanyaan, gejalaId = gejalaId)


@bp_self_diagnose.route('/answer_diagnose', methods=['POST'])
def answer_diagnose():

    jawaban =  request.form.get('pilihan')
    gejalaId = request.args.get("gejalaId")
    print(gejalaId)
    print(jawaban)

    if 'gejalaId' not in session:
        session['gejalaId'] = []
    # if 'flag'


    if jawaban == 'ya':
        gejala_list = session['gejalaId']
        gejala_list.append(gejalaId)
        session['gejalaId'] = gejala_list


    return redirect(url_for('bp_self_diagnose.self_diagnose'))

@bp_self_diagnose.route('/result_diagnose', methods=['POST','GET'])
def result_diagnose():

    if 'gejalaId' in session:
        session.pop('gejalaId')

    return "oke"

    # if jawaban == 'ya':
    #     return redirect(url_for('bp_self_diagnose.self_diagnose'))
    # else:
    #     return 'oke'