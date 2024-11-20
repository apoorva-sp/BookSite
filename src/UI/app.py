from flask import Flask, request,session,jsonify, render_template, redirect, url_for
from src.Beans.Books import Books
from src.Business_Logic.BooksBL import BooksBL
from src.Business_Logic.MemberBL import MemberBL
from src.Database.BookDB import BookDB
from src.Database.MembersDB import MemberDB
from src.Business_Logic.CartBL import CartBL
from src.Beans.Status import Status

app = Flask(__name__, static_url_path='/src/UI/static')
app.secret_key = 'Apoorvasp@2003'


@app.route('/')
def login():
    return render_template("login.html")
@app.route('/signup')
def signup():
    return render_template("signup.html")
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

@app.route('/homepage')
def homepage():
    MBL = MemberBL()
    BBL = BooksBL()
    data = MBL.getpreferences(str(session['phone_number']))
    print(data)
    pref_list = BBL.displayPreferedBooks(data)
    print(pref_list)
    return render_template("home.html", preferences=pref_list)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    book_id = int(data.get('book_id'))
    buyer_id=int(session['mid'])
    if book_id and buyer_id:
        CBL=CartBL()
        status=CBL.AddToCart(book_id,buyer_id)

        return jsonify({'success': True})

    return jsonify({'success': False, 'message': 'Invalid book ID'})
@app.route('/mybooks')
def mybooks():
    bbl=BooksBL()
    buyerid=session['mid']
    books=bbl.mybooks(buyerid)
    print(books)
    return render_template("mybooks.html",books=books)
@app.route('/AddBook')
def add_book_page():
    return render_template('AddBook.html')


@app.route('/search_item', methods=['POST'])
def search_item():
    bookname = request.form['Searched_item']

    # funtions to retrive searched book

    return render_template('Searched_page.html')

@app.route('/deletebook', methods=['POST'])
def delete_book():
    data = request.get_json()
    book_id = data.get('book_id')
    if not book_id:
        return jsonify(success=False, message="Book ID is missing.")
    try:
        print(book_id)
        bbl=BooksBL()
        status = bbl.DeleteBook(book_id,int(session['mid']))
        print(status.message)
        if status.statusId==0:
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Failed to delete the book.")
    except Exception as e:
        print(e)
        return jsonify(success=False, message="An error occurred.")
@app.route('/favorites')
def favorites():
    buyer_id = int(session['mid'])
    CBL = CartBL()
    books=CBL.get_books(buyer_id)
    print(books)
    total = sum(book[3] for book in books)
    return render_template('cart.html' ,books=books , total=total)

@app.route('/delete_from_cart', methods=['POST'])
def delete_from_cart():
    data = request.get_json()
    book_id = int(data.get('book_id'))
    print(book_id)
    buyer_id = int(session['mid'])
    if book_id and buyer_id:
        CBL = CartBL()
        status = CBL.delete_from_cart(book_id, buyer_id)

        return jsonify({'success': True})

    return jsonify({'success': False, 'message': 'Invalid book ID'})

@app.route('/profile')
def profile():
    number=session['phone_number']
    mbl = MemberBL()
    data = mbl.get_info(number)
    print(data)
    data =list(data)
    cat= ', '.join([data[9], data[10], data[11]])
    data.append(cat)

    return render_template('profile.html', data = data)

@app.route('/editprofile')
def editprofile():
    return render_template('editprofile.html')

@app.route('/update_profile',methods=['POST'])
def update_profile():
    fullname = request.form.get('fullname')
    phonenumber = request.form.get('phonenumber')
    oldpassword = request.form.get('oldpassword')  # Optional
    newpassword = request.form.get('newpassword')
    addressline1 = request.form.get('addressline1')
    addressline2 = request.form.get('addressline2')
    city = request.form.get('city')
    state = request.form.get('state')
    pincode = request.form.get('pincode')
    preference_one = request.form.get('preferenceone')
    preference_two = request.form.get('preferencetwo')
    preference_three = request.form.get('preferencethree')

    status = Status(-1, "you need to choose all three preferences")
    if fullname:
        mbl = MemberBL()
        status=mbl.update_name(session['phone_number'],fullname)

    if oldpassword and newpassword:
        mbl = MemberBL()
        status=mbl.update_password(newpassword,oldpassword,session['phone_number'])

    if phonenumber:
        mbl = MemberBL()
        status = mbl.update_number(phonenumber,session['phone_number'])
        if status.statusId==0:
            session['phone_number']=phonenumber

    if addressline1 and  addressline2 and city and state and pincode :
        mbl = MemberBL()
        status=mbl.update_address(phonenumber,addressline1,addressline2,city,state,pincode)

    if preference_one or preference_two or preference_three:

        if len(set([preference_one, preference_two, preference_three])) < 3:
            return render_template('editprofile.html', error="Must select all three preferences.")
        else:
            mbl = MemberBL()
            status=mbl.update_preference(phonenumber,preference_one, preference_two,preference_three)

    if status and status.statusId == 0:
        mbl=MemberBL()
        data = mbl.get_info(session['phone_number'])
        data = list(data)
        cat = ', '.join([data[9], data[10], data[11]])
        data.append(cat)
        return render_template('profile.html',data=data)
    else:
        return render_template('editprofile.html', error =status.message)

@app.route('/orderplaced', methods=['POST'])
def order_placed():
    data = request.get_json()
    book_ids = data.get('book_ids', [])
    buyer_id = session['mid']
    # Example logic: Process the book IDs for order placement
    if book_ids:
        book_ids = [int(id) for id in book_ids]
        print(book_ids)
        # Your order logic here
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="No books in the cart.")
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
