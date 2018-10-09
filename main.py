'''Make sure you can say the following about your app:

The /blog route displays all the blog posts.

You're able to submit a new post at the /newpost route. After submitting a new post, your app displays the 
main blog page.

You have two templates, one each for the /blog (main blog listings) and /newpost (post new blog entry) views. 
Your templates should extend a base.html template which includes some boilerplate HTML that will be used on 
each page.

In your base.html template, you have some navigation links that link to the main blog page and to the add new 
blog page. If either the blog title or blog body is left empty in the new post form, the form is rendered again, 
with a helpful error message and any previously-entered content in the same form inputs.


Use Case 1: We click on a blog entry's title on the main page and go to a blog's individual entry page.
Use Case 2: After adding a new blog post, instead of going back to the main page, we go to that blog post's 
individual entry page.

Add a CSS stylesheet to improve the style of your app
Display the posts in order of most recent to the oldest (the opposite of the current order).'''


from flask import Flask, request, redirect, render_template, flash

from flask_sqlalchemy import SQLAlchemy
# ^^^ SQLAlchemy is a class that enables Python applications to "talk to" databases. It is able to work with 
# several SQL-based database engines.

from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:OTcbo7X64K8dXrte@localhost:8889/build-a-blog'
# ^^^ This line adds a new entry to the app.config dictionary, with key 'SQLALCHEMY_DATABASE_URI. The SQLAlchemy 
# module will use this string to connect to our MySQL database. This string is a regular source of database 
# connection problems. If any portion of it isn't exactly correct, our app won't be able to connect properly.

app.config['SQLALCHEMY_ECHO'] = True
# ^^^ Enabling this setting will turn on query logging. In other words, when our app does anything that results 
# in a database query being executed, the query that SQLAlchemy generates and executes will be logged to the 
# terminal that our app is running within.

db = SQLAlchemy(app)
# ^^^ Create a database connection and interface for our app. We'll use the db object throughout our app, 
# and it will allow us to interact with the database via our Flask/Python code.

app.secret_key = 'VWhwTnBcANvmSTLJ'


class Entry(db.Model):
    # ^^^ Creates a class that extends the db.Model class. By extending this class, we'll get a lot of 
    # functionality that will allow our class to be managed by SQLAlchemy, and thus stored in the database.
   
    id = db.Column(db.Integer, primary_key=True)
    # ^^^ Creates a new property of our class that will map to an integer column in the Entry table. 
    # The column name will be generated from the property name to be id as well. The column will be a 
    # primary key column on the table.

    title = db.Column(db.String(180))
    # ^^^ Creates a property that will map to a column of type String(180) in the Entry table.

    body = db.Column(db.String(1000))

    created = db.Column(db.DateTime)
    # ^^^ Creates a property completed that will map to a column of type BOOL, which is actually a TINYINT 
    # column with a constraint that it can only hold 0 or 1.

    def __init__(self, title, body ):
        self.title = title
        self.body = body
        self.created = datetime.utcnow()

    def is_valid(self):
       
        if self.title and self.body and self.created:
            return True
        else:
            return False


@app.route("/")
def index():
    
    return redirect("/blog")

@app.route("/blog")
def display_blog_entries():
   
    entry_id = request.args.get('id')
    if (entry_id):

        entry = Entry.query.get(entry_id)
        # ^^^ Calling query.get() will query for the specific object/row by it's primary key.

        return render_template('single_entry.html', title="Grievance Entry", entry=entry)

    sort = request.args.get('sort')
    if (sort=="newest"):

        all_entries = Entry.query.order_by(Entry.created.desc()).all()
        # ^^^ Every class that extends db.Model will have a query property attached to it. 
        # This query object contains lots of useful methods for querying the database for data 
        # from the associate table(s).

    else:
        all_entries = Entry.query.all()   
    return render_template('all_entries.html', title="All Grievances", all_entries=all_entries)


@app.route('/newpost', methods=['GET', 'POST'])
def new_entry():
    
    if request.method == 'POST':
        new_entry_title = request.form['title']
        new_entry_body = request.form['body']

        new_entry = Entry(new_entry_title, new_entry_body)
        # ^^^ To create an instance of our persistent Entry class, we use the same syntax as always.

        if new_entry.is_valid():

            db.session.add(new_entry)
            # ^^^ Our ORM system, SQLAlchemy, does not know about our new object until we notify it 
            # that we want our object to be stored in the database. This is done by calling db.session.add().

            db.session.commit()
            # ^^^ Our changes and additions to the database aren't actually run against the database 
            # until we commit the session.

            url = "/blog?id=" + str(new_entry.id)
            return redirect(url)
        else:
            flash("Woe is thee for your entry hath failed. A title and entry is required to voice your grievance")
            return render_template('new_entry_form.html',
                title="Create new blog entry",
                new_entry_title=new_entry_title,
                new_entry_body=new_entry_body)

    else: 
        return render_template('new_entry_form.html', title="Create New Grievance")

if __name__ == '__main__':
    app.run()
    # ^^^ We added this conditional to allow us to import objects and classes from code outside of this 
    # file in a way that doesn't run the application. In particular, we'll want to import db and Task 
    # within a Python shell.