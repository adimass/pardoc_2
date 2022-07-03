import pandas as pd

df = pd.read_csv('gejala.csv')

print(df)

# <!-- 
# {% if session['role'] is 'user' %}

# <head>
#     <title>Patient</title>
#     </head>
    
    
#     <body>
    
#     <h1>This is a Heading</h1>
#     <p>This is a paragraph.</p>


        
#     <a href="https://www.w3schools.com/">lets us diagnose you</a>

  
    
# </body>

# {% elif session['role'] is 'dokter' %}

# <head>
#     <title>ini dokter</title>
#     </head>
    
    
#     <body>
    
#     <h1>This is a Heading</h1>
#     <p>This is a paragraph.</p>


        
#     <a href="https://www.w3schools.com/">lets us diagnose you</a>

 
    
# </body>

# {% else %}


# <head>
#     <title>ini admin</title>
#     </head>
    
    
#     <body>
    
#     <h1>This is a Heading</h1>
#     <p>This is a paragraph.</p>


        
#     <a href="https://www.w3schools.com/">lets us diagnose you</a>
    
# </body>

# {% endif %} -->
