#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User SignUp</title>
</head>
<body>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

# create a function for writing the user signup form
def write_form(username="", username_error="", password_error="", verify_error="", email="", email_error=""):
    user_signup_form = """
    <h1>User SignUp</h1>
    <form action="/" method="post">
        <table>
            <tr>
                <td><label for="username">Username:</label></td>
                <td>
                    <input type="text" name="username" value="{0}">
                    <span class="error">{1}</span>
                </td>
            </tr>
            <tr>
                <td><label for="password">Password:</label></td>
                <td>
                    <input type="password" name="password">
                    <span class="error">{2}</span>
                </td>
            </tr>
            <tr>
                <td><label for="verify">Verify Password:</label></td>
                <td>
                    <input type="password" name="verify">
                    <span class="error">{3}</span>
                </td>
            </tr>
            <tr>
                <td><label for="email">Email (optional):</label></td>
                <td>
                    <input type="email" name="email" value="{4}">
                    <span class="error">{5}</span>
                </td>
            </tr>
        </table>
        <input type="submit">
    </form>
    """.format(username, username_error, password_error, verify_error, email, email_error)

    content = page_header + user_signup_form + page_footer
    return content

class MainHandler(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.usersignup.com/
    """
    def get(self):
        self.response.write(write_form(username="", username_error="", password_error="", verify_error="", email="", email_error=""))

    def post(self):
        # reach into the request to get user input
        username = cgi.escape(self.request.get("username"))
        password = cgi.escape(self.request.get("password"))
        verify = cgi.escape(self.request.get("verify"))
        email = cgi.escape(self.request.get("email"))

        # create regular expressions to test validity of input
        username_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        password_re = re.compile(r"^.{3,20}$")
        email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")

        # set error messages to empty to start with, populate below with message if input invalid
        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""

        # if all input is valid, direct to welcome page.  If not, rewrite form with error message(s)
        have_error = False
        if not username_re.match(username):
            username = ""
            username_error = "Please enter a valid username."
            have_error = True
        if not password_re.match(password):
            password_error = "Please enter a valid password."
            have_error = True
        if not password == verify:
            verify_error = "Your password entries don't match. Please try again."
            have_error = True
        if email:
            if not email_re.match(email):
                email = ""
                email_error = "Please enter a valid email address."
                have_error = True
        if have_error:
            self.response.write(write_form(username, username_error, password_error, verify_error, email, email_error))
        else:
            self.redirect("/welcome?username=" + username)

class WelcomeHandler(webapp2.RequestHandler):
    """ Handles requests coming in to '/welcome'
    e.g. www.usersignup.com/welcome
    """
    def get(self):
        username = (self.request.get("username"))
        welcome_message = "<h1> Welcome, " + username + "!</h1>"
        content = page_header + "<p>" + welcome_message + "</p>" + page_footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
