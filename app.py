from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
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
        
        msg.body = "Hola! He recibido tu mail y en breve me comunicaré contigo. Muchas gracias."
        mail.send(msg)

        # Mensaje avisando del contacto 
        msg = Message(subject='Recibiste un contacto de ' + name, 
                    sender='ricardotizzano@gmail.com', 
                    recipients=['ricardotizzano@gmail.com'])
        
        msg.body = message
        mail.send(msg)
        enviado = "Mensaje enviado!"
        flash(enviado)
    return redirect(url_for("index",_anchor="contact"))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
