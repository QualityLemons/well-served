/* ── Autosave ── */
/* Collects the current state of every `.tool-input` field on the draft
   editor page and POSTs it to the autosave endpoint two seconds after the
   user stops typing.  On a successful response it updates the save-status
   indicator and, when a new draft is created, rewrites the browser URL with
   the instance id so a reload re-opens the same draft. */

/* ── Debounce helper ── */
/* Delays execution of `func` until `timeout` ms have elapsed since the last
   call.  Prevents the autosave endpoint from being hit on every keystroke. */
function debounce(func, timeout = 2000) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
}

/* ── Save draft ── */
/* Gathers all `.tool-input` field values, reads the instance id and tool
   slug from hidden inputs, then POSTs the data as JSON to the autosave
   endpoint.  The endpoint returns `{instance_id, last_saved}` — the
   instance_id is written back to the hidden field so subsequent saves
   update the same draft record rather than creating a new one. */
const saveDraft = debounce(() => {
    /* ── Collect form fields ── */
    const formData = {};
    document.querySelectorAll('.tool-input').forEach(input => {
        if (input.name) {
            formData[input.name] = input.value;
        }
    });

    /* ── Read context from hidden inputs ── */
    const instanceId = document.getElementById('instance-id').value;
    const toolSlug = document.getElementById('tool-slug').value;

    /* ── POST to autosave endpoint ── */
    fetch(`/tools/${toolSlug}/autosave/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            /* getCookie reads the csrftoken cookie set by Django's CsrfViewMiddleware.
               Without it, the POST request will be rejected with HTTP 403 Forbidden.
               getCookie must be defined by the page before this script runs. */
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            instance_id: instanceId,
            form_data: formData
        })
    })

    /* ── Handle response ── */
    .then(response => response.json())
    .then(data => {
        /* Update the visible save-status timestamp. */
        document.getElementById('save-status').innerText = `Autosaved at ${data.last_saved}`;

        /* Write the returned instance id back to the hidden field so future
           saves target the same DB record. */
        const previousId = document.getElementById('instance-id').value;
        document.getElementById('instance-id').value = data.instance_id;

        /* When autosave creates a new draft the URL still lacks the instance id.
           Replace it so that a page reload reopens the same draft instead of a
           blank new one. */
        if (!previousId && data.instance_id) {
            const newUrl = `/tools/${toolSlug}/draft/${data.instance_id}/`;
            history.replaceState(null, '', newUrl);
        }
    });
});

/* ── Attach listeners ── */
/* Wire the debounced save to every tool-input field.  New fields added
   dynamically after page load would need to be wired separately, but the
   draft editor renders a fixed set of fields on initial load so this is
   sufficient. */
document.querySelectorAll('.tool-input').forEach(input => {
    input.addEventListener('input', saveDraft);
});
