# Python Flask API for Product Management

This Python Flask API provides functionalities to manage product information in a SQL Server database. It includes endpoints for fetching product details and user authentication.

## Installation

Before you begin, ensure you have Python installed on your system. This project was built using Python 3.8.

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/greenchoicenow/catapult-api.git
cd catapult-api
```

### Step 2: Set Up a Virtual Environment

It's recommended to use a virtual environment. Create and activate one using:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Dependencies
Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 4: Environment Variables
Create a .env file in the root directory of the project and add your database credentials and secret key:

```env
DB_SERVER=your_server
DB_DATABASE=your_database
DB_USERNAME=your_username
DB_PASSWORD=your_password
SECRET_KEY=your_secret_key
```

## Running the Application

Run the application using:

```bash
python app.py
```
This will start the Flask server on http://localhost:5000.

## Using the API
### Authentication

To use the protected endpoints, you first need to authenticate and obtain a token.

- URL: /login
- Method: GET
- Authentication: Basic Auth (Username: admin, Password: password)
- Response: A JWT token

### Fetch Products
To fetch products, use the token obtained from the login endpoint.

- URL: /products?token=<YOUR_TOKEN>
- Method: GET
- Response: List of products and their stock status