from flask import Flask, render_template, request
import requests
from flask_mail import Mail, Message

app = Flask(__name__)
app.static_folder = 'static'
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
    query = query.replace(' ', '+')
    print(query)

    if ' ' not in query:
        api_url = f'http://localhost:8080/datamart/{query}'
    else:
        api_url = f'http://localhost:8080/datamart-recommend/{query}'
    
    response = requests.get(api_url)

    results = response.json()

    return render_template('search_results.html', results=results)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

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

if __name__ == "__main__":
    app.run(debug=True)
    app.static_folder = 'static'
