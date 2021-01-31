from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
import random

app = Flask(__name__)
database = {}
with open('food.json') as filepointer:
    database = json.load(filepointer)

# enable sessions in flask


def find_food_by_id(food_id):
    wanted_food_record = None
    for food_record in database:
        if food_record["id"] == food_id:
            wanted_food_record = food_record
            break

    return wanted_food_record


def save_to_json():
    with open('food.json', 'w') as filepointer:
        json.dump(database, filepointer)

    return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('index.template.html',
                           food=database)


@app.route('/log')
def show_log_food():
    return render_template('log_food.template.html')


@app.route('/log', methods=["POST"])
def process_log_food():
    new_food = {}
    new_food['id'] = random.randint(1, 10000) + 5
    new_food['when_eaten'] = request.form.get('date')
    new_food['meal'] = request.form.get('meal')
    new_food['food_name'] = request.form.get('food_name')
    new_food['calories'] = request.form.get('calories')

# add to database
    database.append(new_food)

# save into JSON file
    save_to_json()


@app.route('/<int:food_id>/update')
def show_update_food(food_id):
    # linear search to find record to edit
    wanted_food_record = find_food_by_id(food_id)

    return render_template('update_food.template.html',
                           food=wanted_food_record)


@app.route('/<int:food_id>/update', methods=["POST"])
def process_update_food(food_id):
    existing_food_record = find_food_by_id(food_id)
    existing_food_record['food_name'] = request.form.get('food_name')
    existing_food_record['when_eaten'] = request.form.get('date')
    existing_food_record['meal'] = request.form.get('meal')
    existing_food_record['calories'] = request.form.get('calories')

    save_to_json()

    return redirect(url_for('home'))


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
