import pytest
from pipeline.pipeline import *
@pytest.mark.parametrize("user_message", ["Hi",
                                           "Where are you?",

                                           ])
def test_pipeline(user_message):

    assert user_message != None