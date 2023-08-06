import subprocess
from pathlib import Path
import os
import sys
from lollms.personality import APScript, AIPersonality, MSG_TYPE
from lollms.paths import LollmsPaths
import time
import sys
import re
import importlib

class Processor(APScript):
    """
    A class that processes model inputs and outputs.

    Inherits from APScript.
    """

    def __init__(self, personality: AIPersonality) -> None:
        super().__init__()
        self.personality = personality
        self.word_callback = None
        self.config = self.load_config_file(self.personality.lollms_paths.personal_configuration_path / 'personality_artbot_config.yaml')
        self.sd = self.get_sd().SD(self.personality.lollms_paths, self.config)

    def get_sd(self):
        sd_script_path = Path(__file__).parent / "sd.py"
        if sd_script_path.exists():
            module_name = sd_script_path.stem  # Remove the ".py" extension
            # use importlib to load the module from the file path
            loader = importlib.machinery.SourceFileLoader(module_name, str(sd_script_path))
            sd_module = loader.load_module()
            return sd_module

    def remove_image_links(self, markdown_text):
        # Regular expression pattern to match image links in Markdown
        image_link_pattern = r"!\[.*?\]\((.*?)\)"

        # Remove image links from the Markdown text
        text_without_image_links = re.sub(image_link_pattern, "", markdown_text)

        return text_without_image_links


    

    def run_workflow(self, prompt, previous_discussion_text="", callback=None):
        """
        Runs the workflow for processing the model input and output.

        This method should be called to execute the processing workflow.

        Args:
            prompt (str): The input prompt for the model.
            previous_discussion_text (str, optional): The text of the previous discussion. Default is an empty string.
            callback a callback function that gets called each time a new token is received
        Returns:
            None
        """
        self.word_callback = callback

        # 1 first ask the model to formulate a query
        prompt = f"{self.remove_image_links(previous_discussion_text+self.personality.link_text+self.personality.ai_message_prefix)}\n"
        print(prompt)
        sd_prompt = self.generate(prompt, self.config["max_generation_prompt_size"])
        if callback is not None:
            callback(sd_prompt.strip()+"\n", MSG_TYPE.MSG_TYPE_CHUNK)

        files = self.sd.generate(sd_prompt.strip(), self.config["num_images"], self.config["seed"])
        output = sd_prompt.strip()+"\n"
        for i in range(len(files)):
            files[i] = str(files[i]).replace("\\","/")
            output += f"![]({files[i]})\n"

        return output


