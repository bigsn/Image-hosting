document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('keydown', function (event) {
        if (event.key === 'F5' || event.key === 'Escape') {
            event.preventDefault();
            window.location.href = 'upload.html';
        }
    });
    const fileListWrapper = document.getElementById('file-list-wrapper');
    const uploadRedirectButton = document.getElementById('upload-tab-btn');

    const updateTabStyles = () => {
        const uploadTab = document.getElementById('upload-tab-btn');
        const imagesTab = document.getElementById('images-tab-btn');
        const isImagesPage = window.location.pathname.includes('images.html');

        uploadTab.classList.remove('upload__tab--active');
        imagesTab.classList.remove('upload__tab--active');

        if (isImagesPage) {
            imagesTab.classList.add('upload__tab--active');
        } else {
            uploadTab.classList.add('upload__tab--active');
        }
    };

    async function displayFiles(page=1, page_size=10) {
        const res = await fetch(`http://localhost/get-images/?page=${page}&page_size=${page_size}`).catch (() => console.error("error GET files"))
        const storedFiles = await res.json()
        fileListWrapper.innerHTML = '';

        if (storedFiles.length === 0) {
            fileListWrapper.innerHTML = '<p class="upload__promt" style="text-align: center; margin-top: 50px;">No images uploaded yet.</p>';
        } else {
            const container = document.createElement('div');
            container.className = 'file-list-container';
            const header = document.createElement('div');
            header.className = 'file-list-header';
            header.innerHTML = `
                <div class="file-col file-col-name">Name</div>
                <div class="file-col file-col-url">Url</div>
                <div class="file-col file-col-delete">Delete</div>
            `;
            container.appendChild(header);

            const list = document.createElement('div');
            list.id = 'file-list';

            storedFiles.images.forEach((item) => {
                const fileItem = document.createElement('div');
                fileItem.className = 'file-list-item';
                fileItem.innerHTML = `
                    <div class="file-col file-col-name">
                        <span class="file-icon"><img src='/images/${item.original_filename}' with="40px" height="40px" alt="file icon"></span>
                        <span class="file-name">${item.filename}.${item.type}</span>
                    </div>
                    <div class="file-col file-col-url"><a href='http://localhost/images/${item.original_filename}' target="_blank">'http://localhost/images/${item.original_filename}'</a></div>
                    <div class="file-col file-col-delete">
                        <button class="delete-btn" data-index="${item.original_filename}"><img src="../image-uploader/img/icon/crash1.webp" height="30px" alt="delete icon"></button>
                    </div>
                    `
                list.appendChild(fileItem);
            });

            const pages = document.querySelector('.pagination');
            pages.innerHTML = '';
            for (let i=1; i<=storedFiles.max_images; i++){
                const paginationItem = document.createElement('li');
                paginationItem.className = 'page-item';
                const button = document.createElement('button')
                button.className = 'page-link';
                button.textContent = i;
                button.addEventListener('click', () => {
                    displayFiles(i);
                })
                paginationItem.appendChild(button);
                pages.appendChild(paginationItem);
            }

            container.appendChild(list);
            fileListWrapper.appendChild(container);
            addDeleteListeners();
        }

        updateTabStyles();
    };

    const addDeleteListeners = () => {
        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', (event) => {
                const indexToDelete = event.currentTarget.dataset.index;
                console.log(indexToDelete)
                fetch(`http://localhost/delete/${indexToDelete}`, {method: 'DELETE'} )
                    .catch((err) => console.log(err))
                displayFiles();
            });
        });
    };

    if (uploadRedirectButton) {
        uploadRedirectButton.addEventListener('click', () => {
            window.location.href = 'upload.html';
        });
    }

    displayFiles();
});