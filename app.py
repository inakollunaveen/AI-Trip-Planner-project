from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to the database
def get_db():
    conn = sqlite3.connect('login.db')
    return conn

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the form data
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if the user already exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user:
            flash('Username already exists! Please login.', 'error')
            return redirect(url_for('login'))  # Redirect to login page if the username exists
        
        # Insert new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        
        flash('Signup successful! You can now log in.', 'success')
        return redirect(url_for('login'))  # Redirect to login page after successful signup
    
    return render_template('signup.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    destination = request.args.get('destination')  # Get the destination from the URL
    if destination:
        flash(f"Please log in and select {destination} in the menu.", 'info')  # Flash the message
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if the username and password match
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        
        if user:
            session['user'] = username  # Save the username in the session to track logged in user
            return redirect(url_for('trip_planner'))
        else:
            flash('Invalid login credentials. Please try again.', 'error')
    
    return render_template('login.html')

# Trip Planner Route (Only accessible after login)
@app.route('/trip_planner', methods=['GET', 'POST'])
def trip_planner():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Redirect to the trip page after the user submits the trip plan
        return redirect(url_for('trip_page'))

    return render_template('trip_planner.html')

# Trip Page Route (Shows the submitted trip details)
@app.route('/trip_page')
def trip_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Rendering the already designed trip page template
    return render_template('trip_page.html')

# Profile Route (change password, show username)
@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']
    
    return render_template('profile.html', username=username)

# Change Password Route (AJAX request)
@app.route('/change-password', methods=['POST'])
def change_password():
    if 'user' not in session:
        return redirect(url_for('login'))

    old_password = request.form['old-password']
    new_password = request.form['new-password']

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (session['user'], old_password))
    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, session['user']))
        conn.commit()
        conn.close()

        flash('Password updated successfully!', 'success')
        flash('Login with new password.','success')
        return redirect(url_for('login'))  # Redirect to trip_planner page after success
    else:
        conn.close()
        flash('Incorrect old password. Please try again.', 'error')
        return redirect(url_for('trip_planner'))  # Redirect back to trip_planner page on failure

# Logout Route
@app.route('/logout')
def logout():
    # Flash a message and then pop the session user
    session.pop('user', None)  # Remove the user from session
    flash('You have logged out successfully.', 'success')
    return redirect(url_for('login'))

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
