
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    
    if not current_question_id:
        return False, 

    if not answer:
        return False, 


    if "answers" not in session:
        session["answers"] = {}

    
    session["answers"][current_question_id] = answer
    session.modified = True  

    return True, "Answer recorded successfully."

PYTHON_QUESTION_LIST = [
    {"id": 1, "question": "What is Python?", "answer": "A programming language"},
    {"id": 2, "question": "What is a list in Python?", "answer": "A collection of items"},
    {"id": 3, "question": "What is a dictionary in Python?", "answer": "A key-value pair collection"},
]


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    for index, question in enumerate(PYTHON_QUESTION_LIST):
        if question["id"] == current_question_id:
            # Return the next question if it exists
            if index + 1 < len(PYTHON_QUESTION_LIST):
                next_question = PYTHON_QUESTION_LIST[index + 1]
                return next_question["question"], next_question["id"]
            break
    # No more questions or invalid ID
    return "No more questions", -1


    


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    if "answers" not in session:
        return "No answers recorded. Please attempt the questions first."

    answers = session["answers"]
    correct_answers = 0

    # Compare user's answers with the correct ones in PYTHON_QUESTION_LIST
    for question in PYTHON_QUESTION_LIST:
        question_id = question["id"]
        correct_answer = question["answer"]
        user_answer = answers.get(question_id, "").strip().lower()

        if user_answer == correct_answer.lower():
            correct_answers += 1

    total_questions = len(PYTHON_QUESTION_LIST)
    score = f"{correct_answers}/{total_questions}"

    return f"You have completed the quiz! Your score is {score}."

