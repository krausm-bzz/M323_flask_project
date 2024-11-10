from flask import Flask, render_template, request
import json
from functools import reduce

app = Flask(__name__)


# A1G: Pure function: lädt Quizfragen aus einer JSON-Datei ohne Nebeneffekte
def load_quiz_questions():
    with open('quiz_questions.json', 'r', encoding='utf-8') as file:
        return tuple(json.load(file))


# B1G: Algorithmus erklärt, lädt die Fragen und rendert sie
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/quizzes', methods=['GET'])
def quizzes():
    questions = load_quiz_questions()  # B1G: Lade die Fragen
    return render_template('quizzes.html', questions=questions)


@app.route('/submit-answers', methods=['POST'])
def submit_answers():
    user_answers = request.form.to_dict()
    questions = load_quiz_questions()
    score = 0

    def check_answer(question):
        nonlocal score
        question_id = str(question['id'])
        user_answer = user_answers.get(f'answer_{question_id}')
        if user_answer == question['correct_answer']:
            score += 1

    list(map(check_answer, questions))

    return f'Your score: {score} out of {len(questions)}'


@app.route('/quiz-statistics')
def quiz_statistics():
    questions = load_quiz_questions()

    long_questions = list(filter(lambda q: len(q['question']) > 10, questions))

    question_ids = tuple(map(lambda q: str(q['id']), questions))

    count_answers = lambda total_questions: total_questions * 5
    total_answers = count_answers(len(questions))

    sorted_questions_by_length = sorted(questions, key=lambda q: len(q['question']) + len(q['correct_answer']))

    total_characters = reduce(lambda acc, q: acc + len(q['question']), questions, 0)

    return render_template('statistics.html', question_ids=question_ids, total_answers=total_answers,
                           sorted_questions=sorted_questions_by_length, long_questions=long_questions,
                           total_characters=total_characters)


@app.route('/filtered-and-mapped-questions')
def filtered_and_mapped_questions():
    questions = load_quiz_questions()

    question_ids = list(map(lambda q: str(q['id']), filter(lambda q: len(q['question']) > 10, questions)))

    return render_template('filtered_questions.html', question_ids=question_ids)


if __name__ == '__main__':
    app.run(debug=True)
