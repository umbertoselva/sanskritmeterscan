// Custom Javascript functions

// 1) to display error message in forms
// 2) to lower the first checkbox (Bootstrap bug)
// 3) to display the filename in the input bar when user selects file
// 4) to record the filesize in the session cookie (in order to validate filesize with allowed_filesize())

// 1)
// script to display the error message when user clicks on upload without selecting a file
// it affects forms with the class 'needs-validation'
// it grabs tags with the class 'validate-me' and adds to them the Bootstrap class 'was-validated'

window.addEventListener('load', function () {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');

    // Get all form-groups in need of validation
    var validateGroup = document.getElementsByClassName('validate-me');

    // Loop over divs in need of validation and prevent submission
    var validation = Array.prototype.filter.call(forms, function (form) {
        form.addEventListener('submit', function (event) {
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            }

            //Added validation class to all form-groups in need of validation
            for (var i = 0; i < validateGroup.length; i++) {
                validateGroup[i].classList.add('was-validated');
            }
        }, false);
    });
}, false);

// 2)
// script to lower the first checkbox when the error message is displayed when user clicks on upload without selecting a file
// it affects the forms with the class 'needs-validation'
// it grabs the items with the class 'lower-me' and adds the custom class 'lowered' (see global.css)

window.addEventListener('load', function () {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');

    // Get all form-groups in need of validation
    var lowermeGroup = document.getElementsByClassName('lower-me');

    // Loop over divs in need of validation and prevent submission
    var validation = Array.prototype.filter.call(forms, function (form) {
        form.addEventListener('submit', function (event) {
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            }

            //Added validation class to all form-groups in need of validation
            for (var i = 0; i < lowermeGroup.length; i++) {
                lowermeGroup[i].classList.add('lowered');
            }
        }, false);
    });
}, false);


// 3)
// function to display the filename in the input bar when user selects file
$('.custom-file-input').change(function (e) {
    if (e.target.files.length) {
        $(this).next('.custom-file-label').html(e.target.files[0].name);
    }
});


// 4)
// function to send filesize with the session cookie
// add  <input oninput="record_filesize(this)" type="file">
function record_filesize(elem){
    document.cookie = `filesize=${elem.files[0].size}`
}

