from flask import Flask, render_template, request, redirect, url_for
from forms import SignupForm, PostForm

app = Flask(__name__)

app.config['SECRET_KEY']='7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

# VARIABLE POSTS
posts = []

@app.route('/')
def index():
   return render_template("index.html", num_posts=len(posts), posts=posts)

@app.route("/p/<string:slug>/")
def show_post(slug):
   return render_template("post_view.html", slug_title=slug)

@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
def post_form(post_id):
   # Instanciam CLASSE PostForm
   form = PostForm()
   # COMPROVAM SI EL FORMULARI S'HA ENVIAT AMB DADES
   if form.validate_on_submit():
      title=form.title.data
      title_slug=form.title_slug.data
      content=form.content.data
      # CREAM VARIABLE AMB CONTINGUT
      post={'title': title, 'title_slug': title_slug, 'content': content}
      # AFEGIM DADES A ARRAY posts
      posts.append(post)
      return redirect(url_for('index'))
   # RETORNAM FORMULARI BUIT
   return render_template("admin/post_form.html", form=form)

@app.route('/signup/', methods=["GET","POST"])
def show_signup_form():
   # Instanciam CLASSE SignupForm
   form = SignupForm()
   # COMPROVAM SI EL FORMULARI S'HA ENVIAT AMB DADES
   if form.validate_on_submit():
      name=form.name.data
      email=form.email.data
      password=form.password.data
      next = request.args.get('next',None)
      if next:
         return redirect(next)
      return redirect(url_for('index'))
   # RETORNAM FORMULARI BUIT
   return render_template("signup_form.html", form=form)