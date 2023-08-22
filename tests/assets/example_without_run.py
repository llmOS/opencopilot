from opencopilot import OpenCopilot


def create():
    copilot = OpenCopilot(prompt_file="tests/assets/e2e_example_prompt.txt")


def import_app():
    from opencopilot import app


if __name__ == '__main__':
    create()
    import_app()
