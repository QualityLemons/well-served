// A simple debounce function to prevent spamming the server
function debounce(func, timeout = 2000) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
}

const saveDraft = debounce(() => {
    const formData = {}; // Collect your inputs here (e.g., using new FormData(form))
    const instanceId = document.getElementById('instance-id').value;
    const toolSlug = document.getElementById('tool-slug').value;

    fetch(`/tools/${toolSlug}/autosave/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Django security requirement
        },
        body: JSON.stringify({
            instance_id: instanceId,
            form_data: formData
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('save-status').innerText = `Autosaved at ${data.last_saved}`;
        document.getElementById('instance-id').value = data.instance_id;
    });
});

// Trigger save on input change
document.querySelectorAll('.tool-input').forEach(input => {
    input.addEventListener('input', saveDraft);
});