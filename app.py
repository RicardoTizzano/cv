from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from twilio.rest import Client
import os

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
app.config['SECRET_KEY'] = 'some random string'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact_post',methods = ["GET", "POST"])
def send():
    if request.method=='GET':
        name   = request.args.get('name')
        email  = request.args.get('email')
        message= request.args.get('message')
        
        # Mensaje de devolución al contacto
        msg = Message(subject='Contacto de Ricardo Tizzano', 
                    sender='ricardotizzano@gmail.com', 
                    recipients=[email])
        
        #msg.body = "Hola! He recibido tu mail y en breve me comunicaré contigo. Muchas gracias."
        msg.html = render_template('mail.html', name=name)
        mail.send(msg)

        # Mensaje avisando del contacto 
        msg = Message(subject='Recibiste un contacto de ' + name, 
                    sender='ricardotizzano@gmail.com', 
                    recipients=['ricardotizzano@gmail.com'])
        
        msg.body = message + 'El mail es ' + email
        mail.send(msg)
        enviado = "Mensaje enviado!"
        flash(enviado)

        # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
        client = Client()

        # this is the Twilio sandbox testing number
        from_whatsapp_number='whatsapp:+14155238886'
        # replace this number with your own WhatsApp Messaging number
        to_whatsapp_number='whatsapp:+34685775008'

        client.messages.create(body='Te envió un mensaje '+name + ' que dice: '+ message + 
                               ' .El mail es ' + email,
                            from_=from_whatsapp_number,
                       to=to_whatsapp_number)
        
    return redirect(url_for("index",_anchor="contact"))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
