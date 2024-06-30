from extensions import app, db, login_manager, products
from flask import redirect
from flask_login import UserMixin


class Product(db.Model):
    name = db.Column(db.String)
    file = db.Column(db.String)
    price = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    description = db.Column(db.String)
    folder = db.Column(db.String(50))  


    def __str__(self):
        return f"{self.name}"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    product_id = db.relationship("Product", backref="category", lazy=True)

    def __str__(self):
        return f"{self.name}"

def populate_data():
    for product in products:
        product_to_add = Product(name=product["name"],
                                 price=product["price"],
                                 file=product["url"],
                                 description=product["description"]
                                 )
        db.session.add(product_to_add)
        db.session.commit()
    return redirect("/home")    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default="guest")
    email = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, username, password, email, role="guest"):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def __str__(self):
        return f"{self.username}"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    card_cvc = db.Column(db.String(4), nullable=False)
    
    def __repr__(self):
        return f"Purchase('{self.full_name}', '{self.product_id}', '{self.date_purchased}')"
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        populate_data()

        drums = Category(name="DRUM SET")
        sticks = Category(name="STICKS")
        pedals = Category(name="DRUM PEDALS")

        admin = User(username="Gene Hogman", password="password2342", email="gene@example.com", role="admin")
        user = User(username="Dzadza", password="password23", email="dzadza@example.com")
        
        db.session.add_all([drums, sticks, pedals, user, admin])
        db.session.commit()

        products = [
            Product(name="PEARL MASTERS REFERENCE ONE", file = "Pearl_Master_Reference_One.jpg", price = 5000, description="The best elements of our original Hybrid Drum Concept deliver an expressive, wide range sonic boost with enhanced bottom-end", category=drums, folder="Drums"),
            Product(name="PEARL DECADE MAPLE", file = "Pearl_Decade_Maple.jpg", price = 5000, description="Practice time is over. It's time for the world to hear your drumming voice. Decade Maple series drums put all the vital tools in your hands for pure drumming greatness", category=drums, folder="Drums"),
            Product(name="PEARL MAPLE PURE ", file = "Pearl_Maple_Pure.jpg", price = 5000, description="In celebration of three decades of Masters quality and excellence, Pearl fuses new appointments, refreshed finish and hardware choices, and the ground-breaking resonance of the R2 Air Tom Suspension System with the original Masters MMX 4-ply, 5mm shell with 4-ply Re-Rings.", category=drums, folder="Drums"),
            Product(name="PEARL MASTERS MAPLE GUM ", file = "Pearl_Masters_Maple_Gum.jpg", price = 5000, description="Setting the standard for the very best in performance-centered instruments for the pro drummer, Pearl fuses new appointments, refreshed finish, and hardware choices, and the ground-breaking resonance of the R2 Air Tom Suspension System with the Masters Maple/Gum shell in celebration of three decades of studio drumming quality and excellence.", category=drums, folder="Drums"),
            Product(name="PEARL PROFESSIONAL MAPLE SERIES ", file = "Pearl_Professional_Maple_Series.jpg", price = 5000, description="A Tonally Sublime Playing Experience with New-School Vintage Flair.", category=drums, folder="Drums"),
            Product(name="PEARL MASTERS SERIES ", file = "Pearl_Master_Green.jpg", price = 5000, description="In celebration of three decades of Masters quality and excellence, Pearl fuses new appointments, refreshed finish, and hardware choices, and the ground-breaking resonance of the R2 Air Tom Suspension System with the history-making Masters MCX shell formula.", category=drums, folder="Drums"),
            Product(name="PRESIDENTS DELUXE ", file = "President_Deluxe.jpg", price = 5000, description="Culled from the very origins of The World's Largest Drum Company for a traditionally full, controlled playing experience", category=drums, folder="Drums"),
            Product(name="EXPORT EXX ", file = "Export.jpg", price = 5000, description="The drum set that revolutionized drumming and launched a thousand careers, Pearl's Export Series Drums are a prime percussive package for the uncompromised pro in the making!", category=drums, folder="Drums"),
            Product(name="PEARL ROADSHOW ", file = "roadshow.jpg", price = 5000, description="Regardless of when your rhythmic journey starts, Pearl's Roadshow Series has a drum set package to get you on the road to drumming greatness.", category=drums, folder="Drums"),
            Product(name="MIDTOWN SERIES", file = "midtown-series.jpg", price = 5000, description="A complete, totally portable drum set costing less than many snare drums, Pearl's Midtown Series 4-pc. kit is ideal for an on-the-go beatmaking in a platform fit for tight spaces.", category=drums, folder="Drums"),
            Product(name="SESSION STUDIO SELECT", file = "studioeffect.jpg", price = 5000, description="An elite percussion instrument ripe with vintage feel, Session Studio Select strikes a powerful musical balance between warmth and punch.", category=drums, folder="Drums"),
            Product(name="CRYSTAL BEAT", file = "crystalbeat.jpg", price = 5000, description="In celebrating 50 years of our landmark seamless Acrylic shell, Pearl presents Crystal Beat series drums in a Limited Production run of three stunning new colors.", category=drums, folder="Drums"),
            
                       
            Product(name="Vic-Firth Classic 5B",  file="classic5b.webp", price=30, description="the Classics are turned from select hickory — a dense wood with little flex for a more pronounced sound.", category=sticks, folder="Sticks"),
            Product(name="Vic-Firth Conquistador",  file="conquistador.webp", price= 35, description="Alex Acuña's timbale sticks are designed to provide optimum response on timbales and cymbals. In hickory.", category=sticks, folder="Sticks"),
            Product(name="Vic-Firth Jazz",  file="jazz5.webp", price= 35, description="Over the years and in collaboration with some of the world’s top artists, the design team at Vic has produced thousands of prototypes ranging from the highly experimental to the straight-ahead.", category=sticks, folder="Sticks"),
            Product(name="Vic-Firth Mike JohnStonne NE-1",  file="mikejohnstonne1.webp", price= 35, description="In the early 1980's, Vic and Steve Gadd began working together on a top-secret new project: a signature drumstick. A true design collaboration between two legendary world-class artists had never been done before in the drumstick industry.", category=sticks, folder="Sticks"),
            Product(name="Vic-Firth Modern Jazz",  file="modernjazz-vic.webp", price= 35, description="Over the years and in collaboration with some of the world’s top artists, the design team at Vic has produced thousands of prototypes ranging from the highly experimental to the straight-ahead.", category=sticks, folder="Sticks"),
            Product(name="Vic-Firth MS4",  file="MS4.webp", price= 35, description="In Sta-Pac for maximum strength and density. Plays through Kevlar heads for maximum snare and batter head response.", category=sticks, folder="Sticks"),
            Product(name="Vic-Firth 5A Pink",  file="nova5apink.webp", price= 35, description="Tear drop tip for rich cymbal sounds. The #1 stick in the world — great for every style of music!", category=sticks, folder="Sticks"),
            Product(name="Vic-Firth White Classic",  file="whiteclassic.webp", price= 35, description="the Classics are turned from select hickory — a dense wood with little flex for a more pronounced sound.", category=sticks, folder="Sticks"),

            Product(name="dw-2000", file="dw-2000.webp", price= 750, description="Get acquainted with DW pedals with this line of U.S.- engineered, all-metal construction bass drum pedals.W", category=pedals, folder="Pedals"),
            Product(name="dw-3000", file="dw-3000.webp", price= 900, description="A medium-weight pedal with a proven design that makes DW quality and feel available to more players.", category=pedals, folder="Pedals"),
            Product(name="dw-5000", file="dw-5000.webp", price= 900, description="The 5000 Series became the original Drummer's Choice when it changed the game decades ago. It remains revered among players today.", category=pedals, folder="Pedals"),
            Product(name="dw-6000", file="dw-6000.webp", price= 900, description="Add modern pedal features to your vintage or bop kit, while the maintaining the lightweight feel of a timeless era.", category=pedals, folder="Pedals"),
            Product(name="dw-9000", file="dw-9000.webp", price= 500 , description="DW’s flagship line of pedals delivers an unrivaled combination of feel, power, and durability through patented innovations and precise engineering.", category=pedals, folder="Pedals"),
            Product(name="dw-Machined Excellence", file="dw-mfg.webp", price= 600, description="These precision-machined pedals are handcrafted in the U.S.A. of airplane-grade materials to continue the elevation of the craft of drumming.", category=pedals, folder="Pedals"),

        ]

        db.session.add_all(products)
        db.session.commit()

