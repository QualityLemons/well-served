/* ── Timer widget ── */
/* jshint esversion: 11, laxbreak: true, shadow: true, -W082, -W058 */
/* Drives the shared timer widget used on draft, session-open, and guest pages.
   IS_HOST and the pause-reminder threshold are read from data attributes on the
   .timer-widget element so no Django template variables are needed in this file:
     data-is-host            "true" | "false"
     data-pause-threshold    integer seconds or "null" */
(function () {

    /* Delay between clearing and repopulating an aria-live region.
       50 ms gives NVDA/JAWS/VoiceOver enough time to register the cleared state
       before the new text arrives, preventing swallowed announcements. */
    const ANNOUNCE_DELAY_MS = 50;

    const widget = document.querySelector('.timer-widget');
    if (!widget) return;

    /* ── Config from data attributes ── */
    const IS_HOST = widget.dataset.isHost === 'true';
    let pauseReminderThresholdSec = widget.dataset.pauseThreshold === 'null'
        ? null
        : (parseInt(widget.dataset.pauseThreshold, 10) || 300);

    /* ── Element references ── */
    const display        = widget.querySelector('.timer-display');
    const pausedBadge    = widget.querySelector('.timer-paused-badge');
    const staleBadge     = widget.querySelector('.timer-stale-badge');
    const reconnectToast = widget.querySelector('.timer-reconnect-toast');
    const startBtn       = widget.querySelector('.timer-start');
    const pauseBtn       = widget.querySelector('.timer-pause');
    const resetBtn       = widget.querySelector('.timer-reset');

    /* ── Internal state ── */
    let intervalId        = null;
    let pauseTickId       = null;
    let _pausedAtMs       = null;
    let _wasPaused        = null;
    let pollFailCount     = 0;
    let _wasStale         = false;
    let _reconnectToastId = null;
    const POLL_FAIL_THRESHOLD = 3;

    /* ── Reconnect toast ── */
    function showReconnectToast() {
        if (!reconnectToast) return;
        if (_reconnectToastId) clearTimeout(_reconnectToastId);
        reconnectToast.textContent = '\u2713 Reconnected \u2014 syncing timer';
        reconnectToast.removeAttribute('hidden');
        _reconnectToastId = setTimeout(function () {
            reconnectToast.setAttribute('hidden', '');
            _reconnectToastId = null;
        }, 4000);
    }

    /* ── Stale indicator ── */
    function setStaleIndicator(isStale) {
        if (!staleBadge) return;
        if (isStale) {
            staleBadge.removeAttribute('hidden');
            _wasStale = true;
        } else {
            staleBadge.setAttribute('hidden', '');
            if (_wasStale) {
                _wasStale = false;
                showReconnectToast();
            }
        }
    }

    /* ── Paused badge ── */
    function updatePausedText() {
        if (!pausedBadge) return;
        if (!_pausedAtMs) {
            pausedBadge.textContent = '\u25ae\u25ae Paused';
            pausedBadge.classList.remove('long-paused');
            return;
        }
        const elapsedSec = Math.floor((Date.now() - _pausedAtMs) / 1000);
        const isLongPause = IS_HOST && pauseReminderThresholdSec !== null && elapsedSec >= pauseReminderThresholdSec;
        pausedBadge.classList.toggle('long-paused', isLongPause);
        if (elapsedSec < 60) {
            pausedBadge.textContent = '\u25ae\u25ae Paused \u00b7 ' + elapsedSec + 's';
        } else {
            const mins = Math.floor(elapsedSec / 60);
            if (isLongPause) {
                pausedBadge.textContent = '\u25ae\u25ae Still paused \u2014 ' + mins + ' min';
            } else {
                pausedBadge.textContent = '\u25ae\u25ae Paused \u00b7 ' + mins + ' min';
            }
        }
    }

    /* ── Expose threshold setter for pause_reminder.js ── */
    window.setTimerPauseReminderThreshold = function (newSec) {
        pauseReminderThresholdSec = (newSec === '' || newSec == null) ? null : +newSec;
        if (pauseTickId) updatePausedText();
    };

    function setPausedIndicator(isPaused, pausedAtMs, skipAnnounce) {
        if (!pausedBadge) return;
        const _announcer = document.getElementById('phase-announcer');
        if (isPaused) {
            _pausedAtMs = pausedAtMs || null;
            pausedBadge.removeAttribute('hidden');
            if (!skipAnnounce && _wasPaused === false && _announcer) {
                _announcer.textContent = '';
                setTimeout(function () { _announcer.textContent = 'Timer paused'; }, ANNOUNCE_DELAY_MS);
            }
            if (pauseTickId) clearInterval(pauseTickId);
            updatePausedText();
            pauseTickId = setInterval(updatePausedText, 1000);
        } else {
            _pausedAtMs = null;
            pausedBadge.setAttribute('hidden', '');
            pausedBadge.textContent = '\u25ae\u25ae Paused';
            pausedBadge.classList.remove('long-paused');
            if (pauseTickId) { clearInterval(pauseTickId); pauseTickId = null; }
            if (!skipAnnounce && _wasPaused === true && _announcer) {
                _announcer.textContent = '';
                setTimeout(function () { _announcer.textContent = 'Timer resumed'; }, ANNOUNCE_DELAY_MS);
            }
        }
        _wasPaused = isPaused;
    }

    /* ── URL helpers ── */
    const statusUrl      = widget.dataset.statusUrl      || null;
    const timerStartUrl  = widget.dataset.timerStartUrl  || null;
    const timerResetUrl  = widget.dataset.timerResetUrl  || null;
    const sessionMode    = !!statusUrl;

    /* ── Format seconds as MM:SS ── */
    function fmt(s) {
        const m   = Math.floor(s / 60);
        const sec = s % 60;
        return String(m).padStart(2, '0') + ':' + String(sec).padStart(2, '0');
    }

    /* ── Optional audio beep ── */
    function beep(frequency, duration, count) {
        try {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            const ctx  = new AudioCtx();
            for (let i = 0; i < (count || 1); i++) {
                const osc  = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.frequency.value = frequency || 880;
                const start = ctx.currentTime + i * (duration || 0.4) * 1.4;
                gain.gain.setValueAtTime(0.25, start);
                gain.gain.exponentialRampToValueAtTime(0.001, start + (duration || 0.4));
                osc.start(start);
                osc.stop(start + (duration || 0.4));
            }
        } catch (e) {}
    }

    /* ── CSRF token helper ── */
    function getCsrf() {
        const val   = '; ' + document.cookie;
        const parts = val.split('; csrftoken=');
        if (parts.length === 2) return parts.pop().split(';').shift();
        return '';
    }

    /* ── Authenticated fetch POST ── */
    async function postJson(url) {
        const resp = await fetch(url, {
            method: 'POST',
            credentials: 'same-origin',
            headers: { 'X-CSRFToken': getCsrf(), 'Content-Type': 'application/json' },
        });
        return resp.json();
    }

    /* ── Phase data (multi-phase tools) ── */
    const phaseDataEl = document.getElementById('phase-data');
    const phases      = phaseDataEl ? JSON.parse(phaseDataEl.textContent) : null;

    /* ══════════════════════════════════════════════════════════════
       MULTI-PHASE TIMER
    ══════════════════════════════════════════════════════════════ */
    if (phases && phases.length) {

        const phaseLabel    = widget.querySelector('.timer-phase-label');
        const phaseProgress = widget.querySelector('.timer-phase-progress');
        const progressBar   = widget.querySelector('.phase-progress-bar');
        let phaseIdx  = 0;
        let remaining = phases[0].seconds;

        function totalSeconds() {
            return phases.reduce((s, p) => s + p.seconds, 0);
        }

        const announcer = document.getElementById('phase-announcer');

        function announce(msg) {
            if (!announcer) return;
            announcer.textContent = '';
            setTimeout(function () { announcer.textContent = msg; }, ANNOUNCE_DELAY_MS);
        }

        const MILESTONES = [300, 120, 60, 30, 10];
        let announcedMilestones = new Set();
        let firstSync        = true;
        let announceOnReturn = false;
        let clockSkew        = 0;

        function milestoneLabel(s) {
            if (s >= 60) {
                const m = s / 60;
                return m === 1 ? '1 minute' : m + ' minutes';
            }
            return s + ' seconds';
        }

        function approxLabel(s) {
            if (s >= 60) {
                const m = Math.round(s / 60);
                return m === 1 ? 'about 1 minute' : 'about ' + m + ' minutes';
            }
            return 'about ' + s + ' seconds';
        }

        function checkMilestones() {
            MILESTONES.forEach(function (ms) {
                if (remaining === ms && !announcedMilestones.has(ms)) {
                    announcedMilestones.add(ms);
                    announce(milestoneLabel(ms) + ' remaining in ' + phases[phaseIdx].label);
                }
            });
        }

        /* ── Progress bar segments (built once, proportional to phase duration) ── */
        let segmentEls = [];
        if (progressBar && phases.length) {
            const total = totalSeconds();
            phases.forEach(function (phase, i) {
                const seg  = document.createElement('div');
                seg.className = 'phase-segment upcoming';
                seg.style.width = ((phase.seconds / total) * 100).toFixed(2) + '%';
                seg.title = phase.label;
                seg.setAttribute('role', 'img');
                seg.setAttribute('aria-label', phase.label + ' \u2014 upcoming');
                const fill = document.createElement('div');
                fill.className   = 'phase-segment-fill';
                fill.style.width = '0%';
                seg.appendChild(fill);
                progressBar.appendChild(seg);
                segmentEls.push(seg);
            });
        }

        let initialRender = true;

        function renderProgressBar() {
            const phaseDuration = phases[phaseIdx].seconds;
            const elapsed  = phaseDuration - remaining;
            const fillPct  = phaseDuration > 0 ? ((elapsed / phaseDuration) * 100).toFixed(1) : 0;
            segmentEls.forEach(function (seg, i) {
                seg.classList.remove('done', 'active', 'upcoming');
                const fill  = seg.querySelector('.phase-segment-fill');
                const label = phases[i].label;
                if (initialRender && fill) fill.style.transition = 'none';
                if (i < phaseIdx) {
                    seg.classList.add('done');
                    seg.setAttribute('aria-label', label + ' \u2014 completed');
                    if (fill) fill.style.width = '100%';
                } else if (i === phaseIdx) {
                    if (remaining === 0) {
                        seg.classList.add('done');
                        seg.setAttribute('aria-label', label + ' \u2014 completed');
                        if (fill) fill.style.width = '100%';
                    } else {
                        seg.classList.add('active');
                        seg.setAttribute('aria-label', label + ' \u2014 active');
                        if (fill) fill.style.width = fillPct + '%';
                    }
                } else {
                    seg.classList.add('upcoming');
                    seg.setAttribute('aria-label', label + ' \u2014 upcoming');
                    if (fill) fill.style.width = '0%';
                }
            });
            if (initialRender) {
                initialRender = false;
                requestAnimationFrame(function () {
                    requestAnimationFrame(function () {
                        segmentEls.forEach(function (seg) {
                            const fill = seg.querySelector('.phase-segment-fill');
                            if (fill) fill.style.transition = '';
                        });
                    });
                });
            }
        }

        function resetToInitial(announceReset) {
            clearInterval(intervalId); intervalId = null;
            phaseIdx  = 0;
            remaining = phases[0].seconds;
            announcedMilestones = new Set();
            if (startBtn) { startBtn.disabled = false; startBtn.textContent = 'Start'; }
            setPausedIndicator(false, undefined, true);
            if (announceReset) announce('Timer reset');
            renderPhase();
        }

        function updateProgressText() {
            if (phaseProgress) phaseProgress.textContent = 'Phase ' + (phaseIdx + 1) + ' of ' + phases.length;
        }

        function renderPhase() {
            const phase = phases[phaseIdx];
            if (phaseLabel) phaseLabel.textContent = phase.label;
            updateProgressText();
            display.textContent = fmt(remaining);
            const isLastPhase = phaseIdx === phases.length - 1;
            display.classList.toggle('warning', remaining > 0 && remaining <= 10);
            display.classList.toggle('expired',  remaining === 0 && isLastPhase);
            renderProgressBar();
        }

        function flashLabel() {
            if (!phaseLabel) return;
            phaseLabel.classList.add('phase-flash');
            setTimeout(() => phaseLabel.classList.remove('phase-flash'), 1200);
        }

        function tick() {
            if (remaining > 0) {
                remaining -= 1;
                renderPhase();
                checkMilestones();
            }
            if (remaining === 0) {
                if (phaseIdx < phases.length - 1) {
                    phaseIdx  += 1;
                    remaining  = phases[phaseIdx].seconds;
                    announcedMilestones = new Set();
                    beep(880, 0.35, 1);
                    flashLabel();
                    announce('Now entering Phase ' + (phaseIdx + 1) + ' \u2014 ' + phases[phaseIdx].label);
                    renderPhase();
                } else {
                    clearInterval(intervalId); intervalId = null;
                    if (startBtn) { startBtn.disabled = false; startBtn.textContent = 'Start'; }
                    beep(660, 0.4, 2);
                    announce('All phases complete');
                    renderPhase();
                }
            }
        }

        function applyServerTimestamp(timerStartedAt, timerPausedAt) {
            if (!timerStartedAt) { resetToInitial(); return; }
            const referenceTime = timerPausedAt
                ? new Date(timerPausedAt).getTime()
                : Date.now() + clockSkew;
            const elapsedSec = Math.floor((referenceTime - new Date(timerStartedAt).getTime()) / 1000);
            let acc = 0, newPhaseIdx = phases.length - 1, newRemaining = 0;
            for (let i = 0; i < phases.length; i++) {
                if (elapsedSec < acc + phases[i].seconds) {
                    newPhaseIdx   = i;
                    newRemaining  = phases[i].seconds - (elapsedSec - acc);
                    break;
                }
                acc += phases[i].seconds;
            }
            const prevPhaseIdx = phaseIdx;
            phaseIdx  = newPhaseIdx;
            remaining = newRemaining;
            if (newPhaseIdx !== prevPhaseIdx) {
                announcedMilestones = new Set();
                flashLabel();
                announce('Now entering Phase ' + (phaseIdx + 1) + ' \u2014 ' + phases[phaseIdx].label);
            }
            MILESTONES.forEach(function (ms) { if (remaining < ms) announcedMilestones.add(ms); });
            const _wasFSPaused = firstSync && !!timerStartedAt && remaining > 0 && !!timerPausedAt;
            if (firstSync && timerStartedAt && remaining > 0) {
                if (timerPausedAt) {
                    announce('Timer is paused \u2014 ' + approxLabel(remaining) + ' remaining in ' + phases[phaseIdx].label);
                } else {
                    announce(approxLabel(remaining) + ' remaining in ' + phases[phaseIdx].label);
                }
            }
            if (announceOnReturn) {
                announceOnReturn = false;
                if (!timerPausedAt && remaining > 0) {
                    announce(approxLabel(remaining) + ' remaining in ' + phases[phaseIdx].label);
                }
            }
            firstSync = false;
            renderPhase();
            if (timerPausedAt) {
                clearInterval(intervalId); intervalId = null;
                if (startBtn) { startBtn.disabled = false; startBtn.textContent = 'Resume'; }
                setPausedIndicator(true, new Date(timerPausedAt).getTime(), _wasFSPaused);
            } else {
                setPausedIndicator(false);
                if (remaining > 0 && !intervalId) {
                    intervalId = setInterval(tick, 1000);
                    if (startBtn) { startBtn.disabled = true; startBtn.textContent = 'Running\u2026'; }
                } else if (remaining === 0 && intervalId) {
                    clearInterval(intervalId); intervalId = null;
                    if (startBtn) { startBtn.disabled = false; startBtn.textContent = 'Start'; }
                    announce('All phases complete');
                }
            }
        }

        if (sessionMode) {
            const _initStartedEl = document.getElementById('timer-started-at');
            const _initPausedEl  = document.getElementById('timer-paused-at');
            if (_initStartedEl) {
                applyServerTimestamp(
                    JSON.parse(_initStartedEl.textContent),
                    _initPausedEl ? JSON.parse(_initPausedEl.textContent) : null
                );
            }
        }

        let pauseIntent     = false;
        let virtualStartedAt = null;

        if (sessionMode) {
            async function pollTimerState() {
                if (pauseIntent) { pauseIntent = false; return; }
                try {
                    const data = await fetch(statusUrl, { credentials: 'same-origin' }).then(r => r.json());
                    if (pauseIntent) { pauseIntent = false; return; }
                    pollFailCount = 0;
                    setStaleIndicator(false);
                    if (data.server_now) clockSkew = new Date(data.server_now).getTime() - Date.now();
                    applyServerTimestamp(data.timer_started_at, data.timer_paused_at);
                } catch (e) {
                    pollFailCount += 1;
                    if (pollFailCount >= POLL_FAIL_THRESHOLD) setStaleIndicator(true);
                }
            }
            pollTimerState();
            setInterval(pollTimerState, 4000);
            window.addEventListener('offline',  function () { setStaleIndicator(true); });
            window.addEventListener('online',   function () { pollTimerState(); });
            document.addEventListener('visibilitychange', function () {
                if (!document.hidden) {
                    initialRender    = true;
                    announceOnReturn = true;
                    pollTimerState();
                }
            });
        } else {
            document.addEventListener('visibilitychange', function () {
                if (!document.hidden && intervalId && virtualStartedAt) {
                    initialRender = true;
                    applyServerTimestamp(new Date(virtualStartedAt).toISOString(), null);
                    if (intervalId && remaining > 0) {
                        announce(approxLabel(remaining) + ' remaining in ' + phases[phaseIdx].label);
                    }
                }
            });
        }

        if (startBtn) {
            startBtn.addEventListener('click', async () => {
                if (intervalId) return;
                if (phaseIdx >= phases.length - 1 && remaining === 0) {
                    phaseIdx  = 0;
                    remaining = phases[0].seconds;
                    renderPhase();
                }
                if (sessionMode) {
                    pauseIntent = true;
                    try {
                        const data = await postJson(timerStartUrl);
                        if (data.timer_started_at) {
                            pauseIntent = false;
                            applyServerTimestamp(data.timer_started_at);
                            return;
                        }
                    } catch (e) { pauseIntent = false; }
                }
                setPausedIndicator(false);
                intervalId = setInterval(tick, 1000);
                if (startBtn) { startBtn.disabled = true; startBtn.textContent = 'Running\u2026'; }
                if (pauseBtn)  pauseBtn.disabled  = false;
                if (!sessionMode) {
                    var _elapsed = 0;
                    for (var _i = 0; _i < phaseIdx; _i++) _elapsed += phases[_i].seconds;
                    _elapsed += phases[phaseIdx].seconds - remaining;
                    virtualStartedAt = Date.now() - _elapsed * 1000;
                }
            });
        }

        if (pauseBtn) {
            pauseBtn.addEventListener('click', () => {
                if (!intervalId) return;
                pauseIntent = true;
                clearInterval(intervalId); intervalId = null;
                if (startBtn) { startBtn.disabled = false; startBtn.textContent = 'Resume'; }
                pauseBtn.disabled = true;
                setPausedIndicator(true, Date.now());
                if (!sessionMode) virtualStartedAt = null;
            });
        }

        if (resetBtn) {
            resetBtn.addEventListener('click', async () => {
                if (sessionMode) pauseIntent = true;
                virtualStartedAt = null;
                resetToInitial(true);
                if (sessionMode) { try { await postJson(timerResetUrl); } catch (e) {} }
            });
        }

        renderPhase();

    /* ══════════════════════════════════════════════════════════════
       SINGLE-PHASE TIMER
    ══════════════════════════════════════════════════════════════ */
    } else {

        const total     = parseInt(widget.dataset.duration, 10) || 60;
        let remaining   = total;

        const _simpleAnnouncer = document.getElementById('phase-announcer');
        function announce(msg) {
            if (!_simpleAnnouncer) return;
            _simpleAnnouncer.textContent = '';
            setTimeout(function () { _simpleAnnouncer.textContent = msg; }, ANNOUNCE_DELAY_MS);
        }

        const MILESTONES = [300, 120, 60, 30, 10];
        let announcedMilestones = new Set();
        let firstSync        = true;
        let announceOnReturn = false;
        let clockSkew        = 0;

        function milestoneLabel(s) {
            if (s >= 60) {
                const m = s / 60;
                return m === 1 ? '1 minute' : m + ' minutes';
            }
            return s + ' seconds';
        }

        function approxLabel(s) {
            if (s >= 60) {
                const m = Math.round(s / 60);
                return m === 1 ? 'about 1 minute' : 'about ' + m + ' minutes';
            }
            return 'about ' + s + ' seconds';
        }

        function checkMilestones() {
            MILESTONES.forEach(function (ms) {
                if (remaining === ms && !announcedMilestones.has(ms)) {
                    announcedMilestones.add(ms);
                    announce(milestoneLabel(ms) + ' remaining');
                }
            });
        }

        function resetToInitial(announceReset) {
            clearInterval(intervalId); intervalId = null;
            remaining           = total;
            announcedMilestones = new Set();
            if (startBtn) { startBtn.disabled = false; startBtn.textContent = 'Start'; }
            if (pauseBtn)   pauseBtn.disabled  = true;
            setPausedIndicator(false, undefined, true);
            if (announceReset) announce('Timer reset');
            render();
        }

        function render() {
            display.textContent = fmt(remaining);
            display.classList.toggle('warning', remaining > 0 && remaining <= 10);
            display.classList.toggle('expired',  remaining === 0);
        }

        function tick() {
            if (remaining > 0) { remaining -= 1; render(); checkMilestones(); }
            if (remaining === 0) {
                clearInterval(intervalId); intervalId = null;
                if (startBtn) { startBtn.disabled = false; startBtn.textContent = 'Start'; }
                if (pauseBtn)   pauseBtn.disabled  = true;
                announce('Timer complete');
            }
        }

        function applyServerTimestamp(timerStartedAt, timerPausedAt) {
            if (!timerStartedAt) { resetToInitial(); return; }
            const referenceTime = timerPausedAt
                ? new Date(timerPausedAt).getTime()
                : Date.now() + clockSkew;
            const elapsedSec = Math.floor((referenceTime - new Date(timerStartedAt).getTime()) / 1000);
            remaining = Math.max(0, total - elapsedSec);
            MILESTONES.forEach(function (ms) { if (remaining < ms) announcedMilestones.add(ms); });
            const _wasFSPaused = firstSync && !!timerStartedAt && remaining > 0 && !!timerPausedAt;
            if (firstSync && timerStartedAt && remaining > 0) {
                if (timerPausedAt) {
                    announce('Timer is paused \u2014 ' + approxLabel(remaining) + ' remaining');
                } else {
                    announce(approxLabel(remaining) + ' remaining');
                }
            }
            if (announceOnReturn) {
                announceOnReturn = false;
                if (!timerPausedAt && remaining > 0) announce(approxLabel(remaining) + ' remaining');
            }
            firstSync = false;
            render();
            if (timerPausedAt) {
                clearInterval(intervalId); intervalId = null;
                if (startBtn) { startBtn.disabled = false; startBtn.textContent = 'Resume'; }
                setPausedIndicator(true, new Date(timerPausedAt).getTime(), _wasFSPaused);
            } else {
                setPausedIndicator(false);
                if (remaining > 0 && !intervalId) {
                    intervalId = setInterval(tick, 1000);
                    if (startBtn) { startBtn.disabled = true; startBtn.textContent = 'Running\u2026'; }
                } else if (remaining === 0 && intervalId) {
                    clearInterval(intervalId); intervalId = null;
                    if (startBtn) { startBtn.disabled = false; startBtn.textContent = 'Start'; }
                    if (pauseBtn) pauseBtn.disabled = true;
                    announce('Timer complete');
                }
            }
        }

        if (sessionMode) {
            const _initStartedEl = document.getElementById('timer-started-at');
            const _initPausedEl  = document.getElementById('timer-paused-at');
            if (_initStartedEl) {
                applyServerTimestamp(
                    JSON.parse(_initStartedEl.textContent),
                    _initPausedEl ? JSON.parse(_initPausedEl.textContent) : null
                );
            }
        }

        let pauseIntent      = false;
        let virtualStartedAt = null;

        if (sessionMode) {
            async function pollTimerState() {
                if (pauseIntent) { pauseIntent = false; return; }
                try {
                    const data = await fetch(statusUrl, { credentials: 'same-origin' }).then(r => r.json());
                    if (pauseIntent) { pauseIntent = false; return; }
                    pollFailCount = 0;
                    setStaleIndicator(false);
                    if (data.server_now) clockSkew = new Date(data.server_now).getTime() - Date.now();
                    applyServerTimestamp(data.timer_started_at, data.timer_paused_at);
                } catch (e) {
                    pollFailCount += 1;
                    if (pollFailCount >= POLL_FAIL_THRESHOLD) setStaleIndicator(true);
                }
            }
            pollTimerState();
            setInterval(pollTimerState, 4000);
            window.addEventListener('offline',  function () { setStaleIndicator(true); });
            window.addEventListener('online',   function () { pollTimerState(); });
            document.addEventListener('visibilitychange', function () {
                if (!document.hidden) { announceOnReturn = true; pollTimerState(); }
            });
        } else {
            document.addEventListener('visibilitychange', function () {
                if (!document.hidden && intervalId && virtualStartedAt) {
                    applyServerTimestamp(new Date(virtualStartedAt).toISOString(), null);
                    if (intervalId && remaining > 0) announce(approxLabel(remaining) + ' remaining');
                }
            });
        }

        if (startBtn) {
            startBtn.addEventListener('click', async () => {
                if (intervalId) return;
                if (remaining === 0) remaining = total;
                if (sessionMode) {
                    pauseIntent = true;
                    try {
                        const data = await postJson(timerStartUrl);
                        if (data.timer_started_at) {
                            pauseIntent = false;
                            applyServerTimestamp(data.timer_started_at);
                            return;
                        }
                    } catch (e) { pauseIntent = false; }
                }
                setPausedIndicator(false);
                intervalId = setInterval(tick, 1000);
                if (startBtn) { startBtn.disabled = true; startBtn.textContent = 'Running\u2026'; }
                if (pauseBtn)  pauseBtn.disabled  = false;
                if (!sessionMode) virtualStartedAt = Date.now() - (total - remaining) * 1000;
            });
        }

        if (pauseBtn) {
            pauseBtn.addEventListener('click', () => {
                if (!intervalId) return;
                pauseIntent = true;
                clearInterval(intervalId); intervalId = null;
                if (startBtn) { startBtn.disabled = false; startBtn.textContent = 'Resume'; }
                if (pauseBtn)   pauseBtn.disabled  = true;
                setPausedIndicator(true, Date.now());
                if (!sessionMode) virtualStartedAt = null;
            });
        }

        if (resetBtn) {
            resetBtn.addEventListener('click', async () => {
                if (sessionMode) pauseIntent = true;
                virtualStartedAt = null;
                resetToInitial(true);
                if (sessionMode) { try { await postJson(timerResetUrl); } catch (e) {} }
            });
        }

        render();
    }

}());
