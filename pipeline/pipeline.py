from builder.tools import Tools
from builder.builder import Builder
# from pipeline.dialog_manager import DialogManager
# from pipeline.text_assembling import TextAssembler
from dialog_manager import DialogManager
from text_assembling import TextAssembler

from utils.ignore_warnings import ignore_warnings

ignore_warnings()

TOOLS = Tools()


class Pipeline:
    def __init__(self):
        self.builder = Builder(TOOLS)
        self.dm = DialogManager()
        self.text_assenbling = TextAssembler()
        self.next_step = 1

    def run(self, text):
        sent_data = self.builder.build(text)
        raw_response, self.next_step, ai_pipeline = self.dm.update(sent_data, self.next_step)
        response = self.text_assenbling.assemble(raw_response, ai_pipeline)

        return response

pipeline = Pipeline()
import time
t = time.time()
print(pipeline.run("Where I can find Professor Jorge Lobo ?"))
print(time.time()-t)
