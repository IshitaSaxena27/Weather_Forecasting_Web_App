from flask import Flask, render_template, request, redirect, url_for, session
from loginscript import login
from registration import emailCheck, register
from activate import checkToken, activateAccount

# Set up Flask server
app = Flask(__name__)
app.secret_key = b'\xd8\x95\x814Ij\x014S\xc6r\xbaC\x1e>N\xa0\x16d:\x8dp_\xf1'

# Serve the index page (Home page)
@app.route('/')
def index():
    if 'login' in session:  # Check if user is logged in
        return render_template("index2.html", logged_in=True)
    return render_template("index2.html", logged_in=False)

# Serve the about page (Optional)
# @app.route('/about')
# def about():
#     return render_template("about.html")


# Serve the login page
@app.route('/login')
def login_page():
    return render_template("login.html")


# Handle login form submission and verification
@app.route('/verify-login', methods=["POST"])
def verify_login():
    email = request.form.get("email")
    password = request.form.get("password")

    # Verify the username and hashed password
    myMessage, loggedIn = login(email, password)
    
    if loggedIn:
        session['login'] = True  # Set session flag for login
        session['email'] = email  # Set session email for user
        return redirect(url_for('index'))  # Redirect to the home page
    
    else:
        # If verification fails, reload the login page with an error message
        return render_template("login.html", message=myMessage)


# Serve the register page
@app.route('/signup')
def register_page():
    return render_template("register.html")


# Handle registration form submission and verification
@app.route('/verify-register', methods=["POST"])
def verify_register():
    email = request.form.get("email")
    password = request.form.get("password")
    confPassword = request.form.get("confirm_password")

    # Verify email and register
    text, emailVerification = emailCheck(email)
    if emailVerification:
        if password == confPassword:
            text, verifyRegister = register(email, password)
            if verifyRegister:
                return render_template("activate.html", message="Activate your account, Check your email.")
            else:
                return render_template("signup.html", message=text)
        else:
            return render_template("signup.html", message="Passwords do not match.")
    else:
        return render_template("signup.html", message=text)


# Serve the activation page
@app.route('/activate', methods=["GET"])
def activate():
    token = request.args.get("token")
    # Check Token
    text, verifyToken = checkToken(token)
    if verifyToken:
        text, verifyActivation = activateAccount(token)
        return render_template("activate.html", message=text)
    else:
        return render_template("activate.html", message=text)


# Handle weather search page only for logged-in users
@app.route('/weather')
def weather_page():
    if 'login' in session:
        return render_template('index.html')  # Add the weather search template here
    return redirect(url_for('login_page'))  # Redirect to login if not logged in




# Handle logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
