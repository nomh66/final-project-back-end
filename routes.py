from flask import render_template, flash, redirect, request, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from extensions import app, db, products
from forms import AddProduct, RegisterForm, LoginForm, ContactForm, PurchaseForm
from models import Product, Category, User, Purchase
import os

@app.route("/home")
def home():
    products = Product.query.all()
    return render_template("home.html", products=products)

def chunk_list(lst, chunk_size):
    """Split a list into chunks of a specified size."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

@app.route("/store")
def store():
    products = Product.query.all()
    chunk_size = 2
    product_chunks = list(chunk_list(products, chunk_size))
    return render_template('store.html', product_chunks=product_chunks)

@app.route("/about_us")
def about_us():
    return render_template("about us.html")

@app.route("/contact", methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash("Form Submited!", category="success")
        return redirect(url_for('home')) 
    else:
        flash("Submit Error. Try Again.", category="danger")
    return render_template("contact.html", form=form)

@app.route("/addproduct", methods=["GET", "POST"])
def add_product():
    form = AddProduct()
    if form.validate_on_submit():
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)

        product = {"name": form.name.data,
                   "url": form.url.data,
                   "price": form.price.data,
                   "id": len(products) +1}
        products.append(product)
        flash("Request Sent!", category='success')
        

        return redirect("/store")
     
    if form.errors:
        print(form.errors)
        for error in form.errors:
            print(error)

        flash("Request Wasn't Sent Properly.", category="danger")

    return render_template("add Product.html", form=form)

@app.route("/uploadfile", methods=["GET", "POST"])
def upload_file():
    form = AddProduct()
    
    if form.validate_on_submit():
        file = request.files['file']
        folder = 'products' 
        
        if file:
            filename = file.filename
            file_path = os.path.join(app.root_path, 'static', 'image', folder, filename)
            
            file_dir = os.path.dirname(file_path)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

            file.save(file_path)

            product = Product(
                name=form.name.data,
                file=filename,
                price=form.price.data,
                folder=folder,
                description=form.description.data
            )
            db.session.add(product)
            db.session.commit()

            if 'uploaded_products' not in session:
                session['uploaded_products'] = []
            session['uploaded_products'].append({
                'id': product.id,
                'name': product.name,
                'file': product.file,
                'price': product.price,
                'folder': product.folder,
                'description': product.description
            })

            flash("You successfully added the product", category="success")
            return redirect("/user_request")
    
    if form.errors:
        print(form.errors)
        flash("You didn't add the product properly", category="danger")
        
    return render_template("add product.html", form=form)


@app.route("/detail/<int:id>")
def detail(id):
    current = Product.query.get(id)
    user_role = current_user.role if current_user.is_authenticated else None
    return render_template("details.html", product=current, user_role=user_role)

@app.route("/purchase/<int:id>", methods=["POST", "GET"])
@login_required
def purchase(id):
    print(f"Fetching product with ID: {id}")
    current = Product.query.get(id)
    if not current:
        flash('Product not found!', category='danger')
        return redirect(url_for('home'))
    
    form = PurchaseForm()
    
    if form.validate_on_submit():
        print("Form is valid and submitted.")
        new_purchase = Purchase(
            product_id=current.id,
            full_name=form.full_name.data,
            email=form.email.data,
            address=form.address.data,
            city=form.city.data,
            country=form.country.data,
            zip_code=form.zip_code.data,
            card_cvc=form.card_cvc.data
        )
        db.session.add(new_purchase)
        db.session.commit()
        
        if 'ordered_products' not in session:
            session['ordered_products'] = []
        session['ordered_products'].append({
            'name': current.name,
            'file': current.file,
            'price': current.price,
            'description': current.description,
            'folder': current.folder
        })
        
        flash('Purchase successful!', category='success')
        return redirect(url_for('orders'))
    else:
        print("Form did not validate.")

    return render_template('purchase.html', product=current, form=form)

    
@app.route("/category/<int:category_id>")
def category_select(category_id):
    current_category = Category.query.get(category_id)
    if not current_category:
        return "Category not found", 404

    products = Product.query.filter_by(category_id=category_id).all()
    if not products:
        return "No products found for this category", 404

    chunk_size = 2
    product_chunks = list(chunk_list(products, chunk_size))

    return render_template("store.html", products=products, product_chunks=product_chunks)

@app.route("/")
@app.route("/index", methods=["POST", "GET"])
def index():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.mail.data).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", category="danger")
            return redirect(url_for('index'))
        if existing_email:
            flash("Email already exists. Please use a different one.", category="danger")
            return redirect(url_for('index'))

        user = User(username=form.username.data, password=form.password.data, email=form.mail.data)
        db.session.add(user)
        db.session.commit()
        flash("You Successfully Registered!", category="success")
        return redirect("/home")
    return render_template("index.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        exists = User.query.filter(User.username==form.username.data).first()
        print(exists)
        if exists and form.password.data == exists.password:
            login_user(exists)
            flash("Login Successfull!", category="success")
            return redirect("/home")
        else:
            flash("You didn't add the product properly", category="danger")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user
    return redirect("/login")

@app.route("/delete/<int:id>")
@login_required
def delete_product(id):
    if current_user.role == "admin":
        current = Product.query.get(id)
        if current:
            db.session.delete(current)
            db.session.commit()
            return redirect("/store")
        else:
            return "Product not found", 404
    else:
        return "You are not authorized to delete products", 403
    
@app.route("/orders")
@login_required
def orders():
    if current_user.is_authenticated:
        user_orders = db.session.query(Purchase, Product).filter(Purchase.product_id == Product.id, Purchase.email == current_user.username).all()
        products = [product for _, product in user_orders]
        
        if 'ordered_products' in session:
            for ordered_product in session['ordered_products']:
                products.append(Product(
                    name=ordered_product['name'],
                    file=ordered_product['file'],
                    price=ordered_product['price'],
                    description=ordered_product['description'],
                    folder=ordered_product['folder']
                ))
        
        chunk_size = 2
        product_chunks = list(chunk_list(products, chunk_size))
        return render_template("orders.html", product_chunks=product_chunks)
    else:
        flash("You need to log in to view your orders.", category="danger")
        return redirect(url_for('login'))

def chunk_list(lst, chunk_size):
    """Split a list into chunks of a specified size."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

@app.route("/user_request")
def user_request():
    if 'uploaded_products' in session:
        products = [Product(
            id=p['id'],
            name=p['name'],
            file=p['file'],
            price=p['price'],
            folder=p['folder'],
            description=p['description']
        ) for p in session['uploaded_products']]
    else:
        products = []

    chunk_size = 2
    product_chunks = list(chunk_list(products, chunk_size))
    return render_template('user request.html', product_chunks=product_chunks)

def chunk_list(lst, chunk_size):
    """Split a list into chunks of a specified size."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]
