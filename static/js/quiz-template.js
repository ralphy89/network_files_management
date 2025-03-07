
const questionTypeSelect = document.getElementById('question-type');
const multipleChoiceAnswers = document.querySelector('.multiple-choice-answers');
const shortAnswerInput = document.querySelector('.short-answer-input');
const addAnswerBtn = document.getElementById('add-answer-btn');
const answerInputs = document.querySelector('.answer-inputs');
const reset_btn = document.getElementById('reset-question-btn');
const questions_list_div = document.getElementById('questions-list');



// Toggle between multiple choice and short answer
questionTypeSelect.addEventListener('change', function() {
    if (this.value === 'multiple_choice') {
        multipleChoiceAnswers.style.display = 'block';
        shortAnswerInput.style.display = 'none';
        addAnswerBtn.style.display = 'inline-flex';
    } else {
        multipleChoiceAnswers.style.display = 'none';
        shortAnswerInput.style.display = 'block';
        addAnswerBtn.style.display = 'none';
    }
});

// Add new answer input dynamically
addAnswerBtn.addEventListener('click', function() {
    const currentAnswerCount = answerInputs.children.length;
    if (currentAnswerCount < 6) {
        const newAnswerGroup = document.createElement('div');
        newAnswerGroup.classList.add('answer-input-group');
        newAnswerGroup.innerHTML = `
                    <input type="text" class="form-control" placeholder="Answer ${currentAnswerCount + 1}">
                    <div class="form-check">
                        <input type="checkbox" class="form-check-input" id="correct-${currentAnswerCount + 1}">
                        <label class="form-check-label" for="correct-${currentAnswerCount + 1}">Correct</label>
                    </div>
                `;
        answerInputs.appendChild(newAnswerGroup);
    }
});



function editQuestion(questionId) {
    window.location.href = `/quiz/question/${questionId}/edit/`;
}

function removeQuestion(questionId) {
    if (confirm('Are you sure you want to remove this question?')) {
        fetch(`/quiz/question/${questionId}/remove/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            }
        }).then(response => {
            if (response.ok) {
                // Remove the question from the DOM
                document.querySelector(`.question-card[data-question-id="${questionId}"]`).remove();
            } else {
                alert('Failed to remove the question');
            }
        });
    }
}

const display_question = (questions) => {
    questions_list_div.innerHTML = ``;
    Object.keys(questions).forEach((key) => {
        questions_list_div.innerHTML += `
            <div class="question-card">
                <div class="question-header">
                    <span class="question-type">
                        ${
                            Object.values(questions[key])[1] === 'MC' ? 'Multiple Choice' : 'Short Answer'
                        }
                        
                        <span style="font-size: medium; border: 1px solid green" class="text-uppercase text-center badge text-success text-hide">${Object.values(questions[key])[2]} points</span>

                    </span>
                    <div class="question-actions">
                        <button class="edit-btn" onclick="editQuestion({{ question.question_id }})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="remove-btn" onclick="removeQuestion({{ question.question_id }})">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>
                </div>
                <div class="question-content">
                    <div class="question-text">
                        ${Object.keys(questions[key])[0]}
                    </div>
    
                    <div class="answers-container">
                        ${
                            Object.keys(questions[key]).map((quest, index) => {
                                return `
                                ${
                                    (Array.isArray(questions[key][quest])) ?

                                        questions[key][quest].map(answer => {
                                            return `
                                                ${
                                                    Object.keys(answer).map(an => {
                                                        return`<div class="answer-item ${answer[an] ? 'correct-answer': 'incorrect-answer'}">${an}</div>`

                                                })
                                            }
                                            `
                                        }).join(' ')
                                        : ''
                                }
                                `
                            }).join(' ')
                        }
                     
                    </div>
                </div>
            </div>
        `
        console.log(key)
        console.log(Object.keys(questions[key])[0])
        console.log(Object.values(questions[key])[1])
        console.log(Object.values(questions[key])[2])

    })
}

const successMessage = msg => {
    const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 5000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.onmouseenter = Swal.stopTimer;
            toast.onmouseleave = Swal.resumeTimer;
        }
    });
    Toast.fire({
        icon: "success",
        title: msg
    });
}

const saveQuestion =  (quiz_id, csrf_token) => {
    const questionType = questionTypeSelect.value;
    const questionText_ = document.getElementById('question-text');
    const questionText = questionText_.value;
    const points = document.getElementById('points').value;
    const hasQuestionText = questionText.length > 0;
    const hasPoint = points.length > 0;
    if (hasQuestionText && hasPoint) {

        if (questionType === 'MC') {
            const answers = Array.from(document.querySelectorAll('.answer-input-group'))
                .map(group => ({
                    text: group.querySelector('input[type="text"]').value ,
                    isCorrect: group.querySelector('input[type="checkbox"]').checked
                }));
            const expected = 2;
            let has = 0;
            let hasCorrect = 0;
            answers.forEach((a) => {
                a.text.length > 0 ? has++ : '';
                a.isCorrect === true ? hasCorrect++ : '';
            })
            console.log(has, hasCorrect)
            if (has < expected || hasCorrect <= 0){

                Swal.fire({
                    title: "No Answer/correct answer provided",
                    text: `Expected at least 2 Answers and 1 correct answer`,
                    icon: "error",
                });
                return;
            }
            const dataToSend = {
                type: questionType,
                text: questionText,
                points: points,
                answers: answers
            }
            console.log(dataToSend);

            fetch(`/quizHub/addQuestion/to/${quiz_id}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrf_token,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dataToSend)

            }).then(response => {
                if (!response.ok) {
                    Swal.fire({
                        title: "Failed",
                        text: `Failed to add question\nMessage: ${response.status}`,
                        icon: "error",
                    });
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            }).then((data) => {
                if (data.status === 'success'){
                    const questions = (JSON.parse(data.questions));
                    display_question(questions)
                    reset_btn.click();
                    successMessage("Question added successfully!")
                }
            }).catch((error) => console.error('Fetching Error:', error));


        } else {
            const correctAnswer = document.getElementById('correct-answer').value;

            console.log({
                type: questionType,
                text: questionText,
                points: points,
                correctAnswer: correctAnswer
            });
        }
    }
    else {
        Swal.fire({
            title: "Question Text/Points Error",
            text: `Please enter the Question Text/Points to continue`,
            icon: "error",
        });
        questionText_.classList.add('is-invalid')
    }
};





