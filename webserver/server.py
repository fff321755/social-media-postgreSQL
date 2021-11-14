
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python3 server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@34.74.246.148/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@34.74.246.148/proj1part2"
#
DATABASEURI = "postgresql://kw2963:3493@34.74.246.148/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")
User_id = []

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: https://flask.palletsprojects.com/en/2.0.x/quickstart/?highlight=routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
# @app.route('/')
# def index():
#   """
#   request is a special object that Flask provides to access web request information:

#   request.method:   "GET" or "POST"
#   request.form:     if the browser submitted a form, this contains the data in the form
#   request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

#   See its API: https://flask.palletsprojects.com/en/2.0.x/api/?highlight=incoming%20request%20data

#   """

#   # DEBUG: this is debugging code to see what request looks like
#   print(request.args)


#   #
#   # example of a database query
#   #
#   cursor = g.conn.execute("SELECT name, id FROM test")
#   data = []
#   for result in cursor:
#     data.append((result['name'],result['id']))  # can also be accessed using result[0]  
#   cursor.close()

#   #
#   # Flask uses Jinja templates, which is an extension to HTML where you can
#   # pass data to a template and dynamically generate HTML based on the data
#   # (you can think of it as simple PHP)
#   # documentation: https://realpython.com/primer-on-jinja-templating/
#   #
#   # You can see an example template in templates/index.html
#   #
#   # context are the variables that are passed to the template.
#   # for example, "data" key in the context variable defined below will be 
#   # accessible as a variable in index.html:
#   #
#   #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
#   #     <div>{{data}}</div>
#   #     
#   #     # creates a <div> tag for each element in data
#   #     # will print: 
#   #     #
#   #     #   <div>grace hopper</div>
#   #     #   <div>alan turing</div>
#   #     #   <div>ada lovelace</div>
#   #     #
#   #     {% for n in data %}
#   #     <div>{{n}}</div>
#   #     {% endfor %}
#   #
#   context = dict(data = data)


#   #
#   # render_template looks in the templates/ folder for files.
#   # for example, the below file reads template/index.html
#   #
#   return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#

@app.route('/')
def index():
  return render_template("login.html")

@app.route('/test/<myid>')
def test(myid):
  cursor = g.conn.execute("SELECT name FROM test where id={%s}", myid)
  names = []
  for result in cursor:
    names.apppend(result['name'])
  cursor.close()

  if len(names) == 0:
    pass
  else :
    pass

  return redirect('/')

@app.route('/main')
def main():
  User_name = []
  User_mood = []
  User_active = []
  cursor = g.conn.execute("SELECT name, present_mood, is_active FROM Users WHERE uid=%s", User_id[0])
  for result in cursor:
    User_name.append(result['name'])
    User_mood.append(result['present_mood'])
    User_active.append(result['is_active'])
  cursor.close()
  # group_post = g.conn.execute("SELECT FROM Group_posts")
  # #group_in = g.conn.execute("SELECT FROM User_in_group WHERE")
  # group_gen = g.conn.execute("SELECT group_name FROM Groups")
  # follow = g.conn.execute("SELECT uid_followed FROM follow WHERE uid_following = U.uid")
  
  context = dict(name=User_name[0], mood=User_mood[0], active= User_active[0])

  return render_template("mainpage.html", **context)

#from main pages
@app.route('/profile_page')
def profile_page():
  User_profile = []
  cursor = g.conn.execute("""SELECT * FROM Users WHERE uid = %s""", User_id[0])
  for result in cursor:
    User_profile.append((result["name"], result["email"], result["present_mood"]))
  cursor.close()
  Posts = []
  cursor =g.conn.execute("""SELECT D.time, M.longitude, M.latitude, M.mood 
                          FROM Dep_posts D, Personal_mood M WHERE D.uid = %s AND 
                          D.uid=M.uid AND D.post_no=M.post_no""", User_id[0])
  for result in cursor:
    Posts.append((result["time"],result["longitude"],result["latitude"],result["mood"]))
  cursor.close()

  context = dict(profile=User_profile, posts=Posts)

  return render_template('profile_page.html', **context)

@app.route('/glist_page')
def glist_page():
  group_list = []
  cursor = g.conn.execute("""SELECT G.group_name FROM User_in_group Uig, Groups G 
               WHERE Uig.group_id = G.group_id AND Uig.uid = %s""", User_id[0])
  for result in cursor:
    group_list.append(result['group_name'])
  cursor.close()

  context = dict(group_list = group_list)

  return render_template('glist_page.html', **context)

@app.route('/follow_page')
def follow_page():
  following = []
  active = []
  cursor = g.conn.execute("""SELECT U.name, U.is_active FROM Follow F, Users U  
      WHERE F.uid_followed = U.uid AND F.uid_following = %s""", User_id[0])

  for result in cursor:
    following.append((result['name'],result['is_active']))
  cursor.close()

  context = dict(following = following)

  return render_template('follow_page.html', **context)

@app.route('/posting_page')
def posting_page():
  return render_template('posting_page.html')
  
@app.route('/post_page')
def post_page():
  return render_template('post_page.html')




# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')

#login function
@app.route('/login', methods=['POST'])
def login():
  global User_id
  User_id = []
  email = request.form['email']
  #password = request.form('password')
  cursor = g.conn.execute('SELECT U.uid FROM Users U WHERE U.email=%s', email)
  ls = []
  for result in cursor:
    ls.append(result['uid'])
    User_id.append(result['uid'])
  cursor.close()

  #change activeness of user after login
  cursor2 = g.conn.execute("UPDATE Users SET is_active = %s WHERE uid=%s", (True, User_id[0]))
  cursor2.close()

  if len(ls) != 0:
    return redirect('/main') 
  else :
    return redirect('/')

#main page to other pages functions 
@app.route('/see_profile', methods=['GET'])
def see_profile():
  return redirect('/profile_page')

@app.route('/see_glist', methods=['GET'])
def see_glist():
  return redirect('/glist_page')

@app.route('/see_follows', methods=['GET'])
def see_follows():
  return redirect('/follow_page')

@app.route('/posting', methods=['GET'])
def posting():
  return redirect('/posting_page')
  
@app.route('/see_posts', methods=['GET'])
def see_posts():
  return redirect('/post_page')
    
# @app.route('/main')
# def main():
  


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python3 server.py

    Show the help text using:

        python3 server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
