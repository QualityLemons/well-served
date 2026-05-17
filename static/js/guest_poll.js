/* ── Guest session poll ── */
/* Polls the session status endpoint every 4 seconds so guest participants
   are automatically redirected when the host closes the session.
   The status URL is read from data-status-url on #session-announcer. */
(function () {

    var ANNOUNCE_DELAY_MS = 50;
    var POLL_INTERVAL_MS  = 4000;
    var ERROR_THRESHOLD   = 3;

    /* ── Element references ── */
    var _announcer = document.getElementById('session-announcer');
    var statusUrl  = _announcer ? _announcer.dataset.statusUrl : null;

    if (!statusUrl) return;

    /* ── State ── */
    var consecutiveErrors = 0;
    var wasReconnecting   = false;

    /* ── Announce to screen readers ── */
    function announce(msg) {
        if (!_announcer) return;
        _announcer.textContent = '';
        setTimeout(function () { _announcer.textContent = msg; }, ANNOUNCE_DELAY_MS);
    }

    /* ── Poll ── */
    async function poll() {
        try {
            var resp = await fetch(statusUrl, { credentials: 'same-origin' });
            if (!resp.ok) throw new Error('HTTP ' + resp.status);
            var data = await resp.json();

            if (consecutiveErrors >= ERROR_THRESHOLD || wasReconnecting) {
                announce('Reconnected');
                wasReconnecting = false;
            }
            consecutiveErrors = 0;

            if (data.status === 'closed') {
                announce('Session has been closed. Reloading the page.');
                setTimeout(function () { window.location.reload(); }, 600);
            }
        } catch (err) {
            consecutiveErrors += 1;
            if (consecutiveErrors >= ERROR_THRESHOLD && !wasReconnecting) {
                announce('Connection lost. Attempting to reconnect.');
                wasReconnecting = true;
            }
        }
    }

    poll();
    setInterval(poll, POLL_INTERVAL_MS);

}());
