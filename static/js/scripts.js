function incrementValue(id, price) {
    var input = document.getElementById(id);
    var value = parseInt(input.value, 10);
    value = isNaN(value) ? 0 : value;
    if (value < parseInt(input.getAttribute('max'), 10)) {
        value++;
        input.value = value;
        updatePrice(id, price);
    }
}

function decrementValue(id, price) {
    var input = document.getElementById(id);
    var value = parseInt(input.value, 10);
    value = isNaN(value) ? 0 : value;
    if (value > parseInt(input.getAttribute('min'), 10)) {
        value--;
        input.value = value;
        updatePrice(id, price);
    }
}

function updatePrice(id, price) {
    var input = document.getElementById(id);
    var quantity = parseInt(input.value, 10);
    quantity = isNaN(quantity) ? 0 : quantity;
    var p = document.getElementById("p-" + id);
    p.innerText = (price * quantity).toFixed(2);
}