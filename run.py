from flask import Flask, render_template, request, redirect, url_for
from forms import SignupForm, PostForm, LoginForm
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from models import users, get_user, User
from urllib.parse import urlparse
# DEPRECATED
#from werkzeug.urls import url_parse

app = Flask(__name__)

app.config['SECRET_KEY']='7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'


# CREAM OBJECT login_manager DE LA CLASSE LoginManager
login_manager = LoginManager(app)

# SI UN USUARI NO AUTENTICAT VOL ACCEDIR A UNA VISTA PROTEGIDA
# EL REDIRECCIONAM A FER LOGIN
login_manager.login_view="login"


# VARIABLE POSTS
posts = []

@app.route('/')
def index():
   return render_template("index.html", num_posts=len(posts), posts=posts, num_users=len(users), users=users)

@app.route("/p/<string:slug>/")
def show_post(slug):
   return render_template("post_view.html", slug_title=slug)

@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
# NOMES ELS ADMINISTRADORS PODEN CREAR ENTRADES EN EL BLOG
@login_required
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

   # Comprovam si l'usuari actual ha fet login (autenticat)
   # Si esta autenticat, no cal tornar a fer login, per la qual cosa
   # el redirigim a index
   if current_user.is_authenticated:
      return redirect(url_for('index'))

   # Instanciam CLASSE SignupForm
   form = SignupForm()

   # COMPROVAM SI EL FORMULARI S'HA ENVIAT AMB DADES
   if form.validate_on_submit():
      name=form.name.data
      email=form.email.data
      password=form.password.data

      # Cream usuari i el desam
      id = len(users)+1
      print("ID: ")
      print(id)
      user = User (id, name, email, password)
      users.append(user)

      # L'usuari passa a estar autenticat
      login_user(user, remember=True)

      # El parametre next el rebrem quan l'usuari vol accedir a una pàgina 
      # protegida, però encara no estava autenticat
      next_page=request.args.get('next', None)
      if not next_page or urlparse(next_page).netloc != '':
         next_page=url_for('index')
      return redirect(next_page)
   
   # RETORNAM FORMULARI BUIT
   return render_template("signup_form.html", form=form)


# CALLBACK login_manager
# Agafam com a parametre un string amb el ID de l'usuari que ha iniciat sessió
# Retorna el correponent objecte User o None si l'ID no és correcte
@login_manager.user_loader
def load_user(user_id):
   for user in users:
      if user.id == int(user_id):
         return user
   return None

@app.route('/login/', methods=['GET', 'POST'])
def login():

   # Comprovam si l'usuari actual ha fet login (autenticat)
   # Si esta autenticat, no cal tornar a fer login, per la qual cosa
   # el redirigim a index
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   
   # Cream objecte form de la classe LoginForm
   form=LoginForm()
   # COMPROVAM SI EL FORMULARI S'HA ENVIAT AMB DADES
   if form.validate_on_submit():
      # Comprovam si les dades de l'usuari que es vol autenticar son vàlides
      # Intentam recuperar l'usuari a partir del seu email 
      # mitjançant la funció get_user() definida en models.py
      user=get_user(form.email.data)    
      #print(user)
      # Si existeix un usuari amb aquest email i el password coincideix
      # procedim a autenticar l'usuari amb el metode login_user() de Flask-Login
      if user is not None and user.check_password(form.password.data):
         login_user(user, remember=form.remember_me.data)
         # El parametre next el rebrem quan l'usuari vol accedir a una pàgina 
         # protegida, però encara no estava autenticat
         next_page=request.args.get('next')
         if not next_page or urlparse(next_page).netloc != '':
            next_page=url_for('index')
         return redirect(next_page)
   return render_template('login_form.html', form=form)


# LOGOUT
@app.route('/logout/')
def logout():
   logout_user()
   return redirect(url_for('index'))
