import subprocess
from pathlib import Path
import requests
from tqdm import tqdm
import yaml
from lollms.paths import LollmsPaths
from lollms.personality import AIPersonality
class Install:
    def __init__(self, personality:AIPersonality, force_reinstall=False):
        self.personality = personality
        # Get the current directory
        current_dir = Path(__file__).resolve().parent.parent
        install_folder = current_dir / ".install"

        if not install_folder.exists():
            print("This is the first time you are using this personality.")
            print("Installing ...")
            
            # Step 2: Install dependencies using pip from requirements.txt
            requirements_file = current_dir / "requirements.txt"
            subprocess.run(["pip", "install", "--upgrade", "-r", str(requirements_file)])

            self.create_config_file(personality.lollms_paths.personal_configuration_path/"personality_chain_of_thought.yaml")
            
            with open(install_folder, "w") as file:
                file.write("ok")

    def create_config_file(self, path):
        data = {
            'max_thought_size': 50,
            'max_judgement_size': 50,
            'nb_samples_per_thought': 3
        }
        with open(path, 'w') as file:
            yaml.dump(data, file)
