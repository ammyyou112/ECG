$(document).ready(function() {
    // Hide analysis options and result options initially
    $('#analysis-options').hide();
    $('#result-options').hide();

    // Handle form submission to show analysis options
    $('#sampling-form').on('submit', function(event) {
        event.preventDefault();
        $('#analysis-options').show();
    });

    // Handle form submission to show result options
    $('#analysis-form').on('submit', function(event) {
        event.preventDefault();
        populateResultDropdown();
        $('#result-options').show();
    });

    // Handle click on "Show Selected Result" button
    $('#show-result-button').on('click', function() {
        let selectedResult = $('#result-dropdown').val();
        // Send AJAX request to server to get and display the selected result
        // Use the selectedResult value to determine which result to show
    });

    // Function to populate the result dropdown based on user's selections
    function populateResultDropdown() {
        let selectedOptions = [];
        $('input[type="checkbox"]:checked').each(function() {
            selectedOptions.push($(this).attr('name'));
        });

        // Populate the dropdown with selected options
        let resultDropdown = $('#result-dropdown');
        resultDropdown.empty();
        selectedOptions.forEach(function(option) {
            resultDropdown.append($('<option>', {
                value: option,
                text: option
            }));
        });
    }
});
