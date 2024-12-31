import datetime
from collections import defaultdict #dictionary but if you add one that does not exists it creates it.
from flask import Blueprint, render_template, url_for, request, redirect, current_app

pages = Blueprint("habz", __name__, template_folder="templates", static_folder="static") # the reference name, init name, template location, static location.



#every page has acces to functions that are inside the context_processor
@pages.context_processor
def add_calc_date_range():
    #date range around 'start' date
    def date_range(start: datetime.date):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates
    
    return {"date_range": date_range}

# WEBPAGES ROUTES 
@pages.route("/", methods=["GET", "POST"])
@pages.route("/habit/", methods=["GET", "POST"])
@pages.route("/habits/", methods=["GET", "POST"])
def habits():
        
    habz = [
        (
            habit["habits_title"]
            ,habit["habits_descriptions"]

    )
        for habit in current_app.db.habz.find({})
    ]

    return render_template("habits.html"
                           , title = "Habits"
                           , habz = habz
                           #old habits_list = habits_list
                           #old habits_descriptions = habits_descriptions
                          )

@pages.route("/daily/", methods=["GET", "POST"])
@pages.route("/dailies/", methods=["GET", "POST"])
def dailies():
    
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.date.fromisoformat(date_str)
        selected_date_db = datetime.date.fromisoformat(date_str).strftime("%Y-%m-%d")  
    else:
        selected_date = datetime.date.today()
        selected_date_db = datetime.date.today().strftime("%Y-%m-%d")  
        
    habz = [
        (habit["habits_title"])
        for habit in current_app.db.habz.find({})
    ]
    
    completetions = [
        (complete["habits_title"])
        for complete in current_app.db.completions.find({"date":selected_date_db})
    ]
        
    return render_template("dailies.html"
                           , title = "Dailies"
                           , habits_list = habz
                           , selected_date=selected_date
                           , completions = completetions
                          )

@pages.route("/add_habit/", methods=["GET", "POST"])
@pages.route("/add_habits/", methods=["GET", "POST"])
def add_habits():

    if request.method == "POST":
        if request.form.get("habits_title") != '':
            habit = request.form.get("habits_title")
            habit_description = request.form.get("habits_descriptions")
            current_app.db.habz.insert_one({"habits_title": habit, "habits_descriptions": habit_description})

        return redirect(url_for('habz.habits'))
    
    return render_template("add_habits.html"
                           , title = "Adding Habits"
                          )
@pages.route("/completed/", methods=["POST"])
def completed():
    date_string = request.form.get("date")
    daily = request.form.get("dailyName")
    
    date = datetime.date.fromisoformat(date_string).strftime("%Y-%m-%d")    
    current_app.db.completions.insert_one({"habits_title": daily, "date": date})
        
    return redirect(url_for('habz.dailies', date=date_string))
    