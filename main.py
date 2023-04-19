from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


## CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///all_books.db"
### A "all-books.db" file appear in the root folder

# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


## CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()




@app.route('/')
def home():
    ## READ ALL RECORDS
    all_books = db.session.query(Book).all()
    ## or
    # all_books = db.session.execute(db.select(Book)).scalars()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():

    # When the user input and prees the "Add Book" button
    if request.method == "POST":
        new_book = Book(
            title = request.form["title"],
            author = request.form["author"],
            rating = request.form["rating"]
        )
        # Use the SQLAlchemy method to add book data to SQL database
        db.session.add(new_book)
        db.session.commit()

        # Go back to the home page
        return redirect(url_for('home'))

    return render_template("add.html")


## Edit rating function
### Page for the edit rating
@app.route("/edit", methods=["GET", "POST"])
def edit():
    # If user input something then tragger the function
    if request.method == "POST":
        #UPDATE RECORD
        ## Get the id that user want to edit book
        book_id = request.form["id"]
        book_to_update = Book.query.get(book_id)
        # Receiving from edit_rating.html name="rating" and update the rating
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    # Get the id from DB
    book_id = request.args.get('id')
    # Get the book data through book_id
    book_selected = Book.query.get(book_id)
    # Pass book data to the edit_rating.html
    # Using {{book.title}} and  {{book.rating}} to show name and rating on the web page
    # book is HTML variable, book_selected is Python variable
    return render_template("edit_rating.html", book=book_selected)


## Delete function
### Page for the delete
#### When you delete a book, it will go to /delete page > execute the function > then go back home page
#### But the process is very fast, so user will not be aware of the page change
#### And there is no delete.html
@app.route("/delete")
def delete():
    # The "id" come from index.html id=book.id
    book_id = request.args.get('id')

    # DELETE A RECORD BY ID
    # Pass the id to get the book that in DB
    book_to_delete = Book.query.get(book_id)
    # use the method to delete book
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)