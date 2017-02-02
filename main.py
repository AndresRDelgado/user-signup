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
        <input name="username">
    </label>
    <br>
    <label>What is your password? 
        <input name="password">
    </label>
    <br>
    <label>Re-type your password
        <input name="password2">
    </label>
    <br>
    <label>What is your email address?
        <input name="email">
    </label>
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
    def get(self):
        self.response.write(form)
    
    def post(self):
        email = valid_email(self.request.get("email"))
        username = valid_username(self.request.get("username"))
        password = valid_password(self.request.get("password"))
        password2 = matching_password(self.request.get("password"),self.request.get("password2"))

        if not (email and username and password and password2):
            self.response.write("wrong")
        else:
            self.response.write("pretty good")

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
