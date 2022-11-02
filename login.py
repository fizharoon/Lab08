from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login import current_user, login_user


app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('loginpage.html')

 #, methods=['POST']
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index.html'))
#     user = User.query.filter_by(username=request.json['username']).first()
#     if user is None or not user.check_password(request.json['password']):
#         return redirect(url_for('loginpage.html'))
#
#     login_user(user)
#     return redirect(url_for('index.html'))

if __name__ == '__main__':
    app.run(debug=True)
