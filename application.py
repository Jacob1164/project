# Jacob Frabutt
# 10-21-18
# CS50x: Final Project
# Python component for the website
# SQL lite is used in this file
# Thank you to stack exchange for helping me with some of the issues I was having


import csv
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, send_file
from flask_session import Session
from functools import wraps
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# dicts/lists that are used for GPA
scale = {"A+": 97, "A": 93, "A-": 90, "B+": 87, "B": 83, "B-": 80, "C+": 77, "C": 73, "C-": 70, "D+": 67, "D": 63, "D-": 60, "F": 0}
grade_point_average = {"A+": 4, "A": 4, "A-": 3.667, "B+": 3.333, "B": 3, "B-": 2.667,
                       "C+": 2.333, "C": 2, "C-": 1.667, "D+": 1.333, "D": 1, "D-": 0.667, "F": 0}
letters = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"]

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mygrade.db")

# login required function


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# apology function


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=message), code


@app.route("/")
def index():
    """
    This is the home page

    If the user is signed in, it loads a splash screen of their current grades.
    Otherwise, it loads a page with information about the website.
    """
    if not session.get("user_id") is None:
        # get all the classes the person has
        rows = db.execute("SELECT * FROM classes WHERE user_id = :idd",
                          idd=session["user_id"])
        # initialize some variables
        names, value, numbers, lets, ggg, ppp = [], [], [], [], [], 0

        # go through class by class and find grade
        for row in rows:
            names.append(row["name"])
            grades = db.execute("SELECT * FROM :name WHERE class = :clas",
                                name=session["user_name"], clas=row["id"])

            # check if class has any assignments
            if not len(grades) == 0:
                poss, earned = 0, 0

                # iterate over assignments
                for grade in grades:
                    poss += float(grade["possible"])
                    earned += float(grade["earned"])

                hold = (earned / poss) * 100
                numbers.append(round(hold, 2))

                # figure out letter grade and gpa
                for let in letters:
                    if hold >= scale[let]:
                        lets.append(let)
                        value.append(grade_point_average[let] + float(row["scale"]) - 4)
                        ggg.append(grade_point_average[let] + float(row["scale"]) - 4)
                        ppp += 1
                        break

            # if no assignments
            else:
                numbers.append("N/A")
                lets.append("N/A")
                value.append("N/A")

        # calculate gpa
        if not ppp == 0:
            gpa = round(sum(ggg) / ppp, 3)
        else:
            gpa = "N/A"

        return render_template("index.html", names=names, value=value, numbers=numbers, lets=lets, num=len(names), gpa=gpa)

    else:
        return render_template("index.html")


@app.route("/account")
@login_required
def account():
    # get account info
    """
    Displays the account info.
    """
    rows = db.execute("SELECT * FROM users WHERE id = :idd",
                      idd=session["user_id"])

    return render_template("account.html", name=rows[0]["name"], user=rows[0]["user"], grade=rows[0]["grade"])


@app.route("/add", methods=["POST"])
@login_required
def add():
    """
    Add new classes for a user.
    """
    rows = db.execute("SELECT * FROM classes WHERE user_id = :idd",
                      idd=session["user_id"])
    names = []

    # copy over class names
    for row in rows:
        names.append(row["name"])

    for i in range(int(request.form.get("number"))):
        # make sure class doesn't exist
        if request.form.get("name{}".format(i)) in names:
            return render_template("add.html", number=int(request.form.get("number")), message="You already have a class with this name.")

        # add class
        db.execute("INSERT INTO classes (user_id, name, scale) VALUES (:idd, :name, :scale)",
                   idd=session["user_id"], name=request.form.get("name{}".format(i)), scale=float(request.form.get("scale{}".format(i))))

    return redirect("/")


@app.route("/adjust", methods=["GET", "POST"])
def adjust():
    """
    Re-load the add page with a different number of classes.
    """
    amount = 8

    # process the amount of classes they want
    if request.form.get("amount"):
        amount = int(request.form.get("amount"))

    return render_template("gpa.html", amount=amount)


@app.route("/classes/<name>", methods=["GET", "POST"])
@login_required
def classes(name):
    """
    Displays the selected class.
    Shows the overall grades (letter and number), and individual assignment grades (letter and number).
    The user can add an assignment directly from this page
    """

    # querry database and initialize variables
    rows = db.execute("SELECT * FROM classes WHERE user_id = :idd AND name = :name",
                      idd=session["user_id"], name=name)[0]
    assignments = db.execute("SELECT * FROM :name WHERE class = :clas",
                             name=session["user_name"], clas=rows["id"])
    names, points, nums, lets, totearned, totposs, totlet = [], [], [], [], 0, 0, ""

    # make sure there are assignments
    if len(assignments) > 0:

        for assignment in assignments:
            names.append(assignment["name"])

            # keep track of total points
            totearned += float(assignment["earned"])
            totposs += float(assignment["possible"])

            # make sure I won't be dividing by 0
            if float(assignment["possible"]) == 0:
                nums.append("N/A")
                lets.append("A+")
            else:
                per = (float(assignment["earned"]) / float(assignment["possible"])) * 100
                nums.append(round(per, 2))

                # calculate letter grade for assignment
                for let in letters:
                    if per >= scale[let]:
                        lets.append(let)
                        break

            # add the formated string into the list
            points.append("{}/{}".format(assignment["earned"], assignment["possible"]))

        # overall grade
        overall = (totearned / totposs) * 100
        overall = round(overall, 2)

        # overall letter grade
        for let in letters:
            if overall >= scale[let]:
                totlet = let
                break

    else:
        overall = "N/A"
        totlet = "N/A"

    return render_template("class.html", names=names, points=points, nums=nums, lets=lets, totlet=totlet, overall=overall, name=name, num=len(names), idd=rows["id"])


@app.route("/classes/test/<name>", methods=["GET", "POST"])
@login_required
def test(name):
    """
    This page loads all the scores just like the normal classes page, but puts them in text boxes.
    This allows the user to expiriment with their scores in without reloading the page
    """
    rows = db.execute("SELECT * FROM classes WHERE user_id = :idd AND name = :name",
                      idd=session["user_id"], name=name)[0]
    assignments = db.execute("SELECT * FROM :name WHERE class = :clas",
                             name=session["user_name"], clas=rows["id"])
    names, earned, out, nums, lets, totearned, totposs, totlet = [], [], [], [], [], 0, 0, ""

    if len(assignments) > 0:
        for assignment in assignments:
            names.append(assignment["name"])

            # make sure I won't be dividing by 0
            if float(assignment["possible"]) == 0:
                nums.append("N/A")
                lets.append("A+")
            else:
                per = (float(assignment["earned"]) / float(assignment["possible"])) * 100
                nums.append(round(per, 2))

            totearned += float(assignment["earned"])
            totposs += float(assignment["possible"])

            for let in letters:
                if per >= scale[let]:
                    lets.append(let)
                    break

            earned.append(assignment["earned"])
            out.append(assignment["possible"])

        overall = (totearned / totposs) * 100
        overall = round(overall, 2)

        for let in letters:
            if overall >= scale[let]:
                totlet = let
                break

    else:
        overall = "N/A"
        totlet = "N/A"

    return render_template("edit.html", names=names, earned=earned, out=out, nums=nums, lets=lets, totlet=totlet, overall=overall, name=name, num=len(names), idd=rows["id"])


@app.route("/classes/<name>/update", methods=["GET", "POST"])
@login_required
def change(name):
    """
    Displays the assignment info in text boxes.
    Changes the user makes will be updated in the database.
    """
    if request.method == "GET":
        rows = db.execute("SELECT * FROM classes WHERE user_id = :idd AND name = :name",
                          idd=session["user_id"], name=name)[0]
        assignments = db.execute("SELECT * FROM :name WHERE class = :clas",
                                 name=session["user_name"], clas=rows["id"])
        idd, names, earned, out, nums, lets, totearned, totposs, totlet, message = [], [], [], [], [], [], 0, 0, "", ""

        if len(assignments) > 0:
            for assignment in assignments:
                names.append(assignment["name"])
                idd.append(assignment["unique_id"])

                # make sure I won't be dividing by 0
                if float(assignment["possible"]) == 0:
                    nums.append("N/A")
                    lets.append("A+")
                else:
                    per = (float(assignment["earned"]) / float(assignment["possible"])) * 100
                    nums.append(round(per, 2))

                totearned += float(assignment["earned"])
                totposs += float(assignment["possible"])

                for let in letters:
                    if per >= scale[let]:
                        lets.append(let)
                        break

                earned.append(assignment["earned"])
                out.append(assignment["possible"])

            overall = (totearned / totposs) * 100
            overall = round(overall, 2)

            for let in letters:
                if overall >= scale[let]:
                    totlet = let
                    break

        else:
            message = "You must have at least one assignment to edit."

        return render_template("change.html", names=names, earned=earned, out=out, nums=nums, name=name, num=len(names), message=message, idd=idd)

    else:
        classnum = db.execute("SELECT * FROM classes WHERE user_id = :idd AND name = :name",
                              idd=session["user_id"], name=name)[0]["id"]
        assignments = db.execute("SELECT * FROM :name WHERE class = :clas",
                                 name=session["user_name"], clas=classnum)

        for i in range(len(assignments)):
            newname = request.form.get("name{}".format(i))
            newearn = request.form.get("earned{}".format(i))
            newposs = request.form.get("out{}".format(i))
            uid = request.form.get("id{}".format(i))

            db.execute("UPDATE :user SET name = :name, earned = :earn, possible = :poss WHERE class = :idd AND unique_id = :uid",
                       user=session["user_name"], name=newname, earn=newearn, poss=newposs, idd=classnum, uid=uid)

        name = request.form.get("class_name")
        return redirect("/classes/{}".format(name))


@app.route("/compute/<int:method>", methods=["POST"])
def compute(method):
    """
    Calculates the intel for the exams.
    The method depends on what info the user submitted.
    """

    # If they already took the exam
    if method == 0:
        percent = float(request.form.get("per"))
        qpercent = ((100 - percent) / 2) / 100
        qtot = (float(request.form.get("Q1")) * qpercent) + (float(request.form.get("Q2")) * qpercent)
        tot = qtot + (float(request.form.get("E")) * (percent / 100))
        return render_template("final.html", method=method, val=str(round(tot, 2)) + "%")

    # if they still need to take the exam
    elif method == 1:
        percent = float(request.form.get("per"))
        qpercent = ((100 - percent) / 2) / 100
        qtot = (float(request.form.get("Q1")) * qpercent) + (float(request.form.get("Q2")) * qpercent)
        need = ((float(request.form.get("desired")) - qtot) / percent) * 100
        return render_template("final.html", method=method, val=str(round(need, 2)) + "%", goal=request.form.get("desired") + "%")

    # just in case
    else:
        return apology("invalid method")


@app.route("/download")
def download():
    """
    Download a csv file with info from the gpa calculator
    """
    return send_file("gpa.csv")


@app.route("/exams", methods=["GET", "POST"])
def exams():
    return render_template("exams.html")


@app.route("/gpa", methods=["GET", "POST"])
def gpa():
    """
    Calculates the user's GPA based off the inputed numbers.
    It also stores the values into a csv file in case it is downloaded.
    """

    # when click on link
    if request.method == "GET":
        amount = 8
        return render_template("gpa.html", amount=amount)

    else:
        # create a csv file
        file = open("gpa.csv", "w+")
        writer = csv.writer(file)
        writer.writerow(["Class", "Credit hours", "Scale", "Grade", "GPA Value"])

        numbers, weighted, count, totcredits = [], [], 0, 0

        # iterate over classes
        for i in range(int(request.form.get("amount"))):
            numbers.append(grade_point_average[request.form.get("a{}".format(i))])

            # add in the weighted scales
            if not request.form.get("a{}".format(i)) == "F":
                weighted.append((numbers[i] + float(request.form.get("c{}".format(i))) - 4)
                                * float(request.form.get("b{}".format(i))))
            # F is always 0
            else:
                weighted.append(0)

            # update values
            count += weighted[i]
            totcredits += float(request.form.get("b{}".format(i)))

            # update csv file
            writer.writerow([i + 1, request.form.get("b{}".format(i)), request.form.get("c{}".format(i)),
                             request.form.get("a{}".format(i)), weighted[i]])

        # final values
        final = count / totcredits
        final = str(round(final, 3))

        # finish csv file
        writer.writerow(["OVERALL:", "", "", "", final])
        file.close()

        return render_template("gpaResults.html", val=final)


@app.route("/gpa/scale")
def gpaScale():
    """
    Displays the gpa scale used on this website
    """
    return render_template("scale.html")


@app.route("/insert", methods=["POST"])
@login_required
def insert():
    """
    Adds one assignment to the current class.
    """

    # add assignment into database
    db.execute("INSERT INTO :user (class, name, earned, possible) VALUES (:idd, :name, :earned, :possible)",
               user=session["user_name"], idd=request.form.get("idd"), name=request.form.get("name"), earned=request.form.get("a"), possible=request.form.get("b"))

    return redirect("classes/{}".format(request.form.get("class")))


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    login the user
    """
    # forget previous user_id
    session.clear()

    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE user = :user",
                          user=request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["pass_hash"], request.form.get("password")):
            return apology("Invalid username or password")

        # remember id and user name
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["user"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """
    logout the user
    """
    # forget info
    session.clear()

    return redirect("/")


@app.route("/manage", methods=["GET", "POST"])
@login_required
def manage():
    """
    Allows the user to manage info about their classes.
    """

    # link
    if request.method == "GET":
        rows = db.execute("SELECT * FROM classes WHERE user_id = :idd",
                          idd=session["user_id"])
        return render_template("manage.html", rows=rows, num=len(rows))

    else:
        # load add page
        if request.form.get("method") == "add":
            number = int(request.form.get("add"))
            return render_template("add.html", number=number)

        # delete the class they selected
        elif request.form.get("method") == "remove":
            cid = db.execute("SELECT * FROM classes WHERE (name = :name) AND (user_id = :idd)",
                             name=request.form.get("remove"), idd=session["user_id"])[0]["id"]
            db.execute("DELETE FROM classes WHERE (name = :name) AND (user_id = :idd)",
                       name=request.form.get("remove"), idd=session["user_id"])
            db.execute("DELETE FROM :name WHERE class = :cid",
                       name=session["user_name"], cid=cid)
            return redirect("/")


@app.route("/manage/update", methods=["GET", "POST"])
@login_required
def update_classes():
    """
    saves the changes that the user made to the classes info page
    """

    if request.method == "GET":
        rows = db.execute("SELECT * FROM classes WHERE user_id = :idd",
                          idd=session["user_id"])
        scale = []
        for row in rows:
            scale.append(row["scale"])

        return render_template("edit_classes.html", rows=rows, num=len(rows), scale=scale)
    else:
        for i in range(int(request.form.get("number"))):
            name = request.form.get("name{}".format(i))
            scale = request.form.get("scale{}".format(i))
            cid = request.form.get("cid{}".format(i))
            db.execute("UPDATE classes SET name = :name, scale = :scale WHERE user_id = :idd AND id = :cid",
                       name=name, scale=scale, idd=session["user_id"], cid=cid)

        return redirect("/manage")


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """
    Allows the user to change their password.
    """
    if request.method == "GET":
        return render_template("password.html")
    else:
        rows = db.execute("SELECT * FROM users WHERE id = :idd",
                          idd=session["user_id"])
        if not check_password_hash(rows[0]["pass_hash"], request.form.get("previous")):
            return apology("Incorrect current password.")

        db.execute("UPDATE users SET pass_hash = :passw WHERE id = :idd",
                   passw=generate_password_hash(request.form.get("new")), idd=session["user_id"])

        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    allows the user to create an account
    """
    if request.method == "POST":
        # make sure none exist with username
        rows = db.execute("SELECT * FROM users WHERE user = :user",
                          user=request.form.get("username"))

        if len(rows) != 0:
            return apology("Username already exists")

        # set variables
        phash = generate_password_hash(request.form.get("password"))
        last = request.form.get("last")
        first = request.form.get("first")
        middle = request.form.get("middle")
        name = last + ", " + first + " " + middle

        # add to databases
        db.execute("INSERT INTO users (user, pass_hash, name, grade) VALUES (:user, :phash, :name, :grade)",
                   user=request.form.get("username"), phash=phash, name=name, grade=request.form.get("grade"))
        db.execute("CREATE TABLE :name ('unique_id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'class' INTEGER, 'name' TEXT, 'earned' INTEGER, 'possible' INTEGER)",
                   name=request.form.get("username"))

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/remove", methods=["POST"])
@login_required
def remove():
    """
    Delete one assignment
    """
    # remove assignment from database
    db.execute("DELETE FROM :name WHERE (name = :assig) AND (class = :clas)",
               name=session["user_name"], assig=request.form.get("assignment"), clas=request.form.get("idd"))

    return redirect("/classes/{}".format(request.form.get("class")))


@app.route("/wipe", methods=["POST"])
@login_required
def wipe():
    """
    Delete an entire account
    """

    db.execute("DELETE FROM classes WHERE user_id = :idd",
               idd=session["user_id"])
    db.execute("DROP TABLE :name", name=session["user_name"])
    db.execute("DELETE FROM users WHERE id = :idd",
               idd=session["user_id"])

    session.clear()

    return redirect("/")