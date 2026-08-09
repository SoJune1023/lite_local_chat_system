document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');
    const modelSelect = document.getElementById('modelSelect');
    const interactionBtn = document.getElementById('interactionBtn');
    const chatOutput = document.getElementById('chatOutput');

    const BASE_URL = 'http://127.0.0.1:8000';

    function mapRole(serverRole) {
        if (serverRole === 'user') return 'you';
        if (serverRole === 'assistant') return 'ai';
        return serverRole;
    }

    async function sendInteraction() {
        const message = messageInput.value.trim();
        const model = modelSelect.value;

        if (!message) return;

        interactionBtn.disabled = true;
        const prevText = interactionBtn.textContent;
        interactionBtn.textContent = 'Thinking . . .';

        appendMessage('you', message);
        messageInput.value = '';

        const request_dict = {
            message: message,
            model: model
        };

        try {
            const res = await fetch(`${BASE_URL}/interaction`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(request_dict)
            });

            if (!res.ok) {
                const errText = await res.text();
                appendMessage('error', `Server Error ${res.status}: ${errText}`);
                return;
            }

            const data = await res.json();
            appendMessage('ai', data.message);

        } catch (err) {
            appendMessage('error', `Failed to connect server: ${err.message}`);
        } finally {
            interactionBtn.disabled = false;
            interactionBtn.textContent = prevText;
        }
    }

    async function loadHistory(maxMessages = 50) {
        interactionBtn.disabled = true;
        const prevText = interactionBtn.textContent;
        interactionBtn.textContent = 'Load history . . .';

        const request_dict = {
            max_messages: 50
        };

        try {
            const res = await fetch(
                `${BASE_URL}/interaction/history?max_messages=${maxMessages}`
            );

            if (!res.ok) {
                const errText = await res.text();
                appendMessage('error', `Server Error ${res.status}: ${errText}`);
                return;
            }

            const data = await res.json();

            data.messages.forEach((msg) => {
                appendMessage(mapRole(msg.role), msg.content);
            });
        } catch (err) {
            appendMessage('error', `Failed to connect server: ${err.message}`);
        } finally {
            interactionBtn.disabled = false;
            interactionBtn.textContent = prevText;
        }
    }

    function appendMessage(role, text) {
        if (!chatOutput) {
            console.error('chatOutput element not found');
            return;
        }
        const el = document.createElement('div');
        el.className = `message message-${role}`;
        el.innerHTML = `<strong>${role.toUpperCase()}</strong>${text}`;
        chatOutput.appendChild(el);
        chatOutput.scrollTop = chatOutput.scrollHeight;
    }

    loadHistory();

    interactionBtn.addEventListener('click', (e) => {
        e.preventDefault();
        sendInteraction();
    });

    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) {
            e.preventDefault();
            sendInteraction();
        }
    });
});