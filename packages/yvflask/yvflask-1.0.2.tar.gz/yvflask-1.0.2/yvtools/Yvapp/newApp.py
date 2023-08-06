import os

class NewApp:
    def __init__(self):
        self.app_name = None

    def get_app_info(self, func):
        def wrapper():
            self.app_name = input("Enter the name of the app: ")
            func()

        return wrapper

    @get_app_info
    def create_app(self):
        if self.app_name:
            app_dir = os.path.join(os.getcwd(), 'scr', f'yvapp_{self.app_name}')
            os.makedirs(app_dir, exist_ok=True)
            print(f"Created app directory: {app_dir}")

            self._create_manage_file(app_dir)
            self._create_static_directory(app_dir)
            self._create_templates_directory(app_dir)
        else:
            print("Application name is not provided.")
