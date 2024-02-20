function getAgeTitle(count) {
    function declination(number, titles) {
    cases = [2, 0, 1, 1, 1, 2];
    return titles[ (number%100>4 && number%100<20)? 2:cases[(number%10<5)?number%10:5] ];
    }
    title = declination(count, [' год', ' года', ' лет']);
    return count + title;
}

fetch('http://127.0.0.1:8000/api/v1/users/' + '1')
    .then(response => response.json())
    .then(data => {
        document.getElementById('profile-photo').src=data["avatar"];
        document.getElementById('profile-name').innerHTML=data["first_name"];
        document.getElementById('profile-age').innerHTML=getAgeTitle(data["age"]);
        document.getElementById('profile-ride-count').innerHTML="Поездок: " + data["ride_count"];
        document.getElementById('feedback-score').innerHTML=data["rating"] + '/5';
        document.getElementById('profile-date-joined').innerHTML="Дата регистрации: " + data["date_joined"];
        document.getElementById('profile-box').classList.remove("hidden");
    })

fetch('http://127.0.0.1:8000/api/v1/feedbacks/?uid=' + '1')
    .then(response => response.json())
    .then(data => {
        document.getElementById('feedback-count').innerHTML='Отзывов: ' + data['rating_counts']['total'];
        document.getElementById('feedback-rating-5').innerHTML=data['rating_counts']['5'];
        document.getElementById('feedback-rating-4').innerHTML=data['rating_counts']['4'];
        document.getElementById('feedback-rating-3').innerHTML=data['rating_counts']['3'];
        document.getElementById('feedback-rating-2').innerHTML=data['rating_counts']['2'];
        document.getElementById('feedback-rating-1').innerHTML=data['rating_counts']['1'];
        const feedbacks = data['feedbacks'].map((list) => {
            if (list["author"]["avatar"]) {
                avatar = '<img src="' + list["author"]["avatar"] + '" alt="user-image" class="feedback-user-image">';
            } else {
    			avatar = '<svg xmlns="http://www.w3.org/2000/svg" height="45" viewBox="0 -960 960 960" width="45"><path fill="white" d="M234-276q51-39 114-61.5T480-360q69 0 132 22.5T726-276q35-41 54.5-93T800-480q0-133-93.5-226.5T480-800q-133 0-226.5 93.5T160-480q0 59 19.5 111t54.5 93Zm246-164q-59 0-99.5-40.5T340-580q0-59 40.5-99.5T480-720q59 0 99.5 40.5T620-580q0 59-40.5 99.5T480-440Zm0 360q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q53 0 100-15.5t86-44.5q-39-29-86-44.5T480-280q-53 0-100 15.5T294-220q39 29 86 44.5T480-160Zm0-360q26 0 43-17t17-43q0-26-17-43t-43-17q-26 0-43 17t-17 43q0 26 17 43t43 17Zm0-60Zm0 360Z"/></svg>';
            }
            return '<div class="feedback-item"><div class="feedback-item-top"><div class="text-white">' + list["author"]["first_name"] + '</div><div class="ride-user">' + avatar + '<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path fill="white" d="M504-480 320-664l56-56 240 240-240 240-56-56 184-184Z"/></svg></div></div><div class="feedback-item-mid"><div class="text-white">' + list["rating"] + '</div><div class="feedback-item-text">'+ list["text"] + '</div><div class="feedback-item-date">' + list["date"] + '</div></div></div>';
        })
        document.getElementById('feedback-holder').innerHTML=feedbacks.join('');
        document.getElementById('profile-box-feedback').classList.remove("hidden");
    })