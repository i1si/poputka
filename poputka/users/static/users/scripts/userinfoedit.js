document.getElementById('avatar-input').addEventListener('change', event => {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('avatar', file);

    fetch('http://127.0.0.1:8000/api/v1/users/' + uid + '/', {
        method: "PATCH",
        body: formData,
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('profile-photo').src=data["avatar"];
    })
})

function saveUserInfo() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const userName = document.getElementById('profile-name').value;
    const userBirthday = document.getElementById('profile-age').value;
    const formData = new FormData();
    formData.append('first_name', userName);
    formData.append('birthday', userBirthday);

    fetch('http://127.0.0.1:8000/api/v1/users/' + uid + '/', {
        method: "PATCH",
        body: formData,
        headers: {'X-CSRFToken': csrfToken},
        mode: "same-origin"
    })
}

function getAgeTitle(count) {
    function declination(number, titles) {
    cases = [2, 0, 1, 1, 1, 2];
    return titles[ (number%100>4 && number%100<20)? 2:cases[(number%10<5)?number%10:5] ];
    }
    title = declination(count, [' год', ' года', ' лет']);
    return count + title;
}

let uid = document.currentScript.getAttribute('uid');
fetch('http://127.0.0.1:8000/api/v1/users/' + uid)
    .then(response => response.json())
    .then(data => {
        document.getElementById('profile-photo').src=data["avatar"];
        document.getElementById('profile-name').value=data["first_name"];
        document.getElementById('profile-age').value=data["birthday"]
        if (data["age"]) {
            document.getElementById('profile-age').innerHTML=getAgeTitle(data["age"]);
        } else {
            document.getElementById('profile-age').innerHTML='age - todo'
        }

        document.getElementById('profile-box').classList.remove("hidden");
    })
