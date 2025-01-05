window.onload = () => {
    fill_dates()

    let amounts = document.querySelectorAll('.amount')
    for (let i = 0; i < amounts.length; i++){
        amounts[i].addEventListener(
            'input',
            () => {
                if (amounts[i].value === '0'){
                    amounts[i].setCustomValidity('Недопустимое значение')
                }
                if (amounts[i].value.length > 1 && amounts[i].value[0] === '0'){
                    amounts[i].value = amounts[i].value.slice(1);
                }
            }
        )
    }

    let obj = document.getElementById('company-key');
    obj.addEventListener(
        'click',
        () => {
            timer(
                obj,
                () => {
                        navigator.clipboard.writeText(obj.textContent).then(r => {
                        document.getElementById(obj.id + '-message').setAttribute('style', 'opacity: 1;');
                    });
                },
            () => {
                    document.getElementById(obj.id + '-message').removeAttribute('style')
                }
            )
        }
    )

    obj = document.getElementById('refresh-code');
    obj.addEventListener(
        'click',
        () => {
            let xhr = new XMLHttpRequest()

            xhr.open("POST", window.location.pathname + 'refresh-code/')

            xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
            xhr.setRequestHeader('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]').value);

            xhr.onload = () => {
                if (xhr.status === 200) {
                    let data = JSON.parse(xhr.response)
                    document.getElementById('company-key').textContent = data['key']
                    timer(
                        obj,
                        () => {
                            document.getElementById(obj.id + '-message').setAttribute('style', 'opacity: 1;');
                        },
                        () => {
                            document.getElementById(obj.id + '-message').removeAttribute('style')
                        }
                    )
                    return;
                }
                console.log('Error ' + xhr.status)
            }

            xhr.send();
        }
    )

    let buttons_div = document.querySelectorAll('.buttons')

    for (let i = 0; i < buttons_div.length; i++) {
        let buttons = buttons_div[i].children;
        for (let j = 0; j < buttons.length; j++) {
            buttons[j].addEventListener(
                'click',
                () => {
                    let data = {
                        'index': i,
                        'payment': {}
                    }

                    let inputs = document.querySelectorAll('input[id*="worker-' + i + '-"]')
                    for (let k = 0; k < inputs.length; k++) {
                        if (!inputs[k].checkValidity()){
                            timer(
                                inputs[k],
                                () => {
                                    inputs[k].setAttribute('style', 'border-color: var(--decline));');
                                },
                                () => {
                                    inputs[k].removeAttribute('style')
                                }
                            )
                            return
                        }
                        data['payment'][inputs[k].id.slice(('worker-' + i + '-').length)] = inputs[k].value
                    }

                    data['payment']['amount'] = buttons[j].value + data['payment']['amount']

                    console.log(data)

                    let xhr = new XMLHttpRequest()

                    xhr.open("POST", window.location.pathname)

                    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
                    xhr.setRequestHeader('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]').value);

                    xhr.onload = () => {
                        if (xhr.status === 200) {
                            let message = document.querySelector('#' + buttons[j].id + '-message');
                            timer(
                                buttons[j],
                                () => {
                                    message.setAttribute('style', 'opacity: 1;');
                                },
                                () => {
                                    message.removeAttribute('style')
                                }
                            )
                            return;
                        }
                        console.log('Error ' + xhr.status)
                    }

                    xhr.send(JSON.stringify(data));
                }
            );
        }
    }
}
