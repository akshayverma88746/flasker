
# Flask blogging website
This is a blogging website created using the Flask web framework. The website allows users to create, read, update and delete blog posts.


# Dependencies
Python 3.x\
Flask\
SQLAlchemy









## Installation

Clone the repository:

```bash
  git clone https://github.com/akshayverma88746/flasker.git

```
Change into the project directory:

```bash
    cd flasker
```
Create a virtual environment and activate it:

```bash
    python3 -m venv env
    source env/bin/activate
```
Set the environment variables:

```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
```
Run the migration commands to set up the database:
```bash
    flask db init
    flask db migrate
    flask db upgrade
```
Finally run the application:
```bash
    flask run
```
The application will be available at http://localhost:5000.
    
## Features
    1. User registration and login\
    2. Creating, reading, updating and deleting blog posts\
    3. Adding and displaying blog post categories


## Contributing

Contributions are welcome! If you find a bug or have an idea for a new feature, please open an issue or create a pull request.
## License

[MIT](https://choosealicense.com/licenses/mit/)

