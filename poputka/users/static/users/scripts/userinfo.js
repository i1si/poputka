function getAgeTitle(count) {
    function declination(number, titles) {
    cases = [2, 0, 1, 1, 1, 2];
    return titles[ (number%100>4 && number%100<20)? 2:cases[(number%10<5)?number%10:5] ];
    }
    title = declination(count, [' год', ' года', ' лет']);
    return count + title;
}

const urlParams = new URLSearchParams(window.location.search);
var uid = document.currentScript.getAttribute('uid');
var baseURL = document.location.origin

fetch(baseURL + '/api/v1/users/' + uid)
    .then(response => response.json())
    .then(data => {
        document.getElementById('profile-photo').src=data["avatar"];
        document.getElementById('profile-name').innerHTML=data["first_name"];
        if (data["age"]) {
            document.getElementById('profile-age').innerHTML=getAgeTitle(data["age"]);
        }
        document.getElementById('profile-ride-count').innerHTML="Поездок: " + data["ride_count"];
        if (data["rating"]) {
            document.getElementById('feedback-score').innerHTML=data["rating"] + '/5';
        }
        document.getElementById('profile-date-joined').innerHTML="Дата регистрации: " + data["date_joined"];
        document.getElementById('profile-box').classList.remove("hidden");
    })

fetch(baseURL + '/api/v1/feedbacks/?uid=' + uid)
    .then(response => response.json())
    .then(data => {
        document.getElementById('feedback-count').innerHTML='Отзывов: ' + data['rating_counts']['total'];
        document.getElementById('feedback-rating-5').innerHTML=data['rating_counts']['5'];
        document.getElementById('feedback-rating-4').innerHTML=data['rating_counts']['4'];
        document.getElementById('feedback-rating-3').innerHTML=data['rating_counts']['3'];
        document.getElementById('feedback-rating-2').innerHTML=data['rating_counts']['2'];
        document.getElementById('feedback-rating-1').innerHTML=data['rating_counts']['1'];
        const feedbacks = data['feedbacks'].map((list) => {
            avatar = list["author"]["avatar"];
            return '<div class="feedback-item"><a href="' + baseURL + list['author']['uri'] + '" class="feedback-item-top"><div class="text-white">' + list["author"]["first_name"] + '</div><div class="ride-user"><img src="' + avatar + '" alt="user-image" class="feedback-user-image"><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path fill="white" d="M504-480 320-664l56-56 240 240-240 240-56-56 184-184Z"/></svg></div></a><div class="feedback-item-mid"><div class="text-white">' + list["rating"] + '</div><div class="feedback-item-text">'+ list["text"] + '</div><div class="feedback-item-date">' + list["date"] + '</div></div></div>';
        })
        document.getElementById('feedback-holder').innerHTML=feedbacks.join('');
        document.getElementById('profile-box-feedback').classList.remove("hidden");
    })