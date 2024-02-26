function getDatetimeStr(datetime) {
	const date = new Date(datetime)
	const options = {
		weekday: 'short',
		month: 'long',
		day: 'numeric',
		hour: 'numeric',
		minute: 'numeric'
	}
	return date.toLocaleDateString("ru-RU", options);
}

const baseURL = document.location.origin
const rid = document.currentScript.getAttribute('rid');
const did = document.currentScript.getAttribute('did');

fetch(baseURL + '/api/v1/rides/' + rid + '/')
	.then(res => {
		if (res.ok){
			return res.json();
		}
		else {
			throw Error
		}
	})
	.then(data => {
		document.getElementById('ride-date').innerHTML=getDatetimeStr(data['ride_datetime']);
		document.getElementById('ride-dists-from').innerHTML=data['from_place'];
		document.getElementById('ride-dists-to').innerHTML=data['to_place'];
		document.getElementById('ride-total').innerHTML=data['price'] + ' ₽';
		document.getElementById('ride-driver-name').innerHTML=data['driver']['first_name'];
		document.getElementById('ride-drier-rating').innerHTML=data['driver']['rating'] + '/5';
		document.getElementById('ride-driver-image').src=data['driver']['avatar'];
		document.getElementById('ride-text').innerHTML=data['text'];
		if (rid == did) {
			document.getElementById('ride-contact-text').innerHTML='Связаться с ' + data['driver']['first_name'];
		}
	})