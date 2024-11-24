import uvicorn
from asgiref.wsgi import WsgiToAsgi
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, url_for, Response, abort

from flask import Flask, session, request, redirect, url_for, render_template
from sqlalchemy import create_engine, text
from datetime import timedelta

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
asgi_app = WsgiToAsgi(app)# Wrap the Flask app
app.secret_key = 'your_secret_key'  # Set a secure and unique secret key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
DATABASEURI = "postgresql://ELENDB:Ipromise12345@database-2.c9yesue8cf71.us-east-2.rds.amazonaws.com:5432/ELEN"


# This line creates a database engine that knows how to connect to the URI above.
engine = create_engine(DATABASEURI, future = true)
conn = engine.connect()

#routes#
@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/index')
def index():
  managing_results = session.get('managing_results', [])
  Customer_results = session.get('Customer_results', [])
  Product_results = session.get('Product_results', [])
  Order_results = session.get('Order_results', [])
  print(request.args)
  return render_template("index.html",managing=managing_results, customers = Customer_results\
                         ,products = Product_results, orders = Order_results)

### Manages block ###
@app.route('/all_manages_table')
def all_manages_table():
  cursor = g.conn.execute(text("SELECT * FROM Manages"))
  g.conn.commit()
  res =cursor.fetchall()
  cursor.close()
  print(res)
  return render_template("all_manages_table.html", results = res)

@app.route('/Manage_Adminid', methods=['POST'])
def Manage_Adminid(): 
  input = request.form['name']
  params_dict = {"aid":input}
  cursor = g.conn.execute(text('SELECT * FROM Manages WHERE LOWER(Admin_id) = LOWER(:aid)'), params_dict)
  g.conn.commit()
  res =cursor.fetchall()
  if res:
    managing_results = [(str(row[0]), str(row[1])) for row in res]
    session['managing_results'] = managing_results
    return redirect(url_for('index'))
  else:
    return render_template("updatefail.html")

@app.route('/Manage_product', methods=['POST'])
def Manage_product(): 
  input = request.form['name']
  params_dict = {"pdid":input}
  cursor = g.conn.execute(text('SELECT * FROM Manages WHERE LOWER(Product_id) = LOWER(:pdid)'), params_dict)
  g.conn.commit()
  res =cursor.fetchall()
  if res:
    managing_results = [(str(row[0]), str(row[1])) for row in res]
    session['managing_results'] = managing_results
    return redirect(url_for('index'))
  else:
    return render_template("updatefail.html")
### Manages block ###

### customer block ###
@app.route('/all_customer')
def all_customer():
  cursor = g.conn.execute(text("SELECT * FROM Customer"))
  g.conn.commit()
  res =cursor.fetchall()
  cursor.close()
  return render_template("all_customer.html", results = res)

@app.route('/Customer_id', methods=['POST'])
def Customer_id(): 
  input = request.form['name']
  params_dict = {"customerid":input}
  cursor = g.conn.execute(text('SELECT * FROM Customer WHERE LOWER(Customer_id) = LOWER(:customerid)'), params_dict)
  g.conn.commit()
  res =cursor.fetchall()
  if res:
    Customer_results = [(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6])) for row in res]
    session['Customer_results'] = Customer_results
    return redirect(url_for('index'))
  else:
    return render_template("updatefail.html")

@app.route('/First_name', methods=['POST'])
def First_name(): 
  input = request.form['name']
  params_dict = {"fname":input}
  cursor = g.conn.execute(text('SELECT * FROM Customer WHERE LOWER(First_name) = LOWER(:fname)'), params_dict)
  g.conn.commit()
  res =cursor.fetchall()
  if res:
    Customer_results = [(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6])) for row in res]
    session['Customer_results'] = Customer_results
    return redirect(url_for('index'))
  else:
    return render_template("updatefail.html")

@app.route('/city', methods=['POST'])
def city(): 
  input = request.form['name']
  params_dict = {"city":input}
  cursor = g.conn.execute(text('SELECT * FROM Customer WHERE LOWER(City) = LOWER(:city)'), params_dict)
  g.conn.commit()
  res =cursor.fetchall()
  if res:
    Customer_results = [(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6])) for row in res]
    session['Customer_results'] = Customer_results
    return redirect(url_for('index'))
  else:
    return render_template("updatefail.html")

@app.route('/state', methods=['POST'])
def state(): 
  input = request.form['name']
  params_dict = {"state":input}
  cursor = g.conn.execute(text('SELECT * FROM Customer WHERE LOWER(State) = LOWER(:state)'), params_dict)
  g.conn.commit()
  res =cursor.fetchall()
  if res:
    Customer_results = [(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6])) for row in res]
    session['Customer_results'] = Customer_results
    return redirect(url_for('index'))
  else:
    return render_template("updatefail.html")
### customer block ###

### product block ###
@app.route('/all_product')
def all_product():
  cursor = g.conn.execute(text("SELECT * FROM Product"))
  g.conn.commit()
  res =cursor.fetchall()
  cursor.close()
  return render_template("all_product.html", results = res)

@app.route('/Product_id', methods=['POST'])
def Product_id():
  input = request.form['name']
  params_dict = {"productid":input}
  cursor = g.conn.execute(text('SELECT * FROM Product WHERE LOWER(Product_id) = LOWER(:productid)'), params_dict)
  g.conn.commit()
  res =cursor.fetchall()
  if res:
    Product_results = [(str(row[0]), str(row[1]), str(row[2])) for row in res]
    session['Product_results'] = Product_results
    return redirect(url_for('index'))
  else:
    return render_template("updatefail.html")

@app.route('/add', methods=['POST'])
def add(): 
  input = request.form['name']
  params_dict = {"productname":input}
  cursor = g.conn.execute(text("SELECT * FROM Product WHERE LOWER(Product_name) LIKE '%' || LOWER(:productname)|| '%'"), params_dict)
  g.conn.commit()
  res =cursor.fetchall()
  if res:
    Product_results = [(str(row[0]), str(row[1]), str(row[2])) for row in res]
    session['Product_results'] = Product_results
    return redirect(url_for('index'))
  else:
    return render_template("updatefail.html")

@app.route('/Product_price', methods=['POST'])
def Product_price(): 
  low = request.form['low']
  high = request.form['high']
  params_dict = {"low": low, "high": high}
  cursor = g.conn.execute(text('SELECT * FROM Product WHERE Product_price > (:low) AND Product_price < (:high)'), params_dict)
  g.conn.commit()
  res =cursor.fetchall()
  if res:
    Product_results = [(str(row[0]), str(row[1]), str(row[2])) for row in res]
    session['Product_results'] = Product_results
    return redirect(url_for('index'))
  else:
    return render_template("updatefail.html")
### product block ###

### order block ###
@app.route('/all_order')
def all_order():
  cursor = g.conn.execute(text("SELECT A.Order_id, A.Order_amount, A.Customer_id, B.Tracking_id, B.Courier_name, C.Payment_id, D.Product_id FROM CustomerMakesOrder A, OrderHasTrackingDetail B, PaymentFormsOrder C, OrderContainsProduct D WHERE A.Order_id = B.Order_id AND B.Order_id = C.Order_id AND C.Order_id = D.Order_id"))
  g.conn.commit()
  res =cursor.fetchall()
  cursor.close()
  return render_template("all_order.html", results = res)

@app.route('/Order_id', methods=['POST'])
def Order_id(): 
  input = request.form['name']
  params_dict = {"orderid":input}
  cursor = g.conn.execute(text("SELECT A.Order_id, A.Order_amount, A.Customer_id, B.Tracking_id, B.Courier_name, C.Payment_id, D.Product_id FROM CustomerMakesOrder A, OrderHasTrackingDetail B, PaymentFormsOrder C, OrderContainsProduct D WHERE A.Order_id = B.Order_id AND B.Order_id = C.Order_id AND C.Order_id = D.Order_id AND LOWER(A.Order_id) = LOWER(:orderid)"), params_dict)
  g.conn.commit()
  res =cursor.fetchall()
  if res:
    Order_results = [(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6])) for row in res]
    session['Order_results'] = Order_results
    return redirect(url_for('index'))
  else:
    return render_template("updatefail.html")
  
@app.route('/oc_id', methods=['POST'])
def order_id(): 
  input = request.form['name']
  params_dict = {"ocid":input}
  cursor = g.conn.execute(text("SELECT A.Order_id, A.Order_amount, A.Customer_id, B.Tracking_id, B.Courier_name, C.Payment_id, D.Product_id FROM CustomerMakesOrder A, OrderHasTrackingDetail B, PaymentFormsOrder C, OrderContainsProduct D WHERE A.Order_id = B.Order_id AND B.Order_id = C.Order_id AND C.Order_id = D.Order_id AND LOWER(A.Customer_id) = LOWER(:ocid)"), params_dict)
  g.conn.commit()
  res =cursor.fetchall()
  if res:
    Order_results = [(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6])) for row in res]
    session['Order_results'] = Order_results
    return redirect(url_for('index'))
  else:
    return render_template("updatefail.html")
  
@app.route('/Tracking_id', methods=['POST'])
def Tracking_id(): 
  input = request.form['name']
  params_dict = {"tid":input}
  cursor = g.conn.execute(text("SELECT A.Order_id, A.Order_amount, A.Customer_id, B.Tracking_id, B.Courier_name, C.Payment_id, D.Product_id FROM CustomerMakesOrder A, OrderHasTrackingDetail B, PaymentFormsOrder C, OrderContainsProduct D WHERE A.Order_id = B.Order_id AND B.Order_id = C.Order_id AND C.Order_id = D.Order_id AND LOWER(B.Tracking_id) = LOWER(:tid)"), params_dict)
  g.conn.commit()
  res =cursor.fetchall()
  if res:
    Order_results = [(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6])) for row in res]
    session['Order_results'] = Order_results
    return redirect(url_for('index'))
  else:
    return render_template("updatefail.html")
### order block ###

# add product data to the database
@app.route('/addproduct', methods=['POST'])
def addproduct(): 
  product_id = request.form['product_id']
  product_name = request.form['product_name']
  product_price = request.form['product_price']
  cursor = g.conn.execute(text("SELECT * FROM Product WHERE LOWER(Product_id) = LOWER(:product_id)"), {'product_id': product_id})
  g.conn.commit()
  result = cursor.fetchone() 
  cursor.close()
  if result:
      return render_template('addfail.html')
  else:
      g.conn.execute(text("INSERT INTO Product (Product_id, Product_name, Product_price) VALUES (UPPER(:product_id), :product_name, :product_price)"),{'product_id': product_id, 'product_name': product_name, 'product_price': product_price})
      g.conn.commit()
      return redirect('/index')
  
# delete product data to the database
@app.route('/delete', methods=['POST'])
def delete(): 
  product_id = request.form['delete_product_id']
  cursor = g.conn.execute(text("SELECT * FROM Product WHERE LOWER(Product_id) = LOWER(:product_id)"), {'product_id': product_id})
  g.conn.commit()
  result = cursor.fetchone() 
  cursor.close()
  if result:
    g.conn.execute(text("DELETE FROM Product WHERE LOWER(Product_id) = LOWER(:product_id)"),{'product_id': product_id})
    g.conn.commit()
    return redirect('/index')
  else:
    return render_template('deletefail.html')

# update product data to the database
@app.route('/update', methods=['POST'])
def update(): 
  session['product_id'] = request.form['update_product_id']
  cursor = g.conn.execute(text("SELECT product_name, product_price FROM Product WHERE LOWER(Product_id) = LOWER(:product_id)"), {'product_id': session['product_id']})
  g.conn.commit()
  result = cursor.fetchone() 
  cursor.close()
  if result:
    return render_template('edit_product.html',product_name=result[0], product_price=result[1])
  else:
    return render_template('deletefail.html')
  
# edit product data to the database
@app.route('/edit_product', methods=['POST'])
def edit_product():
    product_id = session.get('product_id')
    product_name = request.form['product_name']
    product_price = request.form['product_price']
    # Update the product details
    g.conn.execute(text("UPDATE Product SET Product_name = :product_name, Product_price = :product_price WHERE LOWER(Product_id) = LOWER(:product_id)"),{'product_id': product_id, 'product_name': product_name, 'product_price': product_price})
    g.conn.commit()
    session.pop('product_id', None) # remove product id from session
    return redirect('/index')

# update tracking data to the database
@app.route('/update_tracking', methods=['POST'])
def update_tracking(): 
  session['order_id'] = request.form['update_tracking']
  cursor = g.conn.execute(text("SELECT Tracking_id, Courier_name FROM OrderHasTrackingDetail WHERE LOWER(Order_id) = LOWER(:order_id)"), {'order_id': session['order_id']})
  g.conn.commit()
  result = cursor.fetchone() 
  cursor.close()
  if result:
    return render_template('edit_tracking.html',tracking_id=result[0], courier_name=result[1])
  else:
    return render_template('tracking_fail.html')

# edit tracking data to the database
@app.route('/edit_tracking', methods=['POST'])
def edit_tracking():
  order_id = session.get('order_id')
  tracking_id = request.form['tracking_id']
  courier_name = request.form['courier_name']
  # Update the product details
  cursor = g.conn.execute(text("SELECT * FROM OrderHasTrackingDetail WHERE LOWER(Tracking_id) = LOWER(:tracking_id)"), {'tracking_id': tracking_id})
  g.conn.commit()
  result = cursor.fetchone()
  cursor.close()
  if result:
    return render_template('tracking_exist.html')
  else:
    g.conn.execute(text("UPDATE OrderHasTrackingDetail SET Tracking_id = UPPER(:tracking_id), Courier_name = :courier_name WHERE LOWER(Order_id) = LOWER(:order_id)"),{'tracking_id': tracking_id, 'courier_name': courier_name, 'order_id': order_id})
    g.conn.commit()
    session.pop('order_id', None) # remove order id from session
    return redirect('/index')

# update customer data to the database
@app.route('/update_customer', methods=['POST'])
def update_customer(): 
  session['customer_id'] = request.form['update_customer_id']
  cursor = g.conn.execute(text("""
      SELECT First_name, Last_name, City, State, Postcode, Phone 
      FROM Customer 
      WHERE LOWER(Customer_id) = LOWER(:customer_id)
  """), {'customer_id': session['customer_id']})
  g.conn.commit()
  customer = cursor.fetchone() 
  cursor.close()
  if customer:
      return render_template('edit_customer.html', first_name=customer[0], last_name=customer[1], city=customer[2], state=customer[3], postcode=customer[4], phone=customer[5])
  else:
      return render_template('update_customer_fail.html')  # Render a template that indicates the customer was not found

# edit customer data to the database
@app.route('/edit_customer', methods=['POST'])
def edit_customer():
  customer_id = session.get('customer_id')
  first_name = request.form['first_name']
  last_name = request.form['last_name']
  city = request.form['city']
  state = request.form['state']
  postcode = request.form['postcode']
  phone = request.form['phone']
  # Update the customer details
  g.conn.execute(text("""
      UPDATE Customer 
      SET First_name = :first_name, Last_name = :last_name, City = :city, State = UPPER(:state), Postcode = :postcode, Phone = :phone 
      WHERE LOWER(Customer_id) = LOWER(:customer_id)
  """), {'customer_id':  customer_id, 'first_name': first_name, 'last_name': last_name, 'city': city, 'state': state, 'postcode': postcode, 'phone': phone})
  g.conn.commit()
  session.pop('customer_id', None)  # Remove customer id from session
  return redirect('/index')  # Redirect to index page

@app.route('/orders')
def view_orders():
  cursor = g.conn.execute(text("SELECT cmo.Order_id,cmo.Order_amount,cmo.Customer_id,cmo.At as OrderDate,cmk.Payment_id,cmk.Payment_amount,cmk.At as PaymentDate,oht.Tracking_id,oht.Courier_name, \
                string_agg(p.Product_id, ', ') as Product_ids FROM CustomerMakesOrder cmo LEFT JOIN CustomerMakesPayment cmk ON cmo.Customer_id = cmk.Customer_id LEFT JOIN \
                OrderHasTrackingDetail oht ON cmo.Order_id = oht.Order_id LEFT JOIN OrderContainsProduct ocp ON cmo.Order_id = ocp.Order_id \
                LEFT JOIN Product p ON ocp.Product_id = p.Product_id GROUP BY cmo.Order_id, cmk.Payment_id, oht.Tracking_id") )
  g.conn.commit()
  results = cursor.fetchall()
  cursor.close()
  return render_template('orders.html', orders=results)

#login page
@app.route('/', methods=['GET', 'POST'])  #the main login page
def login():
  error = None
  if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      cursor = g.conn.execute(text("SELECT * FROM Users WHERE User_name = :username AND Password = :password"), {'username': username, 'password': password})
      g.conn.commit()
      result = cursor.fetchone() 
      cursor.close()
      if result:
          # Login success
          cursor = g.conn.execute(text("SELECT A.Admin_name FROM Admins A, Users U, UserHasAdmin UA \
          WHERE A.Admin_id = UA.Admin_id AND U.User_id = UA.User_id AND U.User_name = :username AND U.Password = :password"), {'username': username, 'password': password})
          #return the admin name which one user has exactly only one, bounded with user_id and admin_id
          g.conn.commit()
          names = []
          for result in cursor:
            names.append(result[0])
          cursor.close()
          Admin_name = result[0]
          return render_template('welcome.html', Admin_name=Admin_name)  # Redirect to the home page, the index page
      else:
          error = 'Invalid username or password'
  return render_template('login.html', error=error)



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python3 server.py

    Show the help text using:

        python3 server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
