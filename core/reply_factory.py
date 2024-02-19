
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

    if not answer:
        return False, "Answer cannot be empty"
    
    session['answers'] = session.get('answers', {})
    session['answers'][current_question_id] = answer

    return True, ""


def get_next_question(current_question_id):

    PYTHON_QUESTION_LIST = [
        {"id": 1, "question": "What is the output of the following code?\n\nx = 5\ny = 2\nprint(x + y)"},
        {"id": 2, "question": "Which of the following is NOT a valid Python variable name?"},
        {"id": 3, "question": "What does the 'len()' function do in Python?"},
        {"id": 4, "question": "Which of the following is used to comment a single line in Python?"},
        {"id": 5, "question": "What does the 'range()' function return?"},
        {"id": 6, "question": "What is the correct way to open a file named 'data.txt' in read mode?"},
        {"id": 7, "question": "Which of the following is used to remove an item from a list?"},
        {"id": 8, "question": "What is the result of the expression '3' + '4'?"},
        {"id": 9, "question": "In Python, which module is used to work with dates and times?"},
        {"id": 10, "question": "What is the output of the following code?\n\nx = [1, 2, 3]\ny = x\nx.append(4)\nprint(y)"}
        
    ]
 
    current_index = -1
    for i, question in enumerate(PYTHON_QUESTION_LIST):
        if question["id"] == current_question_id:
            current_index = i
            break

    if current_index == -1:
        return "dummy question", -1

    if current_index + 1 < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[current_index + 1]
        return next_question["question"], next_question["id"]
    else:
        return "dummy question", -1


def generate_final_response(session):
    
    PYTHON_QUESTION_LIST = [
        {"id": 1, "question": "What is the output of the following code?\n\nx = 5\ny = 2\nprint(x + y)", "correct_answer": "7"},
        {"id": 2, "question": "Which of the following is NOT a valid Python variable name?", "correct_answer": "1var"},
        {"id": 3, "question": "What does the 'len()' function do in Python?", "correct_answer": "Returns the number of items in a list"},
        {"id": 4, "question": "Which of the following is used to comment a single line in Python?", "correct_answer": "# Comment"},
        {"id": 5, "question": "What does the 'range()' function return?", "correct_answer": "An iterator"},
        {"id": 6, "question": "What is the correct way to open a file named 'data.txt' in read mode?", "correct_answer": "open('data.txt', 'r')"},
        {"id": 7, "question": "Which of the following is used to remove an item from a list?","correct_answer": "pop()"},
        {"id": 8, "question": "What is the result of the expression '3' + '4'?","correct_answer": "34"},
        {"id": 9, "question": "In Python, which module is used to work with dates and times?","correct_answer": "datetime"},
        {"id": 10, "question": "What is the output of the following code?\n\nx = [1, 2, 3]\ny = x\nx.append(4)\nprint(y)","correct_answer": "[1, 2, 3, 4]"}
    ]

    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = 0

    for question in PYTHON_QUESTION_LIST:
        question_id = question["id"]
        correct_answer = question["correct_answer"]
        user_answer = session.get('answers', {}).get(question_id)

        if user_answer and user_answer.lower() == correct_answer.lower():
            correct_answers += 1

    score_percentage = (correct_answers / total_questions) * 100

    dummy_result = "You answered {correct_answers}/{total_questions} questions correctly. Your score is {score_percentage}%."

    return dummy_result
