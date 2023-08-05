import subprocess
from pathlib import Path
import requests
from tqdm import tqdm
import yaml

class Install:
    def __init__(self, personality):
        # Get the current directory
        root_dir = Path(".")
        current_dir = Path(__file__).resolve().parent.parent

        # We put this in the shared folder in order as this can be used by other personalities.
        shared_folder = root_dir/"shared"
        blip_folder = shared_folder / "blip"
        install_file = current_dir / ".installed"

        if not install_file.exists():
            print("-------------- blip_ai  -------------------------------")
            print("This is the first time you are using this personality.")
            print("Installing ...")
            # Step 2: Install dependencies using pip from requirements.txt
            requirements_file = current_dir / "requirements.txt"
            subprocess.run(["pip", "install", "--upgrade", "-r", str(requirements_file)])            
            try:
                print("Checking pytorch")
                import torch
                import torchvision
                if torch.cuda.is_available():
                    print("CUDA is supported.")
                else:
                    print("CUDA is not supported. Reinstalling PyTorch with CUDA support.")
                    self.reinstall_pytorch_with_cuda()
            except Exception as ex:
                self.reinstall_pytorch_with_cuda()

            # Create configuration file
            self.create_config_file()

            #Create the install file 
            with open(install_file,"w") as f:
                f.write("ok")
            print("Installed successfully")
            
    def reinstall_pytorch_with_cuda(self):
        subprocess.run(["pip", "install", "torch", "torchvision", "torchaudio", "--no-cache-dir", "--index-url", "https://download.pytorch.org/whl/cu117"])

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
            "image_path": "",     # 
        }
        path = Path(__file__).parent.parent / 'local_config.yaml'
        with open(path, 'w') as file:
            yaml.dump(data, file)