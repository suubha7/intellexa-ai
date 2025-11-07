import os
import json
import vertexai
from google.oauth2 import service_account
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from langchain.chat_models import init_chat_model

def initialize_vertex_ai():
    json_str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    gcloud_dict = json.loads(json_str)
    credentials = service_account.Credentials.from_service_account_info(gcloud_dict)
    project_id = gcloud_dict["project_id"]

    vertexai.init(project=project_id, location="us-central1", credentials=credentials)

# Load and parse GCP service account JSON from Hugging Face secret
def load_gcp_credentials():
    """Load GCP credentials from environment variable"""
    json_string = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not json_string:
        raise ValueError("Missing GOOGLE_APPLICATION_CREDENTIALS environment variable.")

    try:
        gcloud_dict = json.loads(json_string)
        project_id = gcloud_dict.get("project_id")
        if not project_id:
            raise ValueError("Missing 'project_id' in service account JSON.")

        credentials = service_account.Credentials.from_service_account_info(gcloud_dict)

        return project_id, credentials
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse GCP credentials JSON: {e}")

# Initialize embedding model
def get_embedding_model():
    """Initialize Vertex AI embedding model"""
    project_id, credentials = load_gcp_credentials()

    vertexai.init(project=project_id, location="us-central1", credentials=credentials)

    return VertexAIEmbeddings(
        model_name="text-embedding-005",
        credentials=credentials
    )

# Initialize Gemini chat model
def get_llm():
    """Initialize Vertex AI Gemini chat model"""
    project_id, credentials = load_gcp_credentials()
    vertexai.init(project=project_id, location="us-central1", credentials=credentials)

    return init_chat_model(
        model="gemini-2.5-flash-lite",
        model_provider="google_vertexai",
        project_id=project_id,
        credentials=credentials
    )