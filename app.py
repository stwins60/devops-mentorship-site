from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
import requests
import markdown
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
import secrets
import json
import mailer
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
import sentry_sdk

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = secrets.token_hex(16)

headers = {
    # 'Content-Type': 'text/html',
    'charset': 'utf-8',
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
}

sentry_sdk.init(
    dsn="https://a8a5fcb0b16a61bc009c9d3d2c11ea16@sentry.africantech.dev/6",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    integrations = [
        AsyncioIntegration(),
        FlaskIntegration(
            transaction_style="url"
        ),
        AioHttpIntegration(
            transaction_style="method_and_path_pattern"
        )
    ]
)

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

with open('cicd.json', 'r') as file:
    cicd = json.load(file)

with open('jenkins.json', 'r') as file:
    jenkins = json.load(file)

with open('ansible.json', 'r') as file:
    ansible = json.load(file)



@app.route('/')
def index():
    courses = {
        'Linux': [
            '00',
            '01',
            '02',
            '03',
            '04',
            '05',
            '06',
            '07',
            '08',
            '09',
            '10',
            '11',
            '12',
            '13',
            '14',
            '15',
            '16',
            '17',
            '18',
            '19',
            '20',
            '21'
        ],
        'Bash-Scripting': list(shellscript.keys()),
        'Python': list(python.keys()),
        'Docker': list(docker.keys()),
        'Kubernetes': list(kubernetes.keys()),
        'AWS': list(aws.keys()),
        'Terraform': list(terraform.keys()),
        'CICD': list(cicd.keys()),
        'Jenkins': list(jenkins.keys()),
        'Ansible': list(ansible.keys())
    }
    return render_template('index.html', courses=courses)

# def cour

@app.route('/courses/search/', methods=['GET', 'POST'])
def course_search():
    choices = [
        "Linux", "Bash Scripting", "Python", "Docker", "Kubernetes", "CI/CD", "AWS", "Terraform", "Jenkins", "Ansible"
    ]
    selected_course = "Linux"
    html_content = ""
    result = ""
    
    try:
        if request.method == 'POST':
            lab_number = request.form.get('lab-number')
            selected_course = request.form.get('search-term')
            if selected_course == "Linux":
                BASE_URL = "https://raw.githubusercontent.com/livialima/linuxupskillchallenge/master/docs/"
                response = requests.get(f"{BASE_URL}{lab_number}.md")
                if response.status_code == 200:
                    content = response.text
                    html_content = markdown.markdown(content)
                else:
                    result = "Course not found"
            elif selected_course == "Bash Scripting":
                if isinstance(shellscript, dict):
                    question = shellscript.get(lab_number, "Lab not found").get('question', "Lab not found")
                    html_content = markdown.markdown(question)
                else:
                    html_content = markdown.markdown("<h1>Lab not found</h1>")

            elif selected_course == "Python":
                question = python.get(lab_number, "Lab not found").get('question', "Lab not found")
                html_content = markdown.markdown(question)
            
            elif selected_course == "Docker":
                question = docker.get(lab_number, "Lab not found").get('question', "Lab not found")
                html_content = markdown.markdown(question)
            
            elif selected_course == "Kubernetes":
                question = kubernetes.get(lab_number, "Lab not found").get('question', "Lab not found")
                html_content = markdown.markdown(question)
            
            elif selected_course == "AWS":                
                question = aws.get(lab_number, "Lab not found").get('question', "Lab not found")
                html_content = markdown.markdown(question)
            
            elif selected_course == "Terraform":
                question = terraform.get(lab_number, "Lab not found").get('question', "Lab not found")
                html_content = markdown.markdown(question)
            elif selected_course == "CI/CD":
                question = cicd.get(lab_number, "Lab not found").get('question', "Lab not found")
                html_content = markdown.markdown(question)
            elif selected_course == "Jenkins":
                question = jenkins.get(lab_number, "Lab not found").get('question', "Lab not found")
                html_content = markdown.markdown(question)
            elif selected_course == "Ansible":
                question = ansible.get(lab_number, "Lab not found").get('question', "Lab not found")
                html_content = markdown.markdown(question)

            else:
                result = "Course not found"
    except Exception as e:
        print(e)
        html_content = markdown.markdown("<h1>Lab not found</h1>")
      
          
    return render_template('course_search.html', choices=choices, selected_course=selected_course, html_content=html_content, result=result)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        if not name or not email or not message:
            return render_template('contact.html', error='Please fill in all fields', success=msg)
        else:
            try:
                if mailer.ValidateEmail(email):
                    subject = 'Message from DevOps Mentorship Site'
                    mailer.sendMyEmail('idrisniyi94@gmail.com', 'idrisniyi94@gmail.com',
                                        subject, name, email, message)
                    return render_template('contact.html', success='Your message has been sent', error=msg)
                else:
                    return render_template('contact.html', error='Please enter a valid email', success=msg)
            except Exception as e:
                return render_template('contact.html', error='Something went wrong', success=msg)
    return render_template('contact.html')


@app.after_request
def add_header(response):
    for key, value in headers.items():
        response.headers[key] = value
    return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(504)
def gateway_timeout(e):
    return render_template('504.html'), 504