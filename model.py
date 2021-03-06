import datetime
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask
db = SQLAlchemy()


class Role_ID(db.Model):
    """Role ID table."""

    __tablename__="roles"

    role_id = db.Column(db.Integer, 
                      primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    ######STATUS####### NEED TO CHECK TO SEE IF THIS IS WORKING RIGHT 6/2/17
    active = db.Column(db.Boolean())
    ######STATUS####### NEED TO CHECK TO SEE IF THIS IS WORKING RIGHT 6/2/17


class User_Roles(db.Model):

    __tablename__="user_roles"

    user_role_id = db.Column(db.Integer, 
                      primary_key=True,
                      unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.role_id', ondelete='CASCADE'))


class User(db.Model):

    __tablename__="users"

    user_id = db.Column(db.Integer(), autoincrement=True, primary_key=True, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.String(2), nullable=True)
    # Information
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    job_title = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(50), nullable=True) 
    birth_date = db.Column(db.Date(), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    phone2 = db.Column(db.String(30), nullable=True)
    company = db.Column(db.String(40), nullable=True)
    # Address
    address1 = db.Column(db.String(255), nullable=True)
    address2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(20), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    module_abbreviation =db.Column(db.String(4), nullable=True)
    ###### STATUS ####### NEED TO CHECK TO SEE IF THIS IS WORKING RIGHT 6/2/17
    active = db.Column(db.Boolean())
    ###### STATUS #######
    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())
    
    roles = db.relationship('Role_ID', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))
   
    def __repr__(self):
        return '<User user_id=%d, email=%s>' % (self.user_id, self.email)


class Product(db.Model):
    """Products Table."""

    __tablename__="product"

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_name = db.Column(db.String(), nullable=True)
    product_number = db.Column(db.String(10))
    description = db.Column(db.String(255))
    product_type = db.Column(db.String(100))
    price = db.Column(db.DECIMAL(10, 2))
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())
    module_abbreviation =db.Column(db.String(4), nullable=True)
    jobs = db.relationship('Job', backref=db.backref('product', lazy='joined'), secondary='job_product')


class Job(db.Model):

    __tablename__="jobs"

    job_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    module_abbreviation = db.Column(db.String(4), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    job_location = db.Column(db.String(100))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    customer_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    total = db.Column(db.Float(precision=10, decimal_return_scale=2, asdecimal=True))

    ######STATUS#######
    active = db.Column(db.Boolean())
    status = db.Column(db.String(20))
    date_due = db.Column(db.DateTime())
    #####STATUS#####

    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())
    received_date = db.Column(db.DateTime())

    user = db.relationship('User', backref=db.backref('user_jobs'), foreign_keys=[user_id])
    customer = db.relationship('User', backref=db.backref('customer_jobs'), foreign_keys=[customer_id])

    
class Job_Product(db.Model):

    __tablename__="job_product"

    jpid = db.Column(db.Integer, 
                      primary_key=True,
                      autoincrement=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.product_id', ondelete='CASCADE'))
    job_id = db.Column(db.Integer(), db.ForeignKey('jobs.job_id', ondelete='CASCADE'))

class Invoice_Product(db.Model):

    __tablename__="invoice_product"

    ipid = db.Column(db.Integer, 
                      primary_key=True,
                      autoincrement=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.product_id', ondelete='CASCADE'))
    invoice_id = db.Column(db.Integer(), db.ForeignKey('invoice.invoice_id', ondelete='CASCADE'))   
# ---------------------
def seed_data():

    role_1=Role_ID(name='admin', description='master')
    role_2=Role_ID(name='staff', description='staff')
    role_3=Role_ID(name='customer', description='customer')

    db.session.add_all([role_1, role_2, role_3])
    db.session.commit()

    user1=User(fname='ninja', lname="Leslie", password='1234', email='her@her.com')
    user2=User(fname='bland', lname="Ninja", password='1234', email='me@her.com')
    user3=User(fname='test', lname="tester", password='1234', email='test@her.com')

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    user_roles_admin=User_Roles(user_id=user1.user_id, role_id=role_1.role_id)
    user_roles_staff=User_Roles(user_id=user2.user_id, role_id=role_2.role_id)
    user_roles_customer=User_Roles(user_id=user3.user_id, role_id=role_3.role_id)

    db.session.add_all([user_roles_admin, user_roles_staff, user_roles_customer])
    db.session.commit()

    job_1=Job(name='project', user_id=user2.user_id, customer_id=user3.user_id, status="active")
    job_2=Job(name='big project', user_id=user2.user_id, customer_id=user3.user_id, status="quote_sent")
    job_3=Job(name='small project', user_id=user2.user_id, customer_id=user3.user_id, status="quote_requested")
    job_4=Job(name='bigger project', user_id=user2.user_id, customer_id=user3.user_id, status="invoice_sent")
    job_5=Job(name='biggest project', user_id=user2.user_id, customer_id=user3.user_id, status="completed")
    job_6=Job(name='smallest project', user_id=user2.user_id, customer_id=user3.user_id, status="active")

    db.session.add_all([job_1, job_2, job_3, job_4, job_5, job_6])
    db.session.commit()

    product_1=Product(product_number='12345678', product_name='Depends on Industry',
        price=29.96,product_type='New',description='extremely descriptive desription')
    product_2=Product(product_number='11111111', product_name='Industry Dependent',
        price=13.99,product_type='NOS',description='extremely descriptive desription')
    product_3=Product(product_number='22222222', product_name='Proprietary to Industry',
        price=23.42,product_type='New',description='extremely descriptive desription')
    product_4=Product(product_number='33333333', product_name='Proprietary Custom Job',
        price=9.99,product_type='New',description='extremely descriptive desription')
    product_5=Product(product_number='44444444', product_name='Proprietary Item',
        price=5.00,product_type='New',description='extremely descriptive desription')
    product_6=Product(product_number='42525252', product_name='Item Custom Job',
        price=3.50,product_type='Special Order',description='extremely descriptive desription')


    db.session.add_all([product_1, product_2, product_3, product_4, product_5, product_6])
    db.session.commit()

    job_product2 = Job_Product(job_id=job_1.job_id, product_id=product_1.product_id)
    job_product3 = Job_Product(job_id=job_4.job_id, product_id=product_1.product_id)
    job_product1 = Job_Product(job_id=job_3.job_id, product_id=product_1.product_id)
    job_product4 = Job_Product(job_id=job_2.job_id, product_id=product_1.product_id)
    job_product5 = Job_Product(job_id=job_5.job_id, product_id=product_1.product_id)
    job_product6 = Job_Product(job_id=job_1.job_id, product_id=product_2.product_id)

    db.session.add_all([job_product1, job_product2, job_product3, job_product4, job_product5, job_product6])
    db.session.commit()

    invoice1 = Invoice(invoice_number='23456789',invoice_created_date='2/4/17', invoice_due_date='2/28/17', modified='2/2/17', received_date='2/7/17', description='Invoice description here') 
    invoice2 = Invoice(invoice_number='98765432',invoice_created_date='8/12/17', invoice_due_date='8/28/17', modified='8/12/17', received_date='8/7/17', description='Invoice description here') 
    invoice3 = Invoice(invoice_number='55555555',invoice_created_date='10/4/17', invoice_due_date='10/28/17', modified='10/4/17', received_date='10/1/17', description='Invoice description here') 
    invoice4 = Invoice(invoice_number='23232329',invoice_created_date='3/24/17', invoice_due_date='3/28/17', modified='3/24/17', received_date='3/7/17', description='Invoice description here') 
    invoice5 = Invoice(invoice_number='28282828',invoice_created_date='7/14/17', invoice_due_date='7/28/17', modified='7/14/17', received_date='7/7/17', description='Invoice description here') 
    invoice6 = Invoice(invoice_number='37373737',invoice_created_date='6/3/17', invoice_due_date='6/28/17', modified='6/3/17', received_date='6/1/17', description='Invoice description here') 

    db.session.add_all([invoice1, invoice2, invoice3, invoice4, invoice5, invoice6])
    db.session.commit()

def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ecrm'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


class Invoice(db.Model):

    __tablename__ ="invoice"

    invoice_id = db.Column(db.Integer,
                      primary_key=True,
                      autoincrement=True)
    invoice_number = db.Column(db.String(11))
    invoice_created_date = db.Column(db.DateTime(timezone=True), default=db.func.now())
    invoice_due_date = db.Column(db.DateTime(timezone=True), default=db.func.now())
    modified = db.Column(db.DateTime())
    received_date = db.Column(db.DateTime())
    description = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
   
    # product = db.relationship('Invoice_Detail', back_populates="invoice")
    # customers = db.relationship('Customer', backref=db.backref('invoice'))


class Invoice_Detail(db.Model):

    __tablename__ ="invoice_detail"

    invoice_detail_id = db.Column(db.Integer, primary_key=True)

    # invoice_number = db.Column(db.Integer(), db.ForeignKey('invoice.invoice_number'))
    # product_number = db.Column(db.Integer(), db.ForeignKey('product.product_number'))
    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())

    # invoice = db.relationship('invoice', back_populates='products')
    # product = db.relationship('product', back_populates='invoices')



if __name__=="__main__":

    from server import app
    
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()