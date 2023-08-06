__version__ = '0.1.0'

import openai

def create_ai_function(function_name, instruction, example_prompt, example_answer):
    def ai_function(real_prompt):
        messages = [
            {"role": "user", "content": instruction + example_prompt},
            {"role": "assistant", "content": example_answer},
            {"role": "user", "content": real_prompt}
        ]
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        full_response = completion.choices[0].message.content
        return full_response
    
    ai_function.__name__ = function_name  # Set the function name
    return ai_function