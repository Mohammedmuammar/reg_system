function activateSearchbox(el) {
    el.classList.add('searchbox--active');
}

function deactivateSearchbox(el) {
    el.classList.remove('searchbox--active');
}

function onFocus() {
    activateSearchbox(document.querySelector('.searchbox'));
}

function onBlur() {
    deactivateSearchbox(document.querySelector('.searchbox'));
}

function onClick(event) {
    event.stopPropagation();
}
