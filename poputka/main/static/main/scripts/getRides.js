const rideFrom = document.getElementById('inp-from').value;
const rideTo = document.getElementById('inp-to').value;
const rideDate = document.getElementById('form_date').value;
const ridePersons = document.getElementById('person_count').value;

const ridesList = document.getElementById('rides-list');

fetch('http://127.0.0.1:8000/api/v1/rides/?from=' + rideFrom + '&to=' + rideTo + '&date=' + rideDate + '&persons=' + ridePersons)
    .then(res => {
        if (res.ok) {
            return res.json();
        } else {
            throw Error
        }
    })
    .then(data => displayRides(data)
    ).catch(error => {
        console.log(error)
    })


function displayRides(rides) {
    const content = rides.map((list) => {
        if (list['driver']['avatar']) {
            driverAvatar = '<img src="' + list['driver']['avatar'] + '" id="ride-user-avatar" class="user-icon ride-user-icon" alt="user icon">'
        } else {
            driverAvatar = '<svg xmlns="http://www.w3.org/2000/svg" height="55" viewBox="0 -960 960 960" width="55"><path fill="white" d="M234-276q51-39 114-61.5T480-360q69 0 132 22.5T726-276q35-41 54.5-93T800-480q0-133-93.5-226.5T480-800q-133 0-226.5 93.5T160-480q0 59 19.5 111t54.5 93Zm246-164q-59 0-99.5-40.5T340-580q0-59 40.5-99.5T480-720q59 0 99.5 40.5T620-580q0 59-40.5 99.5T480-440Zm0 360q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q53 0 100-15.5t86-44.5q-39-29-86-44.5T480-280q-53 0-100 15.5T294-220q39 29 86 44.5T480-160Zm0-360q26 0 43-17t17-43q0-26-17-43t-43-17q-26 0-43 17t-17 43q0 26 17 43t43 17Zm0-60Zm0 360Z"/></svg>'
        }
        return '<div class="ride-box"><div class="ride-time">' + list['ride_time'] + '</div><div class="ride-info"><div class="ride-route">' + list['from_place'] + ' - ' + list['to_place'] + '</div><div class="ride-bottom"><div class="ride-user">' + driverAvatar + '<div>' +list['driver']['first_name'] + '<div class="ride-user-rating"><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path fill="white" d="m354-247 126-76 126 77-33-144 111-96-146-13-58-136-58 135-146 13 111 97-33 143ZM233-80l65-281L80-550l288-25 112-265 112 265 288 25-218 189 65 281-247-149L233-80Zm247-350Z"/></svg><span class="ride-user-rating-text">' + list['driver']['rating'] + '/5</span></div></div></div><div class="ride-seats">Мест: ' + list['driver']['rating'] + '</div></div></div><div class="ride-price">' + list['price'] + ' ₽</div></div>'
    })
    ridesList.innerHTML = content.join("")
}