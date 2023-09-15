WEAVIATE_INVALID_URL = (
    "Invalid weaviate_url='{weaviate_url}' provided. Please make sure it starts with a "
    "schema like http:// or https://"
)

WEAVIATE_ERROR_EXTRA = (
    "\nPlease make sure that Weaviate is running and Copilot has data."
)

COPILOT_IS_NOT_RUNNING_ERROR = (
    "Could not connect to Copilot on url: '{copilot_url}"
    "\nPlease make sure that Copilot is running."
)

INVALID_MODEL_ERROR = (
    "Invalid llm_model_name='{llm_model_name}'.\n"
    "Allowed model names are: {allowed_model_names}"
)

INVALID_LOGS_DIR_ERROR = "Invalid logs_dir passed. Make sure it is non empty value."

LOCAL_LLM_CONNECTION_ERROR = (
    "Failed to connect to Local LLM. Please make sure that the service is running"
)
