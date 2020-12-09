export function orderConfirmation(e) {
    const orderId = e.currentTarget.dataset.orderId

    document.querySelector('.order-info__form')
        .addEventListener('submit', (e) => {
            e.preventDefault()
            const paymentMethod = document.querySelector('#id_payment_method').value
            fetch(`/store/orders/${orderId}/checkout/`, {
                    method: 'post',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: new FormData(e.currentTarget)
            })
            switch(paymentMethod) {
                case 'On receipt': {
                    location.href = `/store/orders/${orderId}/checkout/succeeded?status=in_process`
                    return
                }
                case 'Qiwi wallet': {
                    fetch(`/store/orders/${orderId}/checkout/get_qiwi_secret/`,{
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                        .then((res) => res.json())
                        .then((data) => {
                            const successUrl = data.successUrl
                            fetch(`https://cors-anywhere.herokuapp.com/
                                https://api.qiwi.com/partner/bill/v1/bills/${orderId}/`,
                                {
                                    method: 'put',
                                    headers: {
                                        'Authorization': `Bearer ${data.secretKey}`,
                                        'Accept': 'application/json',
                                        'Content-Type': 'application/json',
                                    },
                                    body: JSON.stringify({
                                        "amount": {
                                            "currency": "RUB",
                                            "value": data.totalPrice
                                        },
                                        "expirationDateTime": data.expirationDateTime
                                    })
                            })
                                .then((res) => res.json())
                                .then((data) => {
                                    location.href = data.payUrl + `?successUrl=${successUrl}`
                                })
                        })
                    break
                }
                case 'Bank Transaction': {
                    const stripe = document.createElement('script')
                    stripe.setAttribute('src', 'https://js.stripe.com/v3/')
                    document.body.appendChild(stripe)

                    fetch(`/store/stripe_conf/`)
                        .then((res) => res.json())
                        .then((data) => {
                            const stripe = Stripe(data.publicKey);
                            fetch(`/store/orders/${orderId}/checkout/create_checkout_session/`)
                                .then((res) => res.json())
                                .then((data) => {
                                    if (data.error) {
                                        return data.error
                                    }
                                    return stripe.redirectToCheckout({sessionId: data.session_id})
                                })
                                .then((res) => {
                                    console.log(res)
                                }, (e) => {
                                    console.log(e.message)
                                })
                        })
                }
            }
        })
}
