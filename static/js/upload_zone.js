
document.addEventListener('DOMContentLoaded', () => {
    const fileDropZone = document.getElementById('file_upload_zone');
    const directoryDropZone = document.getElementById('directory_upload_zone');
    const fileInput = document.getElementById('file_input');
    const directoryInput = document.getElementById('directory_input');
    const share_all_btn = document.getElementById('share_all');
    let files = [];
    let directories = []
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
        [...e.dataTransfer.files].forEach((file) => {
            files.push(file);
        })
        console.log('Files Dropped:', e.dataTransfer.files);
    });

    // Drag-and-Drop for Directories
    directoryDropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        directoryDropZone.style.background = 'rgba(255, 255, 255, 0.1)';
    });
    directoryDropZone.addEventListener('dragleave', () => {
        directoryDropZone.style.background = 'rgba(255, 255, 255, 0.05)';
    });
    directoryDropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        directoryDropZone.style.background = 'rgba(255, 255, 255, 0.05)';
        [...e.dataTransfer.files].forEach((file) => {
            directories.push(file);
        })
        console.log('Directories Dropped:', e.dataTransfer.files);
    });

    // Input File Selection
    fileInput.addEventListener('change', (e) => {
        [...e.target.files].forEach((file) => {
            files.push(file);
        })
        console.log('Selected Files:', e.target.files);
    });

    directoryInput.addEventListener('change', (e) => {
        [...e.target.files].forEach((file) => {
            directories.push(file);
        })
        console.log('Selected Directories:', e.target.files);
    });

    share_all_btn.addEventListener('click', () => {
        console.log("Files       : " , files);
        console.log("Directories : " , directories);
        const upF = files.length > 0 ? uploadFile(files) : '';
        // const upD = directories.length > 0 ? uploadDirectory(directories) : '';
        files = [];
        directories = [];
    })
    const uploadFile = (files_) => {
        const formData = new FormData(); // Create a FormData object

        files_.forEach((file) => {
            console.log("File name:", file.name);
            formData.append('files[]', file); // Add files to the FormData object
        });

        fetch('/upload-f', {
            method: 'POST',
            body: formData,
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => console.log('Upload Success:', data))
            .catch((error) => console.error('Upload Error:', error));
    };

    // const uploadDirectory = (files_) => {
    //     const formData = new FormData();
    //
    //     Array.from(files_).forEach((file) => {
    //         // Log each file path for debugging
    //         formData.append('files[]', file, file.webkitRelativePath); // Preserve the folder structure
    //     });
    //
    //     console.log("Forma data : ", formData)
    //     fetch('/upload-d', {
    //         method: 'POST',
    //         body: formData,
    //     })
    //         .then((response) => {
    //             if (!response.ok) {
    //                 throw new Error(`HTTP error! status: ${response.status}`);
    //             }
    //             return response.json();
    //         })
    //         .then((data) => console.log('Upload Success:', data))
    //         .catch((error) => console.error('Upload Error:', error));
    // };


});