import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from url_shortener import shortener
import webbrowser
import validators

class URLShortenerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("URL Shortener Pro")
        self.root.geometry("800x600")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.shorten_tab = ttk.Frame(self.notebook)
        self.analytics_tab = ttk.Frame(self.notebook)
        self.history_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.shorten_tab, text="Shorten URL")
        self.notebook.add(self.analytics_tab, text="Analytics")
        self.notebook.add(self.history_tab, text="History")
        
        self.setup_shorten_tab()
        self.setup_analytics_tab()
        self.setup_history_tab()
        
    def setup_shorten_tab(self):
        # URL Input
        tk.Label(self.shorten_tab, text="Long URL:", font=("Arial", 12)).pack(pady=10)
        self.url_entry = tk.Entry(self.shorten_tab, width=60, font=("Arial", 10))
        self.url_entry.pack(pady=5)
        
        # Service selection
        tk.Label(self.shorten_tab, text="Service:", font=("Arial", 12)).pack(pady=5)
        self.service_var = tk.StringVar(value="tinyurl")
        service_frame = tk.Frame(self.shorten_tab)
        service_frame.pack(pady=5)
        tk.Radiobutton(service_frame, text="TinyURL", variable=self.service_var, 
                      value="tinyurl").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(service_frame, text="Bitly", variable=self.service_var, 
                      value="bitly").pack(side=tk.LEFT, padx=10)
        
        # Custom code
        tk.Label(self.shorten_tab, text="Custom Code (optional):", font=("Arial", 12)).pack(pady=5)
        self.custom_code_entry = tk.Entry(self.shorten_tab, width=30)
        self.custom_code_entry.pack(pady=5)
        
        # Shorten button
        self.shorten_btn = tk.Button(self.shorten_tab, text="Shorten URL", 
                                    command=self.shorten_url, bg="blue", fg="white",
                                    font=("Arial", 12), padx=20, pady=5)
        self.shorten_btn.pack(pady=20)
        
        # Result frame
        self.result_frame = tk.Frame(self.shorten_tab)
        self.result_frame.pack(pady=20, fill='both', expand=True)
        
        self.result_text = tk.Text(self.result_frame, height=5, width=60)
        self.result_text.pack(pady=5)
        
        # QR Code display
        self.qr_label = tk.Label(self.result_frame, text="")
        self.qr_label.pack(pady=5)
        
    def setup_analytics_tab(self):
        # Analytics input
        tk.Label(self.analytics_tab, text="Short Code:", font=("Arial", 12)).pack(pady=10)
        self.analytics_entry = tk.Entry(self.analytics_tab, width=30)
        self.analytics_entry.pack(pady=5)
        
        tk.Button(self.analytics_tab, text="Get Analytics", 
                 command=self.get_analytics, bg="green", fg="white",
                 font=("Arial", 10)).pack(pady=10)
        
        # Analytics display
        self.analytics_text = scrolledtext.ScrolledText(self.analytics_tab, height=20, width=70)
        self.analytics_text.pack(pady=10, fill='both', expand=True)
        
    def setup_history_tab(self):
        tk.Button(self.history_tab, text="Refresh History", 
                 command=self.load_history, bg="orange", fg="white",
                 font=("Arial", 10)).pack(pady=10)
        
        self.history_text = scrolledtext.ScrolledText(self.history_tab, height=25, width=80)
        self.history_text.pack(pady=10, fill='both', expand=True)
        
        self.load_history()
        
    def shorten_url(self):
        long_url = self.url_entry.get().strip()
        service = self.service_var.get()
        custom_code = self.custom_code_entry.get().strip() or None
        
        if not long_url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        
        if not validators.url(long_url):
            messagebox.showerror("Error", "Invalid URL format")
            return
        
        # Disable button during processing
        self.shorten_btn.config(state='disabled', text='Processing...')
        
        # Run in thread to prevent GUI freezing
        def process():
            short_url, error = shortener.shorten_url(long_url, service, custom_code)
            
            self.root.after(0, lambda: self.update_result(short_url, error, long_url))
        
        threading.Thread(target=process, daemon=True).start()
    
    def update_result(self, short_url, error, long_url):
        self.shorten_btn.config(state='normal', text='Shorten URL')
        
        if error:
            messagebox.showerror("Error", f"Failed to shorten URL: {error}")
            return
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Original URL: {long_url}\n")
        self.result_text.insert(tk.END, f"Shortened URL: {short_url}\n")
        
        # Add clickable link
        link_frame = tk.Frame(self.result_frame)
        link_frame.pack(pady=5)
        
        link_label = tk.Label(link_frame, text="Open in Browser", 
                            fg="blue", cursor="hand2")
        link_label.pack()
        link_label.bind("<Button-1>", lambda e: webbrowser.open(short_url))
        
        # Generate and display QR code
        qr_data = shortener.generate_qr_code(short_url)
        if qr_data:
            # Display QR code (simplified - would need PIL for full implementation)
            self.qr_label.config(text="QR Code generated! (Save functionality coming soon)")
        
        # Load updated history
        self.load_history()
    
    def get_analytics(self):
        short_code = self.analytics_entry.get().strip()
        
        if not short_code:
            messagebox.showerror("Error", "Please enter a short code")
            return
        
        # Extract code from URL if full URL provided
        if '/' in short_code:
            short_code = short_code.split('/')[-1]
        
        data = shortener.get_analytics(short_code)
        
        self.analytics_text.delete(1.0, tk.END)
        
        if not data:
            self.analytics_text.insert(tk.END, "No analytics data found for this URL")
            return
        
        self.analytics_text.insert(tk.END, "="*50 + "\n")
        self.analytics_text.insert(tk.END, f"URL Analytics for: {short_code}\n")
        self.analytics_text.insert(tk.END, "="*50 + "\n\n")
        self.analytics_text.insert(tk.END, f"Original URL: {data['long_url']}\n")
        self.analytics_text.insert(tk.END, f"Created: {data['created_at']}\n")
        self.analytics_text.insert(tk.END, f"Total Clicks: {data['total_clicks']}\n")
        self.analytics_text.insert(tk.END, f"Unique Visitors: {data['unique_ips']}\n\n")
        
        self.analytics_text.insert(tk.END, "Recent Clicks:\n")
        self.analytics_text.insert(tk.END, "-"*50 + "\n")
        
        for click in data['recent_clicks'][:10]:
            self.analytics_text.insert(tk.END, f"Time: {click[0]}\n")
            self.analytics_text.insert(tk.END, f"IP: {click[1]}\n")
            self.analytics_text.insert(tk.END, f"Browser: {click[2][:50]}...\n")
            self.analytics_text.insert(tk.END, "-"*30 + "\n")
    
    def load_history(self):
        self.history_text.delete(1.0, tk.END)
        
        history = shortener.view_history()
        all_urls = shortener.get_all_urls()
        
        self.history_text.insert(tk.END, "📊 ALL SHORTENED URLS\n")
        self.history_text.insert(tk.END, "="*50 + "\n\n")
        
        for url in all_urls:
            self.history_text.insert(tk.END, f"Code: {url[0]}\n")
            self.history_text.insert(tk.END, f"URL: {url[1][:80]}...\n")
            self.history_text.insert(tk.END, f"Clicks: {url[3]}\n")
            self.history_text.insert(tk.END, f"Created: {url[2]}\n")
            self.history_text.insert(tk.END, "-"*40 + "\n")
        
        self.history_text.insert(tk.END, "\n📜 RECENT HISTORY\n")
        self.history_text.insert(tk.END, "="*50 + "\n\n")
        
        for line in history[-20:]:  # Show last 20 entries
            self.history_text.insert(tk.END, line)

def main():
    root = tk.Tk()
    app = URLShortenerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
