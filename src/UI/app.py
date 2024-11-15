from flask import Flask, request, render_template, redirect, url_for
from src.Beans.Books import Books
from src.Business_Logic.BooksBL import BooksBL


app = Flask(__name__, static_url_path='/src/UI/static')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/addbook', methods=['POST'])
def add_book():
    
    title = request.form['book-title']               
    author = request.form['author-name']             
    description = request.form['book-description']   
    price = int(request.form['book-price']) 
    book_types = request.form.getlist('book-type')  

        
    other_type = request.form.get('other-type')
    if other_type:
        book_types.append(other_type)
        
    image = request.files['book-image'] 
    # seller_id = int(request.form['seller_id'])
      

    
    b1 = Books(title=title, author=author, description=description, price=price,seller_id=1,tags=book_types)

   
    books_bl = BooksBL()
    status = books_bl.addBook(b1, image)  

    
    return status.message

if __name__ == '__main__':
    app.run(debug=True)
