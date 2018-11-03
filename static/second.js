// Jacob Frabutt
// 10-21-18
// CS50x: Final Project
// 2nd Javascript component for the website
// Jquerry is used in this document
// Thank you to stack exchange for helping me with some of the issues I was having

// activates when the webpage is ready
$(document).ready(function() {

    // change password page
    $('#pas').submit(function() {
        if (!$('#pas input[name = previous]').val()) {
            alert("Please provide your previous password.");
            return false;
        }
        if (!$('#pas input[name = new]').val()) {
            alert("Please provide a new password.");
            return false;
        }
        if (!$('#pas input[name = confirm]').val()) {
            alert("Please re-enter your password.");
            return false;
        }
        if ($('#pas input[name = new').val() != $('#pas input[name = confirm]').val()) {
            alert("Passwords don't match.");
            return false;
        }
        return true;
    });

    // add a new assignment
    // for some reason this did not work with jQuerry
    $('#insert').submit(function() {
        let val = document.getElementById("assign_name").value;
        if (!val) {
            alert("Please provide an assignment name.");
            return false;
        }
        val = document.getElementById("a").value;
        if (!val) {
            alert("Please provide the assignment points.");
            return false;
        }
        if (isNaN(+val) || val < 0) {
            alert("Scores must be positive numbers");
            return false;
        }
        val = document.getElementById("b").value;
        if (!val) {
            alert("Please provide the assignment points.");
            return false;
        }
        if (isNaN(+val) || val < 0) {
            alert("Scores must be positive numbers");
            return false;
        }
        return true;
    });

    // makes sure the user wants to delete the assignment
    $(".delete").submit(function() {
        if (confirm("Are you sure you want to delete this assignment? This action CAN NOT be undone!")) {
            return true;
        } else {
            return false;
        }
    });

    // edit the assignments
    $('#edit').submit(function() {
        let amount = $('#edit input[name = classes_num]').val();

        // iterates over each assignment
        for (let i = 0; i < amount; i++) {
            if (!$(`#edit input[name = name${i}]`).val()) {
                alert("Please fill in the title of all the assignments.");
                return false;
            }
            let val = $(`#edit input[name = earned${i}]`).val();
            if (!val) {
                alert("Please fill in the number of points earned for all the assignments.");
                return false;
            }
            if (isNaN(val)) {
                alert("All point values must be numbers");
                return false;
            }
            val = $(`#edit input[name = out${i}]`).val();
            if (!val) {
                alert("Please fill in the number of points possible for all the assignments.");
                return false;
            }
            if (isNaN(val)) {
                alert("All point values must be numbers");
                return false;
            }
        }
        return true;
    });

    // changing the names of classes
    $('#edit_classes').submit(function() {
        let amount = $('#edit_classes input[name = number]').val();
        for (let i = 0; i < amount; i++) {
            if (!$(`#edit_classes input[name = name${i}]`).val()) {
                alert("Please fill in the title of all the classes.");
                return false;
            }
        }
        return true;
    });
});


// I found this function of Stack Exchange
// It only allows the user to type in numbers (and the decimal point)
function isNumberKey(evt) {
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57))
        return false;

    return true;
}