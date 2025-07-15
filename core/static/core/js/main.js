 function autoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');
            alert.classList.add('fade');
            // Remove the alert from the DOM after fading out
            setTimeout(() => {
                alert.remove();
            }, 150); // Wait for the fade effect to complete before removing
        }, 5000); // 5000 milliseconds = 5 seconds
    });
}

// Call the function when the document is ready
document.addEventListener('DOMContentLoaded', autoDismissAlerts);