document.getElementById("changePasswordForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    const response = await fetch("/change_password", {
        method: "POST",
        body: new FormData(this)
    });
    if (response.status === 403) {
        const data = await response.json();
        const detail = data.detail;
        alert(detail);
    }
    if (response.status === 404)
    {
        const data = await response.json();
        const detail = data.detail;
        alert(detail);
    }
    if (response.status === 400){
        const data = await response.json();
        const detail = data.detail;
        alert(detail);
    }
    if (response.status === 200) {
        window.location.href = "/";
    }
});