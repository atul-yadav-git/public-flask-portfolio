// dropdown_auto_submit.js

/**
 * This script is responsible for automatically submitting a form 
 * when the user selects an option from a <select> dropdown menu.
 * 
 * Purpose:
 * - Created to bypass the need for a submit button by triggering
 *   a form submission when the dropdown value changes.
 * - Implemented as an external JavaScript file to comply with 
 *   Content Security Policy (CSP) rules, which block inline 
 *   scripts in HTML (e.g., `onchange` attributes).
 * 
 * Usage:
 * - The script listens for a 'change' event on the <select> element 
 *   with the ID "search-query". When the user selects an option, 
 *   the form is automatically submitted.
 */

// Wait for the DOM content to fully load before running the script
document.addEventListener("DOMContentLoaded", function() {
    // Get the <select> element by its ID
    const searchQuery = document.getElementById("search-query");

    // Add an event listener that triggers when the <select> value changes
    searchQuery.addEventListener("change", function() {
        // If a valid value is selected, submit the form
        if (this.value) {
            this.form.submit();
        }
    });
});

