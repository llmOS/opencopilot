from opencopilot import OpenCopilot

copilot = OpenCopilot(
    prompt_file="prompt_template.txt",
    copilot_name="AWS CLI",
)

copilot.add_data_urls([
    "https://awsdocs.s3.amazonaws.com/cli/latest/aws-cli.pdf",
])

copilot()
