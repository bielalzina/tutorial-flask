from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# CREAM CLASSE User LA QUAL HEREDA LES FUNCIONALITATS DE LA CLASSE UserMixin

class User(UserMixin):
    def __init__(self, id, name, email, password, is_admin=False):
        self.id=id
        self.name=name
        self.email =email
        self.password=generate_password_hash(password)
        self.is_admin=is_admin
    
    def set_password(self, password):
        self.password=generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.email)

# DEFINIM VARIABLE users ON DESAREM LES DADES DELS USUARIS 

users = []

# FAREM SERVIR AQUESTA FUNCIÓ PER CERCAR UN USUARI PEL SEU EMAIL DINS LA LLISTA users
def get_user(email):
    for user in users:
        if user.email == email:
            return user
    return None

    
