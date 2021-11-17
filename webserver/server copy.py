
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
from flask import Flask, request, render_template, g, redirect, Response, session
from flask_session import Session
from datetime import datetime, timezone

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
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

UID = 26

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

  #Check Login
  # if session['uid']:
  #   render_template("login.html")

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



# login.html ---------------------------------------------------------------------------------------------------------

@app.route('/')
def index():
  return render_template("login.html")

@app.route('/sign_in', methods=['GET'])
def sign_in():
  return redirect('/sign_in_page')

#login function
@app.route('/login', methods=['POST'])
def login():
  #global User_id
  #User_id = []
  email = request.form['email']
  password = request.form['password']
  cursor = g.conn.execute("SELECT U.uid FROM Users U WHERE U.email='{}' AND U.password='{}'".format(email, password))
  ls = []
  for result in cursor:
    ls.append(result['uid'])
    session['uid'] = result['uid']
  cursor.close()

  if not ls:
    return redirect('/')

  #change activeness of user after login
  cursor2 = g.conn.execute("UPDATE Users SET is_active = %s WHERE uid=%s", (True, session['uid']))
  cursor2.close()

  return redirect('/main') 


# sign_in_page.html ---------------------------------------------------------------------------------------------------------

@app.route('/create_account', methods=['POST'])
def creat_account():
  # name = request.form['name']
  # email = request.form['email']
  # ls = []
  # z g.conn.execute('SELECT email FROM Users WHERE email=%s', email)
  # for result in cursor:
  #   ls.append(result['email'])
  # cursor.close()
  # global UID
  # if len(ls)==0:
  #   UID = UID + 1
  #   g.conn.execute("INSERT INTO Users VALUES (%s,%s,NULL,%s,%s)",
  #                            (str(UID).zfill(10),name,email,False))
  #   return redirect('/')
  # else:
  #   return redirect('/sign_in_page')

  name = request.form['name']
  email = request.form['email']
  password = request.form['password']
  g.conn.execute("INSERT INTO Users VALUES (DEFAULT,'{}',NULL,'{}','{}', False)".format(name,email,password)) 

  #if failed
  # TODO

  return redirect('/')

# mainpage.html ---------------------------------------------------------------------------------------------------------
@app.route('/main')
def main():
  User_name = []
  User_mood = []
  User_active = []
  cursor = g.conn.execute("SELECT name, present_mood, is_active FROM Users WHERE uid=%s", session['uid'])
  for result in cursor:
    User_name.append(result['name'])
    User_mood.append(result['present_mood'])
    User_active.append(result['is_active'])
  cursor.close()

  #post from following users
  Posts = []
  cursor = g.conn.execute("SELECT uid, mood, post_no  FROM Personal_mood WHERE uid IN (SELECT uid_followed FROM Follow WHERE uid_following = %s)", session['uid'])
  for result in cursor:
    Posts.append((result["uid"],result["mood"], result["post_no"]))
  cursor.close()
  
  
  posts_with_count = []
  for post in Posts:
    q = "select mood, COUNT(*) from responses_to_post r where r.uid_post={} AND r.post_no={} group by r.mood".format(post[0],post[2])
    cursor = g.conn.execute(q)
    mood_count=[]
    for result in cursor:
      mood_count.append((result['mood'], result['count']))
    posts_with_count.append((post[0], post[1], post[2], mood_count))
    cursor.close()

  context = dict(name=User_name[0], mood=User_mood[0], active= User_active[0], posts=posts_with_count)

  return render_template("mainpage.html", **context)



# post.html ---------------------------------------------------------------------------------------------------------
@app.route('/post/<uid>/<post_no>', methods=['GET'])
def to_post(uid, post_no):
  Posts = []
  cursor = g.conn.execute("SELECT * FROM Dep_comments WHERE uid_post = %s AND post_no = %s", (uid, post_no))
  for result in cursor:
    Posts.append((result["uid_comment"],result["comment_no"], result["uid_comment"], result["text"]))
  cursor.close()
  context = dict(uid=uid, post_no=post_no, posts=Posts)

  return render_template("post.html", **context)

@app.route('/comment_under_posts/<uid>/<post_no>', methods=['POST'])
def comment_to_post(uid, post_no):
  text = request.form['text']
  q = "INSERT INTO Dep_comments VALUES (DEFAULT,{},{},{},'{}','{}')".format(session['uid'], uid, post_no, text, str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')))
  g.conn.execute(q)
  
  redirect('/post/{}/{}'.format(uid,post_no))



 

#from main pages
@app.route('/profile_page')
def profile_page():
  User_profile = []
  cursor = g.conn.execute("""SELECT * FROM Users WHERE uid = %s""", session['uid'])
  for result in cursor:
    User_profile.append((result["name"], result["email"], result["present_mood"]))
  cursor.close()
  Posts = []
  cursor =g.conn.execute("""SELECT D.time, M.longitude, M.latitude, M.mood 
                          FROM Dep_posts D, Personal_mood M WHERE D.uid = %s AND 
                          D.uid=M.uid AND D.post_no=M.post_no""", session['uid'])
  for result in cursor:
    Posts.append((result["time"],result["longitude"],result["latitude"],result["mood"]))
  cursor.close()

  context = dict(profile=User_profile, posts=Posts)

  return render_template('profile_page.html', **context)

@app.route('/glist_page')
def glist_page():
  group_list = []
  cursor = g.conn.execute("""SELECT G.group_name, G.group_id FROM User_in_group Uig, Groups G 
               WHERE Uig.group_id = G.group_id AND Uig.uid = %s""", session['uid'])
  for result in cursor:
    group_list.append((result['group_name'], result['group_id']))
  cursor.close()

  context = dict(group_list = group_list)

  return render_template('glist_page.html', **context)

#from group list page
@app.route('/group_page/<group_id>', methods=['GET'])
def group_page(group_id):
  
  Group_info = []
  cursor = g.conn.execute("""SELECT group_name, type FROM Groups 
                             WHERE group_id = %s""", group_id)
  
  for result in cursor:
    Group_info.append((result['group_name'],result['type']))
  cursor.close()

  Group_post = []
  cursor = g.conn.execute("""SELECT D.time, G.text, G.image_url
                              FROM Dep_posts D, Group_posts G
                              WHERE D.uid = G.uid AND D.post_no=G.post_no AND
                              G.group_id = %s""", group_id)
                             ## possibly ordered by time?

  for result in cursor:
    Group_post.append((result['time'],result['text'],result['image_url']))
  cursor.close()

  context = dict(group_info = Group_info, group_post = Group_post, gid = group_id)

  return render_template('group_page.html', **context)

@app.route('/group_posting_page/<group_id>', methods=['POST'])
def group_posting_page(group_id):
  context = dict(group_info = group_id)
  return render_template("group_posting_page.html", **context)

@app.route('/follow_page')
def follow_page():
  following = []
  active = []
  cursor = g.conn.execute("""SELECT U.name, U.uid ,U.is_active FROM Follow F, Users U  
      WHERE F.uid_followed = U.uid AND F.uid_following = %s""", session['uid'])

  for result in cursor:
    following.append((result['name'],result['uid'],result['is_active']))
  cursor.close()

  context = dict(following = following)

  return render_template('follow_page.html', **context)

@app.route('/posting_page')
def posting_page():
  return render_template('posting_page.html')
  
@app.route('/post_page')
def post_page():
  Personal_post = []
  cursor = g.conn.execute("""SELECT D.uid, P.mood, D.post_no, D.time FROM Personal_mood P, Dep_posts D
                             WHERE P.uid = D.uid AND P.post_no = D.post_no AND 
                             D.uid IN (SELECT uid_followed FROM Follow 
                             WHERE uid_following != %s)""", session['uid'])
  for result in cursor:
    Personal_post.append((result['uid'],result['mood'],result['post_no'],result['time']))
  cursor.close()
  
  Group_post = []
  cursor = g.conn.execute("""SELECT D.time, G.text, G.image_url
                              FROM Dep_posts D, Group_posts G
                              WHERE D.uid = G.uid AND D.post_no=G.post_no AND
                              G.group_id IN (SELECT group_id FROM User_in_group
                              WHERE uid != %s) """, session['uid'])
                             ## possibly ordered by time?
  for result in cursor:
    Group_post.append((result['time'],result['text'],result['image_url']))
  cursor.close()

  context = dict(personal_post=Personal_post, group_post=Group_post)

  return render_template('post_page.html', **context)

@app.route('/sign_in_page')
def sign_ing_page():
  return render_template('sign_in_page.html')

@app.route('/to_user_profile/<user_id>', methods=['POST'])
def to_user_profile(user_id):
    
  User_profile = []
  cursor = g.conn.execute("""SELECT * FROM Users WHERE uid = %s""", user_id)
  
  for result in cursor:
    User_profile.append((result["name"], result["email"], result["present_mood"]))
  cursor.close()
  Posts = []
  cursor =g.conn.execute("""SELECT D.time, M.longitude, M.latitude, M.mood 
                          FROM Dep_posts D, Personal_mood M WHERE D.uid = %s AND 
                          D.uid=M.uid AND D.post_no=M.post_no""", user_id)
  for result in cursor:
    Posts.append((result["time"],result["longitude"],result["latitude"],result["mood"]))
  cursor.close()

  context = dict(profile=User_profile, posts=Posts)

  return render_template('user_profile_page.html', **context)

# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')


@app.route('/create_personal_post', methods=['POST'])
def create_post():
  mood = request.form['mood']
  longitude = request.form['longitude']
  latitude = request.form['latitude']

  g.conn.execute("""INSERT INTO Dep_posts VALUES 
                    ((SELECT MAX(post_no) FROM Dep_posts WHERE uid=%s)+1,%s, %s)""",
                    (session['uid'],str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')),
                    session['uid']))
  
  g.conn.execute("""INSERT INTO Personal_mood VALUES
                    (%s,%s,%s,(SELECT MAX(post_no) FROM Dep_posts WHERE uid=%s),%s)""",
                    (longitude,latitude,session['uid'],session['uid'],mood))

  return redirect('/main')

@app.route('/create_group_post/<group_id>', methods=['POST'])
def create_group_post(group_id):
  text = request.form['text']
  image = request.form['image']

  g.conn.execute("""INSERT INTO Dep_posts VALUES 
                    ((SELECT MAX(post_no) FROM Dep_posts WHERE uid=%s)+1,%s, %s)""",
                    (session['uid'],str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')),
                    session['uid']))

  g.conn.execute("""INSERT INTO Group_posts VALUES
                    (%s,%s,(SELECT MAX(post_no) FROM Dep_posts WHERE uid=%s),%s,%s)""",
                    (session['uid'],group_id,session['uid'],text,image))

  return redirect('/group_page/'+group_id)


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
