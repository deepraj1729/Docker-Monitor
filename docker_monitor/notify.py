import sendgrid
from docker_monitor.credentials import SEND_GRID_API_KEY
from sendgrid.helpers.mail import *

class SendGridEmail:
    def __init__(self,from_,to_,subject,body):
        self.from_ = from_
        self.to_ = to_
        self.subject = subject
        self.body = body

        
    def send(self):
        sg = sendgrid.SendGridAPIClient(api_key=SEND_GRID_API_KEY)
        from_email = Email(self.from_)
        subject = self.subject
        body = self.body
        content = Content("text/plain",body)

        try:
            for reciever in self.to_:
                to_email = To(reciever)
                mail = Mail(from_email,to_email,subject,content)
                response = sg.client.mail.send.post(request_body=mail.get())
                
                if response.status_code >=200 and response.status_code <=299:
                    print("     EMAIL STATUS: SUCCESS.")
                    print(f"     EMAIL successfully sent to: {reciever}\n")
                else:
                    print("     EMAIL STATUS: Something Went Wrong.")

        except Exception as e:
            exit()