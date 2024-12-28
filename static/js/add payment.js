window.onload = () => {
    let d = new Date();
    document.getElementById('date').value = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDay() + 1).padStart(2, '0');
    let early = document.getElementById('early-payments')
    let values = document.querySelectorAll('.add-payment-block > label > input');

    let timeout = {}
    for (let i = 0; i < values.length; i++){
        timeout[values[i].id] = -1
        values[i].addEventListener(
            'input',
            (ev) => {
                if (values[i].value === '0'){
                    values[i].setCustomValidity('Недопустимое значение')
                }
                if (values[i].value.length > 1 && values[i].value[0] === '0'){
                    values[i].value = values[i].value.slice(1);
                }
            }
        )
    }

    let buttons = document.querySelectorAll('.buttons > *');

    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener(
            'click',
            () => {
                let data = {}

                for (let j = 0; j < values.length; j++){
                    if (!values[j].checkValidity()){
                        let error = document.getElementById(values[j].id + '-error');
                        if (!error.classList.contains('visible')){
                            error.classList.add('visible')
                        } else {
                            clearTimeout(timeout[values[j].id])
                        }
                        timeout[values[j].id] = setTimeout(() => {error.classList.remove('visible')}, 3000)
                        return;
                    }
                    data[values[j].id] = values[j].value;
                }

                data['amount'] = buttons[i].value + data['amount']

                let xhr = new XMLHttpRequest()

                xhr.open("POST", window.location.pathname)

                xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
                xhr.setRequestHeader('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]').value);

                xhr.onload = () => {
                    if (xhr.status === 200){
                        console.log(xhr.response)
                        return;
                    }
                    console.log('Error ' + xhr.status)
                }

                xhr.send(JSON.stringify(data));
            }
        )
    }
}
