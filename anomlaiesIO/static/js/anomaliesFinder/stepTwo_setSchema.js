function triggerStepTwo (uploadedFilePath) {
    showOrHideLoader('hide');
    showOrHideElement(showOrHide='show', elementID='step-two-container');
    modifyFirstStepElementsUI();

    var file_path = uploadedFilePath.file_path;
    var endpoint = "set_fields_schema";

    $.ajax({
        url : endpoint,
        type : "GET",
        data: {'file_path':file_path},

        // handle a successful response
        success: function(context) {
            console.log("AJAX SUCCESS - "+ endpoint);
            document.getElementById("columns-mapping-div-id").innerHTML = GenerateStepTwoHTML(context.columns_mapping);

        },

        error: function (xhr, errmsg, err) {
            console.log("AJAX call ERROR");
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function GenerateStepTwoHTML (columnsMapping) {
    var i, len, text;
    console.log(columnsMapping);
    // Start a UL
    var stepTwoTemplate = `<ul>`;

    // Append each key from columns mapping
    for (var key in columnsMapping) {
      stepTwoTemplate += `<li> ${key} : ${columnsMapping[key]} </li>`;
    }
    // Close ul
    stepTwoTemplate += `</ul>`;
    return stepTwoTemplate;
}

function modifyFirstStepElementsUI () {
    // modify step headers
    var stepOneConainter = document.getElementById("step-one-container-id");

    // var mainHeader = stepOneConainter.querySelectorAll("#main-step-header")[0];
    var helpText = stepOneConainter.querySelectorAll("#help-text")[0];

    helpText.style.display = "none";
    // mainHeader.style.fontSize = "200px";

   // hide upload-file-window (from step-1)
    var dropifyElementID = document.getElementById("dropify-wrapper-id");
    var uploadButtonID = document.getElementById("upload-file-btn-id");
    dropifyElementID.style.display = "none"; uploadButtonID.style.display = "none";

}

