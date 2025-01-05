window.onload = () => {
    fill_dates()
    let early = document.querySelector('#early-payments')

    for (let i = 0; i < early.children.length; i++){
        early.children[i].addEventListener(
            'click',
            (ev) => {
                ev.preventDefault()
                document.getElementById('amount').value = early.children[i].textContent
            }
        )
    }

    let values = document.querySelectorAll('.add-payment-block > label > input');

    let timeout = {}
    for (let i = 0; i < values.length; i++){
        timeout[values[i].id] = -1
        values[i].addEventListener(
            'input',
            () => {
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
                        let data = JSON.parse(xhr.response)
                        early.innerHTML = ''

                        for (let j = 0; j < data['payments'].length; j++) {
                            let pay = document.createElement('a')
                            pay.classList.add('payment-block')
                            pay.textContent = data['payments'][j]['amount_value']
                            early.appendChild(pay)
                        }
                        return;
                    }
                    console.log('Error ' + xhr.status)
                }

                xhr.send(JSON.stringify(data));
            }
        )
    }
}
