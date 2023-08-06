import os
import sys


def create_ai_function(name):
  # get the current path
  path = os.path.dirname(os.path.realpath(__file__))
  py_filename = name + ".py"
  yaml_file_name = name + ".yaml"
  full_path = os.path.join(path, py_filename)
  full_path_yaml = os.path.join(path, yaml_file_name)
  # check if the file already exists
  if os.path.exists(full_path) or os.path.exists(full_path_yaml):
    print("File already exists")
  else:
    # create the file
    with open(full_path, "w") as f:
      pass
    # create the yaml file
    with open(full_path_yaml, "w") as f:
      pass
    print("File created")
  return


if __name__ == "__main__":
  # get the first argument
  name = sys.argv[1]
  create_ai_function(name)
