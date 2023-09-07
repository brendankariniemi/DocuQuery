import hashlib

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from caching import cache_data, get_cached_data


def load_and_split_text(file_path):
    cache_key = get_file_hash(file_path)
    texts = get_cached_data(cache_key)

    if texts is None:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separators=["\n"])
        texts = text_splitter.split_documents(documents)
        cache_data(cache_key, texts)

    return texts


def get_file_hash(file_path):
    sha256_hash = hashlib.sha256()

    with open(file_path, 'rb') as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)

    file_hash = sha256_hash.hexdigest()
    return file_hash
