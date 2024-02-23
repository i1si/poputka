var baseURL = document.location.origin
const autocompleteFrom = document.getElementById("autocomplete-from");
const inputFrom = document.getElementById("inp-from");
const autocompleteTo = document.getElementById("autocomplete-to");
const inputTo = document.getElementById("inp-to");

async function getCities(q) {
    let result = await fetch(baseURL + '/api/v1/cities/?q=' + q)
    return result.json();
}

inputFrom.onkeyup = async function() {
    let result = []
    let input = inputFrom.value;
    if(input.length) {
        result = await getCities(input);
    }
    displayFrom(result);
}

inputTo.onkeyup = async function() {
    let result = []
    let input = inputTo.value;
    if(input.length) {
        result = await getCities(input);
    }
    displayTo(result);
}

function displayFrom(result) {
    const content = result.map((list)=>{
        return "<li onclick=selectInputFrom(this)>" + list['name'] + "</li>";
    })
    autocompleteFrom.innerHTML = '<ul class="autocomplete-list">' + content.join("") + "</ul>";
}

function displayTo(result) {
    const content = result.map((list)=>{
        return "<li onclick=selectInputTo(this)>" + list['name'] + "</li>";
    })
    autocompleteTo.innerHTML = '<ul class="autocomplete-list">' + content.join("") + "</ul>";
}

function selectInputFrom(list) {
    inputFrom.value = list.innerHTML;
    autocompleteFrom.innerHTML = "";
}

function selectInputTo(list) {
    inputTo.value = list.innerHTML;
    autocompleteTo.innerHTML = "";
}