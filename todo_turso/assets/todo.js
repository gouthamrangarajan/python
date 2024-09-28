function textKeyDown(event, self) {
    if (event.key === 'Enter' && self.value.trim() != '') {
        self.dispatchEvent(new Event('add_submit'));
        self.value = '';
        self.classList.toggle('animate-pulse');
    }
}

function addItemRequestCompleted(self) {
    self.classList.toggle('animate-pulse');
}

function removeBtnClick(_, self) {
    let listElement = self.parentElement;
    //below code causes console error during slow network and fast remove buttons click
    // listElement.style.viewTransitionName = 'list'; 
    self.style.opacity = 0;
    let label = listElement.children[0];
    let checkbox = listElement.children[0].children[0];
    label.classList.toggle('animate-pulse');
    checkbox.disabled = true;
    checkbox.classList.toggle('cursor-not-allowed');
    self.dispatchEvent(new Event('remove_submit'));
}

function completeItemRequestInProgress(self) {
    self.parentElement.classList.toggle('animate-pulse');
}

function completeItemRequestCompleted(self) {
    self.parentElement.classList.toggle('animate-pulse');
}
