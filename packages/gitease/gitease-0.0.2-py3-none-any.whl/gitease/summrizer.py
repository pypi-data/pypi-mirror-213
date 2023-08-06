from langchain import OpenAI, PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from pathlib import Path
import openai.error
from langchain.text_splitter import RecursiveCharacterTextSplitter

class Summarizer:
    def __init__(self, verbose: bool = True):
        prompt = PromptTemplate(template=Path("gitease/prompts/prompt_template.txt").read_text(),
                                input_variables=["text"])
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=20,
            length_function=len,
        )
        self.summarize_chain = load_summarize_chain(llm=OpenAI(temperature=0),
                                                    chain_type="map_reduce",
                                                    map_prompt=prompt,
                                                    combine_prompt=prompt,
                                                    verbose=verbose)

    def summarize(self, text: str):
        try:
            texts = self.text_splitter.create_documents([text])
            return self.summarize_chain.run(texts)
        except openai.error.InvalidRequestError as e:
            print(e)

        raise RuntimeError("Summarization failed - try to add a single file")
