from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

all_books = []


@app.route('/')
def home():
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():

    # When the user input and prees the "Add Book" button
    if request.method == "POST":
        new_book = {
            "title": request.form["title"],
            "author": request.form["author"],
            "rating": request.form["rating"]
            }
        # Add the dictionary to the all_book list
        all_books.append(new_book)

        # Go back to the home page
        return redirect(url_for('home'))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)

