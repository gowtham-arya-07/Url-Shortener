# Flask URL Shortener

A simple URL shortener built with Flask and SQLite. It allows users to shorten long URLs, generate custom aliases, track clicks, and generate QR codes for easy sharing. The admin panel provides URL management capabilities.

## Features
- Shorten long URLs with randomly generated or custom short URLs
- Store URL mappings in an SQLite database
- Redirect short URLs to original destinations
- Track the number of clicks for each short URL
- Generate QR codes for shortened URLs
- Admin panel to manage and delete URLs
- Supports expiration dates for short links

## Installation

### Prerequisites
Ensure you have Python installed (version 3.6 or later).

### Setup Instructions
1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/url-shortener.git
   cd url-shortener
2. Run the App
   ```sh
   pip install -r requirements.txt
   python app.py
   ```
