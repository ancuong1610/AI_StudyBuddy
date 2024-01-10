from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from transformers import pipeline
from nltk import sent_tokenize
import fitz

app = Flask(__name__)
app.secret_key = 'hidden'

# Sample data
subjects = ["Introduction into AI", "Math"]

# Initialize BERT summarization pipeline
bert_summarizer = pipeline("summarization")

# Initialize BERT question generation pipeline
bert_qa_generator = pipeline("text2text-generation", model="t5-base", revision="686f1db", tokenizer="t5-base")


@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        student_name = request.form['student_name']
        session['student_name'] = student_name
        return redirect(url_for('home'))
    return render_template('welcome.html')


@app.route('/home', methods=['GET'])
def home():
    student_name = session.get('student_name', 'Guest')
    return render_template('home.html', student_name=student_name, subjects=subjects)


@app.route('/add_subject', methods=['GET', 'POST'])
def add_subject():
    if request.method == 'POST':
        subject_name = request.form['subject_name']
        subjects.append(subject_name)
        return redirect(url_for('home'))
    return render_template('add_subject.html')


@app.route('/subject/<subject>',methods=['GET','POST'])
def subject(subject):
    return render_template('subject.html',subject_name = subject)


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if request.method == 'POST':
        # Get the uploaded file from the request
        pdf_file = request.files['pdf_file']

        # Check if the file is a PDF
        if pdf_file and pdf_file.filename.endswith('.pdf'):
            # Read the PDF content
            pdf_content = read_pdf(pdf_file)

            # Use BERT for summarization
            summary = bert_summarizer(pdf_content, max_length=1000, min_length=50, length_penalty=2.0, num_beams=4)

            print(summary)

            # Use BERT for question generation
            questions = generate_questions(summary[0]['summary_text'])

            # Render the results in the subject.html template
            return jsonify({'summary': summary[0]['summary_text']})

    # Redirect to the home page if there's an issue
    return redirect(url_for('home'))

def generate_questions(text):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Generate questions for each sentence using BERT
    questions = bert_qa_generator(text)

    # Extract the generated questions
    return questions


def read_pdf(pdf_file):
    # Use PyMuPDF to read the content of the PDF
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    pdf_content = ""
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        pdf_content += page.get_text()

    return pdf_content


if __name__ == '__main__':
    app.run(debug=True)
