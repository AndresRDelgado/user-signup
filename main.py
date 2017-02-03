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
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

form = """
<form method="post">
    <h2>Sign Up</h2>
    <label>What is your username?
        <input name="username" value="%(username)s">
    </label><div style="color:red">%(error_username)s</div>
    <br>
    <label>What is your password? 
        <input type="password" name="password" value="%(password)s">
    </label><div style="color:red">%(error_password)s</div>
    <br>
    <label>Re-type your password
        <input type="password" name="password2" value="%(password2)s">
    </label><div style="color:red">%(error_password2)s</div>
    <br>
    <label>What is your email address?
        <input name="email" value="%(email)s">
    </label><div style="color:red">%(error_email)s</div>
    <br>
    <input type="submit">
</form>
"""
def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PW_RE.match(password)

def matching_password(password, password2):
    return password == password2

def valid_email(email):
    return EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def write_form(self,error_email="", error_username="", error_password="", error_password2="", email="", username="", password="", password2=""):
        self.response.out.write(form % {"error_email":error_email,
                                        "error_username":error_username,
                                        "error_password":error_password,
                                        "error_password2":error_password2,
                                        "email": email,
                                        "username": username,
                                        "password": password,
                                        "password2": password2})
        
    def get(self):
        self.write_form()
    
    def post(self):
        email = (self.request.get("email"))
        username = (self.request.get("username"))
        password = (self.request.get("password"))
        password2 = (self.request.get("password"),self.request.get("password2")) 

        goodemail = valid_email(email)
        goodusername = valid_username(username)
        goodpassword = valid_password(password)
        goodpassword2 = matching_password(password,password2)

        error_email = "That's not a good email address!"
        error_username = "That's not a good username!"
        error_password = "That's not a good password!"
        error_password2 = "Your passwords don't match!"

        if not (goodemail or goodusername or goodpassword or goodpassword2):
            self.write_form(error_email, error_username, error_password, error_password2, email, username, "", "")
        elif not (goodemail or goodusername or goodpassword):
            self.write_form(error_email, error_username, error_password, "", email, username, "","")
        elif not (goodemail or goodusername):
            self.write_form(error_email, error_username, "", "", email, username, "", "")
        elif not (goodemail):
            self.write_form(error_email, "", "", "", email, username, "", "")
        else:
            self.redirect("/welcome?username="+ username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.write("Welcome, "+ username)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
