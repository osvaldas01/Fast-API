async function buyCredits(event) {
    let form = event.target;
    let formData = new FormData(form);
    let url = form.action;
    let request = new Request(url, {
        method: 'POST',
        body: formData
    });
    try {
        const response = await fetch(request);
        if (response.status === 200) {
            const data = await response.json();
            console.log(data.message);
        }
        location.reload();
    } catch (error) {
        console.log(error);
    }
}
async function buyPackage(event) {
    let form = event.target;
    let formData = new FormData(form);
    let packageId = formData.get('package_id');
    let buyButton = document.getElementById('buyButton');
    let url = `/store/${packageId}`;
    let request = new Request(url, {
        method: 'POST',
        body: formData
    });
    try {
        const response = await fetch(request);
        if (response.status === 403) {
            alert("You don't have enough credits.");
        } else {
            const data = await response.json();
            console.log(data);
            if (data.message == "Package bought successfully") {
                buyButton.remove();
                let p = document.createElement('p');
                p.innerText = "Already Owned";
                form.appendChild(p);
            }
            location.reload(); // Refresh the page
        }
    } catch (error) {
        console.log(error);
    }
}