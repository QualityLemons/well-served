// A simple debounce function to prevent spamming the server
function debounce(func, timeout = 2000) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
}

const saveDraft = debounce(() => {
    // formData should be populated with the current values of all .tool-input
    // elements.  Currently it is sent as an empty object — a placeholder that
    // will be replaced once structured field collection is implemented.
    const formData = {};
    const instanceId = document.getElementById('instance-id').value;
    const toolSlug = document.getElementById('tool-slug').value;

    fetch(`/tools/${toolSlug}/autosave/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // getCookie reads the csrftoken cookie set by Django's CsrfViewMiddleware.
            // Without it, the POST request will be rejected with HTTP 403 Forbidden.
            // getCookie must be defined by the page before this script runs.
            'X-CSRFToken': getCookie('csrftoken')
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
