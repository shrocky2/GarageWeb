from flask import Flask, render_template, url_for, redirect, Response, request, session
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import InputRequired, ValidationError
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

from data import USERS
from garageFunctions import checkGaragePassword, checkGarageStatus, triggerGarage, garageCamera

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERSAFESECRETKEY-- Change me'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"


class LoginForm(FlaskForm):
    password = PasswordField(validators=[InputRequired()],
                              render_kw={"placeholder" : "password"})
    submit = SubmitField("Login")

class TriggerForm(FlaskForm):
    trigger = SubmitField("Trigger Garage")
    
USER_ID = "1221"

@login_manager.user_loader
def load_user(user_id=USER_ID):
    return USERS.get(str(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        if checkGaragePassword(form.password.data):
            login_user(USERS.get(str(USER_ID)))
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid Credentials'
        
    return render_template('login.html', form=form, error=error)

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    
    if request.method == 'POST':
        if request.form['trigger'] == 'Trigger Garage':
            triggerGarage()
            print("garage triggered") 
    status = checkGarageStatus()
    return render_template('dashboard.html', status=status)


@app.route('/garagecamera', methods=['GET','POST'])
@login_required
def garagecamera():
    return render_template('garageCamera.html')

@app.route('/camera', methods=['GET','POST'])
@login_required
def camera():
    return Response(garageCamera(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/triggerremotegarage', methods=['GET','POST'])
@login_required
def triggerremotegarage():
    triggerGarage()
    return redirect(url_for('dashboard'))

@app.route('/log')
def logfile():
    return app.send_static_file('log.txt')

@app.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)