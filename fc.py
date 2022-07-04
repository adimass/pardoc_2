import database as db
import json

# query2 ='''
# select *
# from gejala
# '''

# df2 = db.df_query(query2)

# arr = []
# flag_q = []
# flag = True
# while flag is True:
#     penyakit = []
#     query = ''
#     query22 = ''
#     for i,row in df2.iterrows():
#         print(row['nama'])
#         jawab = input()
#         if jawab is 'y':
#             arr.append(row['gejalaId'])

#         flag_q.append(row['gejalaId'])
#         gejala = str(arr)[1:-1]
#         skip = str(flag_q)[1:-1]
#         query3 = """
#             with data as (
#                 select *
#                 from relasi
#             ) , data2 as (
#                 select DISTINCT(penyakitId)
#                 from data
#                 where gejalaId in (%s)
#             ),data3 as (
#                 select DISTINCT(gejalaId)
#                 from data join data2 on data.penyakitId = data2.penyakitId
#                 where gejalaId not in (%s)
#             )
#                 select g.gejalaId,nama
#                 from gejala g join data3 d on g.gejalaId = d.gejalaId
#             """%(gejala,skip)

#         query44 = '''
        
#         with da as (
#         select *
#         from relasi
#         where gejalaId in (%s)
#         )
#         select *
#         from da
#         where gejalaId in ('%s')
        
#         '''%(gejala,arr[-1])
        
#         query22 = query44
#         query = query3
        
#         break


    
    
    
    # df2 = db.df_query(query)
    # df3 = db.df_query(query22)
    # print(arr)
    # print(df3)

    # if len(df2) < 1:
    #     flag = False







query ='''
select *
from gejala
where gejalaId = 'G1'
'''

rule = '''
select *
from relasi
'''


gejala = db.df_query(query)
df = db.df_query(rule)


b = df.set_index('penyakitId').groupby(level=0).agg(list)
b['penyakitId'] = b.index
data = json.loads(b.to_json(orient='records'))
# print(data)

for i in data:
    if 'G1' in i['gejalaId']:
        print(i)
    



    

# for i in data :
#     if 'G1' not in i['gejalaId']:
#         print(i['gejalaId'])

# print(gejala)
# # print(relasi)

# yes = []
# no = []



# quest = []


# flag = True
# while flag is True:
#     for i,row in gejala.iterrows():
#         penyakit = []
#         print(row['nama'])
#         jawab = input()
#         quest.append(row['gejalaId'])
#         if jawab is 'y':
#             for a in data :
#                 if row['gejalaId'] in a['gejalaId']:
#                     penyakit.append(a['penyakitId'])
#         if jawab is 'n':
#             for a in data:
#                 if row['gejalaId'] not in a['gejalaId']:
#                     penyakit.append(a['penyakitId'])  

#         # arr = []
#         # for a in range(len(data)):
#         #     if data[a]['penyakitId'] not in penyakit:
#         #         arr.append(data[a])


#         #karena penyakit itu selali di list nol 
        
#         print(quest)
#         print(penyakit)
#         print(data)
        
#         penyakit2 = str(penyakit)[1:-1]
        
#         flag = False

#     flag = False