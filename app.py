from flask import Flask, render_template, request
import requests

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    query = query.replace(' ', '+')

    if ' ' not in query:  # Verifica si la consulta es una sola palabra
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

if __name__ == "__main__":
    app.run(debug=True)
    app.static_folder = 'static'
