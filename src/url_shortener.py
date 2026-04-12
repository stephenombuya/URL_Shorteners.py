import pyshorteners
import os
import sqlite3
import hashlib
import json
from datetime import datetime
from urllib.parse import urlparse

HISTORY_FILE = "history.txt"
DB_FILE = "analytics.db"

def init_analytics_db():
    """Initialize SQLite database for analytics"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS url_clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_url TEXT NOT NULL,
            long_url TEXT NOT NULL,
            click_time TIMESTAMP NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            referrer TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS url_info (
            short_code TEXT PRIMARY KEY,
            long_url TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            total_clicks INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

def generate_short_code(long_url, service="tinyurl"):
    """Generate a short code for the URL"""
    # Create a hash of the URL to use as short code
    url_hash = hashlib.md5(long_url.encode()).hexdigest()[:6]
    return url_hash

class URLShortener:
    def __init__(self):
        init_analytics_db()
        self.s = pyshorteners.Shortener()
    
    def shorten_url(self, long_url, service="tinyurl", custom_code=None):
        try:
            # Generate short code
            short_code = custom_code if custom_code else generate_short_code(long_url)
            
            if service == "tinyurl":
                short_url = self.s.tinyurl.short(long_url)
            elif service == "bitly":
                short_url = self.s.bitly.short(long_url)
            else:
                return None, "Unsupported service"
            
            # Store in database
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO url_info (short_code, long_url, created_at, total_clicks)
                VALUES (?, ?, ?, ?)
            ''', (short_code, long_url, datetime.now(), 0))
            conn.commit()
            conn.close()
            
            # Save to history file
            self.save_history(long_url, short_url)
            
            return short_url, None
            
        except Exception as e:
            return None, str(e)
    
    def expand_url(self, short_url):
        try:
            return self.s.tinyurl.expand(short_url)
        except Exception as e:
            return None
    
    def track_click(self, short_code, ip_address, user_agent, referrer):
        """Track a click on a shortened URL"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Get the long URL
        cursor.execute('SELECT long_url FROM url_info WHERE short_code = ?', (short_code,))
        result = cursor.fetchone()
        
        if result:
            long_url = result[0]
            
            # Record the click
            cursor.execute('''
                INSERT INTO url_clicks (short_url, long_url, click_time, ip_address, user_agent, referrer)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (short_code, long_url, datetime.now(), ip_address, user_agent, referrer))
            
            # Update total clicks
            cursor.execute('''
                UPDATE url_info SET total_clicks = total_clicks + 1
                WHERE short_code = ?
            ''', (short_code,))
            
            conn.commit()
            conn.close()
            return long_url
        
        conn.close()
        return None
    
    def get_analytics(self, short_code):
        """Get analytics for a specific short URL"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Get URL info
        cursor.execute('SELECT long_url, created_at, total_clicks FROM url_info WHERE short_code = ?', (short_code,))
        url_info = cursor.fetchone()
        
        if not url_info:
            conn.close()
            return None
        
        # Get click details
        cursor.execute('''
            SELECT click_time, ip_address, user_agent, referrer 
            FROM url_clicks 
            WHERE short_url = ? 
            ORDER BY click_time DESC 
            LIMIT 100
        ''', (short_code,))
        
        clicks = cursor.fetchall()
        
        # Calculate statistics
        unique_ips = len(set(click[1] for click in clicks))
        
        # Get clicks by hour (last 24 hours)
        cursor.execute('''
            SELECT strftime('%H', click_time) as hour, COUNT(*) 
            FROM url_clicks 
            WHERE short_url = ? AND click_time >= datetime('now', '-1 day')
            GROUP BY hour
        ''', (short_code,))
        
        hourly_clicks = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'long_url': url_info[0],
            'created_at': url_info[1],
            'total_clicks': url_info[2],
            'unique_ips': unique_ips,
            'recent_clicks': clicks,
            'hourly_clicks': hourly_clicks
        }
    
    def get_all_urls(self):
        """Get all shortened URLs"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT short_code, long_url, created_at, total_clicks FROM url_info ORDER BY created_at DESC')
        urls = cursor.fetchall()
        conn.close()
        return urls
    
    def save_history(self, long_url, short_url):
        try:
            with open(HISTORY_FILE, "a") as file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"[{timestamp}] {long_url} -> {short_url}\n")
        except Exception as e:
            print(f"⚠️ Could not save history: {e}")
    
    def view_history(self):
        if not os.path.exists(HISTORY_FILE):
            return []
        
        with open(HISTORY_FILE, "r") as file:
            return file.readlines()
    
    def generate_qr_code(self, url):
        """Generate QR code for URL"""
        try:
            import qrcode
            from io import BytesIO
            import base64
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64 for web display
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            return None

# Initialize the shortener
shortener = URLShortener()
