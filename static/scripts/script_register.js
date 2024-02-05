document.getElementById("registerForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    const response = await fetch("/register", {
        method: "POST",
        body: new FormData(this)
    });
    if (response.status === 400) {
        const data = await response.json();
        const detail = data.detail;
        alert(detail);
    }
    if (response.status === 422) {
        const data = await response.json();
        const detail = data.detail;
        alert("Invalid email address!");
    }
    if (response.status === 200) {
        window.location.href = "/login";
    }
});