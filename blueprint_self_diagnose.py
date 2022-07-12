from flask import Blueprint, render_template, redirect, url_for, send_file,session, abort, redirect, request
import requests
import json
import database as db
from datetime import datetime
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
            
    return redirect(url_for('bp_self_diagnose.self_diagnose'))
   

@bp_self_diagnose.route('/result_diagnose', methods=['POST','GET'])
def result_diagnose():
    

    derita = session['true']
    data = session['flag']
    print(data[0]['penyakitId'])
    sql ="""
        select *
        from penyakit
        where penyakitId like '%s'
    """%(data[0]['penyakitId'])

    
    penyakit = db.df_query(sql)

    
  
    penyakitId = data[0]['penyakitId']
    nama_penyakit = penyakit.iloc[0]['name']
    level_penyakit = penyakit.iloc[0]['level']
    keterangan_penyakit = penyakit.iloc[0]['keterangan']
    date_penyakit = datetime.date(datetime.now())

    if level_penyakit == 'LOW':

        query = """

                select *
                from obat
                where penyakitId like '%s'
            
            """%(data[0]['penyakitId'])

        obat = db.df_query(query)
        print(obat)


    if 'gejalaId' in session:
        session.pop('gejalaId')
        session.pop("true")
        session.pop('false')




    return render_template('content_result_self_diagnose.html',nama_penyakit=nama_penyakit,level_penyakit = level_penyakit,keterangan_penyakit=keterangan_penyakit,date_penyakit=date_penyakit,penyakitId = data[0]['penyakitId'])


@bp_self_diagnose.route('/save_diagnose', methods=['POST','GET'])
def save_diagnose():
    nama_penyakit =  request.args.get('nama_penyakit')
    level_penyakit = request.args.get("level_penyakit")
    date_penyakit = request.args.get("date_penyakit")
    penyakitId = request.args.get("penyakitId")

    query = '''
    
    select count(*)
    from hasil
    
    '''

    tl = datetime.today().strftime('%Y%m%d')
    hasil = db.execute_query_one(query)
    hasil = hasil+1
    hasilId = 'hsl'+str(tl)+str(hasil)
    
    print(hasilId)
    
    if level_penyakit == 'LOW':

        query = """

            select *
            from obat
            where penyakitId like '%s'
        
        """%(penyakitId)

        print(query)
        
        query = """
        
        insert into hasil values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
        
        
        """%(hasilId,session['userId'],penyakitId,'',session['name'],level_penyakit,date_penyakit,session['gender'],nama_penyakit,'')

        print(query)

    else:
        query = """
        
        insert into hasil values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
        
        
        """%(hasilId,session['userId'],penyakitId,'',session['name'],level_penyakit,date_penyakit,session['gender'],nama_penyakit,'')

        print(query)

        



    print(nama_penyakit)
    print(level_penyakit)
    print(date_penyakit)
    print(penyakitId)

    return redirect('/home')