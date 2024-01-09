from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'hidden'  # Change this to a secure key in production

# Sample data
subjects = ["Introduction into AI", "Math"]


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


if __name__ == '__main__':
    app.run(debug=True)
