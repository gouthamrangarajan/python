document.addEventListener('alpine:init', () => {
    Alpine.store('prompts', {
        data: [''],
        currentVal: '',
        pushData(val) {
            this.data.push(val);
        },
        updateData(val, idx) {
            this.data[idx] = val;
        },
        setCurrentVal(val) {
            this.currentVal = val;
        }
    });
    Alpine.store('processing', {
        value: false,
        toggle() {
            this.value = !this.value;
        }
    });
});

function formBeforeSend(_, self) {
    // self.children.
    const textArea = document.getElementById('txtMessage');
    const text = textArea.value;
    Alpine.store('prompts').updateData(text, Alpine.store('prompts').data.length - 1);
    Alpine.store('prompts').pushData('');
    Alpine.store('processing').toggle();
    Alpine.store('prompts').setCurrentVal('');
    const scrollEl = document.getElementById('scroll-div');
    scrollEl.scrollTop = scrollEl.scrollHeight;
}
function beforeSwap(event, _) {
    // event.detail.serverResponse = event.detail.serverResponse.replaceAll('</script>', '<\\x3C/script\\x3E>');
}
function afterSwap(_, self) {
    Alpine.store('processing').toggle();
}

function keyDown(event, self) {
    if (event.key === 'Enter' && !Alpine.store('processing').value
        && event.currentTarget.value.trim() != ''
        && !event.shiftKey
    ) {
        event.preventDefault();
        self.dispatchEvent(new Event("chat_submit", { bubbles: true }));
    }
}

function submitBtnClick(event, self) {
    event.preventDefault();
    if (!Alpine.store('processing').value && Alpine.store('prompts').currentVal.trim() != '') {
        self.dispatchEvent(new Event("chat_submit", { bubbles: true }));
    }
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
    Alpine.store('processing').toggle();
}
