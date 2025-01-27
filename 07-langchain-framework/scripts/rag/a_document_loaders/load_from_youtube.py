from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser

def execute():
    video_url = 'https://www.youtube.com/watch?v=xsbx93-gf08'
    video_local_dir = 'files/youtube'

    loader = GenericLoader(
        YoutubeAudioLoader([video_url], video_local_dir),
        OpenAIWhisperParser(),
    )
    documents = loader.load()

    print(f'Document chunk 0 Content: {documents[0].page_content}')
    print(f'Document chunk 0 Metadata: {documents[0].metadata}')
