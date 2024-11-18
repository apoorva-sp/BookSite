from flask import Flask, request,session, render_template, redirect, url_for
from src.Beans.Books import Books
from src.Business_Logic.BooksBL import BooksBL
from src.Business_Logic.MemberBL import MemberBL
from src.Database.BookDB import BookDB
from src.Database.MembersDB import MemberDB

app = Flask(__name__, static_url_path='/src/UI/static')
app.secret_key = 'Apoorvasp@2003'


@app.route('/')
def login():
    return render_template("login.html")

@app.route('/home',methods= ['POST'])
def home():
    MBL = MemberBL()
    BBL = BooksBL()
    phonenumber = request.form['number']
    password = request.form['password']
    validity = MBL.login(phonenumber,password)
    if validity:
        mID = MBL.get_mid(phonenumber)
        session['phone_number'] = phonenumber
        session['mid'] = mID[0]

        print("hi")
        print(f"Session created for {session['phone_number']} with MID {session['mid']}")
        data = MBL.getpreferences(phonenumber)
        print(data)
        pref_list = BBL.displayPreferedBooks(data)
        print(pref_list)
        return render_template("home.html",preferences = pref_list)
    else:
        return render_template("login.html")


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
    if 'mid' not in session:
        return redirect(url_for('login.html'))
    title = request.form['book-title']
    print(title)
    author = request.form['author-name']
    print(author)
    description = request.form['book-description']
    print(description)
    price = int(request.form['book-price'])
    print(price)
    book_types = request.form.getlist('book-type[]')
    print(book_types)
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
    seller_id = int(session['mid'])

    b1 = Books(title=title, author=author, description=description, price=price, seller_id=seller_id, tags=book_types)

    books_bl = BooksBL()
    status = books_bl.addBook(b1, image,other_type!="")
    print(status)
    MBL = MemberBL()
    bbl = BooksBL()
    data = MBL.getpreferences(str(session['phone_number']))
    print(data)
    pref_list = bbl.displayPreferedBooks(data)
    print(pref_list)
    return render_template("home.html", preferences=pref_list)


if __name__ == '__main__':
    app.run(debug=True)
