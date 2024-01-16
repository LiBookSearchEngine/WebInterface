from flask import Flask, render_template, request, session, redirect, url_for, make_response
import requests
from flask_mail import Mail, Message
import fitz 
import json
import openai

app = Flask(__name__)
api_key = "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"
app.static_folder = 'static'
app.secret_key = 'your_secret_key'
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = 'arduinoalumnos2023@gmail.com'
app.config['MAIL_PASSWORD'] = 'ardualu23'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    query_list = query.split()    

    if len(query_list) == 1:
        print('no relevant_words')
        api_url = f'http://localhost:8080/datamart/{query}'
    else:
        query = query.replace(' ', '+')
        relevant_words = relevant_text(query)
        print(relevant_words)
        print('relevant_words')
        query = relevant_words.replace(' ', '+')
        api_url = f'http://localhost:8080/datamart-recommend/{query}'
    
    response = requests.get(api_url)

    results = response.json()

    return render_template('search_results.html', results=results)

def relevant_text(phrase):
    phrase = phrase.replace('+', ' ')
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=phrase,
        max_tokens=50, 
        n=1, 
        stop=None 
    )

    if response.choices:
        print(response.choices[0].text.strip())
        return response.choices[0].text.strip()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        url = f'http://34.125.120.252/user/login?username={username}&password={password}'

        response = requests.get(url)

        session_id = response.cookies.get('Session')
        session['session_id'] = session_id

        with open('session.txt', 'w') as f:
            f.write(session_id)

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
        pdf = request.files['pdf']

        pdf_content = ""
        if pdf:
            pdf_data = pdf.read()
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            for page_num in range(len(doc)):
                page = doc[page_num]
                pdf_content += page.get_text()

        data = {'name': name, 'language': language, 'date': date, 'status': status, 'conntent': pdf_content}


        api_url ='http://34.125.120.252/user/post'
        response = requests.post(api_url,
                                 data=json.dumps(data))

        if response.status_code == 200:
            data = response.json()
            return render_template('profile.html', data=data)
        else:
            return "Error getting data from the API"
    else:
        api_url = 'http://34.125.120.252/user/books'
        response = requests.get(api_url, cookies={'Session': session['session_id']})

        if response.status_code == 200:
            data = response.json()
            print(data)
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
            url = f'http://34.125.120.252/user/sign-up?username={username}&password={password}'
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

    url = f'http://34.125.120.252/user/logout'
    requests.get(url)

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
    app.static_folder = 'static'