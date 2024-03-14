from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# VARIABLE POSTS
posts = []

@app.route('/')
def index():
   return render_template("index.html", num_posts=len(posts))

@app.route("/p/<string:slug>/")
def show_post(slug):
   return render_template("post_view.html", slug_title=slug)

@app.route("/admin/post/")
@app.route("/admin/post/<int:post_id>/")
def post_form(post_id=None):
   return render_template("admin/post_form.html", post_id=post_id)

@app.route('/signup/', methods=["GET","POST"])
def show_signup_form():
   if request.method=='POST':
      name = request.form['name']
      # print(name)
      email = request.form['email']
      # print(email)
      password = request.form['password']
      # print(password)
      next = request.args.get('next',None)
      # print(next)
      if next:
         return redirect(next)
      return redirect(url_for('index'))
   return render_template("signup_form.html")