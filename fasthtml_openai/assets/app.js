document.body.addEventListener('htmx:load', function (evt) {

});
document.addEventListener('alpine:init', () => {
    Alpine.plugin(focus);
    const length = document.getElementsByName('user').length;
    const data = Array.from({ length }).map(el => "");
    Alpine.store('prompts', {
        data,
        currentVal: '',
        pushData(val) {
            this.data.push(val);
        },
        updateData(idx, val) {
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
        },
        complete() {
            this.value = false;
        }
    });
    Alpine.store('showSessions', {
        value: false,
        toggle() {
            this.value = !this.value;
        }
    })
});

function formBeforeSend(_, __) {
    Alpine.store('prompts').updateData(Alpine.store('prompts').data.length - 1, Alpine.store('prompts').currentVal);
    Alpine.store('prompts').pushData('');
    Alpine.store('processing').toggle();
    Alpine.store('prompts').setCurrentVal('');
    const scrollEl = document.getElementById('scroll-div');
    scrollEl.scrollTop = scrollEl.scrollHeight;
}
function beforeSwap(_, __) {
    // console.log("enter");
    // event.detail.serverResponse = event.detail.serverResponse.replaceAll('</script>', '<\\x3C/script\\x3E>');
}
function afterSwap(event, self) {
    Alpine.store('processing').complete();
    if (event.detail.elt == document.getElementById('sessionId')) {
        const els = document.getElementsByClassName("sessionLink");
        if (els.length > 0) {
            const href = els[els.length - 1].children[0].href
            menuCloseClick(event, self);
            setTimeout(() => {
                if (!document.startViewTransition) {
                    document.location.href = href;
                }
                else {
                    document.startViewTransition(() => document.location.href = href);
                }
            }, 400);
        }
    }
}
function goToSession(event, self) {
    event.preventDefault();
    menuCloseClick(event, self);
    setTimeout(() => {
        if (!document.startViewTransition) {
            document.location.href = self.href;
        }
        else {
            document.startViewTransition(() => document.location.href = self.href);
        }
    }, 400);
}

function keyDown(event, self) {
    if (Alpine.store('showSessions').value) {
        event.preventDefault();
    }
    else {
        if (event.key === 'Enter' && !Alpine.store('processing').value
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
        !Alpine.store('processing').value && Alpine.store('prompts').currentVal.trim() != '') {
        self.dispatchEvent(new Event("chat_submit", { bubbles: true }));
    }
}

function menuOpenClick(event, _) {
    event.preventDefault();
    document.getElementById('menuContainer').classList.toggle('animate-slide-right');
    document.getElementById('menuContainer').classList.toggle('animate-slide-right-opp');
    Alpine.store('showSessions').toggle();
}
function menuCloseClick(event, _) {
    event.preventDefault();
    document.getElementById('menuContainer').classList.toggle('animate-slide-right');
    document.getElementById('menuContainer').classList.toggle('animate-slide-right-opp');
    setTimeout(() => {
        Alpine.store('showSessions').toggle();
    }, 300);
}
function addChatClick(event, self) {
    event.preventDefault();
    if (!Alpine.store('processing').value) {
        Alpine.store('processing').toggle();
        self.dispatchEvent(new Event("chat_new"));
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
