from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import DecimalField, RadioField, SelectField, TextAreaField, FileField
from wtforms.validators import InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import SubmitField
import datetime
import os


app = Flask(__name__)
app.secret_key = 'SecterKeyforhack'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

manager = LoginManager(app)

app.app_context().push()

class UploadForm(FlaskForm):
    photo = FileField('Выберите фото', validators=[
        FileRequired(),  # Файл обязателен
        FileAllowed(['jpg', 'png'], 'Только изображения!')  # Разрешенные форматы
    ])
    submit = SubmitField('Загрузить')

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False, default=False)
    admin = db.Column(db.Boolean(), nullable=False, default=False)
    avatar = db.Column(db.String(400), default="")
    routes_id = db.Column(db.ForeignKey("routes.id"))
    id_routes_traveled = db.Column(db.ForeignKey("routes.id"))
    comments_id = db.Column(db.ForeignKey("comments.id"))
    description = db.Column(db.Text, default="")


class Routes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    objects_id = db.Column(db.ForeignKey("objects.id"))
    author_id = db.Column(db.ForeignKey("users.id"))
    comments_id = db.Column(db.ForeignKey("comments.id"))
    photo_id = db.Column(db.ForeignKey("photo.id"))


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.ForeignKey("users.id"))
    photo_id = db.Column(db.ForeignKey("photo.id"))
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date)
    description = db.Column(db.Text, default="")
    routes_id = db.Column(db.ForeignKey("routes.id"))
    parent = db.Column(db.ForeignKey("comments.id"))


class Objects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), default="")
    coordinates = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(350), default="")


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    objects_id = db.Column(db.ForeignKey("objects.id"))
    comments_id = db.Column(db.ForeignKey("comments.id"))

db.create_all()

@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.route("/out_akk")
def logout():
    logout_user()
    return redirect('general')

@app.route('/')
@app.route('/general')
def general():
        src_img_pm = url_for('static',filename='img/img_map.png')
        src_img_profile = url_for('static',filename='img/img_profile.png')
        src_img_search = url_for('static', filename='img/img_search.png')
        src_img_login = url_for('static', filename='img/img_login.png')
        src_img_add_form = url_for('static', filename='img/img_add_map.png')
        return render_template('gen.html', m = 10, src_img_pm=src_img_pm, src_img_profile=src_img_profile, src_img_search=src_img_search, src_img_login=src_img_login, src_img_add_form=src_img_add_form)


@app.route('/login', methods=['GET','POST'])
def login():
    list = request.args.get("list", type=str)
    if current_user.is_authenticated:
        return redirect(url_for('general'))
    else:
        login = ""
        password = ""
        if request.method == 'POST':
                login = request.form.get('login')
                password = request.form.get('password')
                print(login, password)
                if login and password:
                    try:
                        user = Users.query.filter_by(login=login).first()
                        if check_password_hash(user.password, password):
                            login_user(user)

                            return redirect(url_for('general'))
                        else:


                            password = ''
                    except:

                        login = ''
                        password = ''


        print(login, password)
        return render_template('login.html', b=1)

@app.route('/reg', methods=['GET','POST'])
def reg():
    if current_user.is_authenticated:
        return redirect(url_for('general'))
    else:
        login = ""
        first_name = ""
        last_name = ""
        password = ""
        password2 = ""
        if request.method == 'POST':
                login = request.form.get('login')
                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                password = request.form.get('password')
                password2 = request.form.get('password2')


                user = Users.query.filter_by(login=login).first()

                #login = ''

                if password == password2:
                    print('password ok')
                    password = generate_password_hash(password)
                    user = Users(login = login, password = password, first_name=first_name, last_name = last_name, admin = 0)
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    return redirect(url_for('general'))
                else:

                    password = ''
                    password2 = ''

        print(login, password, first_name, last_name)
        return render_template('login.html', b=2)

@app.route("/profile")
def profile():
    l = 12334
    add_m = 25
    src_img_back = url_for('static', filename='img/img_back.png')
    return render_template("profile.html", d="a "*184, m=100, add_m=add_m,l=l,src_img_back=src_img_back)

@app.route('/ui', methods=['GET', 'POST'])
def marsh():
    print(request)
    list = request.args.get('list', type=str, default="0")
    names_obj = request.args.get('names_obj', type=str, default="0")
    print(list,'\n',names_obj)
    form = UploadForm()
    photos = request.files.getlist('photos[]')  # Получаем массив файлов
    for photo in photos:
        print(photo.filename)
        if photo.filename:  # Проверяем, что файл был загружен
            photo.save(f"uploads/{photo.filename}")
    return render_template('ui.html', list=list, names_obj=names_obj, form=form)

@app.route('/show_map')
def show_map():
    return render_template('show_map.html', g=10)

@app.route('/upl', methods=['GET', 'POST'])
@app.route('/upload', methods=['POST'])
def upload():
    form = UploadForm()
    photos = request.files.getlist('photos[]')  # Получаем массив файлов
    for photo in photos:
        if photo.filename:  # Проверяем, что файл был загружен
            photo.save(f"uploads/{photo.filename}")
    if request.method == 'POST':
        login = request.form.get('login')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        password2 = request.form.get('password2')
    return render_template('phhoto.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)