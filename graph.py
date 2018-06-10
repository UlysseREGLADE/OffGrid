import cgi
import cgitb; cgitb.enable()
import datetime
import data_reader as dr
#import io
#bONJOUR

form = cgi.FieldStorage()

a, b, c = '', '', ''
if(form.getvalue("start") != None):
    a=form.getvalue("start")
    start=datetime.datetime.strptime(form.getvalue("start")+" 00:00:00",'%Y-%m-%d %H:%M:%S')
else:
    start = None
if(form.getvalue("end") != None):
    b=form.getvalue("end")
    end=datetime.datetime.strptime(form.getvalue("end")+" 23:55:00",'%Y-%m-%d %H:%M:%S')
else:
    end=None
if(form.getvalue("variable") !=None):
    c=form.getvalue("variable")
    val = dr.v[form.getvalue("variable")]
else:
    val=None

if(start != None and b!=None and c!=None):
    coue = """<p>
                """+str(a)+""", du: """+str(b)+""" au: """+str(c)+""":
                </p>
                <p class="heures_ok">
					<img src="images/courbe.png" width="35%" height="35%">
				</p>"""
else:
    coue=''

img=""
if(start!=None and end!=None and val!=None):
    #img = io.BytesIO()
    dr.plot_val(val, start, end, "images/courbe.png")
    img = """<img src="images/courbe.png" width="35%" height="35%">"""

    courbe = dr.get_values(val, start, end)

html = """
<!DOCTYPE html>

<html>
    <head>
        <meta charset="utf-8" />
        <style>
html
{
	background-color: #eaf7ff;
	font-family: Verdana, sansserif;
}

body
{
	background-color: #ababab;
	border-radius: 16px;
	padding: 32px;
	box-shadow: 0px 0px 6px gray;
}

header h1
{
	text-align: center;
	font-size: 42px;
	color: white;
    text-shadow: 0px 0px 4px #eaf7ff;
}

nav
{
	border-radius: 8px;
	background-color: #808080;
    box-shadow: 0px 0px 6px gray;
}

li
{
	display: inline-block;
}

ul
{
    list-style-type: none;
	text-align: center;
}

li a
{
    color: #eaf7ff;
	text-shadow: 0px 0px 2px white;
	font-size: 32px;
	text-decoration: none;
	padding-right: 48px;
	padding-left: 48px;
}

li a:hover {
    background-color: #666;
}

p.heures_ok
{
	font-size: 64px;
	color: #ffffff;
	text-shadow: 0px 0px 2px #cdff92;
	text-align: center;
	font-weight: bold;
}

p.detail
{
	font-style: italic;
	color: #3a5c85;
	text-decoration: italic;
	text-align: center;
}
aside
{
	text-align: center;
}

li.image_elec_vert
{
	text-align: center;
	text-shadow: 0px 0px 4px #c7ff85;
	color: #c7ff85;
	font-size: 32px;
	margin-right: 28px;
	margin-left: 28px;
	
}
    
li.image_elec_orange
{
	text-align: center;
	text-shadow: 0px 0px 4px #ffd585;
	color: #ffd585;
	font-size: 32px;
	margin-right: 28px;
	margin-left: 28px;
	
}
    
li.image_elec_rouge
{
	text-align: center;
	text-shadow: 0px 0px 4px #ff9696;
	color: #ff9696;
	font-size: 32px;
	margin-right: 28px;
	margin-left: 28px;
	
}

li.image_eau_chaude_vert
{
	text-align: center;
	text-shadow: 0px 0px 4px #c7ff85;
	color: #c7ff85;
	font-size: 32px;
	margin-right: 28px;
	margin-left: 28px;
}
    
li.image_eau_chaude_orange
{
	text-align: center;
	text-shadow: 0px 0px 4px #ffd585;
	color: #ffd585;
	font-size: 32px;
	margin-right: 28px;
	margin-left: 28px;
}
    
li.image_eau_chaude_rouge
{
	text-align: center;
	text-shadow: 0px 0px 4px #ff9696;
	color: #ff9696;
	font-size: 32px;
	margin-right: 28px;
	margin-left: 28px;
}

li.image_chauffage_vert
{
	text-align: center;
	text-shadow: 0px 0px 4px #c7ff85;
	color: #c7ff85;
	font-size: 32px;
	margin-right: 28px;
	margin-left: 28px;
}
    
li.image_chauffage_orange
{
	text-align: center;
	text-shadow: 0px 0px 4px #ffd585;
	color: #ffd585;
	font-size: 32px;
	margin-right: 28px;
	margin-left: 28px;
}
    
li.image_chauffage_rouge
{
	text-align: center;
	text-shadow: 0px 0px 4px #ff9696;
	color: #ff9696;
	font-size: 32px;
	margin-right: 28px;
	margin-left: 28px;
}

section h1
{
	color: #5c5c5c;
	text-decoration: underline;
	font-size: 32px;
}
        </style>
        <title>Detail consomation</title>
    </head>


    <body>
		
        <nav>
            <ul>
                <li><a href="loading.py">Energy</a></li>
                <li><a href="index.py">Autonomy</a></li>
				<li><a href="graph.py">Charts</a></li>
				<li><a href="graph.py"><img src="images/refresh.png"></a></li>
            </ul>
        </nav>

		<header>
            <h1>Historical charts</h1>
        </header>

        <section>
            <aside>
            <form action="/graph.py" method="post">
                <p class="detail">
					Date de debut:
					<input type="date" name="start"/>
					Date de fin:
					<input type="date" name="end"/>
				
					<label for="variable">Variable a afficher:</label>
					<select name="variable" id="variable">
						<option value="T salon">T salon</option>
						<option value="T chambre 1">T chambre 1</option>
                    <option value="T chambre 2">T chambre 2</option>
                    <option value="T chambre 3">T chambre 3</option>
                    <option value="T chambre combles">T chambre combles</option>
                    <option value="T dehors">T dehors</option>
                    <option value="T ballon 1">T ballon 1</option>
                    <option value="T ballon 2">T ballon 2</option>
                    
                    <option value="Debit chauffage central">Debit chauffage central</option>
                    <option value="T in chauffage central">T in chauffage central</option>
                    <option value="T out chauffage central">T out chauffage central</option>
                    
                    <option value="Debit chauffe eau">Debit chauffage central</option>
                    <option value="T in chauffe eau">T in chauffe eau</option>
                    <option value="T out chauffe eau">T out chauffe eau</option>
                    
                    <option value="Debit fourneau">Debit fourneau</option>
                    <option value="T in fourneau">T in fourneau</option>
                    <option value="T out fourneau">T out fourneau</option>
                    
                    <option value="Debit ECS">Debit ECS</option>
                    <option value="T in ECS">T in ECS</option>
                    <option value="T out ECS">T out ECS</option>
                    
                    <option value="Stock batteries">Stock batteries</option>
                    <option value="Entrees elec">Entrees elec</option>
                    <option value="Sorties elec">Sorties elec</option>
                    <option value="Tension panneaux">Tension panneaux</option>
					</select>
            <input type="submit" name="Graph" value="Go !">
            </p>
            </form>
            </aside>
            <article>
                """+coue+"""
            </article>
        </section>

        

    </body>

</html>
"""
#<img src="images/graph_ex.png" width="35%" height="35%">
print(html)