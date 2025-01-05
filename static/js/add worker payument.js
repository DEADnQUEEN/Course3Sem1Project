window.onload = () => {
    let key = document.getElementById('company-key');
    let click_info = document.getElementById('key-copied-message');
    let interval_copy;
    key.addEventListener(
        'click',
        () => {
            navigator.clipboard.writeText(key.textContent).then(r => {});
            click_info.setAttribute('style', 'opacity: 1;');
            if (interval_copy != null) {
                clearTimeout(interval_copy)
            }
            interval_copy = setTimeout(() => {click_info.removeAttribute('style');}, 3000)
        }
    )
}
