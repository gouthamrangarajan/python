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

function formBeforeSend(_, self) {
    // self.children.
    const textArea = document.getElementById('txtMessage');
    const text = textArea.value;
    Alpine.store('prompts').updateData(text, Alpine.store('prompts').data.length - 1);
    Alpine.store('prompts').pushData('');
    textArea.value = '';
    const scrollEl = document.getElementById('scroll-div');
    scrollEl.scrollTop = scrollEl.scrollHeight;
}
function afterSwap(_, self) {

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

function formError(_, self) {
    const errorElAssistant = document.getElementById("errorTemplateAssistant").innerHTML;
    let errorElUser = document.getElementById("errorTemplateUser").innerHTML;
    errorElUser = errorElUser.replaceAll("store_data_idx", Alpine.store('prompts').data.length - 1)
    const ul = document.getElementById("list");
    const liAssistant = document.createElement('li');
    const liUser = document.createElement('li');
    ul.appendChild(liAssistant);
    ul.appendChild(liUser);
    liAssistant.outerHTML = errorElAssistant;
    liUser.outerHTML = errorElUser;
}
