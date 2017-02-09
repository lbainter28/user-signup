import re
import cgi

# create methods to determine valid inputs
def valid_username(username, username_re):
    username_error = ""
    if username_re.match(username):
        return True
    else:
        username_error += "Please enter a valid username."
        return cgi.escape(username_error)

def valid_password(password, password_re):
    password_error = ""
    if password_re.match(password):
        return True
    else:
        password_error += "Please enter a valid password."
        return cgi.escape(password_error)

def valid_verify(verify, password):
    verify_error = ""
    if verify == password:
        return True
    else:
        verify_error += "Your password entries don't match. Please try again."
        return cgi.escape(verify_error)

def valid_email(email, email_re):
    email_error = ""
    if email_re.match(email) or not email:
        return True
    else:
        email_error += "Please enter a valid email address."
        return cgi.escape(email_error)


        