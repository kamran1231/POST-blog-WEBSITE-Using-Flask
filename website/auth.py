
from flask import Blueprint,url_for
from flask import render_template,request,flash,redirect
from .models import User
from . import db



from flask_login import login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash
auth = Blueprint('auth',__name__)




@auth.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # user_save = {
        #     'first_name':first_name,
        #     'last_name':last_name,
        #     'username':username,
        #     'email':email,
        #
        # }
        # print(first_name,last_name,username,email,password)
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email Already Exist',category='error')
        elif len(first_name) < 3:
            flash('First name must be more than 3 character',category='error')
        elif len(last_name) < 3:
            flash('Last name must be more than 3 character',category='error')
        elif len(username) < 4:
            flash('Username must be more than 4 character',category='error')
        elif len(password) < 5:
            flash('Password must be more than 5 character',category='error')
        elif len(email) < 5:
            flash('email must be more than 5 character',category='error')

        else:
            user = User(first_name=first_name,
                        last_name=last_name,
                        username=username,
                        email=email,
                        password=generate_password_hash(password,method='sha256'))

            db.session.add(user)
            db.session.commit()
            flash('Account Created!!', category='success')
            return redirect('/login')

    return render_template('register.html')


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in Successfully',category='success')
                login_user(user,remember=True)
                return redirect('/')
            else:
                flash('Incorrect Password, Try Again!',category='error')
        else:
            flash('Email does not exist',category='error')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout Successfully','success')
    return redirect('/login')


@auth.route('/profile/<int:id>',methods=['GET','POST'])
@login_required
def user_profile(id):
    user = User.query.get(id)
    return render_template('profile.html',user=user)

@auth.route('/edit_profile/<int:id>',methods=['GET','POST'])
@login_required
def edit_profile(id):
    # user = User.query.get(id)
    user_data = db.session.query(User).filter(User.id == id).first()
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        user_data.username = username
        user_data.first_name = first_name
        user_data.last_name = last_name
        db.session.commit()
        flash('Updated Successfully', 'success')
        return redirect('/')
    else:


        return render_template('edit_profile.html',user_data=user_data)


