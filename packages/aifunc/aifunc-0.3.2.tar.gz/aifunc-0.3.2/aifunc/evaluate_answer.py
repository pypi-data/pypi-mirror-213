
from .utility import create_ai_function_from_yaml


_evaluate_answer = create_ai_function_from_yaml("evaluate_answer.yaml")


def evaluate_answer(question, reference_answer, answer):
  input = question + "\n" + reference_answer + "\n" + answer
  return _evaluate_answer(input)
