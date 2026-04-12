
#  URL Shortener 

A comprehensive, production-ready URL shortener with web interface, desktop GUI, analytics tracking, QR code generation, and cloud deployment support. Built with Python, Flask, and Tkinter.

## Features
### Core Functionality
*  Shorten long URLs using **TinyURL** or **Bitly**
*  Expand shortened URLs back to original links
*  Custom short codes for branded links
*  Persistent history tracking with timestamps
*  Smart URL validation
*  Comprehensive URL analytics
### Advanced Features
*  **Web Application** - Flask-based responsive web interface
*  **Desktop GUI** - Tkinter application with tabbed interface
*  **Analytics Dashboard** - Track clicks, unique visitors, and user agents
*  **QR Code Generation** - Auto-generate QR codes for shortened URLs
*  **Cloud Ready** - Deploy to Render or Railway with one click
*  **Real-time Statistics** - Hourly click patterns and visitor insights
*  **SQLite Database** - Persistent storage for analytics data
---
##  Technologies Used
### Backend
* Python 3.8+
* Flask 2.3.2 - Web framework
* pyshorteners - URL shortening API wrapper
* SQLite3 - Analytics database
* qrcode - QR code generation
* Pillow - Image processing
### Frontend (Web)
* HTML5, CSS3, Bootstrap 5
* JavaScript, Chart.js for analytics
* Responsive design
### Desktop GUI
* Tkinter - Native Python GUI
* Threading for non-blocking operations
### Deployment
* Gunicorn - WSGI HTTP Server
* Render/Railway ready configuration
* Environment variables support
---
##  Requirements
Make sure you have the following installed:
* Python 3.8 or higher
* pip (Python package manager)
* Git (optional)
---
##  Installation
Clone the repository:
```bash
git clone https://github.com/stephenombuya/URL_Shorteners.py
cd url_shortener
```

Create a virtual environment (recommended):

```bash

python3 -m venv venv
```

Activate the virtual environment:

-   **Windows:**
    

```bash

venv\Scripts\activate
```

-   **Linux / Mac:**
    

```bash

source venv/bin/activate
```

Install dependencies:

```bash

pip install -r requirements.txt
```

----------

##  Usage

### 1. Web Application (Flask)

Run the web server:

```bash

python app.py
```

Open your browser and navigate to:

```text

http://localhost:5000
```

**Features available in web version:**

-   URL shortening with custom codes
-   Analytics dashboard with charts
-   QR code download
-   Click tracking and visitor analytics
-   History viewer
    

### 2. Desktop GUI Application (Tkinter)

Run the GUI application:

```bash

python gui_app.py
```

**Features available in GUI:**

-   Multi-tab interface (Shorten, Analytics, History)
-   Real-time URL processing
-   Copy to clipboard functionality
-   Browser integration
-   Visual analytics display
    

### 3. Command Line Interface (Legacy)

For command line usage:

```bash

python shortener.py
```

----------

##  Usage Examples

### Web Interface

1.  Visit `http://localhost:5000`
2.  Enter a long URL (e.g., `https://github.com/stephenombuya`)
3.  Choose service (TinyURL/Bitly)
4.  Optional: Add custom code (e.g., `mygithub`)
5.  Click "Shorten URL"
6.  Copy the shortened link or download QR code
7.  View analytics by clicking "View Analytics"
    

### Desktop GUI

1.  Launch the application
2.  **Shorten Tab:** Enter URL and get shortened link
3.  **Analytics Tab:** Enter short code to view click statistics
4.  **History Tab:** View all shortened URLs and their stats
    

### API Endpoints (Web Version)

```bash

# Shorten URL
POST /shorten
{
 "long_url": "https://example.com",
 "service": "tinyurl",
 "custom_code": "custom"
}
# Get Analytics
GET /analytics/{short_code}
# Get Statistics
GET /api/stats
```

----------

##  Analytics Features

The analytics system tracks:

-   **Total clicks** per shortened URL
-   **Unique visitors** by IP address
-   **Click timestamps** with hourly patterns
-   **User agents** (browser information)
-   **Referrer sources**
-   **Geographic trends** (via IP analysis)
    

View analytics through:

-   Web dashboard with Chart.js visualizations
-   GUI application with formatted output
-   JSON API for programmatic access
    

----------

##  QR Code Generation

Every shortened URL automatically generates a QR code:

-   **Web version:** Displayed instantly, can be saved
-   **GUI version:** Generated and displayed in the result area
-   **Format:** PNG, 200x200 pixels
-   **Customizable:** Colors and size can be modified
    

----------

##  Bitly Integration (Optional)

To use Bitly service:

1.  Create an account at [Bitly](https://bitly.com/)
2.  Generate your API token from developer settings
3.  Create a `.env` file in your project root:

```env

BITLY_API_KEY=your_bitly_api_key_here
FLASK_ENV=production
SECRET_KEY=your_secret_key_here
```

4.  Bitly will be available as an option in all interfaces
    

----------

##  Cloud Deployment

### Deploy to Render

1.  Push your code to GitHub repository   
2.  Create an account at [Render](https://render.com/)   
3.  Click "New +" → "Web Service"  
4.  Connect your GitHub repository
5.  Render will auto-detect the configuration from `render.yaml`
6.  Add environment variables in Render dashboard
7.  Your app will be live at `https://your-app.onrender.com`
    

### Deploy to Railway

1.  Install Railway CLI: `npm install -g @railway/cli`   
2.  Login: `railway login`
3.  Initialize: `railway init`  
4.  Deploy: `railway up`  
5.  Set environment variables: `railway variables set KEY=VALUE`
    

### Manual Deployment (Any VPS)

```
bash

# Install dependencies
pip install -r requirements.txt
# Run with gunicorn
gunicorn app:app --bind 0.0.0.0:8000
# Or with systemd for production
sudo systemctl start url-shortener
```

----------

##  Project Structure


```text

url_shortener/
├── app.py                 # Flask web application
├── gui_app.py            # Tkinter GUI application
├── shortener.py          # Core URL shortening logic (CLI)
├── url_shortener.py      # Enhanced core with analytics
├── requirements.txt      # Project dependencies
├── render.yaml           # Render deployment config
├── .env                  # Environment variables (create this)
├── history.txt           # URL history log
├── analytics.db          # SQLite analytics database
├── templates/            # HTML templates for web version
│   ├── index.html        # Main shortening interface
│   ├── analytics.html    # Analytics dashboard
│   ├── history.html      # History viewer
│   └── 404.html          # Error page
├── static/               # Static files (CSS, JS, images)
└── README.md             # Project documentation
```

----------

##  Configuration

### Database Schema

The SQLite database (`analytics.db`) contains two tables:

**url_info:**

-   `short_code` (PRIMARY KEY)
-   `long_url`
-   `created_at`
-   `total_clicks`
    

**url_clicks:**

-   `id` (PRIMARY KEY)
-   `short_url`
-   `long_url`
-   `click_time`
-   `ip_address`
-   `user_agent`
-   `referrer`
    
-------------------


##  Testing

Run the test suite (if implemented):

```bash

python -m pytest tests/
```

Manual testing checklist:

-   URL shortening with valid URLs
-   Error handling for invalid URLs
-   Custom code functionality
-   Click tracking and analytics
-   QR code generation
-   Database persistence
-   History logging
-   Web interface responsiveness
-   GUI application stability
    

----------

##  Troubleshooting

### Common Issues

**Issue:**  `ModuleNotFoundError: No module named 'qrcode'`

```bash

pip install qrcode[pil]
```

**Issue:** Database locked error

```bash

# Close all connections and restart application
rm analytics.db  # Backup first!
python app.py  # Recreates database
```

**Issue:** Bitly doesn't work

```bash

# Check if BITLY_API_KEY is set
echo $BITLY_API_KEY
# Or verify .env file exists and is loaded
```

**Issue:** Port 5000 already in use (MacOS)

```bash

# Use a different port
python app.py --port 5001
# Or kill the process using port 5000
lsof -ti:5000 | xargs kill -9
```
----------

##  Contributing

Contributions are welcome! Here's how you can help:

1.  Fork the repository
2.  Create a new branch
    
    ``` bash
	git checkout -b feature/amazing-feature
	 ```
3.  Make your changes
4.  Commit your changes
    
    ```bash
    git commit -m 'Add some amazing feature'
    ```
5.  Push to the branch
    
    ```bash
     git push origin feature/amazing-feature
    ```
6.  Open a Pull Request
    

### Development Guidelines

-   Follow PEP 8 style guide
-   Add comments for complex logic
-   Update documentation for new features
-   Test your changes before submitting
    

----------

##  License

This project is licensed under the MIT License - see the [LICENSE](https://license/) file for details.


----------

##  Support

If you found this project useful:

-    Star the repository on GitHub
-    Fork it for your own use
-   Report bugs via Issues
-    Suggest new features
    

----------

##  Quick Start Commands

```bash

# Clone and setup
git clone https://github.com/stephenombuya/URL_Shorteners.py
cd URL_Shorteners.py
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Initialize the database
python init_db.py
# Select option 1 to create a new database with sample data

# Run web version
python app.py

# Run GUI version
python gui_app.py

# Run CLI version
python shortener.py

# Deploy to Render (after pushing to GitHub)
# Just connect your repo at https://render.com

```
