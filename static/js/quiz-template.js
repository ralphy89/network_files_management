
const questionTypeSelect = document.getElementById('question-type');
const multipleChoiceAnswers = document.querySelector('.multiple-choice-answers');
const shortAnswerInput = document.querySelector('.short-answer-input');
const addAnswerBtn = document.getElementById('add-answer-btn');
const answerInputs = document.querySelector('.answer-inputs');
const reset_btn = document.getElementById('reset-question-btn');
const questions_list_div = document.getElementById('questions-list');


// For multiple choice questions
const answerItems = document.querySelectorAll('.answer-item-student');
let preview_answers = JSON.parse(sessionStorage.getItem('answers'));
let selected_answer = preview_answers? Array.from(preview_answers) : [];
answerItems.forEach(item => {
    // Add click event for multiple choice answers
    if (!item.querySelector('input[type="text"]')) {
        item.addEventListener('click', function(e) {
            // For single-select questions (if needed)
           //answerItems.forEach(i => i.classList.remove('selected'));

            if (e.target.dataset.questionId && e.target.dataset.answerId) {
                // set selected state
                if (this.classList.contains('selected')) {
                    this.classList.remove('selected');
                } else {
                    this.classList.toggle('selected');
                    const q = e.target.dataset.questionId;
                    const a = e.target.dataset.answerId;
                    const t = e.target.dataset.questionType;
                    selected_answer.push({
                        'question_id':q,
                        'answer':a,
                        'type':t,
                    })
                    sessionStorage.setItem('answers', JSON.stringify(selected_answer));
                    console.log(sessionStorage.getItem('answers'));
                    // Add ripple effect manually
                    // createRipple(event, this);
                }
            }
            else {
                item.click();
            }

        });
    }
});

answerItems.forEach(item => {
    const question = item.getAttribute('data-question-id').valueOf()
    const answer = item.getAttribute('data-answer-id').valueOf()
    Array.from(preview_answers).forEach(item_ => {
        if (item_.question_id === `${question}` && item_.answer === `${answer}`){
            item.classList.toggle('selected');
        }
    });
});

// Function to create ripple effect
function createRipple(event, element) {
    const circle = document.createElement('div');
    const diameter = Math.max(element.clientWidth, element.clientHeight);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - element.getBoundingClientRect().left - radius}px`;
    circle.style.top = `${event.clientY - element.getBoundingClientRect().top - radius}px`;
    circle.classList.add('ripple');

    // Remove existing ripples
    const ripple = element.querySelector('.ripple');
    if (ripple) {
        ripple.remove();
    }

    element.appendChild(circle);
}

// Add ripple style
const style = document.createElement('style');
style.textContent = `
    .ripple {
      position: absolute;
      background: rgba(255, 255, 255, 0.7);
      border-radius: 50%;
      transform: scale(0);
      animation: ripple-effect 0.6s linear;
      pointer-events: none;
    }

    @keyframes ripple-effect {
      to {
        transform: scale(4);
        opacity: 0;
      }
    }

    .answer-item-student {
      position: absolute;
      overflow: hidden;
      cursor: pointer;
    }
  `;
document.head.appendChild(style);


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
                // 'X-CSRFToken': '{{ csrf_token }}',
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

const scheduleQuiz = (quiz_id, quiz_title, csrf_token) => {
    Swal.fire({
        title: "Schedule this quiz?",
        text: "You can set a specific date and time for this quiz to be available",
        icon: "question",
        showCancelButton: true,
        cancelButtonColor: "#d33",
        confirmButtonColor: "#48c048",
        confirmButtonText: "Yes, schedule it!"
    }).then((result) => {
        if (result.isConfirmed) {
            // Get the current date and time for default values
            const now = new Date();
            const year = now.getFullYear();
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const day = String(now.getDate()).padStart(2, '0');
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const defaultDatetime = `${year}-${month}-${day}T${hours}:${minutes}`;

            Swal.fire({
                title: "Schedule Quiz",
                html: `
          <div class="form-group">
            <label for="quiz-datetime">Date and Time:</label>
            <input id="quiz-datetime" type="datetime-local" class="swal2-input" min="${defaultDatetime}" value="${defaultDatetime}">
          </div>
          <div class="form-group mt-3">
            <label for="quiz-duration">Duration (minutes):</label>
            <input id="quiz-duration" type="number" class="swal2-input" min="5" value="30">
          </div>
        `,
                showCancelButton: true,
                cancelButtonColor: "#d33",
                confirmButtonText: "Schedule",
                confirmButtonColor: "#48c048",
                showLoaderOnConfirm: true,
                preConfirm: async () => {
                    const dateTimeInput = document.getElementById('quiz-datetime').value;
                    const durationInput = document.getElementById('quiz-duration').value;

                    if (!dateTimeInput) {
                        return Swal.showValidationMessage('Please select a date and time');
                    }

                    if (!durationInput || durationInput < 5) {
                        return Swal.showValidationMessage('Duration must be at least 5 minutes');
                    }

                    try {
                        const scheduledDateTime = new Date(dateTimeInput);
                        const currentTime = new Date();

                        if (scheduledDateTime <= currentTime) {
                            return Swal.showValidationMessage('Scheduled time must be in the future');
                        }

                        const dataToSend = {
                            quiz_id: quiz_id,
                            quiz_title: quiz_title,
                            duration: parseInt(durationInput),
                            scheduled_datetime: scheduledDateTime.toISOString()
                        };

                        const response = await fetch('/publishQuiz', {
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrf_token,
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(dataToSend)
                        });

                        if (!response.ok) {
                            return Swal.showValidationMessage(`${JSON.stringify(await response.json())}`);
                        }

                        return response.json();
                    } catch (error) {
                        Swal.showValidationMessage(`Request failed: ${error}`);
                    }
                },
                allowOutsideClick: () => !Swal.isLoading(),
            }).then(confirmed => {
                if (confirmed.isConfirmed) {
                    const scheduledDate = new Date(document.getElementById('quiz-datetime').value);
                    const formattedDateTime = scheduledDate.toLocaleString();

                    Swal.fire({
                        title: "Quiz Scheduled Successfully",
                        html: `Your quiz <b>${quiz_title}</b> has been scheduled for <b>${formattedDateTime}</b>`,
                        icon: "success",
                        confirmButtonColor: "#3085d6",
                    }).then((res) => {
                        location.reload();
                    });
                }
            });
        }
    });
};
const publishQuiz = (quiz_id, quiz_title, csrf_token) => {
    const url = `/publishQuiz`;
    Swal.fire({
        title: "You're about to publish this quiz, are you sure ?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        cancelButtonColor: "#d33",
        confirmButtonColor: "#48c048",
        confirmButtonText: "Yes, publish it!"
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: "Published",
                text: "Enter duration (min).",
                input: 'number',
                inputAttributes: {
                    min: 5,
                },
                showCancelButton: true,
                cancelButtonColor: "#d33",
                confirmButtonText: "Continue",
                confirmButtonColor: "#48c048",
                showLoaderOnConfirm: true,
                preConfirm: async (duration) => {
                    try {
                        const dataToSend = {
                            duration : duration,
                            quiz_id: quiz_id,
                            quiz_title: quiz_title,
                        }
                        const response = await fetch('/publishQuiz', {
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrf_token,
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(dataToSend)
                        });
                        if (!response.ok) {
                            return Swal.showValidationMessage(`${JSON.stringify(await response.json())}`);
                        }
                        return response.json();
                    } catch (error) {
                        Swal.showValidationMessage(`Request failed: ${error}`);
                    }},
                allowOutsideClick: () => !Swal.isLoading(),
            }).then(confirmed => {
                if (confirmed.isConfirmed){
                    Swal.fire({
                        title: "Published Successfully",
                        text: "Quiz has been published!",
                        icon: "success",
                        confirmButtonColor: "#3085d6",
                    }).then((res) => {
                           location.reload();
                    });
                }
            });
        }
    });
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





