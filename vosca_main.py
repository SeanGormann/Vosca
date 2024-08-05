import os
from dotenv import load_dotenv, find_dotenv

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langsmith import Client

import json
#from langchain.llms import Mistral
#from langchain.embeddings import HuggingFaceEmbeddings


from transformers import AutoTokenizer, AutoModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.document_loaders import JSONLoader


import tiktoken
from bs4 import BeautifulSoup as Soup
import json


load_dotenv(find_dotenv())
os.environ["LANGCHAIN_API_KEY"] = str(os.getenv("LANGCHAIN_API_KEY"))
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "vosca"




# Load the LangSmith Client and Test Run
client = Client()

model = "mistral:instruct"
llm = ChatOllama(model=model)

#llm = Mistral(model_path="nomic-embed-text-v1.5.Q2_K.gguf")


"""
prompt = ChatPromptTemplate.from_template("Write code to {topic}")

# using LangChain Expressive Language chain syntax
# learn more about the LCEL on
# https://python.langchain.com/docs/expression_language/why
chain = prompt | llm | StrOutputParser()

# for brevity, response is printed in terminal
# You can use LangServe to deploy your application for production
print(chain.invoke({"topic": "create a wrapper function that tests for errors and logs them"}))

"""

#embeddings = HuggingFaceEmbeddings()



def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


#load in scraped_docs_updates.json
with open("scraped_docs_updated_again.json", "r") as file:
    docs = json.load(file)


docs_texts = [d['content'] for d in docs['documents']]
docs_code = [d['code_examples'] for d in docs['documents']]
combined_docs = [d['content'] + " " + " ".join(d['code_examples']) for d in docs['documents']]
# Calculate the number of tokens for each document
counts = [num_tokens_from_string(d, "cl100k_base") for d in combined_docs]



loader = JSONLoader(
    file_path='scraped_docs_updated_again.json', #data_docs
    jq_schema=".documents[]",
    content_key="content",
    #is_content_key_jq_parsable=True,
    )

data = loader.load()
data


urls = JSONLoader(
    file_path='scraped_docs_updated_again.json',
    jq_schema=".documents[]",
    content_key="url",
    )

titles = JSONLoader(
    file_path='scraped_docs_updated_again.json',
    jq_schema=".documents[]",
    content_key="title",
    )

titles = titles.load()
urls = urls.load()


# Embed and index Nomic v1.5
embd_model_path = "nomic-embed-text-v1.5.Q2_K.gguf"
embedding = LlamaCppEmbeddings(model_path=embd_model_path, n_batch=512, verbose=False)

# Index
vectorstore = Chroma.from_documents(
    documents=data,
    collection_name="rag-chroma",
    embedding=embedding,
)

retriever = vectorstore.as_retriever()



prompt = ChatPromptTemplate.from_template("Answer the following question: {topic}")

chain = prompt | llm | StrOutputParser()

ques = "How can I create a window for my VisionOS application?"
response = chain.invoke({"topic": ques})
print("\n\n")
print(response)



# Simple RAG 
prompt = ChatPromptTemplate.from_template("Here are some relevant documents from the VisionOS documentation: {documents}. \n\
                                          Use the above documents to answer the following question: {topic}")

chain = prompt | llm | StrOutputParser()

ques = "How can I create a window for my VisionOS application?"
response = chain.invoke({"topic": ques, "documents": retriever.get_relevant_documents(ques)})
print("\n\n")
print(response)