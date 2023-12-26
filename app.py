from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    selectedAPI = request.args.get('api')

    api_mapping = {
        "total": "stats/total",
        "length": "stats/length",
        "documents": "datamart",
        "search": "datamart-search",
        "recommend": "datamart-recommend",
        "frequency": "stats/datamart-frequency"
    }

    if selectedAPI in api_mapping:
        api_route = api_mapping[selectedAPI]
        api_url = f'http://localhost:8080/{api_route}/{query}'
        print(api_url)
        response = requests.get(api_url)

        results = response.json()

        return render_template('search_results.html', results=results)
    else:
        return "Opción de API no válida"


if __name__ == "__main__":
    app.run(debug=True)
