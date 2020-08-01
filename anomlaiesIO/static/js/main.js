// Initiate Page
const  uploadDataFormId = "upload-data-form-id"; // This input should be appended to the whole form data
showOrHideElement(showOrHide='show', elementID='step-two-set-schema');

function submitUploadDataForm () {
    "use strict";
    console.log(`Getting data from form ${uploadDataFormId}`);
    var uploadDataFormObject = document.getElementById(uploadDataFormId);
    // showOrHideLoader('show');
    saveUploadedFile(uploadDataFormObject);
}

function saveUploadedFile(form) {
        // Send ajax call to save form
        alert("Entered saveFileAndRunAlgo");
        console.log("Submitting #" + uploadDataFormId);
        var endpoint = "save_uploaded_file" ; // found in urls.py

        // Set file data
        var data = $(form).serialize();
        var fileData = new FormData();
        var file_data = $('#input-file-now')[0].files;
        for (var i = 0; i < file_data.length; i++) {
            fileData.append("my_images[]", file_data[i]);
        }
        data = data+fileData;
        console.log(fileData);
        $.ajax({
            type : "POST",
            url : endpoint,
            data: data,

            // handle a successful response
            success: function(context) {
                console.log("AJAX call SUCCESS!");
                completeFormSubmission(context); // context is what we get from the python-ajax view
            },

            error: function (xhr, errmsg, err) {
                console.log("AJAX call ERROR");
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });

        function completeFormSubmission () {
            alert("Completed!");
        }
    };


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


