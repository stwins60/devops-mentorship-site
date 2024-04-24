from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
import requests
import markdown
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
import secrets
import json


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = secrets.token_hex(16)


class CourseForm(FlaskForm):
    course = SelectField('Course', choices=[('linux', 'Linux'), ('bash-scripting', 'Bash Scripting'), ('python', 'Python'), ('docker', 'Docker'),
                                            ('kubernetes', 'Kubernetes'), ('git', 'Git'), ('ci-cd', 'CI/CD'), ('aws', 'AWS'),
                                            ('terraform', 'Terraform'), ('Jenkins', 'Jenkins'), ('ansible', 'Ansible')])
    course_number = IntegerField('Enter Course Number')
    submit = SubmitField('Search')


with open('shellscript.json', 'r') as file:
    shellscript = json.load(file)
    
with open('python.json', 'r') as file:
    python = json.load(file)
    
with open('docker.json', 'r') as file:
    docker = json.load(file)
    
with open('kubernetes.json', 'r') as file:
    kubernetes = json.load(file)
    
with open('aws.json', 'r') as file:
    aws = json.load(file)
    
with open('terraform.json', 'r') as file:
    terraform = json.load(file)

@app.route('/')
def index():
    return render_template('index.html')

# def cour

@app.route('/courses/search/', methods=['GET', 'POST'])
def course_search():
    choices = [
        "Linux", "Bash Scripting", "Python", "Docker", "Kubernetes", "Git", "CI/CD", "AWS", "Terraform", "Jenkins", "Ansible"
    ]
    selected_course = "Linux"
    html_content = ""
    
    try:
        if request.method == 'POST':
            selected_course = request.form.get('search-term')
            if selected_course == "Linux":
                lab_number = request.form.get('lab-number')
                BASE_URL = "https://raw.githubusercontent.com/livialima/linuxupskillchallenge/master/docs/"
                response = requests.get(f"{BASE_URL}{lab_number}.md")
                if response.status_code == 200:
                    content = response.text
                    html_content = markdown.markdown(content)
                else:
                    result = "Course not found"
            elif selected_course == "Bash Scripting":
                if isinstance(shellscript, dict):
                    lab_number = request.form.get('lab-number')
                    question = shellscript.get(lab_number, "Lab not found").get('question', "Lab not found")
                    html_content = markdown.markdown(question)
                else:
                    html_content = markdown.markdown("<h1>Lab not found</h1>")

            elif selected_course == "Python":
                lab_number = request.form.get('lab-number')
                question = python.get(lab_number, "Lab not found").get('question', "Lab not found")
                html_content = markdown.markdown(question)
            
            elif selected_course == "Docker":
                lab_number = request.form.get('lab-number')
                question = docker.get(lab_number, "Lab not found").get('question', "Lab not found")
                html_content = markdown.markdown(question)
            
            elif selected_course == "Kubernetes":
                lab_number = request.form.get('lab-number')
                question = kubernetes.get(lab_number, "Lab not found").get('question', "Lab not found")
                html_content = markdown.markdown(question)
            
            elif selected_course == "AWS":
                lab_number = request.form.get('lab-number')
                question = aws.get(lab_number, "Lab not found").get('question', "Lab not found")
                html_content = markdown.markdown(question)
            
            elif selected_course == "Terraform":
                lab_number = request.form.get('lab-number')
                question = terraform.get(lab_number, "Lab not found").get('question', "Lab not found")
                html_content = markdown.markdown(question)
            
            else:
                result = "Course not found"
    except Exception as e:
        print(e)
        html_content = markdown.markdown("<h1>Lab not found</h1>")
      
          
    return render_template('course_search.html', choices=choices, selected_course=selected_course, html_content=html_content)

@app.route('/courses/linux/')
def linux_course(course_number):
    if request.method == 'POST':
        course_number = request.form['course']
        BASE_URL = "https://raw.githubusercontent.com/livialima/linuxupskillchallenge/master/docs/"
        response = requests.get(f"{BASE_URL}{course_number}.md")

        if response.status_code == 200:
            content = response.text
            html_content = markdown.markdown(content)

            return redirect(url_for('course', course=course_number))
        else:
            return "Course not found", 404
    return render_template('course-search.html')
    
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')