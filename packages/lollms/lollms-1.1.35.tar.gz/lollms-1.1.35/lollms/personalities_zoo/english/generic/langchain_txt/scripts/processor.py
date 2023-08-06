from lollms import APScript, AIPersonality

from langchain.text_splitter import CharacterTextSplitter 
from langchain.embeddings.llamacpp import LlamaCppEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.base_language import BaseLanguageModel
from langchain.schema import BaseMessage, LLMResult, PromptValue, get_buffer_string
from typing import List, Optional, Sequence, Set
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import Callbacks
from pathlib import Path
import yaml

class Processor(APScript):
    """
    A class that processes model inputs and outputs.

    Inherits from APScript.
    """

    def __init__(self, personality: AIPersonality, model = None) -> None:
        super().__init__()
        self.personality = personality
        self.model = model
        self.config = self.load_config_file(Path(__file__).parent.parent / 'local_config.yaml')
        self.build_db()

    @staticmethod
    def read_text_file(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    
    def build_db(self):
        self.txt =  Processor.read_text_file(self.config["txt_file_path"])

        self.text_splitter = CharacterTextSplitter(
            chunk_size=250,
            chunk_overlap=0,
            length_function=len
        )
        self.chunks = self.text_splitter.split_text(self.txt)
        print("Vectorizing document")
        
        self.vector_store = FAISS.from_texts(self.chunks, embedding=self.model)
        print("Vectorization done successfully")

    def process(self, text):
        bot_says = self.bot_says + text
        if self.personality.detect_antiprompt(bot_says):
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
        output =""
        docs = self.vector_store.similarity_search(prompt, k=3)
        chain = load_qa_chain(llm=self.personality.model, chain_type="stuff")
        response = chain.run(input_documents=docs, question=prompt)
        print(f"response: {response}")


        return output



