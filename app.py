# Import libraries
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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
def main_menu():
    while True:
        print("Menu Options:\nV: View Product\nN: New Product\nA: Analyze\nB: Backup")
        choice = input("Enter your choice: ").upper()
        if choice == 'V':
            view_product()
        elif choice == 'N':
            add_new_product()
        elif choice == 'A':
            analyze_data()
        elif choice == 'B':
            backup_data()
        else:
            print("Invalid choice. Please choose V, N, A, or B.")

# Function to view a product
def view_product():
    # Implement logic to view a product
    pass

# Function to add a new product
def add_new_product():
    # Implement logic to add a new product
    pass

# Function to analyze data
def analyze_data():
    # Implement logic for data analysis
    pass

# Function to backup data into a CSV file
def backup_data():
    # Implement logic for data backup
    pass

# Main execution
if __name__ == '__main__':
    session = get_session()
    load_csv_data(session, 'brands.csv', Brands)
    load_csv_data(session, 'inventory.csv', Product)
    main_menu()
