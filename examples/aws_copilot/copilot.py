from opencopilot import OpenCopilot

copilot = OpenCopilot(
    copilot_name="AWS CLI Copilot",
    llm_model_name="gpt-3.5-turbo-16k", # You can also use gpt-4 for improved accuracy
    prompt_file="prompt_template.txt"
)

# Download and embed the knowledge base from given URL
copilot.add_data_urls([
    "https://awsdocs.s3.amazonaws.com/cli/latest/aws-cli.pdf",
])

# Run the copilot
copilot()
