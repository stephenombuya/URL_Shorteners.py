#!/usr/bin/env python3
"""
Database initialization script for URL Shortener Pro
Creates analytics.db with required tables and sample data
"""

import sqlite3
import os
from datetime import datetime, timedelta
import random

DB_FILE = "analytics.db"

def init_database():
    """Initialize the SQLite database with all required tables"""
    
    # Remove existing database if it exists
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"🗑️ Removed existing database: {DB_FILE}")
    
    # Create new database connection
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    print("📊 Creating database tables...")
    
    # Create url_info table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS url_info (
            short_code TEXT PRIMARY KEY,
            long_url TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            total_clicks INTEGER DEFAULT 0
        )
    ''')
    print("✅ Created table: url_info")
    
    # Create url_clicks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS url_clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_url TEXT NOT NULL,
            long_url TEXT NOT NULL,
            click_time TIMESTAMP NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            referrer TEXT,
            FOREIGN KEY (short_url) REFERENCES url_info (short_code)
        )
    ''')
    print("✅ Created table: url_clicks")
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_short_url ON url_clicks(short_url)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_click_time ON url_clicks(click_time)')
    print("✅ Created indexes")
    
    # Insert sample data for demonstration
    print("\n📝 Inserting sample data...")
    
    sample_urls = [
        ("github", "https://github.com/stephenombuya/URL_Shorteners.py", 
         "Personal GitHub repository"),
        ("linkedin", "https://linkedin.com/in/stephenombuya", 
         "Professional LinkedIn profile"),
        ("portfolio", "https://stephenombuya.dev", 
         "Personal portfolio website"),
        ("twitter", "https://twitter.com/stephenombuya", 
         "Twitter/X profile"),
        ("blog", "https://medium.com/@stephenombuya", 
         "Technical blog on Medium")
    ]
    
    sample_ips = [
        "192.168.1.1", "10.0.0.1", "172.16.0.1", "8.8.8.8", "1.1.1.1",
        "203.0.113.1", "198.51.100.1", "192.0.2.1", "169.254.0.1", "127.0.0.1"
    ]
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36",
        "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
    ]
    
    referrers = [
        "https://google.com",
        "https://twitter.com",
        "https://linkedin.com",
        "https://reddit.com",
        "https://facebook.com",
        "https://github.com",
        "https://medium.com",
        "https://stackoverflow.com",
        "https://news.ycombinator.com",
        "https://direct"
    ]
    
    # Insert sample URLs and generate random clicks
    for short_code, long_url, description in sample_urls:
        created_at = datetime.now() - timedelta(days=random.randint(1, 30))
        total_clicks = random.randint(10, 500)
        
        cursor.execute('''
            INSERT INTO url_info (short_code, long_url, created_at, total_clicks)
            VALUES (?, ?, ?, ?)
        ''', (short_code, long_url, created_at, total_clicks))
        
        print(f"  📌 Added: {short_code} -> {description}")
        
        # Generate random click history
        for _ in range(total_clicks):
            click_time = created_at + timedelta(
                hours=random.randint(0, 24*30),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )
            
            # Don't generate future clicks
            if click_time > datetime.now():
                click_time = datetime.now() - timedelta(hours=random.randint(1, 24))
            
            cursor.execute('''
                INSERT INTO url_clicks (short_url, long_url, click_time, ip_address, user_agent, referrer)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                short_code, 
                long_url, 
                click_time,
                random.choice(sample_ips),
                random.choice(user_agents),
                random.choice(referrers)
            ))
        
        print(f"  📊 Generated {total_clicks} click records")
    
    # Commit changes
    conn.commit()
    
    # Verify database creation
    print("\n🔍 Verifying database...")
    
    cursor.execute("SELECT COUNT(*) FROM url_info")
    url_count = cursor.fetchone()[0]
    print(f"📊 Total URLs in database: {url_count}")
    
    cursor.execute("SELECT COUNT(*) FROM url_clicks")
    click_count = cursor.fetchone()[0]
    print(f"📊 Total click records: {click_count}")
    
    # Display summary
    print("\n" + "="*50)
    print("📊 DATABASE SUMMARY")
    print("="*50)
    
    cursor.execute('''
        SELECT short_code, long_url, total_clicks 
        FROM url_info 
        ORDER BY total_clicks DESC
    ''')
    
    print("\n📈 Top URLs by clicks:")
    for row in cursor.fetchall():
        print(f"  • {row[0]}: {row[2]} clicks -> {row[1][:50]}...")
    
    # Get click statistics
    cursor.execute('''
        SELECT 
            DATE(click_time) as date,
            COUNT(*) as clicks
        FROM url_clicks
        GROUP BY DATE(click_time)
        ORDER BY date DESC
        LIMIT 7
    ''')
    
    print("\n📅 Last 7 days activity:")
    for row in cursor.fetchall():
        print(f"  • {row[0]}: {row[1]} clicks")
    
    # Close connection
    conn.close()
    
    print("\n" + "="*50)
    print(f"✅ Database initialized successfully: {DB_FILE}")
    print("="*50)
    
    return True

def add_custom_url(short_code, long_url, description=""):
    """Add a custom URL to the database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO url_info (short_code, long_url, created_at, total_clicks)
            VALUES (?, ?, ?, ?)
        ''', (short_code, long_url, datetime.now(), 0))
        conn.commit()
        print(f"✅ Added custom URL: {short_code} -> {long_url}")
        if description:
            print(f"   📝 {description}")
        return True
    except sqlite3.IntegrityError:
        print(f"❌ Short code '{short_code}' already exists!")
        return False
    finally:
        conn.close()

def reset_database():
    """Reset the database (delete and recreate)"""
    response = input("⚠️ This will delete all data. Are you sure? (y/n): ")
    if response.lower() == 'y':
        init_database()
        print("✅ Database has been reset!")
    else:
        print("❌ Operation cancelled")

def backup_database():
    """Create a backup of the database"""
    if os.path.exists(DB_FILE):
        backup_name = f"analytics_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        import shutil
        shutil.copy2(DB_FILE, backup_name)
        print(f"✅ Database backed up to: {backup_name}")
        return True
    else:
        print("❌ No database found to backup")
        return False

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════╗
    ║   URL Shortener Pro - Database Manager    ║
    ╚═══════════════════════════════════════════╝
    """)
    
    print("Options:")
    print("1. Initialize new database")
    print("2. Add custom URL")
    print("3. Reset database")
    print("4. Backup database")
    print("5. Exit")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        init_database()
    elif choice == "2":
        short_code = input("Enter short code: ").strip()
        long_url = input("Enter long URL: ").strip()
        description = input("Enter description (optional): ").strip()
        add_custom_url(short_code, long_url, description)
    elif choice == "3":
        reset_database()
    elif choice == "4":
        backup_database()
    elif choice == "5":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid option")
