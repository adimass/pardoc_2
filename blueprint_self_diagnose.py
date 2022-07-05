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

    if "true" in session :
        p_true = session['true']
    if "false" in session :
        f_true = session['false']

    if "gejalaId" not in session:
        query ='''
        select *
        from gejala
        where gejalaId = 'G1'
        '''
        rule = '''
        select *
        from relasi
        '''
        df = db.df_query(rule)
        b = df.set_index('penyakitId').groupby(level=0).agg(list)
        b['penyakitId'] = b.index
        data = json.loads(b.to_json(orient='records'))
        session['flag'] = data

    else:
        penyakit = []
        flag = session['flag']

        for i in flag:
            penyakit.append(i['penyakitId'])


        sakit = str(penyakit)[1:-1]
        gejala = p_true + f_true
        gejala = str(gejala)[1:-1]

        print("=========================")
        print(penyakit)
        print(gejala)
        print("=========================")
            
        query ="""
            
            with data as (
            select *
            from relasi
            where penyakitId in (%s)
            ),data2 as (
            select DISTINCT(gejalaid)
            from data)
            select g.gejalaid,nama,pertanyaan
            from data2 d left join gejala g on d.gejalaid = g.gejalaid
            where g.gejalaId not in (%s)
            
            """%(str(sakit),str(gejala))
    
    gejala = db.df_query(query)

    if len(gejala) == 0:
        return redirect(url_for('bp_self_diagnose.result_diagnose'))

    gejalaId = gejala.iloc[0]['gejalaId']
    pertanyaan = gejala.iloc[0]['pertanyaan']

    return render_template('content_user_self_diagnose.html',pertanyaan = pertanyaan, gejalaId = gejalaId)


@bp_self_diagnose.route('/answer_diagnose', methods=['POST'])
def answer_diagnose():
    jawaban =  request.form.get('pilihan')
    gejalaId = request.args.get("gejalaId")

    flag = session['flag']
    tag = []

    if len(flag) != 1:

        if 'gejalaId' not in session:
            session['gejalaId'] = []
            session['true'] = []
            session['false'] = []

        if jawaban == 'ya':
            gejala_true = session['true']
            gejala_true.append(gejalaId)
            session['true'] = gejala_true
            for i in flag:
                if str(gejalaId) in i['gejalaId']:
                    tag.append(i)
            if len(tag) != 0:
                session['flag'] = tag

        if jawaban == 'tidak':
            gejala_false = session['false']
            gejala_false.append(gejalaId)
            session['false'] = gejala_false
            for i in flag:
                if str(gejalaId) not in i['gejalaId']:
                    tag.append(i)
            if len(tag) != 0:
                session['flag'] = tag

    elif len(flag) == 1:
        if jawaban == 'ya':
            gejala_true = session['true']
            gejala_true.append(gejalaId)
            session['true'] = gejala_true
        if jawaban == 'tidak':
            gejala_false = session['false']
            gejala_false.append(gejalaId)
            session['false'] = gejala_false
            

    # if len(session['flag']) == 1 or len(session['flag']) == 0:
    #     return 'dapet'
    
    print(len(session['flag']))

    # if len(session['flag']) == 1:

    #    return redirect(url_for('bp_self_diagnose.result_diagnose'))

    print(session['flag'])
    return redirect(url_for('bp_self_diagnose.self_diagnose'))
   

@bp_self_diagnose.route('/result_diagnose', methods=['POST','GET'])
def result_diagnose():


    print(session['flag'])
    print(session['true'])
    print(session['false'])
    if 'gejalaId' in session:
        session.pop('gejalaId')
        session.pop('true')
        session.pop('false')


    return 'oke'