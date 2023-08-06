from llama import Type, Context, LLMEngine
from inspect import getmembers, getsource, isfunction, ismodule, isclass
import unittest
import llama


# Input
class Question(Type):
    question: str = Context("question about the function")


# Output
class Answer(Type):
    inputs: list = Context("list of inputs to the function")
    outputs: list = Context("list of outputs from the function")
    description: str = Context("function description in 2 to 5 lines")


class Function(Type):
    name: str = Context("name of the function")
    code: str = Context("text for the python code in the function")


seen = set()


def get_functions(module):
    functions = set()
    if module not in seen:
        seen.add(module)
        for name, member in getmembers(module):
            if isfunction(member):
                functions.add((name, getsource(member).strip()))
            elif ismodule(member) and member.__name__.startswith("llama"):
                functions.update(get_functions(member))
            elif (
                isclass(member)
                and hasattr(member, "__module__")
                and f"{member.__module__}.{member.__qualname__}".startswith("llama")
            ):
                functions.update(get_functions(member))
    return functions


def make_function(function):
    return Function(name=function[0], code=function[1])


class TestLLMTrain(unittest.TestCase):
    def test_train(self):
        functions = [make_function(function) for function in get_functions(llama)]
        questions = [
            [
                Question(question="How do I use this function?"),
                Answer(
                    inputs=["param1", "param2", "param3"],
                    outputs=["output1", "output2", "output3"],
                    description="This function does something useful",
                ),
            ]
        ]
        llm = LLMEngine(id="QA", model_name="hf-internal-testing/tiny-random-gpt2")
        functions = functions + questions
        job = llm.submit_training_job(functions)
        print(job)
        # status = llm.check_job_status(job["job_id"])
        # assert status["status"] not in ("NOT_SCHEDULED", "ERRORED")

        # while status["status"] != "DONE":
        #     print(f"job not done. waiting... {status}")
        #     time.sleep(10)
        #     status = llm.check_job_status(job["job_id"])
        #     assert status["status"] not in ("NOT_SCHEDULED", "ERRORED")

        # result = llm.get_job_results(job["job_id"], output_type=Tweet)
        # print(result)
