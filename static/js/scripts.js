// JavaScript to handle the active class
document.addEventListener('DOMContentLoaded', function() {
    // Get the current path of the window
    var currentPath = window.location.pathname;

    // Get the navigation link elements by their IDs
    var homeLink = document.getElementById('home-link');
    var seedsSuppliesLink = document.getElementById('seeds-supplies-link');
    var articlesLink = document.getElementById('articles-link');
    var contactLink = document.getElementById('contact-link');

    // Add 'active' class to the current active link based on the path
    if (currentPath === '/') {
        homeLink.classList.add('active');
    } else if (currentPath.startsWith('/store/products/')) {
        seedsSuppliesLink.classList.add('active');
    } else if (currentPath === '/articles/' || currentPath.startsWith('/articles/')) {
        articlesLink.classList.add('active');
    } else if (currentPath === '/contact/' || currentPath.startsWith('/contact')) {
        contactLink.classList.add('active');
    }
});

// Script to update the year in the footer
document.addEventListener('DOMContentLoaded', function() {
    // Get the current year
    var currentYear = new Date().getFullYear();
    
    // Set the current year in the element with id 'currentYear'
    document.getElementById('currentYear').textContent = currentYear;
});

// Function to handle adding products to the cart
function addToCart(productId) {

    fetch(`/add_to_cart/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ productId: productId }) 
    })
    .then(response => response.json())  
    .then(data => {
        if (data.success) {
            showMessage('Item added to cart successfully!');  
        } else {
            alert('Something went wrong. Please try again.');  
        }
    });
}
