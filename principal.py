import cgi
import cgitb; cgitb.enable()
import calculator as calc

form = cgi.FieldStorage()

t_elec, t_elec_s = str(calc.t_elec()), str(calc.t_elec(survie=True))
t_thermique, t_thermique_s = str(calc.t_thermique()), str(calc.t_thermique(survie=True))

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
				<li><a href="loading.py"><img src="images/refresh.png"></a></li>
            </ul>
        </nav>
        
        <header>
            <h1>Energy storage status</h1>
        </header>

        <section>
            <aside>
                <h1>At current comfort level:</h1>
                <p class="heures_ok">%s</p>
				<p class="detail"> T-electrique = %s T-thermique=%s heurs</p>
            </aside>
            <article>                
                <h1>In survival mode:</h1>
                <p class="heures_ok">%s</p>
            </article>
        </section>

        

    </body>

</html>
"""%(t_elec, t_elec, t_thermique, t_elec_s)

print(html)