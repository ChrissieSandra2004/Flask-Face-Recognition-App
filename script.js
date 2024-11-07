// Start--> Fuction to preview the uploding image in Add Emp form

function previewImage() {
    var input = document.getElementById('imageInput');
    var preview = document.getElementById('imagePreview');
    preview.innerHTML = '';

    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var img = document.createElement('img');
            img.src = e.target.result;
            img.style.width = '50px';
            img.style.height = '50px';
            preview.appendChild(img);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

document.getElementById('imageInput').addEventListener('change', previewImage);
// End--> Fuction to preview the uploding image in Add Emp form 





// Start--> Function to preview the updated image when a new image is selected in the edit emp form
function previewUpdatedImage(event) {
    var inputUpdate = event.target;
    var rowId = inputUpdate.getAttribute('id').replace('imageInputUpdate', '');

    var previewUpdate = document.getElementById('imagePreviewUpdate' + rowId);
    var currentImage = document.getElementById('currentImage' + rowId);

    previewUpdate.innerHTML = '';

    if (inputUpdate.files && inputUpdate.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            currentImage.style.display = 'none';
            var img = document.createElement('img');
            img.src = e.target.result;
            img.style.width = '100px';
            img.style.height = '100px';
            previewUpdate.appendChild(img);
        };
        reader.readAsDataURL(inputUpdate.files[0]);
    } else {
        currentImage.style.display = 'block';
    }
}

var inputUpdates = document.querySelectorAll('.imageInputUpdate');
inputUpdates.forEach(function (inputUpdate) {
    inputUpdate.addEventListener('change', previewUpdatedImage);
});

inputUpdates.forEach(function (inputUpdate) {
    previewUpdatedImage({ target: inputUpdate });
});

// End--> Function to preview the updated image when a new image is selected in edit emp form





// Start --> Reset Add emp form:
var resetButton = document.querySelector("form button[type='reset']");
var closeButton = document.querySelector("button[data-dismiss='modal']");
var form = document.querySelector("form");
var imageInput = document.querySelector("#imageInput");
var imagePreview = document.querySelector("#imagePreview");


// Function to reset the form and remove the image preview
function resetForm() {
    // Reset the form
    form.reset();
    // Clear the image preview container
    imagePreview.innerHTML = '';
    // Reset the file input
    imageInput.value = '';

    // Remove the image preview element from the DOM
    var previewImage = document.querySelector("#previewImage");
    if (previewImage) {
        previewImage.remove();
    }
}

resetButton.addEventListener("click", resetForm);

closeButton.addEventListener("click", resetForm);

// END --> Reset Add emp form:




// Starts---> Add emp form image reset:
var resetButtonAdd = document.querySelector("#addEmployeeModal button[type='button']");
resetButtonAdd.addEventListener("click", function () {
    // Reset the form
    form.reset();

    // Clear the image preview container
    imagePreview.innerHTML = '';

    // Reset the file input
    imageInput.value = '';
});

// End---> Add emp form image reset:





// Start --> Validating email and password for Add Emp from

function validateEmail() {
    const emailInput = document.querySelector('input[name="mail"]');
    const email = emailInput.value;
    const emailMessage = document.getElementById("emailMessage");

    if (email.indexOf("") === -1 || email.indexOf("") === -1) {
        emailInput.setCustomValidity("The email address must contain '@' and '.com'");
    } else if (email.indexOf("@") === -1) {
        emailInput.setCustomValidity("The email address must contain '@'");
    } else if (email.indexOf(".com") == -1) {
        emailInput.setCustomValidity("The email address must end with '.com'");
    }
    else if (email.indexOf(".com") === -1) {
        emailInput.setCustomValidity("The email address must contain '@'");
    } else {
        emailInput.setCustomValidity("");
        emailMessage.innerText = "";
    }
}

// password
function validatePassword() {
    const passwordInput = document.querySelector('input[name="password"]');
    const password = passwordInput.value;
    const passwordMessage = document.getElementById("passwordMessage");

    const minLength = 8;
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecialChar = /[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]/.test(password);

    const errors = [];

    if (password.length < minLength) {
        errors.push("Password must be at least 8 characters long");
    }

    if (!hasUppercase) {
        errors.push("Password must contain at least one uppercase letter");
    }

    if (!hasLowercase) {
        errors.push("Password must contain at least one lowercase letter");
    }

    if (!hasNumber) {
        errors.push("Password must contain at least one number");
    }

    if (!hasSpecialChar) {
        errors.push("Password must contain at least one special character");
    }

    if (errors.length > 0) {
        const errorMessage = errors.join("\n");
        passwordInput.setCustomValidity(errorMessage);
        passwordMessage.innerText = errorMessage;
    } else {
        passwordInput.setCustomValidity("");
        passwordMessage.innerText = "";
    }
}

const passwordInput = document.querySelector('input[name="password"]');
passwordInput.addEventListener("input", validatePassword);

const emailInput = document.querySelector('input[name="mail"]');
emailInput.addEventListener("input", validateEmail);

// END --> Validating email and password for Add Emp from





// Start --> Validating email and password for edit emp from

document.addEventListener("DOMContentLoaded", function () {
    function validateEmail(event) {
        const emailInput = event.target;
        const email = emailInput.value;
        const emailMessage = emailInput.nextElementSibling;

        if (email.indexOf("@") === -1 || email.indexOf(".com") === -1) {
            emailInput.setCustomValidity("The email address must contain '@' and '.com'");
        } else if (email.indexOf("@") === -1) {
            emailInput.setCustomValidity("The email address must contain '@'");
        } else if (email.indexOf(".com") === -1) {
            emailInput.setCustomValidity("The email address must end with '.com'");
        } else {
            emailInput.setCustomValidity("");
            emailMessage.innerText = "";
        }
    }

    function validatePassword(event) {
        const passwordInput = event.target;
        const password = passwordInput.value;
        const passwordMessage = passwordInput.nextElementSibling;

        const minLength = 8;
        const hasUppercase = /[A-Z]/.test(password);
        const hasLowercase = /[a-z]/.test(password);
        const hasNumber = /[0-9]/.test(password);
        const hasSpecialChar = /[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]/.test(password);

        const errors = [];

        if (password.length < minLength) {
            errors.push("Password must be at least 8 characters long");
        }

        if (!hasUppercase) {
            errors.push("Password must contain at least one uppercase letter");
        }

        if (!hasLowercase) {
            errors.push("Password must contain at least one lowercase letter");
        }

        if (!hasNumber) {
            errors.push("Password must contain at least one number");
        }

        if (!hasSpecialChar) {
            errors.push("Password must contain at least one special character");
        }

        if (errors.length > 0) {
            const errorMessage = errors.join("\n");
            passwordInput.setCustomValidity(errorMessage);
            passwordMessage.innerText = errorMessage;
        } else {
            passwordInput.setCustomValidity("");
            passwordMessage.innerText = "";
        }
    }

    const emailInputs = document.querySelectorAll('.email-input');
    emailInputs.forEach((emailInput) => {
        emailInput.addEventListener("input", validateEmail);
    });

    const passwordInputs = document.querySelectorAll('.password-input');
    passwordInputs.forEach((passwordInput) => {
        passwordInput.addEventListener("input", validatePassword);
    });
});

// End --> Validating email and password for edit emp from



// Starts---> Edit Emp form - image reset:

function previewUpdatedImage(event) {
    var inputUpdate = event.target;
    var rowId = inputUpdate.getAttribute('id').replace('imageInputUpdate', '');
    var previewUpdate = document.getElementById('imagePreviewUpdate' + rowId);
    var currentImage = document.getElementById('currentImage' + rowId);

    previewUpdate.innerHTML = '';

    if (inputUpdate.files && inputUpdate.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            currentImage.style.display = 'none';
            var img = document.createElement('img');
            img.src = e.target.result;
            img.style.width = '50px';
            img.style.height = '50px';
            previewUpdate.appendChild(img);
        };
        reader.readAsDataURL(inputUpdate.files[0]);
    } else {
        currentImage.style.display = 'block';
    }
}

function resetImage(rowId) {
    var inputUpdate = document.getElementById('imageInputUpdate' + rowId);
    var currentImage = document.getElementById('currentImage' + rowId);
    var previewUpdate = document.getElementById('imagePreviewUpdate' + rowId);

    inputUpdate.value = null;
    previewUpdate.innerHTML = ''; // Clear the preview
    currentImage.style.display = 'block'; // Display the current image

    // Restore the original image source
    var originalSrc = currentImage.getAttribute('data-original-src');
    currentImage.src = originalSrc;
}

var inputUpdates = document.querySelectorAll('.imageInputUpdate');
inputUpdates.forEach(function (inputUpdate) {
    inputUpdate.addEventListener('change', previewUpdatedImage);
});

// Call previewUpdatedImage initially to display the current images for all rows
inputUpdates.forEach(function (inputUpdate) {
    previewUpdatedImage({ target: inputUpdate });
});




// Starts -------> disabled future years in the date input fields of (add, edit form)
// function getCurrentDate() {
//     var today = new Date();
//     var year = today.getFullYear();
//     var month = (today.getMonth() + 1).toString().padStart(2, '0');
//     var day = today.getDate().toString().padStart(2, '0');
//     return year + '-' + month + '-' + day;
// }

// document.getElementById('editDob').max = getCurrentDate();
// document.getElementById('addDob').max = getCurrentDate();


var today = new Date();
var maxDate = new Date(today.getFullYear() - 18, today.getMonth(), today.getDate()); // 18 years ago
var minDate = new Date(today.getFullYear() - 100, today.getMonth(), today.getDate()); // 100 years ago

// Format the dates as yyyy-mm-dd strings
var maxDateStr = maxDate.toISOString().split('T')[0];
var minDateStr = minDate.toISOString().split('T')[0];

document.getElementById('addDob').setAttribute('max', maxDateStr);
document.getElementById('addDob').setAttribute('min', minDateStr);

var today = new Date();
var maxDate = new Date(today.getFullYear() - 18, today.getMonth(), today.getDate()); // 18 years ago
var minDate = new Date(today.getFullYear() - 100, today.getMonth(), today.getDate()); // 100 years ago

// Format the dates as yyyy-mm-dd strings
var maxDateStr = maxDate.toISOString().split('T')[0];
var minDateStr = minDate.toISOString().split('T')[0];

// Iterate through all "Date of Birth" input fields in the edit form
var editDobElements = document.querySelectorAll('[id^="editDob"]');
editDobElements.forEach(function (element) {
    element.setAttribute('max', maxDateStr);
    element.setAttribute('min', minDateStr);
});

// End <------ Disabled future years in the date input field of add and edit form

// // per page filter
// function changePerPage() {
//     var perPageSelect = document.getElementById("per_page_select");
//     var selectedPerPage = perPageSelect.value;
//     window.location.href = "/admin?page=1&per_page=" + selectedPerPage;
// }



// Function to change the number of entries per page
// function changePerPage() {
//     var perPageSelect = document.getElementById("per_page_select");
//     var selectedPerPage = perPageSelect.value;
//     window.location.href = "/admin?page=1&per_page=" + selectedPerPage;
// }

// // Event listener to trigger the changePerPage function when the dropdown changes
// document.getElementById("per_page_select").addEventListener("change", changePerPage);



function changePerPage() {
    var perPageSelect = document.getElementById("per_page_select");
    var selectedPerPage = perPageSelect.value;
    var searchName = document.getElementById("searchName").value.trim().toLowerCase();
    var cmpcode = getParameterByName('cmpcode'); // Replace with your method to get "cmpcode" from the URL

    // Update the "per_page" session variable using Flask route
    fetch('/set_entries_per_page', {
        method: 'POST',
        body: new URLSearchParams({ per_page: selectedPerPage, cmpcode: cmpcode }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // If the update was successful, navigate to the first page with the new "per_page" value
                window.location.href = `/admin?cmpcode=${cmpcode}&page=1&search=${searchName}`;
            }
        })
        .catch(error => {
            console.error('Error updating per_page:', error);
        });
}

function searchByName() {
    var searchName = document.getElementById("searchName").value.trim().toLowerCase();
    var cmpcode = getParameterByName('cmpcode'); // Replace with your method to get "cmpcode" from the URL
    var perPageSelect = document.getElementById("per_page_select");
    var selectedPerPage = perPageSelect.value;

    // Navigate to the search route with the search query, "cmpcode," and "per_page" value
    window.location.href = `/admin?cmpcode=${cmpcode}&page=1&search=${searchName}&per_page=${selectedPerPage}`;
}


// Helper function to retrieve a parameter from the URL
function getParameterByName(name) {
    var url = new URL(window.location.href);
    return url.searchParams.get(name);
}

// Global admin javascript starts from here 

// function globalChangePerPage() {
//     var perPageSelect = document.getElementById("global_per_page_select");
//     var perPage = perPageSelect.options[perPageSelect.selectedIndex].value;
//     // Update the URL to include the per_page parameter
//     var currentURL = window.location.href;
//     var updatedURL = currentURL.split('?')[0] + "?page=1&per_page=" + perPage;
//     window.location.href = updatedURL;
// }

// function globalSearchByName() {
//     var searchInput = document.getElementById("globalSearchName");
//     var searchQuery = searchInput.value;
//     // Update the URL to include the search_query parameter
//     var currentURL = window.location.href;
//     var updatedURL = currentURL.split('?')[0] + "?page=1&per_page=" + per_page + "&search_query=" + searchQuery;
//     window.location.href = updatedURL;
// }

function globalChangePerPage() {
    var perPageSelect = document.getElementById("global_per_page_select");
    var perPage = perPageSelect.options[perPageSelect.selectedIndex].value;
    var currentURL = window.location.href;
    var urlParams = new URLSearchParams(window.location.search);
    var page = urlParams.get("page") || 1;
    var searchQuery = urlParams.get("search_query") || "";
    var updatedURL = currentURL.split('?')[0] + `?page=${page}&per_page=${perPage}&search_query=${searchQuery}`;
    window.location.href = updatedURL;
}


function globalSearchByName() {
    var searchInput = document.getElementById("globalSearchName");
    var searchQuery = searchInput.value;
    var currentURL = window.location.href;
    var urlParams = new URLSearchParams(window.location.search);
    var perPage = urlParams.get("per_page") || 5; // Default to 5 if not present
    var updatedURL = currentURL.split('?')[0] + `?page=1&per_page=${perPage}&search_query=${searchQuery}`;
    window.location.href = updatedURL;
}



// // Function to set the selected option based on the per_page parameter in the URL
// function setSelectedOption() {
//     var urlParams = new URLSearchParams(window.location.search);
//     var perPageParam = urlParams.get("per_page");

//     if (perPageParam !== null) {
//         var perPageSelect = document.getElementById("per_page_select");
//         perPageSelect.value = perPageParam;
//     }
// }
// // Call the setSelectedOption function when the page loads
// window.addEventListener("load", setSelectedOption);



// function searchByName() {
//     var searchName = document.getElementById("searchName").value.trim().toLowerCase();
//     var searchLink = document.getElementById("searchLink");
//     searchLink.href = "/admin?search=" + searchName;
//     searchLink.click();  // Trigger the click event to navigate to the search route
// }




// <------------------------------------------------> Face Attendance : 



// Fetch the JWT token and update the video source
async function fetchAndLoadVideo() {
    try {
        // Fetch the JWT token
        const tokenResponse = await fetch('http://127.0.0.1:5000/get_token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                // Add any required credentials here (e.g., email, password)
            }),
        });

        const tokenData = await tokenResponse.json();
        const jwtToken = tokenData.access_token;

        // Make a new request to the videofeed_jwt route with the JWT token as a route parameter
        const videoElement = document.getElementById('video-feed');
        videoElement.src = `http://127.0.0.1:5000/videofeed_jwt/${jwtToken}`;

        // Display the video element
        videoElement.style.display = 'block';
    } catch (error) {
        console.error('Error fetching token:', error);
    }
}

// Call the function when the page loads
window.onload = fetchAndLoadVideo;




























































































//
// Reload Page ---------------------------------------------------------------->>
function reloadPage() {
    location.reload();
}