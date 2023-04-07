roomInput = document.querySelector('#room-name-input');
roomInput.focus();
roomInput.onkeyup = function(e) {
    if (e.keyCode === 13 && roomInput.value.trim()) {  // enter, return
        document.querySelector('#room-name-submit').click();
    }
};

document.querySelector('#room-name-submit').onclick = function(e) {
    var roomName = document.querySelector('#room-name-input').value;
    window.location.pathname = '/chat/' + roomName.trim() + '/';
};