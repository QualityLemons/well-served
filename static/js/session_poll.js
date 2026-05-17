/* ── Host session poll ── */
/* Polls the session status endpoint every 4 seconds, updating the participant
   list and announcing joins, departures, and response submissions.
   Configuration from data attributes and a JSON script element:
     #session-announcer[data-status-url]    — polling endpoint URL
     #initial-responders-data               — JSON array of display names who
                                              had already responded at page load */
(function () {

    var ANNOUNCE_DELAY_MS = 50;
    var POLL_INTERVAL_MS  = 4000;
    var ERROR_THRESHOLD   = 3;

    /* ── Element references ── */
    var _sessionAnnouncer = document.getElementById('session-announcer');
    var listEl            = document.getElementById('participant-list');
    var countEl           = document.getElementById('participant-count');
    var pollStatusEl      = document.getElementById('poll-status');

    if (!_sessionAnnouncer) return;

    var statusUrl = _sessionAnnouncer.dataset.statusUrl;
    if (!statusUrl) return;

    /* ── Announce to screen readers ── */
    function announce(msg) {
        _sessionAnnouncer.textContent = '';
        setTimeout(function () { _sessionAnnouncer.textContent = msg; }, ANNOUNCE_DELAY_MS);
    }

    /* ── Seed known responders from page-load data ── */
    var _initialDataEl = document.getElementById('initial-responders-data');
    var initialNames   = _initialDataEl ? JSON.parse(_initialDataEl.textContent) : [];
    var knownResponders = new Set(initialNames);

    /* ── State ── */
    var consecutiveErrors    = 0;
    var wasReconnecting      = false;
    var lastParticipantCount = parseInt(countEl.textContent, 10) || 0;

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
            if (pollStatusEl) { pollStatusEl.textContent = 'live'; pollStatusEl.style.color = ''; }

            if (data.status === 'closed') {
                if (pollStatusEl) pollStatusEl.textContent = 'session closed \u2014 reloading\u2026';
                announce('Session has been closed. Reloading the page.');
                setTimeout(function () { window.location.reload(); }, 600);
                return;
            }

            var newCount    = data.participants.length;
            var pollMessages = [];

            /* ── Join / leave announcements ── */
            if (newCount !== lastParticipantCount) {
                var diff = newCount - lastParticipantCount;
                if (diff > 0) {
                    pollMessages.push(
                        diff === 1 ?
                            'One participant joined. ' + newCount + ' participants total.' :
                            diff + ' participants joined. ' + newCount + ' participants total.'
                    );
                } else {
                    var removed = -diff;
                    pollMessages.push(
                        removed === 1 ?
                            'One participant left. ' + newCount + ' participants total.' :
                            removed + ' participants left. ' + newCount + ' participants total.'
                    );
                }
                lastParticipantCount = newCount;
            }

            /* ── Response announcements ── */
            var currentNames    = new Set(data.participants.map(function (p) { return p.display_name; }));
            var newKnownResponders = new Set();
            knownResponders.forEach(function (n) { if (currentNames.has(n)) newKnownResponders.add(n); });
            data.participants.forEach(function (p) {
                if (p.has_response) newKnownResponders.add(p.display_name);
            });

            var totalParticipants = data.participants.length;
            var totalResponded    = data.participants.filter(function (p) { return p.has_response; }).length;
            var newResponders     = data.participants.filter(function (p) {
                return p.has_response && !knownResponders.has(p.display_name);
            });

            if (newResponders.length === 1) {
                pollMessages.push(
                    newResponders[0].display_name + ' saved their response. ' +
                    totalResponded + ' of ' + totalParticipants + ' participants have responded.'
                );
            } else if (newResponders.length > 1) {
                pollMessages.push(
                    newResponders.length + ' participants saved their responses. ' +
                    totalResponded + ' of ' + totalParticipants + ' participants have responded.'
                );
            }
            knownResponders = newKnownResponders;

            if (pollMessages.length > 0) announce(pollMessages.join(' '));

            /* ── Update participant list DOM ── */
            if (countEl) countEl.textContent = newCount;
            if (listEl) {
                listEl.innerHTML = data.participants.map(function (p) {
                    var hostTag = p.is_host ? ' <span style="color:#64748b;">(host)</span>' : '';
                    var respTag = p.has_response ?
                        ' \u2014 <span style="color:#15803d;">response saved</span>' : '';
                    var safeName = p.display_name
                        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                    return '<li>' + safeName + hostTag + respTag + '</li>';
                }).join('');
            }
        } catch (err) {
            consecutiveErrors += 1;
            if (consecutiveErrors >= ERROR_THRESHOLD) {
                if (!wasReconnecting) {
                    announce('Connection lost. Attempting to reconnect.');
                    wasReconnecting = true;
                }
                if (pollStatusEl) { pollStatusEl.textContent = 'reconnecting\u2026'; pollStatusEl.style.color = '#b45309'; }
            }
        }
    }

    poll();
    setInterval(poll, POLL_INTERVAL_MS);

}());
