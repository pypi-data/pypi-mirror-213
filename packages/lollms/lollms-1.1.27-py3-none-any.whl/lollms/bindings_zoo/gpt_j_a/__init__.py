######
# Project       : GPT4ALL-UI
# File          : binding.py
# Author        : ParisNeo with the help of the community
# Underlying binding : Abdeladim's pygptj binding
# Supported by Nomic-AI
# license       : Apache 2.0
# Description   : 
# This is an interface class for GPT4All-ui bindings.

# This binding is a wrapper to abdeladim's binding
# Follow him on his github project : https://github.com/abdeladim-s/pygptj

######
from pathlib import Path
from typing import Callable
from pygptj.model import Model
from lollms.binding import LLMBinding, BindingConfig
from lollms  import MSG_TYPE

__author__ = "parisneo"
__github__ = "https://github.com/ParisNeo/lollms_bindings_zoo"
__copyright__ = "Copyright 2023, "
__license__ = "Apache 2.0"

binding_name = "GptJ"
binding_folder_name = "gpt_j_a"

class GptJ(LLMBinding):
    file_extension='*.bin'
    def __init__(self, config:BindingConfig) -> None:
        """Builds a LLAMACPP binding

        Args:
            config (dict): The configuration file
        """
        super().__init__(config, False)
        
        if self.config.model_name.endswith(".reference"):
            with open(str(self.config.models_path/f"{binding_folder_name}/{self.config.model_name}"),'r') as f:
                model_path=f.read()
        else:
            model_path=str(self.config.models_path/f"{binding_folder_name}/{self.config.model_name}")

        self.model = Model(
                model_path=model_path,
                prompt_context="", prompt_prefix="", prompt_suffix=""
                )
    def tokenize(self, prompt:str):
        """
        Tokenizes the given prompt using the model's tokenizer.

        Args:
            prompt (str): The input prompt to be tokenized.

        Returns:
            list: A list of tokens representing the tokenized prompt.
        """
        return None

    def detokenize(self, tokens_list:list):
        """
        Detokenizes the given list of tokens using the model's tokenizer.

        Args:
            tokens_list (list): A list of tokens to be detokenized.

        Returns:
            str: The detokenized text as a string.
        """
        return None
    def generate(self, 
                 prompt:str,                  
                 n_predict: int = 128,
                 callback: Callable[[str], None] = bool,
                 verbose: bool = False,
                 **gpt_params ):
        """Generates text out of a prompt

        Args:
            prompt (str): The prompt to use for generation
            n_predict (int, optional): Number of tokens to prodict. Defaults to 128.
            callback (Callable[[str], None], optional): A callback function that is called everytime a new text element is generated. Defaults to None.
            verbose (bool, optional): If true, the code will spit many informations about the generation process. Defaults to False.
        """
        try:
            self.model.reset()
            output = ""
            for tok in self.model.generate(prompt, 
                                           n_predict=n_predict,                                           
                                            temp=gpt_params["temperature"],
                                            top_k=gpt_params['top_k'],
                                            top_p=gpt_params['top_p'],
                                            #repeat_penalty=gpt_params['repeat_penalty'],
                                            #repeat_last_n = self.config['repeat_last_n'],
                                            n_threads=self.config['n_threads'],
                                           ):
                output += tok
                if callback is not None:
                    if not callback(tok, MSG_TYPE.MSG_TYPE_CHUNK):
                        return output
        except Exception as ex:
            print(ex)
        return output