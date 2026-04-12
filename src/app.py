from flask import Flask, render_template, request, redirect, jsonify, session
from url_shortener import shortener
import validators
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form.get('long_url')
    service = request.form.get('service', 'tinyurl')
    custom_code = request.form.get('custom_code')
    
    if not long_url:
        return jsonify({'error': 'URL is required'}), 400
    
    if not validators.url(long_url):
        return jsonify({'error': 'Invalid URL format'}), 400
    
    short_url, error = shortener.shorten_url(long_url, service, custom_code)
    
    if error:
        return jsonify({'error': error}), 500
    
    # Generate QR code
    qr_code = shortener.generate_qr_code(short_url)
    
    return jsonify({
        'short_url': short_url,
        'long_url': long_url,
        'qr_code': qr_code,
        'analytics_url': f"/analytics/{short_url.split('/')[-1]}"
    })

@app.route('/<short_code>')
def redirect_to_url(short_code):
    # Get client info
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    referrer = request.headers.get('Referer')
    
    # Track the click
    long_url = shortener.track_click(short_code, ip_address, user_agent, referrer)
    
    if long_url:
        return redirect(long_url)
    else:
        return render_template('404.html'), 404

@app.route('/analytics/<short_code>')
def analytics(short_code):
    data = shortener.get_analytics(short_code)
    
    if not data:
        return render_template('404.html'), 404
    
    return render_template('analytics.html', 
                         short_code=short_code,
                         analytics=data)

@app.route('/history')
def history():
    history_data = shortener.view_history()
    all_urls = shortener.get_all_urls()
    return render_template('history.html', 
                         history=history_data,
                         urls=all_urls)

@app.route('/api/stats')
def api_stats():
    all_urls = shortener.get_all_urls()
    total_clicks = sum(url[3] for url in all_urls)
    
    return jsonify({
        'total_urls': len(all_urls),
        'total_clicks': total_clicks,
        'urls': [{'code': url[0], 'long_url': url[1], 'clicks': url[3]} for url in all_urls]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
