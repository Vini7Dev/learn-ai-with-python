# Learn AI With Python
Learn Python for Artificial Intelligence Applications with ASIMOV Academy

## 01 Setup Project

> Project dependencies

> Configure projet import - Root folder to import

> Python Virtual Environment

## 02 Starting OpenAI Lib

### **[SIMPLE] Text generation chats**

> Chat Stream: My Chat GPT

> Temperature Chat: Chat Tools (calling APIs to give information to AI response)

> Finance Chat: Chat Tools (calling APIs to give information to AI response)

> Fine Tuning: Create models with sandarlization in the AI response messages

### **[ADVANCED] Assistants API: OpenAI Ready-Made Tools**

> Math Assistant: Code interpreter, to create and execute Python codes

> Finance Assistant: Reading CSV file to made a finance analytics

> Attendant Assistant: Reading PDFs to respond questions

### **Working with Images: DALL-E e GPT-Vision**

> Image Generator: Generate, edit and variate images with Dall-E

> GPT Vision: Image analyzation

### **Audio Generation and Transcription**

> Audio Generation: Create audio by text (with or without stream)

> Audio Transcription: Extract text from audio

> Voice Chat: Talking with AI

## 03 Streamlit Web Apps

> Streamlit Docs: https://docs.streamlit.io/

> To Start Web Server:

```shell
python -m streamlit run .\__init__.py
```

> Custom Components (Examples)

```shell
pip install streamlit-extras
pip install streamlit-elements
pip install streamlit-image-annotation
pip install graph-app-kit
pip install streamlit-player
pip install streamlit-login-auth-ui
pip install streamlit-drawable-canvas
...
```

## 04 Asimov Chatbot With Streamlit

> Streamlit Project with Chat GPT: Chat Completions Model

## 05 Asimov Audio Transcripts

> Streamlit Project with OpenAI Audios: With Whisper Model

## 06 Hugging Face - The AI Comunity

> Transformers Lib

> Fill Mask Models

> Tokenizers: Tokens, Inputs and Outputs

> Inference API: Working with very largest models

> Restricted Models: Authentication and Terms of Use

> Translation Models

> Abstract Models

> Text Classification Models

> Datasets and Spaces

## 07 AI APPs With LangChain Framework

> Models
    - LLMs
    - Chat Models
        - Prompt Few-Shot
    - Debug
    - Response Caching

> Prompt Templates

> Output Parsers

> Chain
    - Memory: History for model conversations
    - Break problems down into smaller problems
    - Multiple chains to solve a problem of one application
    - Each chain has a responsibility
    - Simplify complex prompts
    - Parallel and sequential chains

> Router Chains
    - Router that directs the query to the ideal chain

> RAG: Retrieval Argumented Generation
    - Document Loading: In this stage, data is loaded from different sources, such as PDFs, CSVs, or databases. LangChain offers various tools to facilitate this process.
    - Document Splitting: The loaded data is divided into smaller chunks. This splitting should be done intelligently to preserve context and ensure that relevant information is maintained.
    - Embedding: The text chunks are converted into numerical vectors. This transformation is crucial for enabling semantic comparisons between texts, making it easier to retrieve relevant information.
    - Storage in VectorStore: The generated vectors are stored in a specific database for vectors, called VectorStore. This allows for efficient information retrieval.
    - Retrieval: When a user asks a question, a vector corresponding to the query is generated and compared with the vectors stored in the VectorStore. The closest texts are retrieved and used to generate a personalized response.
