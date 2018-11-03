// Jacob Frabutt
// 10-21-18
// CS50x: Final Project
// Javascript component for the website
// Jquerry is used in this document
// Thank you to stack exchange for helping me with some of the issues I was having

// whole website in one file
$(document).ready(function() {

    // register form
    $('#register').submit(function() {
        if (!$('#register input[name = username]').val()) {
            alert("Please provide a username.");
            return false;
        }
        if (!$('#register input[name = password]').val()) {
            alert("Please provide a password.");
            return false;
        }
        if (!$('#register input[name = confirmation]').val()) {
            alert("Please re-enter your password.");
            return false;
        }
        if (!$('#register input[name = first]').val()) {
            alert("Please provide a first name.");
            return false;
        }
        if (!$('#register input[name = middle]').val()) {
            alert("Please provide a middle name.");
            return false;
        }
        if (!$('#register input[name = last]').val()) {
            alert("Please provide a last name.");
            return false;
        }

        // I found this code on stackExchange and it makes sure they select something from the drop-down menu
        var e = document.getElementById("selectGrade");
        var strUser = e.options[e.selectedIndex].value;
        if (strUser == "grade") {
            alert("Please provide a grade level.");
            return false;
        }

        if ($('#register input[name = password').val() != $('#register input[name = confirmation]').val()) {
            alert("Passwords don't match.");
            return false;
        }
        return true;
    });

    // Login form
    $('#login').submit(function() {
        if (!$('#login input[name = username]').val()) {
            alert("Please provide your username.");
            return false;
        }
        if (!$('#login input[name = password]').val()) {
            alert("Please provide your password.");
            return false;
        }
    });

    // If the person already took their final
    $('#taken').click(function() {
        // add this in when button is clicked
        document.getElementById('depends').innerHTML =
            '<form id="took" action="/compute/0" method="post"><div class="form-group"><input autofocus class="wide" name="Q1" placeholder="Q1 Grade" type="text" onkeypress="return isNumberKey(event)"/></div><div class="form-group"><input class="wide" name="Q2" placeholder="Q2 Grade" type="text" onkeypress="return isNumberKey(event)"/></div><div class="form-group"><input class="wide" name="E" placeholder="Exam grade" type="text" onkeypress="return isNumberKey(event)"/></div><div class="form-group"><input class="wide" name="per" placeholder="% exam is worth in overall grade" type="text" onkeypress="return isNumberKey(event)"/></div><div class="form-group"><button type="submit" class="btn btn-primary" id="took">Calculate</button></div></form>';

        // form
        $('#took').submit(function() {
            if (!$('#took input[name = Q1]').val()) {
                alert("Please provide a Q1 grade.");
                return false;
            }
            if (!$('#took input[name = Q2]').val()) {
                alert("Please provide a Q2 grade.");
                return false;
            }
            if (!$('#took input[name = E]').val()) {
                alert("Please provide a exam grade.");
                return false;
            }
            if (!$('#took input[name = per]').val()) {
                alert("Please provide a percentage.");
                return false;
            }
            if ($('#took input[name = Q1]').val() < 0 || $('#took input[name = Q2]').val() < 0 ||
                $('#took input[name = E]').val() < 0) {
                alert("No negative numbers, please.");
                return false;
            }
            if ($('#took input[name = per]').val() <= 0) {
                alert("Percent exam is worth must be larger than 0");
                return false;
            }
            // make sure all are numbers
            if (isNaN($('#took input[name = Q1]').val()) || isNaN($('#took input[name = Q2]').val()) ||
                isNaN($('#took input[name = E]').val()) || isNaN($('#took input[name = per]').val())) {
                alert("All fields must be valid numbers.");
                return false;
            }
            return true;
        });
    });

    // if the person needs to take their final
    $('#upcoming').click(function() {
        // add this when button clicked
        document.getElementById('depends').innerHTML =
            '<form id="take" action="/compute/1" method="post"><div class="form-group"><input autofocus class="wide" name="Q1" placeholder="Q1 Grade" type="text" onkeypress="return isNumberKey(event)"/></div><div class="form-group"><input class="wide" name="Q2" placeholder="Q2 Grade" type="text" onkeypress="return isNumberKey(event)"/></div><div class="form-group"><input class="wide" name="desired" placeholder="Desired overall grade" type="text" onkeypress="return isNumberKey(event)"/></div><div class="form-group"><input class="wide" name="per" placeholder="% exam is worth in overall grade" type="text" onkeypress="return isNumberKey(event)"/></div><div class="form-group"><button class="btn btn-primary" id="take">Calculate</button></div></form>';

        // form
        $('#take').submit(function() {
            if (!$('#take input[name = Q1]').val()) {
                alert("Please provide a Q1 grade.");
                return false;
            }
            if (!$('#take input[name = Q2]').val()) {
                alert("Please provide a Q2 grade.");
                return false;
            }
            if (!$('#take input[name = desired]').val()) {
                alert("Please provide a desired grade.");
                return false;
            }
            if (!$('#take input[name = per]').val()) {
                alert("Please provide a percentage.");
                return false;
            }
            if ($('#take input[name = Q1]').val() < 0 || $('#take input[name = Q2]').val() < 0 ||
                $('#take input[name = desired]').val() < 0) {
                alert("No negative numbers, please.");
                return false;
            }
            if ($('#take input[name = per]').val() <= 0) {
                alert("Percent exam is worth must be larger than 0");
                return false;
            }
            // make sure all are numbers
            if (isNaN($('#take input[name = Q1]').val()) || isNaN($('#take input[name = Q2]').val()) ||
                isNaN($('#take input[name = desired]').val()) || isNaN($('#take input[name = per]').val())) {
                alert("All fields must be valid numbers.");
                return false;
            }
            return true;
        });
    });

    // gpa form
    $('#gpa').submit(function() {
        let amount = 8;
        amount = $('#gpa input[name = amount]').val();
        // for loop goes through each row
        for (let i = 0; i < amount; i++) {
            let val = $(`#gpa input[name = b${i}]`).val();
            if (isNaN(+val)) {
                alert("Only valid numbers please.");
                return false;
            }
            if (!val) {
                alert(`Please fill in the credit hours section for class ${i + 1}.`);
                return false;
            }
            if (val <= 0) {
                alert("Credit hours must be a postivie number");
                return false;
            }
        }
        return true;
    });

    // change number of classes for gpa
    $('#adjust').submit(function() {
        if (!$('#adjust input[name = amount]').val()) {
            alert("You must have a number to adjust to.");
            return false;
        }
        if ($('#adjust input[name = amount]').val() < 1) {
            alert("You must have at least one class.");
            return false;
        }
        if ($('#adjust input[name = amount]').val() > 20) {
            alert("There is a cap of 20 classes.");
            return false;
        }
    });

    // new classes
    $('#new').submit(function() {
        if (!$('#new input[name = add]').val()) {
            alert("Please fill in how many classes you want to add.");
            return false;
        }
        if ($('#new input[name = add]').val() < 1) {
            alert("Number must be a positive integer.");
            return false;
        }
    });

    // make sure they want to delete that class
    $('#remove').submit(function() {
        if (confirm("Are you sure you want to delete this class? This action CAN NOT be undone!")) {
            return true;
        } else {
            return false;
        }
    });

    // add form
    $('#add').submit(function() {
        for (let i = 0; i < $('#add input[name = number]').val(); i++) {
            if (!$(`#add input[name = name${i}]`).val()) {
                alert("Please fill in all sections.");
                return false;
            }
        }
    });

    // make sure they want to delete their account
    $('#wipe').submit(function() {
        if (confirm("Are you sure you want to delete your account? THIS CAN NOT BE UNDONE.")) {
            return true;
        } else {
            return false;
        }
    });
});

// update the class page
function update() {
    let num = document.getElementById("classes_num").value;
    let earned = 0;
    let possible = 0;

    for (let i = 0; i < num; i++) {
        let hold1 = parseFloat($(`#test input[name = earned${i}]`).val());
        let hold2 = parseFloat($(`#test input[name = out${i}]`).val());

        if (!hold1) {
            hold1 = 0;
        }
        if (!hold2) {
            hold2 = 0;
        }

        earned += hold1;
        possible += hold2;

        let per = ((hold1 / hold2) * 100);
        let lett = letter(per);

        // I found the +var.toFixed on stackExchange
        $(`#a${i}`).html(+per.toFixed(2));
        $(`#b${i}`).html(lett);
    }

    let oper = (earned / possible) * 100;
    let olett = letter(oper);

    document.getElementById("overall").innerHTML = (+oper.toFixed(2));
    document.getElementById("overall_let").innerHTML = olett;
}

// figure out the letter grade
function letter(percent) {
    if (percent >= 97)
        return "A+";
    if (percent >= 93)
        return "A";
    if (percent >= 90)
        return "A-";
    if (percent >= 87)
        return "B+";
    if (percent >= 83)
        return "B";
    if (percent >= 80)
        return "B-";
    if (percent >= 77)
        return "C+";
    if (percent >= 73)
        return "C";
    if (percent >= 70)
        return "C-";
    if (percent >= 67)
        return "D+";
    if (percent >= 63)
        return "D";
    if (percent >= 60)
        return "D-";
    return "F";
}