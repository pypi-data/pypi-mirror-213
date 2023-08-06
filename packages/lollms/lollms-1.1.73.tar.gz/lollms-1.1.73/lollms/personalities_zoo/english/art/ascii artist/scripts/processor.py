from pathlib import Path
from lollms.personality import APScript, AIPersonality, MSG_TYPE
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
        self.config = self.load_config_file(self.personality.lollms_paths.personal_configuration_path / 'personality_painter_config.yaml')
        self.sd = self.get_sd().SD(self.personality.lollms_paths, self.config)

    def get_sd(self):
        sd_script_path = Path(__file__).parent / "sd.py"
        if sd_script_path.exists():
            module_name = sd_script_path.stem  # Remove the ".py" extension
            # use importlib to load the module from the file path
            loader = importlib.machinery.SourceFileLoader(module_name, str(sd_script_path))
            sd_module = loader.load_module()
            return sd_module


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

        # 1 first ask the model to formulate a query
        prompt = f"{self.remove_image_links(previous_discussion_text+self.personality.user_message_prefix+prompt+self.personality.link_text)}\n### Instruction:\nWrite a more detailed description of the proposed image. Include information about the image style.\n### Imagined description:\n"
        print(prompt)
        sd_prompt = self.generate(prompt, self.config["max_generation_prompt_size"])
        if callback is not None:
            callback(sd_prompt+"\n", MSG_TYPE.MSG_TYPE_CHUNK)

        files = self.sd.generate(sd_prompt, self.config["num_images"], self.config["seed"])
        output = ""
        for i in range(len(files)):
            print("Converting image to ascii")
            image = Image.open(files[i])
            (width, height) = image.size
            ascii_art = convert_to_ascii_art(image)
            output +="```\n"+ "\n".join(ascii_art) + "\n```"


        return output


