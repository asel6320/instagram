async function makeRequest(url, method = "GET") {
    let csrfToken = await getCookie('csrftoken')
    let headers = {}
    if (method !== "GET") {
        headers['X-CSRFToken'] = csrfToken
    }
    let response = await fetch(url,
        {
            "method": method,
            "headers": headers,
        }
    );
    if (response.ok) {
        return await response.json();
    } else {
        let error = new Error(response.text);
        console.log(error);
        throw error;
    }
}

async function onClick(event) {
    event.preventDefault();
    let a = event.currentTarget;
    let url = a.href;
    let icon = a.querySelector('i');
    let isLiked = icon.classList.contains('bi-heart-fill');
    let method = isLiked ? "DELETE" : "POST";

    let response = await makeRequest(url, method);

    // Toggle the icon class
    if (isLiked) {
        icon.classList.remove('bi-heart-fill');
        icon.classList.add('bi-heart');
    } else {
        icon.classList.remove('bi-heart');
        icon.classList.add('bi-heart-fill');
    }

    // Update like count
    let span = a.parentElement.querySelector("#like-count");
    span.innerText = response.like_count;
}

function onLoad() {
    let links = document.querySelectorAll('[data-like="like"]');
    for (let link of links) {
        link.addEventListener("click", onClick);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.addEventListener("load", onLoad);