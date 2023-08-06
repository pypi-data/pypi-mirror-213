from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from typing import Optional

import pinecone

import os


def proposal_chatbot(proposal_path: str, memory_window_size: Optional[int] = None, similarity_threshold: float = 0.76, model_name: str = "gpt-4", return_source_documents: bool = False) -> ConversationalRetrievalChain:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
    PROPOSAL_NAMESPACE = os.getenv("PROPOSAL_NAMESPACE")
    VERBOSE = True if os.getenv("VERBOSE") and os.getenv("VERBOSE").lower() == "true"  else False

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    pinecone.init(
        api_key=PINECONE_API_KEY,  # find at app.pinecone.io
        environment=PINECONE_API_ENV  # next to api key in console
    )
    vector_store = Pinecone.from_existing_index(
        index_name=PINECONE_INDEX_NAME, embedding=embeddings)
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "namespace": PROPOSAL_NAMESPACE,
            "filter": {"governance_proposal_path": proposal_path},
            # "score_threshold": similarity_threshold
        })
    llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY,
                     model_name=model_name, verbose=VERBOSE)
    qa_chain = load_qa_chain(llm=llm, chain_type="stuff", verbose=VERBOSE)
    question_generator_chain = LLMChain(
        llm=llm, prompt=CONDENSE_QUESTION_PROMPT, verbose=VERBOSE)

    memory = None
    if memory_window_size:
        memory = ConversationBufferWindowMemory(
            memory_key="chat_history", return_messages=True, k=memory_window_size, output_key="answer")

    return ConversationalRetrievalChain(combine_docs_chain=qa_chain,
                                        retriever=retriever,
                                        return_source_documents=return_source_documents,
                                        memory=memory,
                                        question_generator=question_generator_chain,
                                        verbose=VERBOSE)
