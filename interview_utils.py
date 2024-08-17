# interview_utils.py

import random
from prompt_instructions import get_interview_initial_message_sarah, get_interview_initial_message_aaron, get_interview_prompt_sarah, get_interview_prompt_aaron
from ai_config import n_of_questions

def random_interviewer(language):
    if random.choice([True, False]):
        initial_message, interviewer_name = get_interview_initial_message_sarah()
        get_interview_prompt = get_interview_prompt_sarah(language, n_of_questions)
        voice = 'alloy'
    else:
        initial_message, interviewer_name = get_interview_initial_message_aaron()
        get_interview_prompt = get_interview_prompt_aaron(language, n_of_questions)
        voice = 'onyx'
    return initial_message, interviewer_name, get_interview_prompt, voice

def get_prompt():
    # This function should return the actual prompt
    # You might need to adjust this based on how you're storing the prompt
    return get_interview_prompt_sarah(language, n_of_questions)  # or whatever is appropriate