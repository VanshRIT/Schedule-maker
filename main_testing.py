import csv
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/search', methods=['GET'])
def search():
    input_value = request.args.get('input_value')
    results = get_search_results(input_value)
    return jsonify(results)

def get_search_results(input_value):
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        results = []
        for row in reader:
            my_string = row[2]
            my_string = str(my_string) if my_string is not None else ""
            if input_value in my_string:
                results.append(row[2])
        return results


if __name__ == '__main__':
    app.run(debug=True)
