from flask import Flask, render_template, request
import nltk

app = Flask(__name__)

# Download NLTK resources (you might need to run this in your terminal)
nltk.download('punkt')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form['question']
        # Basic NLP processing (tokenization)
        tokens = nltk.word_tokenize(question)
        response = f"Your question tokens: {', '.join(tokens)}"
        return render_template('index.html', response=response)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
