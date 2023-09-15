from opencopilot import OpenCopilot


def create():
    copilot = OpenCopilot(prompt="{question}-{history}-{context}")


def import_app():
    from opencopilot import app


if __name__ == '__main__':
    create()
    import_app()
