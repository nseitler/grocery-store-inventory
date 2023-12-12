# Import libraries
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import csv
from datetime import datetime

# Initialize sqlalchemy Base
Base = declarative_base()

# Define the Brands model
class Brands(Base):
    __tablename__ = 'brands'
    brand_id = Column(Integer, primary_key=True)
    brand_name = Column(String)

    # Representation method for easier debugging
    def __repr__(self):
        return f"<Brand(brand_name={self.brand_name})>"

# Define the Product model
class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer) # Store price in cents
    date_updated = Column(Date)
    brand_id = Column(Integer, ForeignKey('brands.brand_id'))

    # Representation method for easier debugging
    def __repr__(self):
        return f"<Product(product_name={self.product_name}, product_price={self.product_price})>"

# Function to create and return a database session
def get_session():
    engine = create_engine('sqlite:///inventory.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

# Function to load CSV data into the database
def load_csv_data(session, file_name, model):
    with open(file_name) as file:
        reader = csv.reader(file)
        next(reader) # Skip header row
        for row in reader:
            # Add logic to process and add each row to the database
            pass

# Define main menu function
def main_menu(session):
    while True:
        print("Menu Options:\nV: View Product\nN: New Product\nA: Analyze\nB: Backup")
        choice = input("Enter your choice: ").upper()
        if choice == 'V':
            view_product(session)
        elif choice == 'N':
            add_new_product(session)
        elif choice == 'A':
            analyze_data(session)
        elif choice == 'B':
            backup_data()
        else:
            print("Invalid choice. Please choose V, N, A, or B.")

# Function to view a product
def view_product(session):
    while True:
        try:
            product_id = int(input("Enter the product ID to view: "))
            product = session.query(Product).filter_by(product_id=product_id).first()
            if product:
                print(f"Product ID: {product.product_id}")
                print(f"Name: {product.product_name}")
                print(f"Quantity: {product.product_quantity}")
                print(f"Price: ${product.product_price / 100:.2f}")
                print(f"Date Updated: {product.date_updated}")
                print(f"Brand ID: {product.brand_id}")
                break
            else:
                print(f"No product found with ID {product_id}. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid product ID.")


# Function to add a new product
def add_new_product(session):
    try:
        # Prompting user for product details
        product_name = input("Enter the product name: ")
        product_quantity = int(input("Enter the product quantity: "))
        product_price = float(input("Enter the product price (in dollars, e.g., 2.99): "))
        brand_name = input("Enter the brand name: ")

        # Convert price to cents
        product_price_in_cents = int(product_price * 100)

        # Find or create brand
        brand = session.query(Brands).filter_by(brand_name=brand_name).first()
        if not brand:
            brand = Brands(brand_name=brand_name)
            session.add(brand)
            session.commit()

        # Create and add new product
        new_product = Product(
            product_name=product_name, 
            product_quantity=product_quantity, 
            product_price=product_price_in_cents, 
            date_updated=datetime.now(), 
            brand_id=brand.brand_id
        )
        session.add(new_product)
        session.commit()

        print(f"Product '{product_name}' added successfully.")

    except ValueError:
        print("Invalid input. Please ensure quantities and prices are correctly formatted.")


# Function to analyze data
def analyze_data(session):
    try:
        # Find the most expensive product
        most_expensive_product = session.query(Product).order_by(Product.product_price.desc()).first()
        if most_expensive_product:
            print(f"Most Expensive Product: {most_expensive_product.product_name} at ${most_expensive_product.product_price / 100:.2f}")

        # Find the least expensive product
        least_expensive_product = session.query(Product).order_by(Product.product_price.asc()).first()
        if least_expensive_product:
            print(f"Least Expensive Product: {least_expensive_product.product_name} at ${least_expensive_product.product_price / 100:.2f}")

        # Find the brand with the most products
        most_products_brand = session.query(Brands.brand_name, func.count(Product.brand_id)).join(Product, Brands.brand_id == Product.brand_id).group_by(Brands.brand_name).order_by(func.count(Product.brand_id).desc()).first()
        if most_products_brand:
            print(f"Brand with Most Products: {most_products_brand[0]} ({most_products_brand[1]} products)")

    except Exception as e:
        print(f"An error occurred: {e}")

# Function to backup data into a CSV file
def backup_data():
    # Implement logic for data backup
    pass

# Main execution
if __name__ == '__main__':
    session = get_session()
    load_csv_data(session, 'brands.csv', Brands)
    load_csv_data(session, 'inventory.csv', Product)
    main_menu(session)
