from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
database = {}
with open('food.json') as filepointer:
    database = json.load(filepointer)
print(database)


@app.route('/')
def home():
    return render_template('index.template.html',
                           food=database)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host='localhost',
            port=8080,
            debug=True)
