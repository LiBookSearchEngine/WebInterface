from flask import Flask, render_template, request, session, redirect, url_for, make_response, send_file, flash
import requests
from flask_mail import Mail, Message
import json


app = Flask(__name__)
app.static_folder = 'static'

mail = Mail(app)
ip_nginx=""
ip_server="34.16.163.134"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search-by-author')
def select_by_author():
    return render_template('select-by-author.html')

@app.route('/search-by-language')
def select_by_language():
    return render_template('select-by-language.html')

@app.route('/search-by-author')
def search_by_author():
    return render_template('search-by-author.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        flash('Error: The search field is empty. Please enter a query.', 'error')
        return redirect(url_for('index'))
    
    query_list = query.split()    

    if len(query_list) == 1:
        api_url = f'http://{ip_nginx}:8080/datamart/{query}'
    else:
        query = query.replace(' ', '+')
        api_url = f'http://{ip_nginx}:8080/datamart-recommend/{query}'
    
    response = requests.get(api_url)

    results = response.json()
    transformed_data = transform(results)
    print(transformed_data)

    return render_template('search_results.html', results=transformed_data,json_dumps=json.dumps)

@app.template_filter('tojson')
def tojson_filter(obj):
    return json.dumps(obj)

@app.route('/book-details/<book_id>')
def book_details():
    book_json = request.args.get('book')
    if book_json:
        book = json.loads(book_json)
    else:
        book = None
    return render_template('book_details.html', book=book)


def transform(results):
    transformed_data = []

    for item in results:
        for key, value in item.items():
            value['id']=key
            transformed_data.append(value)

    return transformed_data

@app.route('/search-author')
def search_author():
    author = request.args.get('query')

    api_url = f'http://{ip_nginx}:8080/metadata/author/{author}'
    response = requests.get(api_url)
    results = response.json()
    return render_template('metadata_results.html', results=results,  author=author)

@app.route('/search-language')
def search_language():
    language = request.args.get('query')

    api_url = f'http://{ip_nginx}:8080/metadata/language/{language}'
    response = requests.get(api_url)
    results = response.json()
    return render_template('metadata_results.html', results=results,  language=language)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        url = f'http://{ip_server}/user/login?username={username}&password={password}'

        response = requests.get(url)

        session_id = response.cookies.get('Session')
        session['session_id'] = session_id
        if response.status_code == 200:

            session['username'] = username
            response = make_response(redirect(url_for('index')))
            return response

        else:
            error_message = 'Incorrect credentials. Please try again.'

    return render_template('login.html', error=error_message if 'error_message' in locals() else None)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        name = request.form['name']
        language = request.form['language']
        date = request.form['date']
        status = request.form['status']
        txt_file = request.files['txt']

        txt_content = ""
        if txt_file:
            txt_content = txt_file.read().decode('utf-8')


        api_url =f'http://{ip_server}/user/post'
        params = f"?name={name}&language={language}&date={date}&status={status}"
        response = requests.post(api_url + params, cookies={'Session': session['session_id']})

        if response.status_code == 200:
            return user_books()
        
    else:
        return user_books()
    
def user_books():
    api_url = f'http://{ip_server}/user/books'
    response = requests.get(api_url, cookies={'Session': session['session_id']})

    if response.status_code == 200:
        data = response.json()
        return render_template('profile.html', data=data)
    else:
        return "Error getting data from the API"

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg_to_company = Message('New message', sender=email, recipients=['arduinoalumnos2023@gmail.com'])
        msg_to_company.body = f'Name: {name}\nEmail address: {email}\Message:\n{message}'
        mail.send(msg_to_company)

        msg_to_user = Message('Confirmation of message sent', sender='arduinoalumnos2023@gmail.com', recipients=[email])
        msg_to_user.body = 'Thank you for contacting us. We have received your message and will get back to you soon.'
        mail.send(msg_to_user)

        return redirect(url_for('index')) 
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if len(password) < 8:
            error = 'Password must be at least 8 characters long.'
        elif password != confirm_password:
            error = 'Passwords do not match. Please try again.'
        else:
            url = f'http://{ip_server}/user/sign-up?username={username}&password={password}'
            response = requests.get(url)

            if response.status_code == 200:
                message = 'Correctly registered'
            else:
                error = 'Registration failed. Please try again.'
            
    return render_template('register.html', error=error, message=message)

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    session.pop('username', None)
    response.delete_cookie('Session')

    url = f'http://{ip_server}/user/logout'
    requests.get(url)

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    app.static_folder = 'static'