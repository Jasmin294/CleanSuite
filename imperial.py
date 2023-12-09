from flask import Flask, render_template, request, redirect, url_for, session
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {
    'business_owner': {'username': 'Jasmin123@gmail.com', 'password': 'Jasmin123'},
    'employee': {},
    'customer': {}
}


pending_employee_requests = []

employees = {}

booking_requests = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    user_type = request.form['user_type']

    session['user_type'] = user_type

    if user_type == 'business_owner':
        return redirect(url_for('business_owner_login'))

    elif user_type == 'employee':
        if 'employee' not in users:
            return render_template('employee_registration.html')
        else:
            return redirect(url_for('employee_login'))

    elif user_type == 'customer':
        if 'customer' not in users:
            return render_template('customer_registration.html')
        else:
            return redirect(url_for('customer_login'))
    return render_template('login.html')

@app.route('/employee_registration', methods=['POST'])
def employee_registration():
    employee_name = request.form['employee_name']
    employee_email = request.form['employee_email']

    pending_employee_requests.append({'name': employee_name, 'email': employee_email})

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
            # Set user type in session
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
    # Check if the user is logged in
    if 'user_type' in session and session['user_type'] == 'customer':
        return render_template('customer_dashboard.html', user=users['customer'])
    else:
        return redirect(url_for('home'))



@app.route('/book/<time>', methods=['GET'])
def book(time):
    if 'user_type' in session and session['user_type'] == 'customer':
        customer_info = users.get('customer', {})
        if 'username' in customer_info:
            business_account_type = users.get('business_owner', {}).get('business_account_type', 'Basic')
            booking_info = {
                'time': time,
                'customer_username': customer_info['username'],
            }
            if business_account_type == 'Basic':
                basic_booking_logic(booking_info)
            elif business_account_type == 'Premium':
                premium_booking_logic(booking_info)

            return render_template('booking_successful.html', booking_info=booking_info)
    return redirect(url_for('home'))

def setup_business_owner_account(form_data):
    business_owner_first_name = form_data['business_owner_first_name']
    business_owner_last_name = form_data['business_owner_last_name']
    business_account_type = form_data['business_account_type']

    # Store business owner information in the users dictionary
    users['business_owner'] = {
        'username': 'Jasmin123@gmail.com',
        'password': 'Jasmin123',
        'first_name': business_owner_first_name,
        'last_name': business_owner_last_name,
        'business_account_type': business_account_type
    }

    return business_account_type

@app.route('/business_owner_setup_account', methods=['GET', 'POST'])
def business_owner_setup_account():
    if 'user_type' in session and session['user_type'] == 'business_owner':
        if request.method == 'POST':
            business_account_type = setup_business_owner_account(request.form)

            if business_account_type == 'Basic':
                employees_list = [(username, 'Active' if data.get('active') else 'Inactive') for username, data in employees.items()]
                booking_requests_list = list(booking_requests.keys())
                return render_template('business_owner_basic_welcome.html', user=users['business_owner'], employees_list=employees_list, booking_requests_list=booking_requests_list)

            elif business_account_type == 'Premium':
                employees_list = [(username, 'Active' if data.get('active') else 'Inactive', data.get('location', 'Not available')) for username, data in employees.items()]
                booking_requests_list = list(booking_requests.keys())

                return render_template('business_owner_premium_welcome.html', user=users['business_owner'], employees_list=employees_list, booking_requests_list=booking_requests_list)

            return render_template('business_owner_dashboard.html', user=users['business_owner'])

        return render_template('business_owner_setup_account.html')

    return redirect(url_for('business_owner_login'))

def send_notification_to_business_owner(employee_name, employee_email):
    print(f"New employee registration request:\nName: {employee_name}\nEmail: {employee_email}")


@app.route('/business_owner_login', methods=['GET', 'POST'])
def business_owner_login():
    if request.method == 'POST':
        provided_username = request.form['business_owner_username']
        provided_password = request.form['business_owner_password']

        if 'business_owner' in users and users['business_owner']['username'] == 'Jasmin123@gmail.com' and users['business_owner']['password'] == 'Jasmin123':
            # Set user type in session
            session['user_type'] = 'business_owner'
            return redirect(url_for('business_owner_setup_account'))

    return render_template('business_owner_login.html')

@app.route('/business_owner_dashboard')
def business_owner_dashboard():
    if 'user_type' in session and session['user_type'] == 'business_owner':
        return render_template('business_owner_dashboard.html', user=users['business_owner'], pending_employee_requests=pending_employee_requests)
    else:
        return redirect(url_for('business_owner_login'))




@app.route('/process_employee_request/<username>/<action>')
def process_employee_request(username, action):
    if action == 'accept':
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        employees[username] = {
            'username': username,
            'password': password,
            'active': False,
        }
    pending_employee_requests[:] = [req for req in pending_employee_requests if req['email'] != username]

    return redirect(url_for('business_owner_dashboard'))

    if username in employees:
        del employees[username]

    return redirect(url_for('business_owner_setup_account'))


@app.route('/process_booking_request/<customer_username>/<action>')
def process_booking_request(customer_username, action):
    if action == 'accept':
        if customer_username in booking_requests:
            del booking_requests[customer_username]

    elif action == 'deny':
        if customer_username in booking_requests:
            del booking_requests[customer_username]

    return redirect(url_for('business_owner_dashboard'))

@app.route('/employee_dashboard')
def employee_dashboard():
    return render_template('employee_dashboard.html', user=users['employee'])

@app.route('/employee_registration_success')
def employee_registration_success():
    return render_template('employee_registration_success.html', name=employee_name)

@app.route('/logout')
def logout():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

