from flask import Flask, render_template,request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from models import db, Users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)

with app.app_context():
  db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
  if request.method == "POST":
    login = request.form.get('login')
    password = request.form.get('password')
    user = Users(login=login, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login'))
  return render_template('register.html')
 
@app.route("/login/", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    login_name = request.form.get('login')
    password = request.form.get('password')
    user = db.session.scalar(db.select(Users).where(Users.login == login_name))
    if user and check_password_hash(user.password, password):
      login_user(user)
      return redirect(url_for('index'))
    return redirect(url_for('home'))
  return render_template('login.html')

@app.route('/logout/')
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
  cards = [
        {'id': 1, 'title': 'День 1', 'subtitle': 'Проба пера'},
        {'id': 2, 'title': 'День 2', 'subtitle': 'Финал'},
    ]
  return render_template('index.html', cards=cards)

@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/card/<int:id>')
@login_required
def card(id):
  return render_template('card.html', id=id)

@app.route('/create')
@login_required
def create():
  return render_template('create.html')

@app.route('/form_create', methods=['GET','POST'])
@login_required
def form_create():
  return redirect(url_for('index'))

if __name__ == "__main__":
    app.secret_key = 'lol'
    app.run(debug=True)