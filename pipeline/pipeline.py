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
print("Start!!!")
print(pipeline.run("Where I can find Professor Jorge Lobo ?"))
print(pipeline.run("How does the course Mathematical Engineering in Data Science fit into the curriculum?"))
print(pipeline.run("What time does the Mar open and close each day?"))
print(pipeline.run("How many faculty members are in Natural Language Processing?"))
print(pipeline.run("Can you tell me about the faculties at Universitat Pompeu Fabra?"))
print(pipeline.run("Can you tell me the schedule for the Introduction to Psychology course?"))
print(time.time()-t)
