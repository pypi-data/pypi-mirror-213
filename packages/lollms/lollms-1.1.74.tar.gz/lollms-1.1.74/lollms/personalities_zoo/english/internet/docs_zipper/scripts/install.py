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
                            
            # Step 2: Install dependencies using pip from requirements.txt
            requirements_file = current_dir / "requirements.txt"
            if requirements_file.exists():
                subprocess.run(["pip", "install", "--upgrade", "--no-cache-dir", "-r", str(requirements_file)])

            # Create configuration file
            self.create_config_file()

            # Create .installed file
            with open(install_file,"w") as f:
                f.write("ok")
            print("Installed successfully")

    def reinstall_pytorch_with_cuda(self):
        return subprocess.run(["pip", "install", "--upgrade", "torch", "torchvision", "torchaudio", "--upgrade", "--no-cache-dir", "--index-url", "https://download.pytorch.org/whl/cu117"])


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
            "database_path":    f"{self.personality.name}_db.json",
            "chunk_size":       512, # Max chunk size
            "overlap_size":     50, # Overlap between text chunks
            "max_answer_size":  128,  # Maximum answer size
            "visualize_data_at_startup":            False,
            "visualize_data_at_add_file":           False,            
            "visualize_data_at_generate":           False,            
        }
        path = self.personality.lollms_paths.personal_configuration_path/f"personality_{self.personality.name}.yaml"
        with open(path, 'w') as file:
            yaml.dump(data, file)