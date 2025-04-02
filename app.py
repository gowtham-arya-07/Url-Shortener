from flask import Flask, request, jsonify, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import shortuuid
import datetime
import qrcode
import io
import base64
import validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.secret_key = 'test'
db = SQLAlchemy(app)

class ShortenedURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String, nullable=False)
    short_url = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    click_count = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()


def generate_qr(short_url):
    img = qrcode.make(short_url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.form
    original_url = data.get('original_url')
    custom_alias = data.get('custom_alias')
    expires_in_days = data.get('expires_in_days')
    response = request.get(original_url)
    if response.status_code != 200:
        flash("Invalid URL. Please enter a valid URL.", "error")
        return render_template('index.html', error=True)
    short_url = custom_alias if custom_alias else shortuuid.uuid()[:6]
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=int(expires_in_days)) if expires_in_days else None
    
    new_url = ShortenedURL(original_url=original_url, short_url=short_url, expires_at=expires_at)
    db.session.add(new_url)
    db.session.commit()
    
    qr_code = generate_qr(f"http://localhost:5000/{short_url}")
    return render_template('index.html', short_url=f"http://localhost:5000/{short_url}", qr_code=qr_code, error=False)

@app.route('/<short_url>')
def redirect_url(short_url):
    url_entry = ShortenedURL.query.filter_by(short_url=short_url).first()
    if not url_entry or (url_entry.expires_at and url_entry.expires_at < datetime.datetime.utcnow()):
        return "URL not found or expired", 404
    
    url_entry.click_count += 1
    db.session.commit()
    return redirect(url_entry.original_url)

@app.route('/admin/delete/<short_url>', methods=['POST'])
def delete_url(short_url):
    url_entry = ShortenedURL.query.filter_by(short_url=short_url).first()
    if url_entry:
        db.session.delete(url_entry)
        db.session.commit()
        return redirect('/admin')
    return "URL not found", 404

@app.route('/admin')
def admin_dashboard():
    urls = ShortenedURL.query.all()
    return render_template('admin.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True)
