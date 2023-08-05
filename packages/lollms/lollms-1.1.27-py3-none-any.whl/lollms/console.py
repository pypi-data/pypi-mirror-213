from lollms import AIPersonality, lollms_path, MSG_TYPE
from lollms.binding import BindingConfig, LLMBinding
import lollms
import shutil
import yaml
import importlib
from pathlib import Path
import sys
import pkg_resources
import argparse
from tqdm import tqdm

class ASCIIColors:
    # Reset
    color_reset = '\u001b[0m'

    # Regular colors
    color_black = '\u001b[30m'
    color_red = '\u001b[31m'
    color_green = '\u001b[32m'
    color_yellow = '\u001b[33m'
    color_blue = '\u001b[34m'
    color_magenta = '\u001b[35m'
    color_cyan = '\u001b[36m'
    color_white = '\u001b[37m'

    # Bright colors
    color_bright_black = '\u001b[30;1m'
    color_bright_red = '\u001b[31;1m'
    color_bright_green = '\u001b[32;1m'
    color_bright_yellow = '\u001b[33;1m'
    color_bright_blue = '\u001b[34;1m'
    color_bright_magenta = '\u001b[35;1m'
    color_bright_cyan = '\u001b[36;1m'
    color_bright_white = '\u001b[37;1m'

class BindingBuilder:
    def build_binding(self, bindings_path: Path, cfg: BindingConfig)->LLMBinding:
        binding_path = Path(bindings_path) / cfg["binding_name"]
        # first find out if there is a requirements.txt file
        install_file_name = "install.py"
        install_script_path = binding_path / install_file_name
        if install_script_path.exists():
            module_name = install_file_name[:-3]  # Remove the ".py" extension
            module_spec = importlib.util.spec_from_file_location(module_name, str(install_script_path))
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            if hasattr(module, "Install"):
                module.Install(cfg)
        # define the full absolute path to the module
        absolute_path = binding_path.resolve()
        # infer the module name from the file path
        module_name = binding_path.stem
        # use importlib to load the module from the file path
        loader = importlib.machinery.SourceFileLoader(module_name, str(absolute_path / "__init__.py"))
        binding_module = loader.load_module()
        binding_class = getattr(binding_module, binding_module.binding_name)
        return binding_class
    

class ModelBuilder:
    def __init__(self, binding_class:LLMBinding, config:BindingConfig):
        self.binding_class = binding_class
        self.model = None
        self.build_model(config) 

    def build_model(self, cfg: BindingConfig):
        self.model = self.binding_class(cfg)

    def get_model(self):
        return self.model


class MainMenu:
    def __init__(self, conversation):
        self.binding_infs = []
        self.conversation = conversation

    def show_logo(self):
        print(f"{ASCIIColors.color_bright_yellow}")
        print("█          █        █       █▄ ▄█▄ ▄█       ")
        print("█     ▄▀▀▄ █        █       █ ▀   ▀ █  ▄▀▀▄ ")
        print("█     █  █ █        █       █       █  ▀▄▄  ")
        print("█▄▄▄▄ ▀▄▄▀ █▄▄▄▄▄   █▄▄▄▄   █       █  ▄▄▄▀ ")
        print(f"{ASCIIColors.color_reset}")
        print(f"{ASCIIColors.color_red}Version: {ASCIIColors.color_green}{pkg_resources.get_distribution('lollms').version}")
        print(f"{ASCIIColors.color_red}By : {ASCIIColors.color_green}ParisNeo")
        print(f"{ASCIIColors.color_reset}")

    def show_commands_list(self):
        print()
        print("Commands:")
        print(f"   {ASCIIColors.color_red}├{ASCIIColors.color_reset} menu: shows main menu")        
        print(f"   {ASCIIColors.color_red}├{ASCIIColors.color_reset} help: shows this info")        
        print(f"   {ASCIIColors.color_red}├{ASCIIColors.color_reset} reset: resets the context")
        print(f"   {ASCIIColors.color_red}├{ASCIIColors.color_reset} <empty prompt>: forces the model to continue generating")
        print(f"   {ASCIIColors.color_red}├{ASCIIColors.color_reset} context_infos: current context size and space left before cropping")
        print(f"   {ASCIIColors.color_red}├{ASCIIColors.color_reset} start_log: starts logging the discussion to a text file")
        print(f"   {ASCIIColors.color_red}├{ASCIIColors.color_reset} stop_log: stops logging the discussion to a text file")
        print(f"   {ASCIIColors.color_red}├{ASCIIColors.color_reset} send_file: uploads a file to the AI")
        print(f"   {ASCIIColors.color_red}└{ASCIIColors.color_reset} exit: exists the console")

    def show_menu(self, options):
        print("Menu:")
        for index, option in enumerate(options):
            print(f"{ASCIIColors.color_green}{index + 1} -{ASCIIColors.color_reset} {option}")
        choice = input("Enter your choice: ")
        return int(choice) if choice.isdigit() else -1

    def select_binding(self):
        bindings_list = []
        print()
        print(f"{ASCIIColors.color_green}Current binding: {ASCIIColors.color_reset}{self.conversation.config['binding_name']}")
        for p in (lollms_path/"bindings_zoo").iterdir():
            if p.is_dir():
                with open(p/"binding_card.yaml", "r") as f:
                    card = yaml.safe_load(f)
                with open(p/"models.yaml", "r") as f:
                    models = yaml.safe_load(f)
                entry=f"{card['name']} (by {card['author']})"
                bindings_list.append(entry)
                entry={
                    "name":p.name,
                    "card":card,
                    "models":models
                }
                self.binding_infs.append(entry)
        bindings_list += ["Back"]
        choice = self.show_menu(bindings_list)
        if 1 <= choice <= len(bindings_list)-1:
            print(f"You selected binding: {ASCIIColors.color_green}{self.binding_infs[choice - 1]['name']}{ASCIIColors.color_reset}")
            self.conversation.config['binding_name']=self.binding_infs[choice - 1]['name']
            self.conversation.load_binding()
            self.conversation.config.save_config()
        elif choice <= len(bindings_list):
            return
        else:
            print("Invalid choice!")

    def select_model(self):
        print()
        print(f"{ASCIIColors.color_green}Current model: {ASCIIColors.color_reset}{self.conversation.config['model_name']}")
        models_dir:Path = (lollms_path/"models"/self.conversation.config['binding_name'])
        models_dir.mkdir(parents=True, exist_ok=True)
        models_list = [m.name for m in models_dir.iterdir()] + ["Install model", "Change binding", "Back"]
        choice = self.show_menu(models_list)
        if 1 <= choice <= len(models_list)-3:
            print(f"You selected model: {ASCIIColors.color_green}{models_list[choice - 1]}{ASCIIColors.color_reset}")
            self.conversation.config['model_name']=models_list[choice - 1]
            self.conversation.load_model()
            self.conversation.config.save_config()
        elif choice <= len(models_list)-2:
            self.install_model()
        elif choice <= len(models_list)-1:
            self.select_binding()
            self.menu.select_model()
        elif choice <= len(models_list):
            return
        else:
            print("Invalid choice!")

    def install_model(self):
        models_list = ["Install model from internet","Install model from local file","Back"]
        choice = self.show_menu(models_list)
        if 1 <= choice <= len(models_list)-2:
            url = input("Give a URL to the model to be downloaded :")
            def progress_callback(blocks, block_size, total_size):
                tqdm_bar.total=total_size
                tqdm_bar.update(block_size)

            # Usage example
            with tqdm(total=100, unit="%", desc="Download Progress", ncols=80) as tqdm_bar:
                self.conversation.config.download_model(url,self.conversation.binding_class, progress_callback)
            self.select_model()
        elif choice <= len(models_list)-1:
            path = Path(input("Give a path to the model to be used on your PC:"))
            if path.exists():
                self.conversation.config.reference_model(path)
            self.select_model()
        elif choice <= len(models_list):
            return
        else:
            print("Invalid choice!")

    def select_personality(self):
        print()
        print(f"{ASCIIColors.color_green}Current personality: {ASCIIColors.color_reset}{self.conversation.config['personalities'][self.conversation.config['default_personality_id']]}")
        personality_languages = [p.stem for p in (lollms_path/"personalities_zoo").iterdir() if p.is_dir()] + ["Back"]
        print("Select language")
        choice = self.show_menu(personality_languages)
        if 1 <= choice <= len(personality_languages)-1:
            language = personality_languages[choice - 1]
            print(f"You selected language: {ASCIIColors.color_green}{language}{ASCIIColors.color_reset}")
            personality_categories = [p.stem for p in (lollms_path/"personalities_zoo"/language).iterdir() if p.is_dir()]+["Back"]
            print("Select category")
            choice = self.show_menu(personality_categories)
            if 1 <= choice <= len(personality_categories):
                category = personality_categories[choice - 1]
                print(f"You selected category: {ASCIIColors.color_green}{category}{ASCIIColors.color_reset}")

                personality_names = [p.stem for p in (lollms_path/"personalities_zoo"/language/category).iterdir() if p.is_dir()]+["Back"]
                print("Select personality")
                choice = self.show_menu(personality_names)
                if 1 <= choice <= len(personality_names)-1:
                    name = personality_names[choice - 1]
                    print(f"You selected personality: {ASCIIColors.color_green}{name}{ASCIIColors.color_reset}")
                    self.conversation.config["personalities"]=[f"{language}/{category}/{name}"]
                    self.conversation.load_personality()
                    self.conversation.config.save_config()
                    print("Personality saved successfully!")
                elif 1 <= choice <= len(personality_names):
                    return
                else:
                    print("Invalid choice!")
            elif 1 <= choice <= len(personality_categories):
                return
            else:
                print("Invalid choice!")
        elif 1 <= choice <= len(personality_languages):
            return
        else:
            print("Invalid choice!")

    def main_menu(self):
        while True:
            print("\nMain Menu:")
            print(f"{ASCIIColors.color_green}1 -{ASCIIColors.color_reset} Select Binding")
            print(f"{ASCIIColors.color_green}2 -{ASCIIColors.color_reset} Select Model")
            print(f"{ASCIIColors.color_green}3 -{ASCIIColors.color_reset} Select Personality")
            print(f"{ASCIIColors.color_green}0 -{ASCIIColors.color_reset} Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.select_binding()
            elif choice == "2":
                self.select_model()
            elif choice == "3":
                self.select_personality()
            elif choice == "0":
                print("Exiting the program...")
                break
            else:
                print("Invalid choice! Try again.")

class Conversation:
    def __init__(
                    self, 
                    configuration_path:str|Path=None, 
                    show_logo:bool=True, 
                    show_commands_list:bool=False, 
                    show_personality_infos:bool=True, 
                    show_welcome_message:bool=True
                ):
        
        # Fore it to be a path
        self.is_logging = False
        self.log_file_path = ""
        
        self.bot_says = ""
        
        # Build menu
        self.menu = MainMenu(self)
        
        # Change configuration
        original = lollms_path / "configs/config.yaml"
        if configuration_path is None:
            local = lollms_path / "configs/local_config.yaml"        
        else:
            local = Path(configuration_path)
            
        if not local.exists():
            shutil.copy(original, local)
        self.cfg_path = local

        self.config = BindingConfig(self.cfg_path)
        # load binding
        self.load_binding()

        # Load model
        self.load_model()
        # cfg.binding_name = llm_binding.binding_folder_name
        # cfg.model_name = model_name

        # Load personality
        try:
            self.load_personality()
        except:
            print("No personality selected. Please select one from the zoo.")
            self.menu.select_personality()

        if show_logo:
            self.menu.show_logo()
        if show_commands_list:
            self.menu.show_commands_list()
            
        if show_personality_infos:
            print()
            print(f"{ASCIIColors.color_green}Current personality : {ASCIIColors.color_reset}{self.personality}")
            print(f"{ASCIIColors.color_green}Version : {ASCIIColors.color_reset}{self.personality.version}")
            print(f"{ASCIIColors.color_green}Author : {ASCIIColors.color_reset}{self.personality.author}")
            print(f"{ASCIIColors.color_green}Description : {ASCIIColors.color_reset}{self.personality.personality_description}")
            print()


        # If there is a disclaimer, show it
        if self.personality.disclaimer != "":
            print(f"\n{ASCIIColors.color_red}Disclaimer")
            print(self.personality.disclaimer)
            print(f"{ASCIIColors.color_reset}")

        if show_welcome_message and self.personality.welcome_message:
            print(self.personality.name+": ", end="")
            print(self.personality.welcome_message)
            
    def ask_override_file(self):
        user_input = input("Would you like to override the existing file? (Y/N): ")
        user_input = user_input.lower()
        if user_input == "y" or user_input == "yes":
            print("File will be overridden.")
            return True
        elif user_input == "n" or user_input == "no":
            print("File will not be overridden.")
            return False
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")
            # Call the function again recursively to prompt the user for valid input
            return self.ask_override_file() 
                   
    def start_log(self, file_name):
        if Path(file_name).is_absolute():
            self.log_file_path = Path(file_name)
        else:
            home_dir = Path.home()/"Documents/lollms/logs"
            home_dir.mkdir(parents=True, exist_ok=True)
            self.log_file_path = home_dir/file_name
            if self.log_file_path.exists():
                if not self.ask_override_file():
                    print("Canceled")
                    return
        try:
            with(open(self.log_file_path, "w") as f):
                self.header = f"""------------------------
Log file for lollms discussion                        
Participating personalities:
{self.config['personalities']}                  
------------------------
"""
                f.write(self.header)
            self.is_logging = True
            return True
        except:
            return False            

    def log(self, text, append=False):
        try:
            with(open(self.log_file_path, "a" if append else "w") as f):
                f.write(text) if append else f.write(self.header+self.personality.personality_conditioning+text)
            return True
        except:
            return False            

    def stop_log(self):
        self.is_logging = False           



    def load_binding(self):
        if self.config.binding_name is None:
            print(f"No bounding selected")
            print("Please select a valid model or install a new one from a url")
            self.menu.select_binding()
            # cfg.download_model(url)
        else:
            try:
                self.binding_class = BindingBuilder().build_binding(lollms_path/"bindings_zoo", self.config)
            except Exception as ex:
                print(ex)
                print(f"Couldn't find binding. Please verify your configuration file at {self.cfg_path} or use the next menu to select a valid binding")
                self.menu.select_binding()

    def load_model(self):
        if not self.config.check_model_existance():
            print(f"No model found for binding {self.config['binding_name']}")
            print("Please select a valid model or install a new one from a url")
            self.menu.select_model()
            # cfg.download_model(url)
        else:
            try:
                self.model = ModelBuilder(self.binding_class, self.config).get_model()
            except Exception as ex:
                print(ex)
                print(f"Couldn't load model. Please verify your configuration file at {self.cfg_path} or use the next menu to select a valid model")
                self.menu.select_model()

    def load_personality(self):
        if len(self.config["personalities"][self.config["default_personality_id"]].split("/"))==3:
            self.personality = AIPersonality(lollms_path / "personalities_zoo" / self.config["personalities"][self.config["default_personality_id"]], self.model)
        else:
            self.personality = AIPersonality(self.config["personalities"][self.config["default_personality_id"]], self.model, is_relative_path=False)
        self.cond_tk = self.personality.model.tokenize(self.personality.personality_conditioning)
        self.n_cond_tk = len(self.cond_tk)

    def reset_context(self):
        if self.personality.include_welcome_message_in_disucssion:
            full_discussion = (
                self.personality.ai_message_prefix +
                self.personality.welcome_message +
                self.personality.link_text
            )
        else:
            full_discussion = ""
        return full_discussion
        
    def safe_generate(self, full_discussion:str, n_predict=None, callback=None):
        """safe_generate

        Args:
            full_discussion (string): A prompt or a long discussion to use for generation
            callback (_type_, optional): A callback to call for each received token. Defaults to None.

        Returns:
            str: Model output
        """
        if n_predict == None:
            n_predict =self.personality.model_n_predicts
        tk = self.personality.model.tokenize(full_discussion)
        n_tokens = len(tk)
        fd = self.personality.model.detokenize(tk[-min(self.config.ctx_size-self.n_cond_tk,n_tokens):])
        self.bot_says = ""
        output = self.personality.model.generate(self.personality.personality_conditioning+fd, n_predict=n_predict, callback=callback)
        return output
        
    def start_conversation(self):
        full_discussion = self.reset_context()
        while True:
            try:
                prompt = input(f"{ASCIIColors.color_green}You: {ASCIIColors.color_reset}")
                if prompt == "exit":
                    return
                if prompt == "menu":
                    self.menu.main_menu()
                    continue
                if prompt == "reset":
                    self.reset_context()
                    print(f"{ASCIIColors.color_red}Context reset issued{ASCIIColors.color_reset}")
                    continue
                if prompt == "start_log":
                    fp = input("Please enter a log file path (ex: log.txt): ")               
                    self.start_log(fp)
                    print(f"{ASCIIColors.color_red}Started logging to : {self.log_file_path}{ASCIIColors.color_reset}")
                    continue
                if prompt == "stop_log":
                    self.stop_log()
                    print(f"{ASCIIColors.color_red}Log stopped{ASCIIColors.color_reset}")
                    continue    
                if prompt == "send_file":
                    if self.personality.processor is None:
                        print(f"{ASCIIColors.color_red}This personality doesn't support file reception{ASCIIColors.color_reset}")
                        continue
                    fp = input("Please enter a file path: ")
                    # Remove double quotes using string slicing
                    if fp.startswith('"') and fp.endswith('"'):
                        fp = fp[1:-1]
                    if self.personality.processor.add_file(fp):
                        print(f"{ASCIIColors.color_green}File imported{ASCIIColors.color_reset}")
                    else:
                        print(f"{ASCIIColors.color_red}Couldn't load file{ASCIIColors.color_reset}")
                    continue    
                            
                   
                if prompt == "context_infos":
                    tokens = self.personality.model.tokenize(full_discussion)
                    print(f"{ASCIIColors.color_green}Current context has {len(tokens)} tokens/ {self.config.ctx_size}{ASCIIColors.color_reset}")
                    continue                
                              
                if prompt != '':
                    if self.personality.processor is not None and self.personality.processor_cfg["process_model_input"]:
                        preprocessed_prompt = self.personality.processor.process_model_input(prompt)
                    else:
                        preprocessed_prompt = prompt
                    
                    if self.personality.processor is not None and self.personality.processor_cfg["custom_workflow"]:
                        full_discussion += (
                            self.personality.user_message_prefix +
                            preprocessed_prompt
                        )
                    else:
                        full_discussion += (
                            self.personality.user_message_prefix +
                            preprocessed_prompt +
                            self.personality.link_text +
                            self.personality.ai_message_prefix
                        )

                def callback(text, type:MSG_TYPE=None):
                    if type == MSG_TYPE.MSG_TYPE_CHUNK:
                        print(text, end="", flush=True)
                        bot_says = self.bot_says + text
                        antiprompt = self.personality.detect_antiprompt(bot_says)
                        if antiprompt:
                            self.bot_says = self.remove_text_from_string(bot_says,antiprompt)
                            print("Detected hallucination")
                            return False
                        else:
                            self.bot_says = bot_says
                            return True

                tk = self.personality.model.tokenize(full_discussion)
                n_tokens = len(tk)
                fd = self.personality.model.detokenize(tk[-min(self.config.ctx_size-self.n_cond_tk,n_tokens):])
                
                print(f"{ASCIIColors.color_red}{self.personality.name}:{ASCIIColors.color_reset}", end='', flush=True)
                if self.personality.processor is not None and self.personality.processor_cfg["custom_workflow"]:
                    output = self.personality.processor.run_workflow(prompt, previous_discussion_text=self.personality.personality_conditioning+fd, callback=callback)
                    print(output)

                else:
                    output = self.personality.model.generate(self.personality.personality_conditioning+fd, n_predict=self.personality.model_n_predicts, callback=callback)
                full_discussion += output.strip()
                print()

                if self.personality.processor is not None and self.personality.processor_cfg["process_model_output"]: 
                    output = self.personality.processor.process_model_output(output)

                self.log(full_discussion)
                
            except KeyboardInterrupt:
                print("Keyboard interrupt detected.\nBye")
                break

        print("Done")
        print(f"{self.personality}")

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='App Description')

    # Add the configuration path argument
    parser.add_argument('--configuration_path', default=None,
                        help='Path to the configuration file')
    
    # Parse the command-line arguments
    args = parser.parse_args()
            
    configuration_path = args.configuration_path
        
    conversation = Conversation(configuration_path=configuration_path, show_commands_list=True)
    conversation.start_conversation()
    

if __name__ == "__main__":
    main()