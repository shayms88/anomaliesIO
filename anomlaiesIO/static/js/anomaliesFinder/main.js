/*jshint esversion: 6 */

// Initiate Page
const  uploadDataFormId = "upload-data-form-id"; // This input should be appended to the whole form data
showOrHideElement(showOrHide='hide', elementID='step-two-container');

function submitUploadDataForm () {
    "use strict";
    console.log(`Getting data from form ${uploadDataFormId}`);
    var uploadDataFormObject = document.getElementById(uploadDataFormId);
    showOrHideLoader('show');
    var file_path = saveUploadedFile(uploadDataFormObject);
    console.log(file_path);
}


function showOrHideElement (showOrHide, elementID) {
    var elementObject = document.getElementById(elementID) ;
    if (showOrHide === 'show'){
        elementObject.style.display = 'block';
    }
    else {
        elementObject.style.display = 'none';
    }
}

function showOrHideLoader (showOrHide) {
    if (showOrHide==='show') {
        $('body').removeClass('loaded');
    }
    else {
        $('body').addClass('loaded');
    }
}

// UI changes functions

function changeIcon(iconID, newIconString, newColor='') {
    var iconElement = document.getElementById(iconID);
    iconElement.className=newIconString;
    iconElement.style.color = newColor;
}

// ###############################################################
//   This part just Validates the csrftoken on each AJAX request
//   This piece of code was copied directly from StackOverflow
// ###############################################################

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


