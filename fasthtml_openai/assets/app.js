document.addEventListener('alpine:init', () => {
    Alpine.plugin(focus);
    const length = document.getElementsByName('user').length;
    const data = Array.from({ length }).map(el => "");
    Alpine.store('prompts', {
        data,
        currentVal: '',
        processsing: false,
        pushData(val) {
            this.data.push(val);
        },
        updateData(idx, val) {
            this.data[idx] = val;
        },
        setCurrentVal(val) {
            this.currentVal = val;
        },
        completeProcessing() {
            this.processing = false;
        },
        toggleProcessing() {
            this.processing = !this.processing;
        }
    });
    Alpine.store('showSessions', {
        value: false,
        toggle() {
            this.value = !this.value;
        }
    });
    Alpine.store('errors', {
        value: [],
        nextId: 1,
        remove(errorId) {
            if (!document.startViewTransition) {
                this.value = this.value.filter(el => el.id != errorId);
            }
            else {
                document.startViewTransition(async () => {
                    this.value = this.value.filter(el => el.id != errorId);
                });
            }
        }
    });
});

function afterTitleEditSwap(_, self) {
    if (self.children[0].children[0].nodeName === 'INPUT') {
        const input = self.children[0].children[0];
        input.focus();
        input.setSelectionRange(input.value.length, input.value.length);
    }
    self._x_dataStack[0].processing = false;
}
function goToSession(event, self) {
    event.preventDefault();
    Alpine.store('showSessions').toggle();
    setTimeout(() => {
        document.location.href = self.href;
    }, 400);
}
function addChatClick(event, self) {
    event.preventDefault();
    if (!self._x_dataStack[0].processing) {
        self._x_dataStack[0].processing = true;
        self.dispatchEvent(new Event("chat_new"));
    }
}
function afterSwap(event, self) {
    if (event.detail.elt == document.getElementById('sessionId')
        && Alpine.store('showSessions').value
    ) {
        const els = document.getElementsByClassName("sessionLink");
        if (els.length > 0) {
            const href = els[els.length - 1].children[0].href
            goToSession(event, { href })
        }
    }
    else {
        Alpine.store('prompts').completeProcessing();
    }
}
function addNewChatError(_, self) {
    if (!document.startViewTransition) {
        Alpine.store('errors').value.push({ id: Alpine.store('errors').nextId, msg: 'Error creating new chat. Please try again later' });
        Alpine.store('errors').nextId = Alpine.store('errors').nextId + 1;
    }
    else {
        document.startViewTransition(() => {
            Alpine.store('errors').value.push({ id: Alpine.store('errors').nextId, msg: 'Error creating new chat. Please try again later' });
            Alpine.store('errors').nextId = Alpine.store('errors').nextId + 1;
        });
    }
    self._x_dataStack[0].processing = false;
}
function keyDown(event, self) {
    if (Alpine.store('showSessions').value) {
        event.preventDefault();
    }
    else {
        if (event.key === 'Enter' && !Alpine.store('prompts').processing
            && event.currentTarget.value.trim() != ''
            && !event.shiftKey
        ) {
            event.preventDefault();
            self.dispatchEvent(new Event("chat_submit", { bubbles: true }));
        }
    }
}
function submitBtnClick(event, self) {
    event.preventDefault();
    if (!Alpine.store('showSessions').value &&
        !Alpine.store('prompts').processing && Alpine.store('prompts').currentVal.trim() != '') {
        self.dispatchEvent(new Event("chat_submit", { bubbles: true }));
    }
}
function formBeforeSend(_, __) {
    Alpine.store('prompts').updateData(Alpine.store('prompts').data.length - 1, Alpine.store('prompts').currentVal);
    Alpine.store('prompts').pushData('');
    Alpine.store('prompts').toggleProcessing();
    Alpine.store('prompts').setCurrentVal('');
    const scrollEl = document.getElementById('scroll-div');
    scrollEl.scrollTop = scrollEl.scrollHeight;
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
    Alpine.store('prompts').toggleProcessing();
}