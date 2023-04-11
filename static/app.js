/**
 * Validates file input
 */
fileInput = document.getElementById('file');

fileInput.addEventListener('change', e => {
    if (!e.target.value.endsWith('.csv')) {
        alert('Please upload CSV files only!');
        e.target.value = "";
    }
})

