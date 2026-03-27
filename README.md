# 🔗 URL Shortener

A powerful and user-friendly Python-based URL shortener built with **pyshorteners**. This tool allows you to shorten, expand, and manage URLs directly from the command line with support for multiple services.

---

## 🚀 Features

* 🔗 Shorten long URLs using **TinyURL**
* 🔁 Expand shortened URLs back to original links
* 🌐 Support for multiple services (TinyURL & Bitly)
* 📜 Persistent history tracking
* 🧠 Smart URL validation
* 🖥️ Interactive CLI menu system
* ⚠️ Error handling for invalid inputs and API issues

---

## 🛠️ Technologies Used

* Python 3.8+
* pyshorteners
* requests
* validators
* python-dotenv

---

## 📦 Requirements

Make sure you have the following installed:

* Python 3.8 or higher
* pip (Python package manager)

---

## ⚙️ Installation

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

* **Windows:**

```bash
venv\Scripts\activate
```

* **Linux / Mac:**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the application:

```bash
python shortener.py
```

---

## 💻 Example

```
🚀 Welcome to the PRO URL Shortener

🔗 URL Shortener Menu
----------------------------------------
1. Shorten URL
2. Expand URL
3. View History
4. Exit

Choose an option (1-4): 1

Enter a long URL: https://google.com

Choose service:
1. TinyURL (default)
2. Bitly

Select (1-2): 1

✅ Shortened URL: https://tinyurl.com/abc123
```

---

## 🔐 Bitly Integration (Optional)

To use Bitly, you need an API key:

1. Create an account on Bitly
2. Generate your API token
3. Create a `.env` file in your project root:

```
BITLY_API_KEY=your_api_key_here
```

4. Update your code to load environment variables using `python-dotenv`

---

## 📁 Project Structure

```
url_shortener/

├── shortener.py        # Main application logic
├── history.txt         # Stores shortened URLs
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

---

## 📈 Future Improvements

* Web version using Flask or Django
* GUI version (Tkinter / PyQt)
* URL analytics (click tracking)
* QR code generation for shortened URLs
* Cloud deployment (Render / Railway)

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch

   ```bash
   git checkout -b feature-branch
   ```
3. Make your changes
4. Commit your changes

   ```bash
   git commit -m "Add new feature"
   ```
5. Push to the branch

   ```bash
   git push origin feature-branch
   ```
6. Open a Pull Request 🚀

---

## 📄 License

This project is licensed under the MIT License.

---

## ⭐ Support

If you found this project useful:

* ⭐ Star the repo
* 🍴 Fork it
* 🧠 Share ideas

---

## 👨‍💻 Author

Built with passion by **Stephen Ombuya**
