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
const switch_btn_inactive = [... document.getElementsByClassName('switch-btn-inactive')];
const switch_btn_active = [... document.getElementsByClassName('switch-btn-active')];

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

const  confirm_alert = (msg, callBack) => {
    Swal.fire({
        position: "top",
        icon: 'warning',
        draggable: true,
        title: `${msg}`,
        html: ``,
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
        focusCancel: false
    }).then(result => {
        if(result.isConfirmed) {
            callBack();
        }
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


const addStudent = (name_, code_, email_, status_, computer_, option_) => {
    refresh_after_close_btn("btn-close-student-form");
    const dataToSend = JSON.stringify({
        name: name_,
        code: code_,
        email: email_,
        status: status_,
        computer: computer_,
        option: option_
    });

    const formData = new FormData()
    formData.append('student', dataToSend);
    fetch('add-student', {
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
    computer !== 'Choose' ? '' : student_computer.className += ' is-invalid';
    const isEmailOk = email_regex.test(email)
    isEmailOk ? '' : student_email.className += ' is-invalid'

    let isAllOk = name && code && isEmailOk && computer !== 'Choose' || false;

    isAllOk ? addStudent(name, code, email, status, computer) : '';
});

switch_btn_inactive ? switch_btn_inactive.forEach(btn => {
    btn.addEventListener('click', (e) => {
        if(e.target.value){
            const code = e.target.value;
            confirm_alert(`Student ${code} will be set to ACTIVE`, () => {
                const dataToSend = JSON.stringify({
                    code: code,
                    status: 'Inactive',
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
                                icon: SUCCESS
                            });
                            refreshPage()
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
            () => {

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
                                icon: SUCCESS
                            });
                            refreshPage();
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

document.getElementById("btn-show-registered-student").addEventListener("click", function () {
    const studentListSection = document.getElementById("student-list");
    studentListSection.scrollIntoView({ behavior: "smooth", block: "start" });
});

document.getElementById("btn-show-registered-student").addEventListener("click", function () {
    const studentListSection = document.getElementById("student-list");
    studentListSection.scrollIntoView({ behavior: "smooth", block: "start" });
});
