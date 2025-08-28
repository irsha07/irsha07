# services/rag_engine.py
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

CHROMA_DB_PATH = "data/chroma"

def get_rag_chain(subject: str):
    """Initializes and returns a RetrievalQA chain for a specific subject."""
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings,
        collection_name=subject.lower().replace(" ", "_")
    )
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )
    return chain

def get_rag_context_and_sources(query: str, subject: str):
    """
    Gets the retrieved context and also returns the raw source text.
    """
    chain = get_rag_chain(subject)
    retrieved_docs = chain.retriever.invoke(query)
    # Combine the content of the retrieved documents for the AI context
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    print(f"\n--- Retrieved Context for Query: '{query}' ---\n{context}\n----------------------------------------\n")
    return context, context # Return the same text for both for simplicity

def get_rag_response(query: str, subject: str) -> str:
    """Gets a response from the RAG chain for a given query and subject."""
    chain = get_rag_chain(subject)
    result = chain.invoke({"query": query})
    return result.get("result", "I'm not sure how to answer that.")
