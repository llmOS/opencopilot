WEAVIATE_DID_NOT_START = (
    "Weaviate did not start up in 5 seconds. Either the Weaviate URL "
    "http://localhost:8080 is wrong or Weaviate did not start up in the interval "
    "given in 'startup_period'."
    "\nPlease make sure that Weaviate is running."
)

WEAVIATE_CONNECTION_ERROR = (
    "Could not connect to Weaviate vector store."
    "\nPlease make sure that Weaviate client is running."
)

WEAVIATE_QUERY_ERROR = (
    "Could not query Weaviate." "\nPlease make sure that Weaviate has data."
)

COPILOT_IS_NOT_RUNNING_ERROR = (
    "Could not connect to Copilot." "\nPlease make sure that Copilot is running."
)

INVALID_MODEL_ERROR = (
    "Invalid llm_model_name='{llm_model_name}'.\n"
    "Allowed model names are: {allowed_model_names}"
)
