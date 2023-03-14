from pipeline.builder.tools import Tools
from pipeline.builder.builder import  Builder
from pipeline.dialog_manager import DialogManager
from pipeline.text_assembling import TextAssembler

TOOLS = Tools()
class Pipeline:
    def __init__(self):
        self.builder = Builder(TOOLS)
        self.dm = DialogManager()
        self.text_assenbling = TextAssembler()
    def run(self, text):
        sent_data = self.builder.build(text)
        raw_response, ai_pipeline = self.dm.update(sent_data)
        response = self.text_assenbling.assemble(raw_response,ai_pipeline)

        return response
