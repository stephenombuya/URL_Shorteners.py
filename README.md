# URL_Shorteners.py

## URL Shortener

A simple Python project that shortens long URLs using the pyshorteners library. This project uses the TinyURL service to convert long URLs into shorter, more manageable URLs.

### Table of Contents

* Features
* Technologies
* Requirements
* Installation
* Usage
* Project Structure
* Contributing
* License
  
### Features
* Shortens a long URL using the TinyURL service.
* Simple and efficient for quick URL shortening tasks.

### Technologies
* Python 3.8+
* pyshorteners library

### Requirements
Before running the project, ensure you have the following installed:
 * Python 3.8 or higher
 * pip (Python package manager)

### Installation
To set up and run the URL Shortener project, follow these steps:

1. Clone the repository:

```
git clone https://github.com/stephenombuya/URL_Shorteners.py
cd url_shortener
```
2. Create a virtual environment (optional but recommended):

```
python3 -m venv venv
source venv/bin/activate  # For Windows use venv\Scripts\activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

The requirements.txt should contain:
```
pyshorteners
```

### Usage
#### Command-line Usage
To run the script and shorten a URL, simply execute the Python file:

```
python url_shortener.py
```

The code will print out the shortened URL for the provided link. By default, the example link is shortened.

Example

Running the code:

```
python shortener.py
```

Expected output:

```
('The shorter url is ', 'https://tinyurl.com/2p9h9vqj')
```

### Project Structure

url_shortener/

├── shortener.py          # Main Python script for URL shortening

├── requirements.txt      # Required dependencies

└── README.md             # Project documentation

### Contributing

Contributions are welcome! To contribute:

* Fork the repository.
* Create a new branch (git checkout -b feature-branch).
* Make your changes.
* Commit your changes (git commit -m 'Add new feature').
* Push to the branch (git push origin feature-branch).
* Create a pull request.

### License
This project is licensed under the MIT License. See the LICENSE file for more details.
