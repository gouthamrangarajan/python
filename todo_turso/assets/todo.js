function textKeyDown(event, self) {
    if (event.key === 'Enter' && self.value.trim() != '') {
        self.dispatchEvent(new Event('add_submit'));
        self.value = '';
    }
}

function removeBtnClick(_, self) {
    self.parentElement.style.viewTransitionName = 'list';
    self.dispatchEvent(new Event('remove_submit'));
}