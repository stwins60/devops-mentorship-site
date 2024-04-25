from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
import re


load_dotenv()

# sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
def ValidateEmail(email):
    regrex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    email_domain = ['gmail', 'yahoo', 'hotmail', 'outlook']
    user_email_domain = email.split('@')[1]
    user_email_domain = user_email_domain.split('.')[0]
    
    if re.fullmatch(regrex, email) and user_email_domain in email_domain:
        return True
    else:
        return False
def sendMyEmail(sender, recipient, subject, name, email, content):
    # """
    # Takes in email details to send an email to whoever.
    # """
    # message = f"""Message from {fname} {lname}: \n\n{content} \n\n
    # Email: {email}
    # """
    html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f2f2f2;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                }}
                h1 {{
                    color: #333333;
                    text-align: center;
                }}
                p {{
                    color: #666666;
                    line-height: 1.6;
                }}
                .signature {{
                    text-align: right;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Hello {recipient},</h1>
                <p>This form was submitted on your website by {name}.</p>
                <p>Their message is as follows:</p>
                <p>{content}</p>
                <p>For further contact, their email is <a href="mailto:{email}">{email}</a></p>
                <div class="signature">
                    <p>Best Regards,<br/>Your Website Team</p>
                </div>
            </div>
        </body>
        </html>
    """


    # Sendgrid client
    email = Mail(
        from_email=sender,
        to_emails=recipient,
        subject=subject,
        html_content=html_content
    )
    
    # Sending the email 
    response = sg.send(email)
    
    # Returning either a successful message or not
    if response.status_code==202:
        return "Email has been accepted!"
    
    return "Email wasn't sent"

