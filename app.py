from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    test_string = request.form['test_string']
    regex_pattern = request.form['regex_pattern']
    
    matches = re.finditer(regex_pattern, test_string)
    highlighted_string = highlight_matches(test_string, matches)
    
    return render_template('result.html', highlighted_string=highlighted_string)

def highlight_matches(test_string, matches):
    highlighted_string = test_string
    offset = 0
    for match in matches:
        start, end = match.span()
        highlighted_string = highlighted_string[:start + offset] + '<span class="highlight">' + \
                             highlighted_string[start + offset:end + offset] + '</span>' + \
                             highlighted_string[end + offset:]
        offset += len('<span class="highlight"></span>')
    return highlighted_string

@app.route('/validate-email', methods=['POST'])
def validate_email():
    email = request.form['email']
    if re.match(r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        result = 'Valid email address'
        valid = True
    else:
        result = 'Invalid email address'
        valid = False
    return render_template('index.html', result=result, valid=valid)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
