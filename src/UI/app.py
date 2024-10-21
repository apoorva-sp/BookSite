from flask import Flask, request, render_template, redirect, url_for
from src.Beans.Books import Books
from src.Business_Logic.BooksBL import BooksBL


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addbook', methods=['POST'])
def add_book():
    
    title = request.form['title']
    author = request.form['author']
    description = request.form['description']
    price = float(request.form['price'])
    seller_id = int(request.form['seller_id'])
    image = request.files['image']  

    
    b1 = Books(title=title, author=author, description=description, price=price,seller_id=seller_id)

   
    books_bl = BooksBL()
    status = books_bl.addBook(b1, image)  

    
    return status.message

if __name__ == '__main__':
    app.run(debug=True)
