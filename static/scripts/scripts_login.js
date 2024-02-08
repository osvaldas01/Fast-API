document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    const response = await fetch("/login_form", {
        method: "POST",
        body: new FormData(this)
    });
    if (response.status === 403) {
        const data = await response.json();
        const detail = data.detail;
        alert(detail);
    }
    if (response.status === 200) {
        window.location.href = "/";
    }
});