import * as NavBar from './navbar.js'
import * as Product from './product.js'
import * as Order from './order.js'


document.addEventListener('DOMContentLoaded', () => {
    if (location.href.match('/store')) {
        document.querySelectorAll('.cart-toggle')
            .forEach((el) => {
               el.addEventListener('click', NavBar.toggleCart)
            })
        document.querySelector('.nav__search-form')
            .addEventListener('submit', NavBar.findPath)

        if (location.href.match('/category/.+')) {
            try {
                document.querySelectorAll('.add-to-cart__btn')
                    .forEach((el) => {
                        el.addEventListener('click', Product.addProductToCart)
                    })
                const tabData = document.querySelectorAll('.toggle-tab-data')
                    if (tabData.length) {
                        tabData.forEach((el) => {
                            el.addEventListener('click', Product.toggleTabData)
                        })
                    }

                const reviewForm = document.querySelector('.review-form')
                    if (reviewForm) {
                        reviewForm.addEventListener('submit', Product.createReview)
                    }

               const modals = document.querySelectorAll('.modal')
                    if (modals.length) {
                        M.Modal.init(modals)
                    }

            } catch(e) {
                //if (!e instanceof TypeError) {
                    console.log(e.message)
                //}
            }

        } else if (location.href.match('/checkout/$')) {
            document.querySelector('.checkout-form__submit')
                .addEventListener('click', Order.orderConfirmation)
        }
    }
})