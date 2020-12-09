export function toggleCart() {
   document.querySelector('.content-wrap__cart')
       .classList.toggle('cart_visible')
}

export function findPath() {
    const form = event.currentTarget
    event.preventDefault()
    fetch(`/store/find_path?q=${form.querySelector('input#q').value}`, {
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.error) {
                alert(data.error)
            } else {
                location.href = data.url
            }

        })
}

// function toggleMenu() {
//     document.querySelector('.toggle-sidebar-btn')
//         .addEventListener('click', (e) => {
//             e.preventDefault()
//             document.querySelector('.sidebar')
//                 .classList.toggle('.expanded')
//         })
// }