from django.core.mail import EmailMultiAlternatives
import os

class Util:
    @staticmethod
    def send_email(data):
        subject = data['subject']
        from_email = os.environ.get('EMAIL_FROM')
        to_email = data['to_email']
        text_content = data['body']  
        html_content = f"""
            <p>{data['body']}</p>
            
            <a href="{data['link']}">{data['link']}</a>
        """
       

        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        email.send()
