let btn = document.getElementById('cancel-button');
let confirm = document.getElementById('confirm-cancel');
let button = document.getElementById('confirm-button');
let cancel = document.getElementById('cancel');


btn.onclick = function() {
    confirm.style.display = 'block';
    btn.style.display = 'none';
};

window.onclick = function (event) {
    if (event.target == button) {
        button.style.display = "none";
    }
    if (event.target == cancel) {
        btn.style.display = 'block';
        confirm.style.display = 'none';
    }
}

