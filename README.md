# The Flask Bucketlist App
[![Build Status](https://travis-ci.org/borenho/flask-bucketlist.svg?branch=challenge-1)](https://travis-ci.org/borenho/flask-bucketlist)\
[![Coverage Status](https://coveralls.io/repos/github/borenho/flask-bucketlist/badge.svg?branch=master)](https://coveralls.io/github/borenho/flask-bucketlist?branch=master)

A simple Python Flask bucket-list application that allows users to keep track of the things they want to achieve and experience before reaching a certain age, and to share the fun with others along the way.

# Prerequisites
To run the app, you need to install a couple of dependencies. Check the `requirements.txt` file to see the dependencies. I will guide you on the installation part below.

# Features
Sign up using email, username and password

Login with email and password

Create a bucketlist (a bucketlist is a container of bucketlist items)

Add another bucketlist

View a single and all the bucketlists

Create a bucketlist item (the goal you want to achieve)

Add another bucketlist item to the same bucketlist

View all the bucketlist items of a bucketlist

Update and delete a bucketlist

Update and delete a bucketlist item

# Installation
You need to have Python installed to run the application. 

Use this simple tutorial I wrote to set it up within minutes - https://medium.com/@BoreCollins/task-automation-on-linux-3cf68fe0b389

Remember to also set up virtualenv and virtualenvwrapper to manage the dependencies (the tutorial shall guide you)

Now clone the repo to get a copy of the working directory on your local machine.

Fire up your terminal/cmd and paste the following command: `git clone https://github.com/borenho/flask-bucketlist.git` and press Enter

Once you're done, install all the requirements with the following command (paste it on your terminal) `pip install -r requirements.txt`

# Running the application
To run the app, fire up your terminal and navigate onto the project directory.

On Linux, it would be something like this: `cd folder/with/thisproject/flask-bucketlist`

Then run the flask server with: `flask run`

N.B: Ensure you followed the 'Just automate it tutorial' to run the app successfully. I covered most of the repetitive work in the tutorial to avoid the hassle of typing in many commands just to run the application

# To Test the application
The app follows TDD (Test Driven Develoment) principles and the tests are in the `tests/` directory.

Navigate to that dir and run the tests with the following command:

`pytest bucketlist.py`

# Authors
Bore Collins
