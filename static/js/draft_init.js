/* ── Draft editor initialisation ── */
/* Defines the getCookie helper required by autosave.js and adds the
   .tool-input class to all form fields that autosave should monitor.
   Must be loaded before autosave.js. */

function getCookie(name) {
    var value = '; ' + document.cookie;
    var parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}

document.querySelectorAll(
    'form textarea, form input[type="text"], form input[type="number"], ' +
    'form input[type="url"], form input[type="email"], form select'
).forEach(function (el) {
    el.classList.add('tool-input');
});
