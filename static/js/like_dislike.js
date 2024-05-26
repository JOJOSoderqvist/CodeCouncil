const likeDislike = () => {
    const questions = document.querySelectorAll('article');
    console.log(questions);
    for (const question of questions) {
        const likeButton = question.querySelector('#vote-up-button');
        const dislikeButton = question.querySelector('#vote-down-button');
        const currentRating = question.querySelector('#rating');
        const questionId = question.dataset.questionId;
        console.log(question, likeButton, dislikeButton, currentRating, questionId)

        // likeButton.addEventListener('click', () => {
        //     const request = new Request(`${}`)
        // })
    }
}

likeDislike()