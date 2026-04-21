// Theme toggle
function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    html.setAttribute('data-theme', current === 'dark' ? 'light' : 'dark');
    localStorage.setItem('theme', html.getAttribute('data-theme'));
}
(function () {
    const saved = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
})();

// Voice assistant
function startVoice() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        document.getElementById('voice-status').textContent = 'Not supported in this browser.';
        return;
    }
    const rec = new SpeechRecognition();
    rec.lang = 'en-US';
    rec.start();
    document.getElementById('voice-status').textContent = '🎤 Listening...';

    rec.onresult = async (e) => {
        const text = e.results[0][0].transcript;
        document.getElementById('voice-status').textContent = `You said: "${text}"`;
        const res = await fetch('/api/voice', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        const data = await res.json();
        const replyEl = document.getElementById('voice-reply');
        replyEl.textContent = '🤖 ' + data.reply;
        replyEl.style.display = 'block';
    };
    rec.onerror = () => {
        document.getElementById('voice-status').textContent = 'Error. Try again.';
    };
}
