import africastalking
import os


class SMS:
    def __init__(self):
        username = os.environ.get("AFRICASTALKING_USERNAME")
        api_key = os.environ.get("AFRICASTALKING_API_KEY")

        if not username or not api_key:
            print("Africastalking credentials not found\nWill print to stdout")
            return

        self.transporter = africastalking
        self.transporter.initialize(username, api_key)

    def send(self, phone, message):
        if not self.transporter:
            print(f"Redirected SMS to StdOut {phone}\n: {message}")
            return
        
        try:
            response = self.transporter.SMS.send(message, [phone], os.environ.get("AFRICASTALKING_SENDER_ID"))
            print(response)
        except Exception as e:
            print(f"Error sending SMS to {phone}\n: {e}")
        
