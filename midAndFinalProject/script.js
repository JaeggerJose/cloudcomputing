function showPage(page) {
    var pages = ['upload', 'progress', 'admin'];
    pages.forEach(function(item) {
        var pageElement = document.getElementById(item + 'Page');
        if (item === page) {
            pageElement.classList.remove('hidden');
        } else {
            pageElement.classList.add('hidden');
        }
    });
}

function checkFiles() {
    if (document.getElementById('fileElem').files.length === 0) {
        alert('請選擇一個檔案來上傳！');
        return false;
    }
    return true;
}

var dropArea = document.getElementById('drop-area');
var fileInfo = document.getElementById('fileInfo');

dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropArea.style.background = '#f0f0f0';
    dropArea.style.border = '2px solid #333';
}, false);

dropArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropArea.style.background = '#fff';
    dropArea.style.border = '2px dashed #ccc';
}, false);

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropArea.style.background = '#fff';
    dropArea.style.border = '2px dashed #ccc';
    var files = e.dataTransfer.files;
    handleFiles(files);
}, false);

function handleFiles(files) {
    if (files.length > 0) {
        var fileNames = Array.from(files).map(file => file.name).join(', ');
        fileInfo.textContent = 'Selected file(s): ' + fileNames;
    }
}
document.addEventListener('DOMContentLoaded', function() {
    function showPage(page) {
        var pages = ['upload', 'progress', 'admin'];
        pages.forEach(function(item) {
            var pageElement = document.getElementById(item + 'Page');
            if (item === page) {
                pageElement.classList.remove('hidden');
            } else {
                pageElement.classList.add('hidden');
            }
        });
    }

    function checkFiles() {
        var files = document.getElementById('fileElem').files;
        if (files.length === 0) {
            alert('請選擇一個檔案來上傳！');
            return false;
        }
        return true;
    }

    function handleFiles() {
        var files = document.getElementById('fileElem').files;
        var fileInfo = document.getElementById('fileInfo');
        if (files.length > 0) {
            var fileNames = Array.from(files).map(file => file.name).join(', ');
            fileInfo.textContent = '已選擇檔案: ' + fileNames;
        } else {
            fileInfo.textContent = '或者將檔案拖到這裡';
        }
    }
    var fileElem = document.getElementById('fileElem');
    if (fileElem) {
        fileElem.onchange = handleFiles;
    }
});
