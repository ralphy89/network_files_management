const SUCCESS = 'success';
const ERROR = 'error'
const save_computer_btn = document.getElementById('save-computer-btn');
const pc_name = document.getElementById('pc-name');
const pc_mac = document.getElementById('pc-mac');
const pc_status = document.getElementById('pc-status');

const save_student_btn = document.getElementById('save-student-btn');
const student_name = document.getElementById('student-name');
const student_code = document.getElementById('student-code');
const student_email = document.getElementById('student-email');
const student_status = document.getElementById('student-status');
const student_computer = document.getElementById('assigned-computer');
const student_option = document.getElementById('student-option');
const history_container = document.getElementById('history-container');
const modal_title_h3 = document.getElementById('modal-title-h3');
const myStudentModal = document.getElementById('student-form-modal')
const studentModal = new bootstrap.Modal(myStudentModal)

const switch_btn_inactive = [... document.getElementsByClassName('switch-btn-inactive')];
const switch_btn_active = [... document.getElementsByClassName('switch-btn-active')];
const history_btn = [... document.getElementsByClassName('history-btn')];
const btn_edit = [... document.getElementsByClassName('btn-edit')];

mac_regex = /^([0-9A-Fa-f]{2}([-:])?){5}[0-9A-Fa-f]{2}$/;
email_regex = /^[a-zA-Z0-9._%+-]+@uniq\.edu$/;
pc_mac.addEventListener('change', (e) => {
    mac_regex.test(e.target.value) ? pc_mac.className += ' is-valid': pc_mac.className += ' is-invalid'
})

student_email.addEventListener('change', (e) => {
    email_regex.test(e.target.value) ? student_email.className += ' is-valid': student_email.className += ' is-invalid'
})

const refreshPage = () => {
    window.location.reload(true)
}

const refresh_after_close_btn = (id) => {
    const btn_close = document.getElementById(id);
    btn_close.addEventListener('click', () => {
        refreshPage();
    })
}

const  display_alert = (data_name, data, type, response=null) => {
    Swal.fire({
        position: "top-end",
        icon: type,
        draggable: true,
        title: type == SUCCESS ? `${data_name} "${data}" Saved Successfully`: `Error saving ${data_name} "${data}"! Please try again later or contact the administrator`,
        html: type == SUCCESS ? `` : `<p><strong>API Response : </strong> <i>${response.status}</i></p>`,
        customClass: {
            popup: 'swal-popup',
            title: 'swal-title',
            htmlContainer: 'swal-html',
        },
        showConfirmButton: true,
        confirmButtonText: 'OK',
        timer: 24000,
        timerProgressBar: true,
        background: '#363132', // Futuristic dark background
        color: '#ffffff', // Text color for contrast
    });

}

const addComputer = (pc_name_, pc_mac_, pc_status_) => {
    refresh_after_close_btn("btn-close-computer-form");
    const dataToSend = JSON.stringify({
        name: pc_name_,
        mac: pc_mac_,
        status: pc_status_,
    });

    const formData = new FormData()
    formData.append('computer', dataToSend);
    fetch('add-computer', {
        method: 'POST',
        body: formData,
    })
        .then((response) => {
            if(!response.ok) {
                display_alert('Computer', pc_name_, ERROR, response);
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if(data.status === SUCCESS) {
                display_alert('Computer', pc_name_, SUCCESS);
                pc_name.value = '';
                pc_mac.value='';
                pc_status.value = 'Available';
            }
        })
        .catch((error) => console.error('Fetching Error :', error))
};
save_computer_btn.addEventListener('click', (e) => {
    const name = pc_name.value;
    const mac = pc_mac.value;
    const status = pc_status.value;
    let isAllOk = name && status || false;
    isAllOk ? '' : pc_name.className += ' is-invalid';
    const isMacOk = mac_regex.test(mac)
    isMacOk ? '' : pc_mac.className += ' is-invalid';

    isMacOk && isAllOk ? addComputer(name, mac, status) : '';
});

const cleanModal = () => {
    student_name.value = '';
    student_name.classList.remove('is-invalid');
    student_name.classList.remove('is-valid');

    student_code.value = '';
    student_code.classList.remove('is-invalid');
    student_code.classList.remove('is-valid');

    student_status.value = 'Active';
    student_email.value = '';
    student_email.classList.remove('is-valid');
    student_email.classList.remove('is-invalid');

    student_computer.value = 'Choose';

    student_computer.classList.remove('is-invalid');
    student_computer.classList.remove('is-valid');

    student_option.value = ''
    student_option.classList.remove('is-invalid');

    save_student_btn.value = '';
    modal_title_h3.innerHTML = 'Register Student';
    save_student_btn.name = ''
    // student_status.disabled = 'disabled'

    studentModal.hide();
}
const addStudent = (name_, code_, email_, status_, computer_, option_, update=false) => {
    refresh_after_close_btn("btn-close-student-form");
    const dataToSend = JSON.stringify({
        name: name_,
        code: code_,
        email: email_,
        status: status_,
        computer: computer_,
        option: option_,
        prev_code: save_student_btn.name
    });
    const endPoints = ['add-student', 'update-student'];
    let endPoint = endPoints[0];
    if (update) {
        endPoint = endPoints[1]
    }
    const formData = new FormData()
    formData.append('student', dataToSend);
    fetch(endPoint, {
        method: 'POST',
        body: formData,
    })
        .then((response) => {
            if(!response.ok) {
                display_alert('Student', `${code_}-${name_}`, ERROR, response)
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if(data.status === SUCCESS) {
                display_alert('Student', `${code_}-${name_}`, SUCCESS)
                cleanModal();
            }
        })
        .catch((error) => console.error('Fetching Error :', error))
}
save_student_btn.addEventListener('click', (e) => {
    const name = student_name.value;
    name ? '' : student_name.className += ' is-invalid';
    const code = student_code.value;
    code ? '' : student_code.className += ' is-invalid';
    const status = student_status.value;
    const email = student_email.value;
    const computer = student_computer.value;
    const option = student_option.value;
    option ? '' : student_option.className += ' is-invalid';

    computer !== 'Choose' ? '' : student_computer.className += ' is-invalid';
    const isEmailOk = email_regex.test(email)
    isEmailOk ? '' : student_email.className += ' is-invalid'

    let isAllOk = name && code && isEmailOk && option && computer !== 'Choose' || false;
    if(save_student_btn.value === 'update-btn') {
        if(isAllOk) {
            addStudent(name, code, email, status, computer, option, true)

        }
    } else {
        isAllOk ? addStudent(name, code, email, status, computer, option, false) : '';
    }
});

const  confirm_alert = (msg, disabled_comment, callBack) => {
    const inputAttributes =
        {
            placeholder: 'eg. Pour la seance de Python ou TP personnel',
            autocapitalize: "off",
            required: "required",
            id: "comment",
        }
        if (disabled_comment === 'disabled') {
            inputAttributes.disabled = disabled_comment
        }
    Swal.fire({
        position: "top",
        icon: 'warning',
        draggable: true,
        title: `${msg}`,
        html: `<strong><label>Comment/Context</label></strong>`,
        input: "textarea",
        inputAttributes,
        customClass: {
            popup: 'swal-popup',
            title: 'swal-title',
            htmlContainer: 'swal-html',
        },
        showCancelButton: true,
        showConfirmButton: true,
        confirmButtonText: 'Confirm',
        background: '#363132', // Futuristic dark background
        color: '#ffffff', // Text color for contrast
        focusConfirm: true,
        focusCancel: false,
        preConfirm: (value) => {
            comment = value;
        }
    }

    ).then(result => {

        if(result.isConfirmed) {
            callBack(comment);
        }
    });

}


switch_btn_inactive ? switch_btn_inactive.forEach(btn => {
    btn.addEventListener('click', (e) => {
        if(e.target.value){
            const code = e.target.value;
            confirm_alert(`Student ${code} will be set to ACTIVE`, false,(comment) => {
                const dataToSend = JSON.stringify({
                    code: code,
                    status: 'Inactive',
                    comment: comment
                });

                const formData = new FormData()
                formData.append('update', dataToSend);
                fetch('update-student-status', {
                    method: 'POST',
                    body: formData,
                })
                    .then((response) => {
                        if(!response.ok) {
                            Swal.fire({
                                title: "Inactive!",
                                text: `Student ${code} is still INACTIVE, try later or contact the administrator\nMessage : ${response.status}`,
                                icon: ERROR
                            });
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then((data) => {
                        if(data.status === SUCCESS) {

                            Swal.fire({
                                title: "Active!",
                                text: `Student ${code} is Active`,
                                icon: SUCCESS,
                                showConfirmButton: true,
                                confirmButtonText: "Close Message"
                            }).then(result => {
                                refreshPage()
                            });

                        }
                    })
                    .catch((error) => console.error('Fetching Error :', error))
            });

        }
        else {
            btn.click();
        }
    })
}
): '';

switch_btn_active ? switch_btn_active.forEach(btn => {
    btn.addEventListener('click', (e) => {
    if (e.target.value) {
        const code = e.target.value
        confirm_alert(`Student ${code} will be set to INACTIVE (Confirm if student free his/her assigned computer)`,
            "disabled", () => {

                const dataToSend = JSON.stringify({
                    code: code,
                    status: 'Active',
                });
                console.log(dataToSend)
                const formData = new FormData()
                formData.append('update', dataToSend);
                fetch('update-student-status', {
                    method: 'POST',
                    body: formData,
                })
                    .then((response) => {
                        if (!response.ok) {
                            Swal.fire({
                                title: "Active!",
                                text: `Student ${code} is still ACTIVE, try later or contact the administrator\nMessage : ${response.status}`,
                                icon: ERROR
                            });
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then((data) => {
                        if (data.status === SUCCESS) {
                            Swal.fire({
                                title: "Inactive!",
                                text: `Student ${code} is Inactive`,
                                icon: SUCCESS,
                                showConfirmButton: true,
                                confirmButtonText: "Close Message"
                            }).then(result => {
                                refreshPage()
                            });
                        }
                    })
                    .catch((error) => console.error('Fetching Error :', error))
        });

    }   else {
        btn.click();
    }
    })
}
): '';

btn_edit ? btn_edit.forEach(btn => {


    btn.addEventListener('click', (e) => {
        modal_title_h3.innerHTML = 'Update Student';

        if (e.target.value){
            const code = e.target.value;
            const dataToSend = JSON.stringify({
                code: code,
            });
            const formData = new FormData()
            formData.append('student', dataToSend);
            fetch('get-student', {
                method: 'POST',
                body: formData,
            })
                .then((response) => {
                    if (!response.ok) {
                        Swal.fire({
                            title: "Active!",
                            text: `Error fetching data<br>Message : ${response.status}`,
                            icon: ERROR
                        });
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.status === SUCCESS) {
                        const student = JSON.parse(data.student);
                        student_name.value = student.name;
                        student_code.value = student.code;
                        student_status.value = student.status ;
                        student_status.disabled = "disabled"
                        student_email.value = student.email;
                        student_computer.value = student.computer_id;
                        student_option.value = student.option;
                        save_student_btn.value = 'update-btn';
                        save_student_btn.name = code
                        studentModal.show()
                    }
                })
                .catch((error) => console.error('Fetching Error :', error))
        } else {
            btn.click();
        }
    })
}) : ''

const formatHistoryDate = (start_date, end_date) => {
    const s_date = new Date(start_date);
    const e_date = new Date(end_date);

    const formatTime = (date) => {
        const hours = date.getHours();
        const minutes = date.getMinutes().toString().padStart(2, '0');
        const period = hours >= 12 ? 'PM' : 'AM';
        const formattedHours = hours % 12 || 12; // Convert 0 to 12 for 12-hour format
        return `${formattedHours}:${minutes} ${period}`;
    };

    const formatDate = (date) => {
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September"
            , "October", "November", "December"];
        const month = monthNames[date.getMonth()];
        const day = date.getDate();
        const year = date.getFullYear();
        return `${month} ${day}, ${year}`;
    };

    if (
        s_date.toDateString() === e_date.toDateString() // Check if both dates are on the same day
    ) {
        return `${formatDate(s_date)}, ${formatTime(s_date)} - ${formatTime(e_date)}`;
    }

    return '-';
};

const display_history = (histories) => {
    history_container.innerHTML = ``;

    histories.length !== 0 ? histories.forEach((h) => {
        history_container.innerHTML +=
            `
            <div id="history-${h.history_id}" class="history-item">
                <i class="fas fa-user"></i>
                <div class="info">
                    <p>${h.student_id} used the computer ${h.computer_id}.</p>
                    <p class="description">${h.description}.</p>
                </div>
                <div class="timestamp">${formatHistoryDate(h.start_date, h.end_date)}</div>
             </div>
        `
    }) : history_container.innerHTML = `
            <p class="text-warning">
                <i class="fas fa-warning"></i></i> No history for this computer
            </p>
    `;

}

history_btn ? history_btn.forEach((btn) => {
    btn.addEventListener('click', (e) => {
        if (e.target.ariaValueText) {
            const pc_name = e.target.ariaValueText;
            const dataToSend = JSON.stringify({
                name: pc_name,
            });
            const formData = new FormData()
            formData.append('name', dataToSend);
            fetch('get-histories', {
                method: 'POST',
                body: formData,
            })
                .then((response) => {
                    if (!response.ok) {
                        Swal.fire({
                            title: "History",
                            text: `Error fetching histories, please try later or contact the administrator\nMessage : ${response.status}`,
                            icon: ERROR
                        });
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.status === SUCCESS) {

                        const histories = JSON.parse(JSON.parse(data.histories))
                        display_history(histories);
                    }
                })
                .catch((error) => console.error('Fetching Error :', error))
        } else {
            throw new Error(`e.target.ariaValueText is ${e.target.ariaValueText}`)
        }
    });
}): '';

document.getElementById("btn-show-registered-student").addEventListener("click", function () {
    const studentListSection = document.getElementById("student-list");
    studentListSection.scrollIntoView({ behavior: "smooth", block: "start" });
});

document.getElementById("btn-show-registered-student").addEventListener("click", function () {
    const studentListSection = document.getElementById("student-list");
    studentListSection.scrollIntoView({ behavior: "smooth", block: "start" });
});

document.getElementById('btn-register-student').addEventListener('click', () => {
    save_student_btn.value = '';
    modal_title_h3.innerHTML = 'Register Student';
    student_status.disabled = false
    save_student_btn.name = ''
})
