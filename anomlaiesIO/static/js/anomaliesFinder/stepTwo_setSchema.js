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
    console.log(columnsMapping);
    const pandasFieldTypesMapping = {'int64':'Numbers', 'float64':'Numbers', 'bool':'Booleans','object':'Strings'};

    var stepTwoTemplate = `<div class="row">`;
        for (var fieldTypeKey in columnsMapping) {
            var fieldList = columnsMapping[fieldTypeKey];
            console.log("Fields List:", fieldList);
            stepTwoTemplate += generateStepFieldsCard(pandasFieldTypesMapping[fieldTypeKey], fieldList);
        }

        stepTwoTemplate += `</div>`
    return stepTwoTemplate;
     }

function generateStepFieldsCard (header, fieldList) {
    var stepFieldsCardTemplate = '';
            stepFieldsCardTemplate += '<div class="col-lg-3 col-md-6"> <div class="card">';
                stepFieldsCardTemplate += '<div class="card-body">';
                    stepFieldsCardTemplate += `<h5 class="card-title"> ${header}</h5>`; // Card Header
                    for (var field in fieldList) {
                        stepFieldsCardTemplate += `<p class="card-text"> ${fieldList[field]} </p>`; // Fields
                    }
                stepFieldsCardTemplate += '</div>'; // closing card-body div

            stepFieldsCardTemplate += '</div> </div>'; // closing "card" and "col-lg-3..." divs

    return stepFieldsCardTemplate
}

function modifyFirstStepElementsUI () {
    // modify step headers
    var stepOneConainter = document.getElementById("step-one-container-id");

    var mainHeader = stepOneConainter.querySelectorAll("#main-step-header")[0];
    var helpText = stepOneConainter.querySelectorAll("#help-text")[0];

    helpText.style.display = "none";
    mainHeader.style.fontSize = "20px";

   // hide upload-file-window (from step-1)
    var dropifyElementID = document.getElementById("dropify-wrapper-id");
    var uploadButtonID = document.getElementById("upload-file-btn-id");
    dropifyElementID.style.display = "none"; uploadButtonID.style.display = "none";

}

