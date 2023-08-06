import subprocess
from pathlib import Path
import yaml
from lollms.paths import LollmsPaths
from lollms.personality import AIPersonality
class Install:
    def __init__(self, personality:AIPersonality, force_reinstall=False):
        self.personality = personality
        # Get the current directory
        current_dir = Path(__file__).resolve().parent.parent
        install_file = current_dir / ".installed"

        if not install_file.exists() or force_reinstall:
            print(f"This is the first time you are using this personality : {personality.name}.")
            print("Installing ...")
            
            # Step 2: Install dependencies using pip from requirements.txt
            requirements_file = current_dir / "requirements.txt"
            subprocess.run(["pip", "install", "--upgrade", "--no-cache-dir", "-r", str(requirements_file)])

            # Create configuration file
            self.create_config_file()

            # Create .installed file
            with open(install_file,"w") as f:
                f.write("ok")
            print("Installed successfully")

    def create_config_file(self):
        """
        Create a local_config.yaml file with predefined data.

        The function creates a local_config.yaml file with the specified data. The file is saved in the parent directory
        of the current file.

        Args:
            None

        Returns:
            None
        """
        data = {
            "pdf_file_path":  "" # Path to the PDF that will be discussed
        }
        path = self.personality.lollms_paths.personal_configuration_path/"personality_gpt4internet.yaml"
        with open(path, 'w') as file:
            yaml.dump(data, file)