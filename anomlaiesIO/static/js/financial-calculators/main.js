
/* Beautify form-input fields */
$('input.number-input').on('blur', function() {
  const value = this.value.replace(/,/g, '');
  this.value = parseFloat(value).toLocaleString('en-US', {
    style: 'decimal',
    maximumFractionDigits: 0,
    minimumFractionDigits: 0
  });
});

$('input.percentage-input').on('blur', function() {
  let value = this.value.replace(/,/g, '');
  value = value/100;
  this.value = parseFloat(value).toLocaleString('en-US', {
    style: 'percent'
  });
});


var elem = document.querySelector('input[type="range"]');

var rangeValue = function(){
  var newValue = elem.value;
  var target = document.querySelector('.value');
  target.innerHTML = newValue;
}

elem.addEventListener("input", rangeValue);