from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key in a production environment

users = {
    'business_owner': {'username': 'Jasmin123@gmail.com', 'password': 'Jasmin123'},
    'employee': {},
    'customer': {}
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    user_type = request.form['user_type']

    # Set the user type in the session for later use
    session['user_type'] = user_type

    if user_type == 'business_owner':
        return redirect(url_for('business_owner_login'))

    elif user_type == 'employee':
        if 'employee' not in users:
            return render_template('employee_registration.html')
        else:
            return redirect(url_for('employee_login'))

    # Check if the user is a customer and prompt for registration or login
    elif user_type == 'customer':
        if 'customer' not in users:
            return render_template('customer_registration.html')
        else:
            return redirect(url_for('customer_login'))
    return render_template('login.html')

@app.route('/employee_registration', methods=['POST'])
def employee_registration():
    # Get employee information from the registration form
    employee_name = request.form['employee_name']
    employee_email = request.form['employee_email']

    users['employee'] = {'username': employee_email, 'name': employee_name}

    return redirect(url_for('employee_dashboard'))


@app.route('/request_account', methods=['GET', 'POST'])
def request_account():
    if request.method == 'POST':
        return redirect(url_for('home'))

    return render_template('request_account.html')



@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        customer_username = request.form['customer_username']
        customer_password = request.form['customer_password']

        if 'customer' in users and users['customer']['username'] == customer_username and users['customer']['password'] == customer_password:

            session['user_type'] = 'customer'
            return redirect(url_for('customer_dashboard'))

    return render_template('customer_login.html')

@app.route('/customer_registration', methods=['GET', 'POST'])
def customer_registration():
    if request.method == 'POST':
        customer_username = request.form['customer_username']
        customer_password = request.form['customer_password']
        customer_phone = request.form['customer_phone']

        users['customer'] = {'username': customer_username, 'password': customer_password, 'phone': customer_phone}

        session['user_type'] = 'customer'

        return redirect(url_for('customer_dashboard'))

    return render_template('customer_registration.html')


@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    if request.method == 'POST':
        return redirect(url_for('employee_dashboard'))

    return render_template('employee_login.html')


@app.route('/customer_dashboard')
def customer_dashboard():
    if 'user_type' in session and session['user_type'] == 'customer':
        return render_template('customer_dashboard.html', user=users['customer'])
    else:
        return redirect(url_for('home'))

# @app.route('/business_owner_setup_account', methods=['GET', 'POST'])
# def business_owner_setup_account():
#     if request.method == 'POST':
#         # Get business owner information from the setup form
#         business_owner_username = request.form['business_owner_first_name']
#         business_owner_password = request.form['business_owner_last_name']
#         business_owner_password = request.form['business_account_type']

#         users['business_owner'] = {
#         'username': session['business_owner_username'],
#         'password': session['business_owner_password'],
#         'first_name': business_owner_first_name,
#         'last_name': business_owner_last_name,
#         'business_account_type': business_account_type
#         }

#         return redirect(url_for('business_owner_dashboard'))

#     return render_template('business_owner_setup_account.html')



@app.route('/business_owner_setup_account', methods=['GET', 'POST'])
def business_owner_setup_account():
    if 'user_type' in session and session['user_type'] == 'business_owner':
        if 'business_owner_username' in session and 'business_owner_password' in session:
            if request.method == 'POST':

                business_owner_first_name = request.form['business_owner_first_name']
                business_owner_last_name = request.form['business_owner_last_name']
                business_account_type = request.form['business_account_type']

                users['business_owner'] = {
                    'username': session['business_owner_username'],
                    'password': session['business_owner_password'],
                    'first_name': business_owner_first_name,
                    'last_name': business_owner_last_name,
                    'business_account_type': business_account_type
                }

                return redirect(url_for('business_owner_dashboard'))

            return render_template('business_owner_setup_account.html')

    return redirect(url_for('home'))

@app.route('/business_owner_login', methods=['GET', 'POST'])
def business_owner_login():
    if request.method == 'POST':
        provided_username = request.form['business_owner_username']
        provided_password = request.form['business_owner_password']


        if 'business_owner' in users and users['business_owner']['username'] == 'Jasmin123@gmail.com' and users['business_owner']['password'] == 'Jasmin123':

            session['user_type'] = 'business_owner'
            return redirect(url_for('business_owner_setup_account'))

    return render_template('business_owner_login.html')


@app.route('/business_owner_dashboard')
    if 'user_type' in session and session['user_type'] == 'business_owner':
        return render_template('business_owner_dashboard.html', user=users['business_owner'])
    else:
        return redirect(url_for('business_owner_login'))

@app.route('/employee_dashboard')
def employee_dashboard():
    return render_template('employee_dashboard.html', user=users['employee'])

# Logout route
@app.route('/logout')
def logout():
    return redirect(url_for('home'))


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
