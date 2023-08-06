import os
import inspect


class Manager:
    def __init__(self) -> None:
        # Get the absolute path of the calling file
        frame = inspect.stack()[1]
        self.project_path: str = os.path.abspath(frame.filename)

        # Extract the project name from the file path
        self.project_name: str = inspect.getmodulename(self.project_path)

    def manager(self, is_delete: bool = True):
        # Create the project directory
        project_dir = os.path.join(os.getcwd(), self.project_name)
        os.makedirs(project_dir, exist_ok=True)

        # Create the manager.py file
        self._create_manager_file(project_dir=project_dir)

        if is_delete:
            # Remove the original file after creating the manager.py
            os.remove(self.project_path)

    def _create_manager_file(self, project_dir: str):
        # Define the file path for manager.py
        file_path = os.path.join(project_dir, 'manager.py')

        with open(file_path, 'w') as file:
            file.write("""
import YvFlask

# Create an instance of the newApp class from Yvapp module
tools = YvFlask.Yvapp.NewApp()

if __name__ == '__main__':
    # Call the create_app method to create the Yvapp
    tools.create_app()
""")

        print(f"Created manager file: {file_path}")
