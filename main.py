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
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:OTcbo7X64K8dXrte@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'VWhwTnBcANvmSTLJ'


class Entry(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(1000))
    created = db.Column(db.DateTime)

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
        return render_template('single_entry.html', title="Grievance Entry", entry=entry)

    sort = request.args.get('sort')
    if (sort=="newest"):
        all_entries = Entry.query.order_by(Entry.created.desc()).all()
    else:
        all_entries = Entry.query.all()   
    return render_template('all_entries.html', title="All Grievances", all_entries=all_entries)


@app.route('/newpost', methods=['GET', 'POST'])
def new_entry():
    
    if request.method == 'POST':
        new_entry_title = request.form['title']
        new_entry_body = request.form['body']
        new_entry = Entry(new_entry_title, new_entry_body)

        if new_entry.is_valid():
            db.session.add(new_entry)
            db.session.commit()

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