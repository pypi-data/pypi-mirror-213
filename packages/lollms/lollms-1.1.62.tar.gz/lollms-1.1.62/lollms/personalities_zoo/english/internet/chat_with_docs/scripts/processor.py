from lollms.personality import APScript, AIPersonality
from lollms.helpers import ASCIIColors

import torch
import numpy as np
import torch
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import json
from pathlib import Path
import PyPDF2

class TextVectorizer:
    def __init__(self, model_name, database_file:Path|str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.embeddings = {}
        self.texts = {}
        self.ready = False
        self.database_file = Path(database_file)

        # Load previous state from the JSON file
        if Path(self.database_file).exists():
            self.load_from_json()

    def index_document(self, document_id, text, chunk_size, force_vectorize=False):
        if document_id in self.embeddings and not force_vectorize:
            print(f"Document {document_id} already exists. Skipping vectorization.")
            return

        # Tokenize text
        tokens = self.tokenizer.encode(text)

        # Split tokens into chunks
        chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]

        # Generate embeddings for each chunk
        for i, chunk in enumerate(chunks):
            # Convert tokens to IDs
            input_ids = chunk

            # Convert input to PyTorch tensor
            input_tensor = torch.tensor([input_ids])

            # Generate chunk embedding
            with torch.no_grad():
                self.model.eval()
                outputs = self.model(input_tensor)
                embeddings = outputs.last_hidden_state.mean(dim=1)

            # Store chunk ID, embedding, and original text
            chunk_id = f"{document_id}_chunk_{i + 1}"
            self.embeddings[chunk_id] = embeddings
            self.texts[chunk_id] = self.tokenizer.decode(chunk)

        self.save_to_json()
        self.ready = True

    def embed_query(self, query_text):
        # Tokenize query text
        query_tokens = self.tokenizer.encode(query_text)

        # Convert input to PyTorch tensor
        query_input_tensor = torch.tensor([query_tokens])

        # Generate query embedding
        with torch.no_grad():
            self.model.eval()
            query_outputs = self.model(query_input_tensor)
            query_embedding = query_outputs.last_hidden_state.mean(dim=1)

        return query_embedding

    def recover_text(self, query_embedding, top_k=1):
        similarities = {}
        for chunk_id, chunk_embedding in self.embeddings.items():
            similarity = cosine_similarity(query_embedding.numpy(), chunk_embedding.numpy())[0][0]
            similarities[chunk_id] = similarity

        # Sort the similarities and retrieve the top-k most similar embeddings
        sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k]

        # Retrieve the original text associated with the most similar embeddings
        texts = [self.texts[chunk_id] for chunk_id, _ in sorted_similarities]

        return texts

    def save_to_json(self):
        state = {
            "embeddings": {str(k): v.tolist() for k, v in self.embeddings.items()},
            "texts": self.texts,
        }
        with open(self.database_file, "w") as f:
            json.dump(state, f)

    def load_from_json(self):
        with open(self.database_file, "r") as f:
            state = json.load(f)
            self.embeddings = {k: torch.tensor(v) for k, v in state["embeddings"].items()}
            self.texts = state["texts"]
            self.ready = True


class Processor(APScript):
    """
    A class that processes model inputs and outputs.

    Inherits from APScript.
    """

    def __init__(self, personality: AIPersonality, model = None) -> None:
        super().__init__()
        self.personality = personality
        self.model = model
        try:
            self.config = self.load_config_file(self.personality.lollms_paths.personal_configuration_path/f"personality_{self.personality.name}.yaml")
        except Exception as ex:
            print("Error loading configuration file.\nTrying to reinstall.")
            self.install_personality(Path(__file__).parent.parent, force_reinstall=True)
            self.config = self.load_config_file(self.personality.lollms_paths.personal_configuration_path/f"personality_{self.personality.name}.yaml")

        self.vector_store = TextVectorizer("bert-base-uncased", self.personality.lollms_paths.personal_data_path/self.config["database_path"])
        self.personality.lollms_paths.personal_configuration_path/f"personality_{self.personality.name}.yaml"

    @staticmethod        
    def read_pdf_file(file_path):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text


    @staticmethod
    def read_text_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    
    def build_db(self):
        ASCIIColors.info("-> Vectorizing the database"+ASCIIColors.color_orange)
        for file in self.files:
            try:
                if Path(file).suffix==".pdf":
                    text =  Processor.read_pdf_file(file)
                else:
                    text =  Processor.read_text_file(file)
                try:
                    chunk_size=int(self.config["chunk_size"])
                except:
                    ASCIIColors.warning(f"Couldn't read chunk size. Verify your configuration file")
                    chunk_size=512
                self.vector_store.index_document(file, text, chunk_size=chunk_size)
                print(ASCIIColors.color_reset)
                ASCIIColors.success(f"File {file} vectorized successfully")
            except Exception as ex:
                ASCIIColors.error(f"Couldn't vectorize {file}: The vectorizer threw this exception:{ex}")

    def add_file(self, path):
        super().add_file(path)
        try:
            self.build_db()
            return True
        except Exception as ex:
            ASCIIColors.error(f"Couldn't vectorize the database: The vectgorizer threw this exception: {ex}")
            return False        

    

    def run_workflow(self, prompt, previous_discussion_text="", callback=None):
        """
        Runs the workflow for processing the model input and output.

        This method should be called to execute the processing workflow.

        Args:
            generate_fn (function): A function that generates model output based on the input prompt.
                The function should take a single argument (prompt) and return the generated text.
            prompt (str): The input prompt for the model.
            previous_discussion_text (str, optional): The text of the previous discussion. Default is an empty string.

        Returns:
            None
        """
        output =""

        docs = self.vector_store.recover_text(self.vector_store.embed_query(prompt), top_k=2)
        docs = '\nDoc:\n'.join([v for v in docs])
        full_text = self.personality.personality_conditioning+"\n### Documentation:\nDoc:\n"+docs+"### Question: "+prompt+"\n### Answer:"
        output = self.generate(full_text, self.config["max_answer_size"])
        return output



