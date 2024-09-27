function loginRedirect() {
    if (document.getElementById('error').innerText == '') {
        document.location.href = document.location.href.replace('/login', '')
    }
}

function pwdKeyDown(event, self) {
    if (event.key === 'Enter' && self.value.trim() != '') {
        event.preventDefault();
        self.dispatchEvent(new Event('login', { bubbles: true }));
    }
}

function loginButtonClick(event, self) {
    event.preventDefault();
    self.dispatchEvent(new Event('login', { bubbles: true }));
}

function disableForm() {
    document.getElementById('loginForm').disabled = true;
    document.getElementById('loginBtn').disabled = true;
    document.getElementById('loginBtn').classList.toggle('cursor-not-allowed');
    document.getElementById('loginBtn').classList.toggle('animate-pulse');
}
function enableForm() {
    document.getElementById('loginForm').disabled = false;
    document.getElementById('loginBtn').disabled = false;
    document.getElementById('loginBtn').classList.toggle('cursor-not-allowed');
    document.getElementById('loginBtn').classList.toggle('animate-pulse');
}