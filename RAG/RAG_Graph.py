from RAG.document_processing import extract_documents_from_zip
from RAG.vector_store import create_vector_store
from RAG.agent_workflow import create_workflow

def setup_workflow(file_obj):
    # Extract documents from the zip file
    documents = extract_documents_from_zip(file_obj)
    
    # Create vector store
    db = create_vector_store(documents)
    retriever = db.as_retriever()
    
    # Create workflow
    workflow = create_workflow(retriever)
    
    return workflow
