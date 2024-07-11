document.getElementById('drop-area').addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.target.style.background = '#f0f0f0';
    e.target.style.border = '2px solid #333';
}, false);

document.getElementById('drop-area').addEventListener('dragleave', (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.target.style.background = '#fff';
    e.target.style.border = '2px dashed #ccc';
}, false);

document.getElementById('drop-area').addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.target.style.background = '#fff';
    e.target.style.border = '2px dashed #ccc';
}, false);
