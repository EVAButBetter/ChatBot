class TemplateGenerator:
    def __init__(self, model):
        self.model = model

    def generate_from_template(self, input, **kwargs):
        raise NotImplementedError
