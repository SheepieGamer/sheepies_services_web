import random
import http.client
import requests
import smtplib
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
from dotenv import load_dotenv
load_dotenv()

import os
discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

port = 443

app = Flask(__name__)

@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/routemanager')
def routemanager():
    return render_template('routemanager.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        service = request.form['service']
        complexity = request.form['complexity']
        message = request.form['message']
        product_id = random.randint(100000, 999999)

        # Calculate base price
        basePrice = 0
        hostingPrice = 0
        if service == 'discord-bot':
            if complexity == 'starter':
                basePrice = 0
            elif complexity == 'hobbyist':
                basePrice = 5
            elif complexity == 'professional':
                basePrice = 15
            hostingPrice = 10 if request.form.get('hosting') else 0
        elif service == 'discord-server':
            if complexity == 'starter':
                basePrice = 3
            elif complexity == 'hobbyist':
                basePrice = 5
            elif complexity == 'professional':
                basePrice = 10
            hostingPrice = 10 if request.form.get('hosting') else 0
        elif service == 'minecraft-server':
            if complexity == 'starter':
                basePrice = 10
            elif complexity == 'hobbyist':
                basePrice = 15
            elif complexity == 'professional':
                basePrice = 20
            hostingPrice = 10 if request.form.get('hosting') else 0

        totalPrice = basePrice + hostingPrice

        embed = {
                "content": "<@1117914448745738444>",
                "embeds": [
                    {
                    "description": f'{name} has inquired about {service}',
                    "color": None,
                    "fields": [
                        {
                        "name": "Complexity",
                        "value": f'{complexity}',
                        },
                        {
                        "name": "Price",
                        "value": f'${totalPrice}',
                        },
                        {
                        "name": "Message",
                        "value": f'{message}',
                        },
                        {
                        "name": "Hosting",
                        "value": "Yes" if hostingPrice > 0 else "No",
                        }
                    ],
                    "author": {
                        "name": f'{name}'
                    },
                    "footer": {
                        "text": f'Product ID: {product_id}'
                    }
                    }
                ],
                "attachments": []
                }

        #requests.post(discord_webhook_url, json=embed) # type: ignore

        subject = 'Product Inquiry Confirmation'
        html = f'''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>{subject}</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; color: #333; margin: 0; padding: 0; }}
                            .container {{ width: 90%; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px; }}
                            h1 {{ color: #4a90e2; }}
                            .footer {{ margin-top: 20px; font-size: 0.9em; color: #777; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>Thank You for Your Inquiry!</h1>
                            <p>Hello {name},</p>
                            <p>Thank you for your inquiry about <strong>{service} ({complexity})</strong>. The total price is <strong>${totalPrice}</strong>.</p>
                            <p>To proceed, please join our Discord server <a href="https://discord.gg/d67SWT3JyD">here</a> and open a ticket under the "Product Inquiry" category with the product ID: <strong>{product_id}</strong>.</p>
                            <p>Best regards,<br>Sheepie</p>
                            <div class="footer">
                                <p>&copy; 2024 Sheepie's Tech Services</p>
                            </div>
                        </div>
                    </body>
                    </html>
        '''

        send_email(email, subject, name, service, complexity, totalPrice, product_id, discord_webhook_url, embed)

        return redirect(url_for('contact'))
    return render_template('contact.html')

def send_email(to_email, subject, name, service, complexity, totalPrice, product_id, url, embed):
    json_data = {
        "email": to_email,
        "subject": subject,
        "name": name,
        "service": service,
        "complexity": complexity,
        "totalPrice": totalPrice,
        "product_id": product_id
    }
    headers = {
        "Content-Type": "application/json",
    }
    # Convert JSON data to a string and then encode it to bytes
    body = json.dumps(json_data).encode('utf-8')

    conn = http.client.HTTPSConnection("sheepiestechservices.pythonanywhere.com")
    conn.request("POST", "/email", body, headers)
    response = conn.getresponse()
    print(response.read().decode("utf-8"))
    requests.post(url, json=embed)

    return

    from_email = os.getenv('FROM_EMAIL')
    from_password = os.getenv('FROM_PASSWORD')

    msg = f'Subject: {subject}\nContent-Type: text/html; charset="utf-8"\n\n{html}'

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, from_password) # type: ignore
        server.sendmail(from_email, to_email, msg) # type: ignore

if __name__ == '__main__':
    context = ('fullchain.crt', 'server.key')
    app.run(debug=False, host="0.0.0.0", port=port, ssl_context=context)