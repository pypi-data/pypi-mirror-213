import subprocess
from pathlib import Path
import os
import sys
from lollms import APScript, AIPersonality, MSG_TYPE
import time
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent))
import torch
from torchvision import transforms
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration
   
class Processor(APScript):
    """
    A class that processes model inputs and outputs.

    Inherits from APScript.
    """

    def __init__(self, personality: AIPersonality) -> None:
        super().__init__()
        self.personality = personality
        self.word_callback = None
        self.generate_fn = None
        self.model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")
        self.processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")

        self.config = self.load_config_file(Path(__file__).parent.parent / 'local_config.yaml')
        if self.config["image_path"]!="":
            self.raw_image = Image.open(self.config["image_path"]).convert('RGB')

    def add_file(self, path):
        # only one path is required
        self.files = [path]

    def remove_file(self, path):
        # only one path is required
        self.files = []

    def remove_text_from_string(self, string, text_to_find):
        """
        Removes everything from the first occurrence of the specified text in the string (case-insensitive).

        Parameters:
        string (str): The original string.
        text_to_find (str): The text to find in the string.

        Returns:
        str: The updated string.
        """
        index = string.lower().find(text_to_find.lower())

        if index != -1:
            string = string[:index]

        return string
    
    def process(self, text):
        bot_says = self.bot_says + text
        antiprompt = self.personality.detect_antiprompt(bot_says)
        if antiprompt:
            self.bot_says = self.remove_text_from_string(bot_says,antiprompt)
            print("Detected hallucination")
            return False
        else:
            self.bot_says = bot_says
            return True

    def generate(self, prompt, max_size):
        self.bot_says = ""
        return self.personality.model.generate(
                                prompt, 
                                max_size, 
                                self.process,
                                temperature=self.personality.model_temperature,
                                top_k=self.personality.model_top_k,
                                top_p=self.personality.model_top_p,
                                repeat_penalty=self.personality.model_repeat_penalty,
                                ).strip()    
        

    def run_workflow(self, prompt, previous_discussion_text="", callback=None):
        """
        Runs the workflow for processing the model input and output.

        This method should be called to execute the processing workflow.

        Args:
            generate_fn (function): A function that generates model output based on the input prompt.
                The function should take a single argument (prompt) and return the generated text.
            prompt (str): The input prompt for the model.
            previous_discussion_text (str, optional): The text of the previous discussion. Default is an empty string.
            callback a callback function that gets called each time a new token is received
        Returns:
            None
        """
        self.word_callback = callback
        inputs = self.processor(self.raw_image, prompt, return_tensors="pt").to("cpu") #"cuda")
        output = self.processor.decode(self.model.generate(**inputs)[0], skip_special_tokens=True)
        return output


