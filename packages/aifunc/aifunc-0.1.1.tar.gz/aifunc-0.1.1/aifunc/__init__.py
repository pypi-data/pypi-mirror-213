__version__ = '0.1.1'

import openai
import time

def create_ai_function(function_name, instruction: str, example_prompt: str | list[str], example_answer: str | list[str]):
    # check the type of parameters
    assert isinstance(function_name, str)
    assert isinstance(instruction, str)
    if isinstance(example_prompt, str):
        assert isinstance(example_answer, str)
        example_prompt = [example_prompt]
        example_answer = [example_answer]
    elif isinstance(example_prompt, list):
        assert isinstance(example_answer, list)
        assert len(example_prompt) == len(example_answer)
        # check the type of elements in the list
        for prompt in example_prompt:
            assert isinstance(prompt, str)
        for answer in example_answer:
            assert isinstance(answer, str)

    def ai_function(real_prompt):
        messages = []
        messages.append({
          "role": "user", "content": instruction + example_prompt[0]
        })
        messages.append({
          "role": "assistant", "content": example_answer[0]
        })
        for prompt, answer in zip(example_prompt[1:], example_answer[1:]):
            messages.append({
              "role": "user", "content": prompt
            })
            messages.append({
              "role": "assistant", "content": answer
            })
        
        messages.append({
          "role": "user", "content": real_prompt
        })

        for i in range(5):
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                full_response = completion.choices[0].message.content
                return full_response
            except Exception as e:
                if i < 4:  # if it's not the last attempt
                    print(f"Attempt {i+1} failed, retrying in 5 seconds...")
                    time.sleep(5)  # wait for 5 seconds before next attempt
                else:  # if it's the last attempt
                    print("All attempts failed.")
                    raise e  # re-raise the last exception
    
    ai_function.__name__ = function_name  # Set the function name
    return ai_function