function saveUploadedFile(form) {
        // Send ajax call to save form
        console.log("Submitting #" + uploadDataFormId);

        // Set file data
        var uploadInputId = "uploaded-file-id";
        var formData = new FormData();
        formData.append('file', $(`#${uploadInputId}`)[0].files[0]);
        formData.append('csrfmiddlewaretoken', form.elements['csrfmiddlewaretoken'].value);
        // Set AJAX params
        $.ajax({
            url : 'save_uploaded_file',
            type : "POST",
            data: formData,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',

            // handle a successful response
            success: function(context) {
                console.log("AJAX SUCCESS - save_uploaded_file");
                // Change icon
                changeIcon('step-one-icon', 'fas fa-check', '#1abc9c');
                triggerStepTwo(context);
            },

            error: function (xhr, errmsg, err) {
                console.log("AJAX call ERROR");
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };