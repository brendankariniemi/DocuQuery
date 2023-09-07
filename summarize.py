from langchain import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains.summarize import load_summarize_chain

from caching import get_cached_data, cache_data
from config import SUMMARIZE_DOCUMENTS, DOCUQUERY_PDF, DOCUQUERY_SUMMARY
from utils import load_and_split_text, get_file_hash


def generate_summary(file_path):
    try:
        if file_path == DOCUQUERY_PDF:
            return DOCUQUERY_SUMMARY

        if SUMMARIZE_DOCUMENTS:
            cache_key = 'Summary - ' + get_file_hash(file_path)
            summary = get_cached_data(cache_key)

            if summary is None:
                texts = load_and_split_text(file_path)
                chain = load_summarize_chain(llm=OpenAI(), chain_type="map_reduce")

                with get_openai_callback() as cb:
                    summary = chain.run(texts)
                print(cb)

                cache_data(cache_key, summary)

            return summary
        else:
            return 'SUMMARIZE_DOCUMENTS = False'
    except Exception as e:
        return str(e)
