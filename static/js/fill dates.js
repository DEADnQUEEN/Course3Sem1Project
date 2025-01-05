function fill_dates() {
    let d = new Date();
    let date = document.querySelectorAll('input[type=date]')
    for (let i = 0; i < date.length; i++) {
        date[i].value = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
    }
}