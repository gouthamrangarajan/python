document.addEventListener('alpine:init', () => {
    Alpine.store('prompts', {
        data: [''],
        pushData(val) {
            this.data.push(val);
        },
        updateData(val, idx) {
            this.data[idx] = val;
        }
    });
});

function formBeforeSend() {
    // self.children.
    const textArea = document.getElementById('txtMessage');
    const text = textArea.value;
    Alpine.store('prompts').updateData(text, Alpine.store('prompts').data.length - 1);
    Alpine.store('prompts').pushData('');
    textArea.value = '';
    const scrollEl = document.getElementById('scroll-div');
    scrollEl.scrollTop = scrollEl.scrollHeight;
}

function keyDown(event, self) {
    if (event.key === 'Enter') {
        event.preventDefault();
        self.dispatchEvent(new Event("chat_submit", { bubbles: true }));
    }
}

function submitBtnClick(event, self) {
    event.preventDefault();
    self.dispatchEvent(new Event("chat_submit", { bubbles: true }));
}

