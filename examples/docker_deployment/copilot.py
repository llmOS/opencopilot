from opencopilot import OpenCopilot

copilot = OpenCopilot(
    prompt_file="prompt_template.txt",
    host="0.0.0.0",
    api_port=3000,
    weaviate_url="http://weaviate:8080"
)
copilot.add_local_files_dir("data")
copilot()
