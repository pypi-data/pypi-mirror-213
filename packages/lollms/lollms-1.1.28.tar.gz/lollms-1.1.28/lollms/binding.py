######
# Project       : GPT4ALL-UI
# File          : binding.py
# Author        : ParisNeo with the help of the community
# Supported by Nomic-AI
# license       : Apache 2.0
# Description   : 
# This is an interface class for GPT4All-ui bindings.
######
from pathlib import Path
from typing import Callable
from lollms.paths import lollms_path, lollms_bindings_zoo_path, lollms_personalities_zoo_path, lollms_personal_configuration_path, lollms_personal_models_path
import inspect
import yaml
import sys
from tqdm import tqdm
import urllib.request

__author__ = "parisneo"
__github__ = "https://github.com/ParisNeo/lollms_bindings_zoo"
__copyright__ = "Copyright 2023, "
__license__ = "Apache 2.0"


import yaml

DEFAULT_CONFIG = {
    # =================== Lord Of Large Language Models Configuration file =========================== 
    "version": 5,
    "binding_name": "llama_cpp_official",
    "model_name": "Wizard-Vicuna-7B-Uncensored.ggmlv3.q4_0.bin",

    # Host information
    "host": "localhost",
    "port": 9600,

    # Genreration parameters 
    "seed": -1,
    "n_predict": 1024,
    "ctx_size": 2048,
    "temperature": 0.9,
    "top_k": 50,
    "top_p": 0.95,
    "repeat_last_n": 40,
    "repeat_penalty": 1.2,

    "n_threads": 8,

    #Personality parameters
    "personalities": ["english/generic/lollms"],
    "default_personality_id": 0,
    "override_personality_model_parameters": False, #if true the personality parameters are overriden by those of the configuration (may affect personality behaviour) 

    "user_name": "user",

}


class BindingConfig:
    def __init__(self, file_path=None, models_path = None, bindings_path = None, personalities_path = None):
        
        self.config = None
                
        if file_path:
            self.file_path = Path(file_path)
            self.configs_path = self.file_path.parent
            if models_path is None:
                self.models_path = lollms_personal_models_path
            else:
                self.models_path = Path(models_path)
            if bindings_path is None:
                self.bindings_path = lollms_bindings_zoo_path
            else:
                self.bindings_path = Path(bindings_path)
            if personalities_path is None:
                self.personalities_path = lollms_personalities_zoo_path
            else:
                self.personalities_path = Path(personalities_path)

                
        else:
            self.file_path = None
            self.configs_path  = lollms_personal_configuration_path
            self.models_path = lollms_personal_models_path
            self.bindings_path = lollms_bindings_zoo_path
            self.personalities_path = lollms_personalities_zoo_path

        if file_path is not None:
            self.load_config(file_path)
        else:
            self.config = DEFAULT_CONFIG.copy()

    def to_dict(self):
        return self.config


    def check_model_existance(self):
        try:
            model_path = self.models_path/self.binding_name/self.model_name
            return model_path.exists()
        except:
            return False 
           
    def download_model(self, url, binding, callback = None):
        folder_path = self.models_path/self.binding_name
        model_name  = url.split("/")[-1]
        model_full_path = (folder_path / model_name)
        if binding is not None and hasattr(binding,'download_model'):
            binding.download_model(url, model_full_path, callback)
        else:

            # Check if file already exists in folder
            if model_full_path.exists():
                print("File already exists in folder")
            else:
                # Create folder if it doesn't exist
                folder_path.mkdir(parents=True, exist_ok=True)
                progress_bar = tqdm(total=None, unit="B", unit_scale=True, desc=f"Downloading {url.split('/')[-1]}")
                # Define callback function for urlretrieve
                def report_progress(block_num, block_size, total_size):
                    progress_bar.total=total_size
                    progress_bar.update(block_size)
                # Download file from URL to folder
                try:
                    urllib.request.urlretrieve(url, folder_path / url.split("/")[-1], reporthook=report_progress if callback is None else callback)
                    print("File downloaded successfully!")
                except Exception as e:
                    print("Error downloading file:", e)
                    sys.exit(1)

    def reference_model(self, path):
        path = str(path).replace("\\","/")
        folder_path = self.models_path/self.binding_name
        model_name  = path.split("/")[-1]+".reference"
        model_full_path = (folder_path / model_name)

        # Check if file already exists in folder
        if model_full_path.exists():
            print("File already exists in folder")
        else:
            # Create folder if it doesn't exist
            folder_path.mkdir(parents=True, exist_ok=True)
            with open(model_full_path,"w") as f:
                f.write(path)
            print("Reference created, please make sure you don't delete the file or you will have broken link")

    def __getitem__(self, key):
        if self.config is None:
            raise ValueError("No configuration loaded.")
        return self.config[key]

    def __getattr__(self, key):
        if key in ["file_path", "config", "models_path", "bindings_path", "personalities_path"] or key.startswith("__"):
            return super().__getattribute__(key)
        else:
            if self.config is None:
                raise ValueError("No configuration loaded.")
            return self.config[key]


    def __setattr__(self, key, value):
        if key in ["file_path", "config","models_path","bindings_path","personalities_path","configs_path"] or key.startswith("__"):
            super().__setattr__(key, value)
        else:
            if self.config is None:
                raise ValueError("No configuration loaded.")
            self.config[key] = value

    def __setitem__(self, key, value):
        if self.config is None:
            raise ValueError("No configuration loaded.")
        self.config[key] = value
    
    def __contains__(self, item):
        if self.config is None:
            raise ValueError("No configuration loaded.")
        return item in self.config

    def load_config(self, file_path:Path=None):
        if file_path is None:
            file_path = self.file_path
        with open(file_path, 'r', encoding='utf-8') as stream:
            self.config = yaml.safe_load(stream)

    def save_config(self, file_path:Path=None):
        if file_path is None:
            file_path = self.file_path
        if self.config is None:
            raise ValueError("No configuration loaded.")
        with open(file_path, "w") as f:
            yaml.dump(self.config, f)


class BindingInstaller:
    def __init__(self, config: BindingConfig) -> None:
        self.config = config

class LLMBinding:
   
    file_extension='*.bin'
    binding_path = Path(__file__).parent
    def __init__(self, config:BindingConfig, inline:bool) -> None:
        self.config = config
        self.inline = inline

    def load_config_file(self, path):
        """
        Load the content of local_config.yaml file.

        The function reads the content of the local_config.yaml file and returns it as a Python dictionary.

        Args:
            None

        Returns:
            dict: A dictionary containing the loaded data from the local_config.yaml file.
        """     
        with open(path, 'r') as file:
            data = yaml.safe_load(file)
        return data


    def generate(self, 
                 prompt:str,                  
                 n_predict: int = 128,
                 callback: Callable[[str], None] = None,
                 verbose: bool = False,
                 **gpt_params ):
        """Generates text out of a prompt
        This should ber implemented by child class

        Args:
            prompt (str): The prompt to use for generation
            n_predict (int, optional): Number of tokens to prodict. Defaults to 128.
            callback (Callable[[str], None], optional): A callback function that is called everytime a new text element is generated. Defaults to None.
            verbose (bool, optional): If true, the code will spit many informations about the generation process. Defaults to False.
        """
        pass
    def tokenize(self, prompt:str):
        """
        Tokenizes the given prompt using the model's tokenizer.

        Args:
            prompt (str): The input prompt to be tokenized.

        Returns:
            list: A list of tokens representing the tokenized prompt.
        """
        pass

    def detokenize(self, tokens_list:list):
        """
        Detokenizes the given list of tokens using the model's tokenizer.

        Args:
            tokens_list (list): A list of tokens to be detokenized.

        Returns:
            str: The detokenized text as a string.
        """
        pass

    @staticmethod
    def list_models(config:dict, root_path="."):
        """Lists the models for this binding
        """
        root_path = Path(root_path)
        models_dir =(root_path/'models')/config["binding_name"]  # replace with the actual path to the models folder
        return [f.name for f in models_dir.glob(LLMBinding.file_extension)]
    
    @staticmethod
    def get_available_models():
        # Create the file path relative to the child class's directory
        binding_path = Path(__file__).parent
        file_path = binding_path/"models.yaml"

        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
        
        return yaml_data

