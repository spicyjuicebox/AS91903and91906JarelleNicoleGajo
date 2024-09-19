document.addEventListener('DOMContentLoaded', function () {
    /* The const will get the different variables from the HTML. */
    const form = document.getElementById('paymentForm');
    const cardNumber = document.getElementById('cardNumber');
    const expMonth = document.getElementById('expMonth');
    const expYear = document.getElementById('expYear');
    const cvv = document.getElementById('cvv');
    const submitPayment = document.getElementById('submitPayment');

    /* Creating the function to validate the input. */
    function validateInput() {
        const cardNumberValid = /^[0-9]{16}$/.test(cardNumber.value); /* This will make sure that the card number is 16 digits long. */
        const expMonthValid = expMonth.value !== ""; /* This will make sure the expiry month is not empty. */
        const expYearValid = expYear.value !== ""; /* This will make sure the expiry year is not empty. */
        const cvvValid = /^[0-9]{3}$/.test(cvv.value); /* This will make sure that the cvv is 3 digits long. */
        // The submit payment button cannot be pressed unless all these required fields have been filled.
        submitPayment.disabled = !(cardNumberValid && expMonthValid && expYearValid && cvvValid);
    }

    /* Creating the function to only allow numbers to be entered in the input for the card number and cvv. */
    function allowOnlyNumbers(inputElement, maxLength) {
        inputElement.addEventListener('input', function () {
            inputElement.value = inputElement.value.replace(/\D/g, '').slice(0, maxLength); /* If the user tries to enter anything else other than a number, nothing will show up. */
            validateInput(); /* Runs the function to validate the input. */
        });
    }
    allowOnlyNumbers(cardNumber, 16); /* This is going to max out at 16 characters. */
    allowOnlyNumbers(cvv, 3); /* This is going to max out at 3 characters. */
    /* If changed, the validateInput will run to validate it. */
    expMonth.addEventListener('change', validateInput);
    expYear.addEventListener('change', validateInput);

    /* This is for disabling the submit button if the fields are not all filled. */
    form.addEventListener('submit', function (event) {
        if (submitPayment.disabled) {
            event.preventDefault();
        }
    });
    validateInput();
});