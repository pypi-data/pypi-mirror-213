import os


class NewApp:
    def __init__(self):
        self.app_name = None

    def get_app_info(self, func):
        """
        Decorator to get the application name from user input.
        """
        def wrapper():
            self.app_name = input("Enter the name of the app: ")
            func()

        return wrapper

    @get_app_info
    def create_app(self):
        """
        Create a new Yvapp with the provided name.
        """
        if self.app_name:
            # Create the app directory
            app_dir = os.path.join(os.getcwd(), 'scr', f'yvapp_{self.app_name}')
            os.makedirs(app_dir, exist_ok=True)
            print(f"Created app directory: {app_dir}")

            # Create the manage.py file
            self._create_manage_file(app_dir)
            # Create the static directory
            self._create_static_directory(app_dir)
            # Create the templates directory
            self._create_templates_directory(app_dir)
        else:
            print("Application name is not provided.")

    def _create_manage_file(self, app_dir):
        """
        Create the manage.py file for the Yvapp.
        """
        manage_file_path = os.path.join(app_dir, f'{self.app_name}.py')

        with open(manage_file_path, mode='w', encoding='utf-8') as file:
            file.write('''
from flask import Flask, Blueprint, render_template


app = Flask(__name__)
bp = Blueprint('main', __name__)

@app.route('/')
def index():
    return render_template('main/index.html')

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run()
''')
        print(f"Created manage file: {manage_file_path}")

    def _create_static_directory(self, app_dir):
        """
        Create the static directory for the Yvapp.
        """
        static_dir = os.path.join(app_dir, 'static')
        os.makedirs(static_dir, exist_ok=True)
        print(f"Created static directory: {static_dir}")

        css_dir = os.path.join(static_dir, 'css')
        os.makedirs(css_dir, exist_ok=True)
        print(f"Created CSS directory: {css_dir}")

    def _create_templates_directory(self, app_dir):
        """
        Create the templates directory for the Yvapp.
        """
        templates_dir = os.path.join(app_dir, 'templates')
        os.makedirs(templates_dir, exist_ok=True)
        print(f"Created templates directory: {templates_dir}")

        main_dir = os.path.join(templates_dir, 'main')
        os.makedirs(main_dir, exist_ok=True)
        print(f"Created main directory: {main_dir}")
        index_file_path = os.path.join(main_dir, 'index.html')

        with open(index_file_path, mode='w', encoding='utf-8') as file:
            file.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Main Page</title>
    <link rel="stylesheet" href="{{ url_for('main.static', filename='css/main.css') }}">
</head>
<body>
    <h1>Welcome to the Main Page!</h1>
</body>
</html>
''')
        print(f"Created index file: {index_file_path}")
