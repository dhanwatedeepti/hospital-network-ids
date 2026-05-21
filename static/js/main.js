// console.log("App Loaded");

// Simple alert popup for flash messages
window.onload = function() {
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(alert => {
        alert.style.position = "fixed";
        alert.style.top = "20px";
        alert.style.right = "20px";
        alert.style.zIndex = "9999";

        setTimeout(() => {
            alert.remove();
            // alert.style.display = "none";
        }, 3000);
    });
};