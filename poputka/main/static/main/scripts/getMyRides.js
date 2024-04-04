var baseURL = document.location.origin
const uid = document.currentScript.getAttribute('uid');

fetch(baseURL + '/api/v1/rides/?uid=' + uid )
    .then(res => res.json())
    .then(data => {
        displayRides(data)
    })

function displayRides(rides) {
    var ridesList = document.getElementById('ride-list')
    if (rides.length) {
        const content = rides.map((list) => {
            rideUrl = baseURL + '/rides/' + list['id']
            rideDate = getDatetimeStr(list['ride_datetime'])
            rideFrom = list['from_place']
            rideTo = list['to_place']
            if (uid == list['driver']['id']){
                rideDriver = 'Вы'
            } else{
                rideDriver = list['driver']['first_name']
            }
			return '<li><a href="' + rideUrl + '" class="myride flex-center"><div>' + rideDate + '</div><div>' + rideFrom + ' - ' + rideTo + '</div><div>' + rideDriver + '</div></a></li>'
        })
        ridesList.innerHTML = content.join('')
    } else {
        ridesList.innerHTML = 'Поездок пока что нет'
    }
}

function getDatetimeStr(datetime) {
    const date = new Date(datetime);
    var day = date.getDate();
    var month = date.getMonth();
    var year = date.getFullYear();
    return [day, month, year].join('.')
}