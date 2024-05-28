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


const changeRating = () => {
    const cards = document.querySelectorAll('article');
    for (const card of cards) {
        const likeButton = card.querySelector('#vote-up-button');
        const dislikeButton = card.querySelector('#vote-down-button');
        const ratingDisplay = card.querySelector('#rating');
        const cardId = card.dataset.cardId;
        const cardType = card.dataset.cardType;
        const baseUrl = window.location.origin;

        [likeButton, dislikeButton].forEach((button) => {
            button.addEventListener('click', () => {
                let rating = 0;
                (button === likeButton) ? rating = 1 : rating = -1;
                const request = new Request(`${baseUrl}/${cardId}/change_rating`, {
                    method: 'post',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'new_rating': rating,
                        'card_type': cardType
                    }),
                    mode: 'same-origin'
                });
                fetch(request)
                    .then((response) => response.json())
                    .then((data) => {
                        ratingDisplay.innerHTML = `Rating: ${data['rating']}`
                    })
            });
        });
    }
}

changeRating();