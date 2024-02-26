const form = document.getElementById('offer-form');

function createRide(e) {
    if (form.checkValidity()) {
        e = e || window.event;
        e.preventDefault();

        document.getElementById('overlay').classList.remove('hidden')

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const from = document.getElementById('inp-from').value;
        const to = document.getElementById('inp-to').value;
        const datetime = document.getElementById('offer-datetime').value;
        const seats = document.getElementById('offer-seats').value;
        const price = document.getElementById('offer-price').value;
        const text = document.getElementById('offer-text').value;

        const formData = new FormData();
        formData.append('from_place', from);
        formData.append('to_place', to);
        formData.append('text', text);
        formData.append('ride_datetime', datetime);
        formData.append('seats_count', seats);
        formData.append('price', price);


        fetch(baseURL + '/api/v1/rides/', {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            body: formData,
            mode: "same-origin"
        })
            .then(res => {
                if (res.ok) {
                    return res.json();
                } else {
                    throw Error;
                }
            })
            .then(data => {
                window.location.replace(baseURL + '/rides/' + data['id'])
            })
    }
}