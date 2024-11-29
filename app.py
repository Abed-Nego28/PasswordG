from flask import Flask, render_template, request, redirect, url_for, session
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  
# Utilisateurs fictifs (pour simplifier)
users = {
    "admin": "password123",  
}

def generate_password(length=12, use_uppercase=True, use_digits=True, use_special_chars=True):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if use_uppercase else ''
    digits = string.digits if use_digits else ''
    special = string.punctuation if use_special_chars else ''
    all_chars = lower + upper + digits + special

    if length < 4 or not all_chars:
        raise ValueError("Invalid password configuration")

    password = []
    if use_uppercase:
        password.append(random.choice(upper))
    if use_digits:
        password.append(random.choice(digits))
    if use_special_chars:
        password.append(random.choice(special))
    password.append(random.choice(lower))
    password += random.choices(all_chars, k=length - len(password))
    random.shuffle(password)
    return ''.join(password)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['user'])

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        try:
            length = int(request.form['length'])
            use_uppercase = 'uppercase' in request.form
            use_digits = 'digits' in request.form
            use_special_chars = 'special_chars' in request.form
            password = generate_password(length, use_uppercase, use_digits, use_special_chars)
            return render_template('generate.html', password=password)
        except ValueError as e:
            return render_template('generate.html', error=str(e))
    return render_template('generate.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html', username=session['user'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if username in users:
            return render_template('register.html', error="Username already exists")
        users[username] = {'email': email, 'password': password}
        return redirect(url_for('login'))
    return render_template('register.html')
import requests



UNSPLASH_API_KEY = "N_VVeRrkRRhEyef7kMyENgreznxfwvyfHrZNMKVYeKM" 
@app.route('/image', methods=['GET', 'POST'])
@app.route('/generate_image', methods=['POST'])
def generate_image():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    keyword = request.form.get('keyword', None)
    if not keyword:
        error = "Keyword is required to search for an image."
        return render_template('dashboard.html', error=error, username=session['user'])
    
    url = f"https://api.unsplash.com/photos/random?query={keyword}&client_id={UNSPLASH_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifier si la requête a réussi
        data = response.json()
        
        # Vérifier si la réponse contient des images
        if isinstance(data, list) and len(data) > 0:
            image_url = data[0].get('urls', {}).get('regular', None)
            if image_url:
                return render_template('dashboard.html', image_url=image_url, keyword=keyword, username=session['user'])
            else:
                error = "Image URL not found in the response."
                return render_template('dashboard.html', error=error, username=session['user'])
        else:
            error = "No images found for the given keyword."
            return render_template('dashboard.html', error=error, username=session['user'])
    except requests.exceptions.RequestException as e:
        error = f"An error occurred: {str(e)}"
        return render_template('dashboard.html', error=error, username=session['user'])


if __name__ == '__main__':
    app.run(debug=True)
