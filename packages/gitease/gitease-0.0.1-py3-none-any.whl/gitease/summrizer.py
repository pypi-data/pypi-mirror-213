from langchain import OpenAI, PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from pathlib import Path


class Summarizer:
    def __init__(self, verbose: bool = True):
        prompt = PromptTemplate(template=Path("gitease/prompts/prompt_template.txt").read_text(),
                                input_variables=["text"])
        self.summarize_chain = load_summarize_chain(llm=OpenAI(temperature=0),
                                                    chain_type="map_reduce",
                                                    map_prompt=prompt,
                                                    combine_prompt=prompt,
                                                    verbose=verbose)

    def summarize(self, text: str):
        return self.summarize_chain.run([Document(page_content=text)])
