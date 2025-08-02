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
    // Send a POST request to add the product to the cart
    fetch(`/add_to_cart/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ productId: productId })  // Send product ID as JSON data
    })
    .then(response => response.json())  // Parse the response JSON
    .then(data => {
        if (data.success) {
            showMessage('Item added to cart successfully!');  // Show success message
        } else {
            alert('Something went wrong. Please try again.');  // Show error message
        }
    });
}

// Function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;

    // Check if document.cookie is not empty
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        // Loop through cookies to find the required one
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            // If the cookie starts with the name, extract its value
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

// Script to handle the subscription form submission
document.getElementById('subscriptionForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission

    // Get the email value from the input field
    var email = document.getElementById('emailSubscription').value;

    // Send a POST request to subscribe with the email
    fetch('/subscribe/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: 'emailSubscription=' + encodeURIComponent(email)  // Send the email as URL-encoded data
    })
    .then(response => response.text())  // Parse the response text
    .then(data => {
        alert(data);  // Show the response as an alert
        window.location.href = '/';  // Redirect to the home page
    });
});








