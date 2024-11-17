from flask import Flask, request, render_template, redirect, url_for
from src.Beans.Books import Books
from src.Business_Logic.BooksBL import BooksBL
from src.Business_Logic.MemberBL import MemberBL
from src.Database.BookDB import BookDB
from src.Database.MembersDB import MemberDB

app = Flask(__name__, static_url_path='/src/UI/static')


@app.route('/')
def login():
    return render_template("login.html")

@app.route('/loginverification',methods= ['POST'])
def loginverifiction():
    MBL = MemberBL()
    BBL = BooksBL()
    phonenumber = request.form['number']
    password = request.form['password']
    validity = MBL.login(phonenumber,password)
    if validity:
        print("hi")
        data = MBL.getpreferences(phonenumber)
        print(data)
        pref_list = BBL.displayPreferedBooks(data)
        print(pref_list)
        return render_template("index.html",preferences = pref_list)
    else:
        return render_template("login.html")

@app.route('/home')
def home():

    preferences = [
        [  # Books for the first preference (e.g., Fiction)
            ['Book One', 'Author A', 'A thrilling fiction story.', 15.99, 'image/book-1.png','Fiction'],  # Book 1
            ['Book Two', 'Author B', 'Another exciting tale.', 20.99, 'image/book-1.png','Fiction']  # Book 2
        ],
        [  # Books for the second preference (e.g., Science)
            ['Book Three', 'Author C', 'A fascinating scientific exploration.', 12.99, 'image/book-1.png','Science'],
            ['Book Four', 'Author D', 'An intriguing mystery novel.', 17.99, 'image/book-1.png','Science'],
            ['Book Five', 'Author E', 'A suspenseful journey.', 19.99, 'image/book-1.png','Science']
        ],
        [  # Books for the third preference (e.g., Mystery)
            ['Book Four', 'Author D', 'An intriguing mystery novel.', 17.99, 'image/book-1.png','Mystery'],
            ['Book Five', 'Author E', 'A suspenseful journey.', 19.99, 'image/book-1.png','Mystery']
        ]
    ]
    return render_template('index.html', preferences=preferences)


@app.route('/AddBook')
def add_book_page():
    return render_template('AddBook.html')


@app.route('/search_item', methods=['POST'])
def search_item():
    bookname = request.form['Searched_item']

    # funtions to retrive searched book

    return render_template('Searched_page.html')


@app.route('/favorites')
def favorites():
    return render_template('favorites.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/addbook', methods=['POST'])
def add_book():
    title = request.form['book-title']
    print(title)
    author = request.form['author-name']
    print(author)
    description = request.form['book-description']
    print(description)
    price = int(request.form['book-price'])
    print(price)
    book_types = request.form.getlist('book-type[]')


    other_type = request.form.get('other-book-type')
    if other_type:
        other_types_list = [tag.strip() for tag in other_type.split(',')]
        for item in other_types_list:
            book_types.append(item)
    if book_types:
        for i in book_types:
            print(i)
    else:
        print('book_types is empty')

    image = request.files['book-image']
    # seller_id = int(request.form['seller_id'])
    print("taken all values")

    b1 = Books(title=title, author=author, description=description, price=price, seller_id=1, tags=book_types)

    books_bl = BooksBL()
    status = books_bl.addBook(b1, image)
    print(status)
    return render_template('AddBook.html')


if __name__ == '__main__':
    app.run(debug=True)
