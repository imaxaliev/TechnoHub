export function addProductToCart(e) {
    const productId = e.currentTarget.dataset.productId
    const orderId = e.currentTarget.dataset.orderId

    const productAmount = document.querySelector(`#product${productId}Amount`)
    fetch(`/store/orders/${orderId}/add_to_cart/products/${productId}?productAmount=${productAmount.value}`)
        .then((res) => res.json())
        .then((data) => {
            if (data.productTitle) {
                const orderDetailWrap = document.querySelector('.cart-wrap__container')
                let orderDetail = document.querySelector('.container__order-detail')

                if (!orderDetail) {
                    orderDetailWrap.innerHTML = `
                        <h4 class="cart__product-total-amount">Cart</h4>
                        <ul class="container__order-detail">
                            <li class="order-detail__total-price">
                                <ul>
                                    <li>
                                        <h6>Total price:</h6>
                                    </li>
                                    <li id="cartTotalPrice"></li>
                                </ul>
                            </li>
                        </ul>
                        <div class="checkout-link">
                            <a
                                href="/store/orders/${orderId}/checkout/"
                            >
                                Go to checkout
                            </a>
                        </div>
                        <a
                            href="/store/orders/${orderId}/delete/"
                            class="deletion-link"
                        >
                            Decline order
                        </a>
                    `
                }

                const productTitle = data.productTitle.toUpperCase()[0] + data.productTitle.slice(1)
                const productHTML = `
                    <li>
                        <ul>
                            <li>
                                <h6>${productTitle}</h6>
                            </li>
                            <li id="cartProduct${productId}Amount">
                                ${'\u00A0'}x${data.productOrderAmount}
                            </li>
                            <li id="cartProduct${productId}Price">
                                =  ${data.productOrderPrice} RUB
                            </li>
                        </ul>
                    </li>
                `
                const parser = new DOMParser()
                const newItem = parser.parseFromString(productHTML, 'text/xml').querySelector('li')

                orderDetail = document.querySelector('.container__order-detail')
                orderDetail.insertBefore(
                    newItem, orderDetail.children[orderDetail.children.length - 1]
                )
            } else {
                // document.querySelector('.cart__product-total-amount')
                //     .textContent = `${data.cartProductsTotalAmount} product(s) in cart.`
                document.querySelector(`#cartProduct${productId}Amount`)
                    .textContent  = '\u00A0x' + data.productOrderAmount
                document.querySelector(`#cartProduct${productId}Price`)
                    .textContent = `=  ${data.productOrderPrice} RUB`
            }
            document.querySelector('#cartTotalPrice')
                .textContent = data.orderTotalPrice + ' RUB'

            if(data.productTotalAmount === 0) {
                document.querySelector(`#addProduct${productId}ToCart`)
                    .innerHTML = '<p>Out of stock.</p>'
            } else {
                 productAmount
                    .setAttribute('max', data.productTotalAmount)
                 productAmount
                    .value = 1
            }
        })
}

export const createReview = async (e) => {
    e.preventDefault()

    const modal = document.querySelector('#review-modal')
    const modalInst = M.Modal.getInstance(modal)

    const form = e.currentTarget
    const productId = e.currentTarget.dataset.productId

    const rqData = {}
    new FormData(form).forEach((value, key) => {
        rqData[key] = value
    })

    await fetch(`/store/product/${productId}/review/create`, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(rqData)
    })
        .then((res) => res.json())
        .then((data) => {
            if(data) {
                modalInst.close()
                modalInst.destroy()

                form.reset()

                modal.insertAdjacentHTML('afterend', `
                    <li class="review">
                        <ul class="review__container">
                            <li>
                                <ul class="review__details">
                                    <li class="review__author"><p>${data.user}</p></li>
                                    <li class="review__rate"><p>${data.rate}</p></li>
                                </ul>
                            </li>
                            <li class="review__text">
                                <p>${data.text}</p>
                            </li>
                        </ul>
                    </li>
                `)
            }
        })
}

export const toggleTabData = (e) => {
    const tabData = [...document.querySelector('.tab-data').childNodes]
        .filter((el) => el.nodeName !== '#text')
    let targetTab = null
        if (e.currentTarget.getAttribute('id') === 'show-review-list') {
        targetTab = document.querySelector('.review-list')
    } else if (e.currentTarget.getAttribute('id') === 'show-product-params') {
        targetTab = document.querySelector('.card__params-wrap')
    }

    targetTab.classList.add('active')
    tabData.splice(tabData.indexOf(targetTab), 1)

    for (const child of tabData) {
        if (child.classList.contains('active')) {
           child.classList.toggle('active')
        }
    }
}