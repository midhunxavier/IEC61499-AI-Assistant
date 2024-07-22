import zipfile

class Document:
    def __init__(self, text, metadata):
        self.page_content = text
        self.metadata = metadata

def extract_documents_from_zip(file_obj):
    docs_list = []
    with zipfile.ZipFile(file_obj, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith('.fbt'):
                with zip_ref.open(file_info) as file:
                    file_content = file.read()
                    file_content_str = file_content.decode('utf-8')
                    docs_list.append({"text": file_content_str, "source": file_info.filename})
    documents = [Document(doc["text"], {"source": doc["source"]}) for doc in docs_list]
    return documents
