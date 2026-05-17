/* ── Aria wiring ── */
/* Connect error message elements to their input fields.
   Error elements follow the naming convention: id="{{ field_id }}-error"
   The script sets aria-describedby on the input and marks it aria-invalid. */
(function () {
    document.querySelectorAll('[id$="-error"]').forEach(function (errEl) {
        var inputId = errEl.id.replace(/-error$/, '');
        var input = document.getElementById(inputId);
        if (input) {
            input.setAttribute('aria-describedby', errEl.id);
            input.setAttribute('aria-invalid', 'true');
        }
    });
}());
