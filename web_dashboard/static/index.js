// funzione per caricare i log
function fetchLogs() {
    fetch('/api/logs')
        .then(response => response.json())
        .then(data => {
            const logsEl = document.getElementById('logs');
            if (data.length === 0) {
                logsEl.textContent = "Caricamento log...";
            } else {
                logsEl.textContent = data.join('\n');
                logsEl.scrollTop = logsEl.scrollHeight;
            }
        })
        .catch(() => {
            const logsEl = document.getElementById('logs');
            logsEl.textContent = "Errore caricamento log.";
        });
}

// funzione per caricare i log ogni secondo
setInterval(fetchLogs, 1000);
window.onload = fetchLogs;

// funzione per inviare i comandi
function sendCommand(cmd) {
    const consoleBox = document.getElementById('action-console');
    if (consoleBox.children.length > 0) {
        addConsoleLine('------', true);
    }
    const msg = `> Inviato comando: ${cmd}`;
    addConsoleLine(msg);

    fetch('/command', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({command: cmd})
    })
    .then(res => res.json())
    .then(data => {
        addConsoleLine(`✔ ${data.status || 'Comando inviato!'}`);
    })
    .catch(() => {
        addConsoleLine('✖ Errore invio comando');
    });
}

// funzione per aggiungere le linee nella console
function addConsoleLine(text, isSeparator = false) {
    const consoleBox = document.getElementById('action-console');
    const line = document.createElement('span');
    line.textContent = text;
    if (isSeparator) {
        line.style.margin = '0.7em 0 0.7em 0';
    }
    consoleBox.appendChild(line);
    consoleBox.scrollTop = consoleBox.scrollHeight;
    while (consoleBox.children.length > 10) {
        consoleBox.removeChild(consoleBox.firstChild);
    }
}
