const SUCCESS = 'success';
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
const switch_btn_inactive = document.getElementById('switch-btn-inactive')
const switch_btn_active = document.getElementById('switch-btn-active')

mac_regex = /^([0-9A-Fa-f]{2}([-:])?){5}[0-9A-Fa-f]{2}$/;
email_regex = /^[a-zA-Z0-9._%+-]+@uniq\.edu$/;
pc_mac.addEventListener('change', (e) => {
    mac_regex.test(e.target.value) ? pc_mac.className += ' is-valid': pc_mac.className += ' is-invalid'
})

student_email.addEventListener('change', (e) => {
    email_regex.test(e.target.value) ? student_email.className += ' is-valid': student_email.className += ' is-invalid'
})

const refreshPage = () => {
    window.location.reload()
}

const addComputer = (pc_name_, pc_mac_, pc_status_) => {
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
                alert("Data not sent");
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if(data.status === SUCCESS) {
                alert('Data sent successfully')
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


const addStudent = (name_, code_, email_, status_, computer_) => {
    const dataToSend = JSON.stringify({
        name: name_,
        code: code_,
        email: email_,
        status: status_,
        computer: computer_
    });

    const formData = new FormData()
    formData.append('student', dataToSend);
    fetch('add-student', {
        method: 'POST',
        body: formData,
    })
        .then((response) => {
            if(!response.ok) {
                alert("Data not sent");
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if(data.status === SUCCESS) {
                alert('Data sent successfully')
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
    isEmailOk ? '' : student_email += ' is-invalid'

    let isAllOk = name && code && isEmailOk && computer !== 'Choose' || false;

    isAllOk ? addStudent(name, code, email, status, computer) : '';
});

switch_btn_inactive ? switch_btn_inactive.addEventListener('click', (e) => {
    const code = e.target.value;
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
                alert("Data not sent");
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if(data.status === SUCCESS) {
                alert('Data sent successfully')
                refreshPage()
            }
        })
        .catch((error) => console.error('Fetching Error :', error))
}) : '';

switch_btn_active ? switch_btn_active.addEventListener('click', (e) => {
    const code = e.target.value;
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
            if(!response.ok) {
                alert("Data not sent");
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if(data.status === SUCCESS) {
                alert('Data sent successfully')
                refreshPage();
            }
        })
        .catch((error) => console.error('Fetching Error :', error))
}) : '';
