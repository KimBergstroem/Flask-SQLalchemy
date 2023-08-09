from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task


@app.route("/")
def home():
    return render_template("tasks.html")


@app.route("/categories")
def categories():  # Will retreive all the data into the variable
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories)
    # first categories present the html page, second present the list above function


# GET AND POST IS NEEDED TO HAVE THE STUFF INTO DATABASE
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = Category(category_name=request.form.get("category_name"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")


# This is a Flask route that handles both GET and POST requests for editing a category.
@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    # Retrieve the category with the given category_id from the database
    # Otherwise trought a 404 error message
    category = Category.query.get_or_404(category_id)

    # Check if the incoming request method is POST(from form)
    if request.method == "POST":  # If the form have been submitted
        # Update the category name with the value from the form's 'category_name' input.
        category.category_name = request.form.get("category_name")

        # Commit the changes to the database.
        db.session.commit()

        # Redirect the user back to the categories page
        return redirect(url_for("categories"))

    # If the request method is GET (when the user accesses the edit category page):
    # Render the 'edit_category.html' template and provide the category data for pre-filling the form.
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))
