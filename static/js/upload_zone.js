// import Swal from 'sweetalert2';

// or via CommonJS
// const Swal = require('sweetalert2');
export const SUCCESS = 'success';

document.addEventListener('DOMContentLoaded', () => {
    const fileDropZone = document.getElementById('file_upload_zone');
    const fileInput = document.getElementById('file_input');
    const directoryInput = document.getElementById('directory_path_input');
    const addDirectoryPath_btn = document.getElementById('add_directory_path')
    const share_all_btn = document.getElementById('share_all');
    const file_list = document.getElementById('file-list');
    let files = [];
    let directories = []
    const isDirectory = (input) =>
        /^([a-zA-Z]:\\|\\\\)(?:[^<>:"|?*\r\n]+\\)*[^<>:"|?*\r\n]*$/.test(input) || /^(\/[^<>:"|?*\r\n]+)+\/?$/.test(input);

    const shared_ip = (IPs) =>
        IPs.map(ip => `<li style="margin-bottom: 8px; color: #8fbc8f; font-weight: 600;">${ip}</li>`).join('');

    const  display_alert = data => {
        Swal.fire({
            position: "top-end",
            icon: "success",
            draggable: true,
            title: `Files/Directories shared successfully to ${data.hosts.ips.length} DEVICES : `,
            html: `
                    <ul style="list-style: none; padding: 0; margin: 0;">
                       ${shared_ip(data.hosts.ips)}
                    </ul>
                           `,
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
    const remove_directory = (e) => {
        directories = directories.filter((d) => d !== e.target.id);
        update_file_list(files, directories);
    }
    const remove_file = (e) => {
        files = files.filter((f) => e.target.id !== f.name);
        update_file_list(files, directories);
    }
    const set_remove_listeners = (files_, type) => {
        type === 'f' ?
            files_.forEach((file) => {
            document.getElementById(file.name).addEventListener('click', remove_file)
        })
            :
            files_.forEach((dir) => {
                document.getElementById(dir).addEventListener('click', remove_directory)
            })
    };
    const update_file_list = (files_, directories_) => {
        file_list.innerHTML = '';
            files_.map((file)=> file_list.innerHTML += `
                <li name="${file.name}">
                    File: ${file.name}
                    <i id='${file.name}' class="fa fa-remove" style="font-size:18px;color:red"> </i>
                </li>
            `).join(',');

            directories_.map((dir)=> file_list.innerHTML += `
                <li name="${dir}">
                    Dir: ${dir}
                    <i id='${dir}' class="fa fa-remove" style="font-size:18px;color:red"> </i>
                </li>
            `).join(',');

        set_remove_listeners(directories, 'd');
        set_remove_listeners(files, 'f');
    }

    const update_files = (e) => {
        [...e.target.files].forEach((file) => {
            files = files.filter((f) => file.name !== f.name);
            files.unshift(file);
            update_file_list(files, directories);
            // set_remove_listeners(files, 'f');
        });

        fileInput.value = '';
    }

    const update_directories = (dir) => {
        directories.length > 0 ? directories.forEach((directory) => {
            directories = directories.filter((d) => d !== dir);
            directories.unshift(dir)
        })
        : directories.unshift(dir);
        update_file_list(files, directories);
        // set_remove_listeners(directories, 'd');
        directoryInput.value = '';
    }


    // Drag-and-Drop for Files
    fileDropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileDropZone.style.background = 'rgba(255, 255, 255, 0.1)';
    });
    fileDropZone.addEventListener('dragleave', () => {
        fileDropZone.style.background = 'rgba(255, 255, 255, 0.05)';
    });
    fileDropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        fileDropZone.style.background = 'rgba(255, 255, 255, 0.05)';
        update_files(e);
        console.log('Files Dropped:', e.dataTransfer.files);
    });


    // Input File Selection
    fileInput.addEventListener('change', (e) => {
        update_files(e);
    });

    addDirectoryPath_btn.addEventListener('click', (e) => {
        const dir = directoryInput.value;
        if (isDirectory(dir)) {
            dir ? update_directories(dir) : '';
        } else {
            Swal.fire({
                draggable: true,
                icon: "error",
                title: "Oops...",
                text: "Invalid directory path!!",
                // footer: '<a href="#">Why do I have this issue?</a>'
            });
            directoryInput.value = '';
        }
    });

    share_all_btn.addEventListener('click', () => {
        console.log("Files       : " , files);
        console.log("Directories : " , directories);
        const upF = files.length > 0 ? uploadFile(files) : '';
        const upD = directories.length > 0 ? uploadDirectory(directories) : '';
        // files = [];
        // directories = [];
    })
    const uploadFile = (files_) => {
        const formData = new FormData(); // Create a FormData object

        files_.forEach((file) => {
            formData.append('files[]', file); // Add files to the FormData object
        });
        fetch('/upload-f', {
            method: 'POST',
            body: formData,
        })
            .then((response) => {
                if (!response.ok) {
                    Swal.fire({
                        draggable: true,
                        icon: "error",
                        title: "Oops...",
                        text: "Something went wrong! Try again later or contact the admin",
                        // footer: '<a href="#">Why do I have this issue?</a>'
                    });
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                if (data.status === SUCCESS) {
                    display_alert(data)
                    files = []
                    update_file_list(files, directories);
                }
                console.log('Upload Success:', data);
            })
            .catch((error) => console.error('Upload Error:', error));
    };

    const uploadDirectory = (directories_) => {
        const formData = new FormData(); // Create a FormData object
        directories_.forEach((dir) => {
            formData.append('dirs[]', dir); // Add dirs to the FormData object

        });

        fetch('/upload-d', {
            method: 'POST',
            body: formData,
        })
            .then((response) => {
                if (!response.ok) {
                    Swal.fire({
                        icon: "error",
                        title: "Oops...",
                        text: "Something went wrong! Try again later or contact the admin",
                        // footer: '<a href="#">Why do I have this issue?</a>'
                    });
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                if (data.status === SUCCESS) {
                    display_alert(data);
                    directories = []
                    update_file_list(files, directories);
                } else {
                    Swal.fire({
                        draggable: true,
                        icon: "error",
                        title: "Oops...",
                        text: `${data.message} \n"${data.directory}"`,
                        // footer: '<a href="#">Why do I have this issue?</a>'
                    });
                    directoryInput.value = '';
                }
                console.log('Upload Success:', data);

            })
            .catch((error) => console.error('Upload Error:', error));
    };



});