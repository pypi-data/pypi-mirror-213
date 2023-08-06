from .utility import create_ai_function_from_yaml

_follow_up = create_ai_function_from_yaml("follow_up.yaml")


def follow_up(question, reference_answer):
  input = question + "\n" + reference_answer
  return _follow_up(input)
