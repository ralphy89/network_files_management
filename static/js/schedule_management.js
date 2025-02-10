const save_sc_btn = document.getElementById('save-sc-btn');
const sc_assigned_student = document.getElementById('sc-assigned-student');
const sc_assigned_computer = document.getElementById('sc-assigned-computer');
const end_hour = document.getElementById('end-hour');
const start_hour = document.getElementById('start-hour');
const sc_day = document.getElementById('sc-day');
const table_body_schedule = document.getElementById('table-body-schedule');
const modal_title_h3_sc = document.getElementById('modal-title-h3-sc');
const SUCCESS_sc = 'success';
const myScheduleModal = document.getElementById('schedule-form-modal');
const scheduleModal = new bootstrap.Modal(myScheduleModal);
const cleanScModal = () => {
    sc_day.classList.remove('is-invalid');
    end_hour.classList.remove('is-invalid');
    start_hour.classList.remove('is-invalid');
    sc_assigned_student.classList.remove('is-invalid');
    sc_assigned_computer.classList.remove('is-invalid');
    sc_day.value = '---';
    end_hour.value = '---';
    start_hour.value = '---';
}
const refreshPage_sc = () => {
    window.location.reload(true)
}
const refresh_after_close_btn_sc = (id) => {
    const btn_close = document.getElementById(id);
    btn_close.addEventListener('click', () => {
        refreshPage_sc();
    })
}

const  display_alert_sc = (type, response=null, update, check) => {

    if (check){
        Swal.fire({
            title: "Check Availability",
            text: `${response.message}`,
            icon: response.status,
            showConfirmButton: true,
            confirmButtonText: "Close Message",
        })
    } else {
        Swal.fire({
            position: "top-end",
            icon: type,
            draggable: true,
            title: type === SUCCESS_sc ? `Schedule Saved Successfully` : `Error saving Schedule! Please try again later or contact the administrator`,
            html: type === SUCCESS_sc ? `` : `<p><strong>API Response : </strong> <i>${response.status}</i></p>`,
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
        }).then(result => {
            if (result.isConfirmed) {
                cleanScModal();
                if (update) {
                    refreshPage_sc();
                }
            }
        });
    }
}

const addSchedule = (s_hour_, e_hour_, computer_, student_, day_, update, check) => {
    refresh_after_close_btn_sc("btn-close-schedule-form");
    console.log('Je suis la')
    const dataToSend = JSON.stringify({
        s_hour: s_hour_,
        e_hour: e_hour_,
        computer: computer_,
        student: student_,
        day: day_,
        prev_code: save_sc_btn.name,
    });
    const endPoints = ['add-schedule', 'update-schedule', 'check-schedule'];
    let endPoint = endPoints[0];
    if (update) {
        endPoint = endPoints[1]
    }
    if (check){
        console.log('je suis la')
        endPoint = endPoints[2]
    }
    const formData = new FormData()
    formData.append('schedule', dataToSend);
    fetch(endPoint, {
        method: 'POST',
        body: formData,
    })
        .then((response) => {
            if(!response.ok) {
                display_alert_sc(ERROR, response, update, check)
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if(data.status === SUCCESS_sc) {
                display_alert_sc(SUCCESS_sc, data, update, check)
            } else {
                Swal.fire({
                    title: "Warning!",
                    text: `${data.message}`,
                    icon: 'warning',
                    showConfirmButton: true,
                    confirmButtonText: "Close Message",
                })
            }
        })
        .catch((error) => console.error('Fetching Error :', error))
};

save_sc_btn.addEventListener('click', e => {
    const day = sc_day.value;
    day ?
        day !== '---' ? '': sc_day.classList.add('is-invalid')
        : ''
    const s_hour = start_hour.value;
    s_hour ?
        s_hour !== '---' ? '': start_hour.classList.add('is-invalid')
        : ''
    const e_hour = end_hour.value;
    e_hour ?
        e_hour !== '---' ? '': end_hour.classList.add('is-invalid')
        : ''
    const student = sc_assigned_student.value;
    student ?
        student !== '---' || save_sc_btn.value === 'check-btn' ? '': sc_assigned_student.classList.add('is-invalid')
        : ''
    const computer = sc_assigned_computer.value;
    computer ?
        computer !== '---' ? '': sc_assigned_computer.classList.add('is-invalid')
        : ''

    const isAllOk = computer !== '---'  &&
        e_hour !== '---' && s_hour !== '---' && day !== '---';

    if (save_sc_btn.value === 'save-sc-btn') {
        if (isAllOk) {
            Number(e_hour) <= Number(s_hour) || Number(e_hour) - Number(s_hour) > 4 ?
                end_hour.classList.add('is-invalid') :
                addSchedule(Number(s_hour), Number(e_hour), computer, student, day, false, false);
        }
    } else if (save_sc_btn.value === 'update-sc-btn' ) {
        if (isAllOk) {
            Number(e_hour) <= Number(s_hour) || Number(e_hour) - Number(s_hour) > 4 ?
                end_hour.classList.add('is-invalid') :
                addSchedule(Number(s_hour), Number(e_hour), computer, student, day, true, false);

        }
    } else if (save_sc_btn.value === 'check-btn') {
        if (isAllOk) {
            Number(e_hour) <= Number(s_hour) || Number(e_hour) - Number(s_hour) > 4 ?
                end_hour.classList.add('is-invalid') :
                addSchedule(Number(s_hour), Number(e_hour), computer, student, day, false, true);
        }
    }
})
const extractHours = (start_hour_, end_hour_) => {
    const s = start_hour_.split(':')[0]
    const e = end_hour_.split(':')[0]
    return [s, e]
}

table_body_schedule.addEventListener('click', (e) => {
    const target = e.target;
    const button = target.tagName === 'BUTTON' ? target : target.closest('button');

    if (!button) return; // If no button is found, exit early

    if (button.classList.contains('btn-edit')) {
        const code = button.value || '';
        if (code) {
            modal_title_h3_sc.innerHTML = 'Update Schedule';

            const dataToSend = JSON.stringify({
                schedule_id: code,
            });

            const formData = new FormData();
            formData.append('schedule', dataToSend);
            fetch('get-schedule', {
                method: 'POST',
                body: formData,
            })
                .then((response) => {
                    if (!response.ok) {
                        Swal.fire({
                            title: "Active!",
                            text: `Error fetching data<br>Message: ${response.status}`,
                            icon: "error",
                        });
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then((data) => {

                    if (data.status === SUCCESS) {
                        const schedule = JSON.parse(data.schedule);
                        sc_day.value = schedule.day;
                        const hours = extractHours(schedule.start_hour, schedule.end_hour)
                        end_hour.value = hours[1];
                        start_hour.value = hours[0];
                        sc_assigned_student.value = schedule.student_id;
                        sc_assigned_computer.value = schedule.computer_id;

                        save_sc_btn.value = 'update-sc-btn';
                        save_sc_btn.name = code;
                        scheduleModal.show()
                    }
                })
                .catch((error) => console.error('Fetching Error:', error));
        } else {
            button.click(); // Re-click the button if value is empty
        }
    }
});

document.getElementById('btn-register-schedule').addEventListener('click', () => {
    save_sc_btn.value = '';
    modal_title_h3_sc.innerHTML = 'Add Schedule';
    save_sc_btn.name = '';
    save_sc_btn.innerHTML = 'Save Schedule';
    sc_assigned_student.disabled = null

    cleanScModal()
    sc_assigned_student.value = '---';
    sc_assigned_computer.value = '---';
})

document.getElementById('btn-check-schedule').addEventListener('click', () => {
    save_sc_btn.value = 'check-btn';
    save_sc_btn.innerHTML = 'Check';
    modal_title_h3_sc.innerHTML = 'Check Schedule Availability';
    save_sc_btn.name = '';
    cleanScModal()
    sc_assigned_student.value = '---';
    sc_assigned_computer.value = '---';
    sc_assigned_student.disabled = 'disabled'
})
