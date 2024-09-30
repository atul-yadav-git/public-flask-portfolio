#  🚀 Personal Flask Portfolio Page   


![image](https://github.com/user-attachments/assets/8c7606a3-8369-4623-8b2f-bb7f19b50d15)

Welcome to my personal Flask portfolio page! This project serves as a comprehensive career page and portfolio built using Flask. Feel free to use this as a template or for your own learning purposes.

## 🎉Description

This project is a fully functional personal portfolio page created with Flask, a popular Python web framework. It includes all necessary components for a complete web application, such as:

- **Backend**: Flask application with routing and authentication.
- **Frontend**: HTML and CSS files for layout and styling.
- **Deployment**: Configured to be served using Gunicorn and Nginx.

## 🌟Features

- **User Authentication**: Basic login functionality using Flask-WTF and Flask-Login.
- **Responsive Design**: Customizable HTML and CSS for a professional look.
- **Deployment Ready**: Includes setup for deploying with Gunicorn and Nginx.

## 🛠️Installation

To get started with this project locally:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/atul-yadav-git/public-flask-portfolio.git
   cd your-repository
   ```
2. **Set Up a Virtual Environment**

```bash
python -m venv
source venv/bin/activate
```
3. **Install Dependencies**

```bash
pip install -r requirements.txt
```
4. **Run the Application**

```bash
python app.py
```
By default, Flask runs on http://127.0.0.1:5000/.

## 📖Deployment
For deployment using Gunicorn and Nginx:

1. **Install Gunicorn**

```bash
pip install gunicorn
```
2. **Run Gunicorn**

```bash
gunicorn -w 4 app:app
```
3. **Configure Nginx**: Set up your Nginx configuration to proxy requests to Gunicorn. Refer to the Nginx documentation for guidance.

---
## 🤝Feedback and Contributions
I welcome any feedback or suggestions for improvements. Feel free to open an issue or submit a pull request if you have enhancements or fixes. Your contributions and ideas are greatly appreciated!
