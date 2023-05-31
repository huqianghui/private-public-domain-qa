import os
import mimetypes
import time
import logging
import openai
from flask import Flask, request, jsonify, Response
from azure.identity import DefaultAzureCredential, AzureAuthorityHosts
from azure.identity import ClientSecretCredential
from azure.search.documents import SearchClient
from approaches.retrievethenread import RetrieveThenReadApproach
from approaches.readretrieveread import ReadRetrieveReadApproach
from approaches.readdecomposeask import ReadDecomposeAsk
from approaches.chatreadretrieveread import ChatReadRetrieveReadApproach
from approaches.bingsearchandanswer import BingSearchApproach
from approaches.databaseSqlQuery import DatabaseSqlQueryApproach
from azure.storage.blob import BlobServiceClient
from azure.core.credentials import AzureKeyCredential
import azure.cognitiveservices.speech as speechsdk

# Replace these with your own values, either in environment variables or directly here
AZURE_SEARCH_SERVICE = os.environ.get("AZURE_SEARCH_SERVICE") 
AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX")
AZURE_COGNITIVE_SEARCH_KEY = os.environ.get("AZURE_COGNITIVE_SEARCH_KEY")
AZURE_COGNITIVE_SEARCH_ENDPOINT = 'https://{AZURE_SEARCH_SERVICE}.search.windows.net'.format_map(vars())

# bing search config
AZURE_BING_SEARCH_SUBSCRIPTION_KEY = os.environ.get("AZURE_BING_SEARCH_SUBSCRIPTION_KEY")
AZURE_BING_SEARCH_ENDPOINT = os.environ.get("AZURE_BING_SEARCH_ENDPOINT") or "https://api.bing.microsoft.com/v7.0/search"

# blob storage config
AZURE_BLOB_STORAGE_ACCOUNT = os.environ.get("AZURE_BLOB_STORAGE_ACCOUNT") 
AZURE_BLOB_STORAGE_CONTAINER = os.environ.get("AZURE_BLOB_STORAGE_CONTAINER")
AZURE_BLOB_STORAGE_ACCOUNT_ENDPOINT = os.environ.get("AZURE_BLOB_STORAGE_ACCOUNT_ENDPOINT")

# azure openAI config
AZURE_OPENAI_SERVICE = os.environ.get("AZURE_OPENAI_SERVICE")
AZURE_OPENAI_GPT_DEPLOYMENT = os.environ.get("AZURE_OPENAI_GPT_DEPLOYMENT")
AZURE_OPENAI_CODEX_DEPLOYMENT = os.environ.get("AZURE_OPENAI_CODEX_DEPLOYMENT") 
AZURE_OPENAI_CHATGPT_DEPLOYMENT = os.environ.get("AZURE_OPENAI_CHATGPT_DEPLOYMENT")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_BASE = os.environ.get("AZURE_OPENAI_BASE") or f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com"

# indexer config
KB_FIELDS_CONTENT = os.environ.get("KB_FIELDS_CONTENT") or "content"
KB_FIELDS_CATEGORY = os.environ.get("KB_FIELDS_CATEGORY") or "category"
KB_FIELDS_SOURCEPAGE = os.environ.get("KB_FIELDS_SOURCEPAGE") or "sourcepage"
KB_FIELDS_SOURCE_PATH = os.environ.get("KB_FIELDS_SOURCE_PATH") or "sourcefile"

# client config
AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID") 
AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID") 
AZURE_SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID") 

# speech service config 
AZURE_SPEECH_SERVICE_KEY = os.environ.get("AZURE_SPEECH_SERVICE_KEY") 
AZURE_SPEECH_SERVICE_REGION = os.environ.get("AZURE_SPEECH_SERVICE_REGION")

speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_SERVICE_KEY,region=AZURE_SPEECH_SERVICE_REGION)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)


def azurearm_credentials():
    return DefaultAzureCredential()


blob_credential = azurearm_credentials()
search_credential = AzureKeyCredential(AZURE_COGNITIVE_SEARCH_KEY)

openai.api_type = "azure"
openai.api_key = AZURE_OPENAI_API_KEY
openai.api_base = AZURE_OPENAI_BASE
openai.api_version = "2022-12-01"

# Comment these two lines out if using keys, set your API key in the OPENAI_API_KEY environment variable instead
# openai.api_type = "azure_ad"
# openai_token = azure_credential.get_token("https://cognitiveservices.azure.com/.default")
# openai.api_key = openai_token.token

# Set up clients for Cognitive Search and Storage
search_client = SearchClient(
        endpoint=AZURE_COGNITIVE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX,
        credential=search_credential)
blob_client = BlobServiceClient(
        account_url=AZURE_BLOB_STORAGE_ACCOUNT_ENDPOINT, 
        credential=blob_credential)
blob_container = blob_client.get_container_client(AZURE_BLOB_STORAGE_CONTAINER)
blob_list = blob_container.list_blobs()
    

# Various approaches to integrate GPT and external knowledge, most applications will use a single one of these patterns
# or some derivative, here we include several for exploration purposes
ask_approaches = {
    "rtr": RetrieveThenReadApproach(search_client, AZURE_OPENAI_GPT_DEPLOYMENT, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT),
    "rrr": ReadRetrieveReadApproach(search_client, AZURE_OPENAI_GPT_DEPLOYMENT, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT),
    "rda": DatabaseSqlQueryApproach(AZURE_OPENAI_GPT_DEPLOYMENT, AZURE_OPENAI_CODEX_DEPLOYMENT),
    "bing": BingSearchApproach(search_client, AZURE_OPENAI_CHATGPT_DEPLOYMENT, KB_FIELDS_SOURCEPAGE, KB_FIELDS_SOURCE_PATH, AZURE_BING_SEARCH_SUBSCRIPTION_KEY, AZURE_BING_SEARCH_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_BASE)
}

chat_approaches = {
    "rrr": ChatReadRetrieveReadApproach(search_client, AZURE_OPENAI_CHATGPT_DEPLOYMENT, AZURE_OPENAI_GPT_DEPLOYMENT, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT, KB_FIELDS_SOURCE_PATH,AZURE_BING_SEARCH_SUBSCRIPTION_KEY,AZURE_BING_SEARCH_ENDPOINT)
}

app = Flask(__name__)

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def static_file(path):
    return app.send_static_file(path)

# Serve content files from blob storage from within the app to keep the example self-contained. 
# *** NOTE *** this assumes that the content files are public, or at least that all users of the app
# can access all the files. This is also slow and memory hungry.
@app.route("/content/<path>")
def content_file(path):
    blob = blob_container.get_blob_client(blob=path).download_blob()
    mime_type = blob.properties["content_settings"]["content_type"]
    if mime_type == "application/octet-stream":
        mime_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
    return blob.readall(), 200, {"Content-Type": mime_type, "Content-Disposition": f"inline; filename={path}"}
    
@app.route("/ask", methods=["POST"])
def ask():
    ensure_openai_token()
    approach = request.json["approach"]
    try:
        impl = ask_approaches.get(approach)
        if not impl:
            return jsonify({"error": "unknown approach"}), 400
        r = impl.run(request.json["question"], request.json.get("overrides") or {})
        print(r)
        return jsonify(r)
    except Exception as e:
        logging.exception("Exception in /ask")
        return jsonify({"error": str(e)}), 500
    
@app.route("/askBing", methods=["POST"])
def askBing():
    ensure_openai_token()
    approach = request.json["approach"]
    try:
        impl = ask_approaches.get(approach)
        if not impl:
            return jsonify({"error": "unknown approach"}), 400
        r = impl.run(request.json["question"], request.json.get("overrides") or {})
        return jsonify(r)
    except Exception as e:
        logging.exception("Exception in /askBing")
        return jsonify({"error": str(e)}), 500
    
@app.route("/chat", methods=["POST"])
def chat():
    ensure_openai_token()
    approach = request.json["approach"]
    try:
        impl = chat_approaches.get(approach)
        if not impl:
            return jsonify({"error": "unknown approach"}), 400
        r = impl.run(request.json["history"], request.json.get("overrides") or {})
        return jsonify(r)
    except Exception as e:
        logging.exception("Exception in /chat")
        return jsonify({"error": str(e)}), 500
    
@app.route("/read", methods=["POST"])
def readOutLoud():
    ensure_openai_token()
    def generate():
        speech_config.speech_synthesis_voice_name='zh-CN-YunxiNeural'

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # Get text from the console and synthesize to the default speaker.
        text = request.json["answer"]
        modified_text = text.split(":")[1]
        speech_synthesis_result = speech_synthesizer.speak_text_async(modified_text).get()

        stream = speechsdk.audio.PullAudioOutputStream(callback=lambda: speech_synthesis_result.audio_data_stream.read(speech_synthesis_result.audio_data_stream.get_length()))
        
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
        return stream
    stream = generate()
    return Response(stream.read(), mimetype="audio/mp3")
                
def ensure_openai_token():
    # global openai_token
    # if openai_token.expires_on < int(time.time()) - 60:
    #     openai_token = azure_credential.get_token("https://cognitiveservices.azure.com/.default")
    #     openai.api_key = openai_token.token
    openai.api_key = AZURE_OPENAI_API_KEY
    
if __name__ == "__main__":
    app.run()
