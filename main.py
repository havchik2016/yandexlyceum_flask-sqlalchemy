from flask import Flask, render_template, redirect, make_response, jsonify
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_restful import Api
from data import db_session, jobs, users, jobs_api, users_resource
from wtforms.fields.html5 import EmailField
from wtforms import PasswordField, StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня', default=False)
    submit = SubmitField('Войти')


class JobForm(FlaskForm):
    job = StringField('Описание работы', validators=[DataRequired()])
    team_leader = IntegerField('ID командира', validators=[DataRequired()])
    work_size = IntegerField('Длительность работы в часах', validators=[DataRequired()])
    collaborators = StringField('Помощники', validators=[DataRequired()])
    is_finished = BooleanField('Завершена ли работа?', default=False)
    submit = SubmitField('Добавить')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


@app.route('/')
def start():
    session = db_session.create_session()
    tasks = session.query(jobs.Jobs).all()
    leaders = [session.query(users.User).filter(users.User.id == task.team_leader).all() for task in tasks]
    return render_template("main.html", title="Список работ", tasks=tasks, leaders=leaders)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               title='Вход',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Вход', form=form)


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = jobs.Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        session.add(job)
        session.commit()
        return redirect('/')
    return render_template('add_job.html', title='Добавить работу', form=form)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/mars.sqlite")
    app.register_blueprint(jobs_api.blueprint)
    api.add_resource(users_resource.UserListResource, '/api/v2/users')
    api.add_resource(users_resource.UserResource, '/api/v2/users/<int:user_id>')
    app.run()


if __name__ == '__main__':
    main()
