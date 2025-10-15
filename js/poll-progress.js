// Poll Progress Circle Functionality
// Tracks completion of required form fields and displays progress

function updateProgressCircle() {
    const form = document.querySelector('form[id$="Form"]'); // Matches any form ending with "Form"
    if (!form) return;

    const formSections = document.querySelectorAll('.form-section');
    const sectionStatus = [];
    let totalRequiredFields = 0;
    let completedFields = 0;
    let completedSections = 0;
    let totalRequiredSections = 0;
    let currentSectionName = '';

    formSections.forEach((section) => {
        const h3 = section.querySelector('h3');
        if (!h3) return;

        const sectionName = h3.textContent.trim();

        let sectionTotalFields = 0;
        let sectionCompletedFields = 0;

        // Find ALL questions by looking for main labels (both required and optional)
        // Main question labels are direct children of .form-group
        const allLabels = section.querySelectorAll('.form-group > label');

        allLabels.forEach((label) => {
            // Get the "for" attribute
            const forAttr = label.getAttribute('for');

            // Skip the suggestions field - don't count it in progress
            if (forAttr === 'suggestions') {
                return;
            }

            // Count this as one question
            sectionTotalFields++;
            totalRequiredFields++;

            // Find the associated input/field for this label
            let isCompleted = false;

            if (forAttr) {
                // Try to find the input by ID
                const input = section.querySelector(`#${forAttr}`);
                if (input) {
                    // Found a single input field (text, email, select, etc.)
                    if (input.tagName === 'INPUT' || input.tagName === 'TEXTAREA' || input.tagName === 'SELECT') {
                        isCompleted = input.value && input.value.trim() !== '';
                    }
                } else {
                    // ID not found - probably a checkbox/radio group where label has for="role" but inputs have different IDs
                    // Fall back to checking the parent form-group
                    const formGroup = label.closest('.form-group');
                    if (formGroup) {
                        const checkedInputs = formGroup.querySelectorAll('input[type="checkbox"]:checked, input[type="radio"]:checked');
                        isCompleted = checkedInputs.length > 0;
                    }
                }
            } else {
                // Label doesn't have "for" - check parent form-group
                const formGroup = label.closest('.form-group');
                if (formGroup) {
                    // Check for any checked checkboxes or radios in this form group
                    const checkedInputs = formGroup.querySelectorAll('input[type="checkbox"]:checked, input[type="radio"]:checked');
                    isCompleted = checkedInputs.length > 0;
                }
            }

            if (isCompleted) {
                sectionCompletedFields++;
                completedFields++;
            }
        });

        // Update section status
        if (sectionTotalFields > 0) {
            totalRequiredSections++;
            const sectionComplete = (sectionCompletedFields === sectionTotalFields);

            if (sectionComplete) {
                completedSections++;
                sectionStatus.push({ name: sectionName, completed: true });
            } else {
                sectionStatus.push({ name: sectionName, completed: false });
                if (!currentSectionName) {
                    currentSectionName = sectionName;
                }
            }
        }
    });

    // Calculate progress percentage based on all questions (required + optional)
    const progressPercentage = totalRequiredFields > 0 ?
        Math.round((completedFields / totalRequiredFields) * 100) : 0;

    // Update circle progress
    const circumference = 2 * Math.PI * 45; // radius = 45 for 100px circle
    const offset = circumference - (progressPercentage / 100) * circumference;
    const progressRing = document.getElementById('progressRing');
    const progressPercent = document.getElementById('progressPercent');
    const progressCircle = document.getElementById('progressCircle');

    if (progressRing) {
        progressRing.style.strokeDashoffset = offset;

        // Dynamic color based on progress percentage
        let startColor, endColor;

        if (progressPercentage <= 30) {
            // Red to Orange (0-30%)
            startColor = '#ff5555';
            endColor = '#ff8c00';
        } else if (progressPercentage <= 70) {
            // Orange to Yellow (30-70%)
            startColor = '#ff8c00';
            endColor = '#FFC947';
        } else {
            // Yellow to Green (70-100%)
            startColor = '#FFC947';
            endColor = '#50fa7b';
        }

        // Update gradient stops
        const gradient = document.querySelector('#progressGradient');
        if (gradient) {
            const stop1 = gradient.querySelector('stop:first-child');
            const stop2 = gradient.querySelector('stop:last-child');
            if (stop1) stop1.style.stopColor = startColor;
            if (stop2) stop2.style.stopColor = endColor;
        }
    }
    if (progressPercent) {
        progressPercent.textContent = progressPercentage + '%';
    }

    // Update color and class based on progress
    if (progressCircle) {
        if (progressPercentage === 100) {
            progressCircle.classList.add('complete');
        } else {
            progressCircle.classList.remove('complete');
        }
    }

    // Update details popup
    updateProgressDetails(sectionStatus, currentSectionName, completedSections, totalRequiredSections);
}

function updateProgressDetails(sectionStatus, currentSection, completed, total) {
    const sectionsList = document.getElementById('sectionsList');
    const currentDetail = document.getElementById('currentSectionDetail');

    if (!sectionsList || !currentDetail) return;

    // Build sections list
    let html = '';
    sectionStatus.forEach(section => {
        const icon = section.completed ? '✓' : '○';
        const className = section.completed ? 'completed' : 'incomplete';
        html += `<div class="section-item ${className}">${icon} ${section.name}</div>`;
    });
    sectionsList.innerHTML = html;

    // Update current section detail
    if (completed === total) {
        currentDetail.textContent = '✓ Ready to submit!';
        currentDetail.style.color = '#50fa7b';
    } else {
        currentDetail.textContent = `Current: ${currentSection}`;
        currentDetail.style.color = 'var(--text-secondary)';
    }
}

function toggleProgressDetails() {
    const details = document.getElementById('progressDetails');
    if (details) {
        details.style.display = details.style.display === 'none' ? 'block' : 'none';
    }
}

// Initialize progress circle
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form[id$="Form"]');
    if (form) {
        // Initial progress check
        setTimeout(updateProgressCircle, 100);

        // Update on any input change
        form.addEventListener('input', updateProgressCircle);
        form.addEventListener('change', updateProgressCircle);

        // Close details popup when clicking outside
        document.addEventListener('click', function(e) {
            const circle = document.getElementById('progressCircle');
            const details = document.getElementById('progressDetails');
            if (circle && details && !circle.contains(e.target) && !details.contains(e.target)) {
                details.style.display = 'none';
            }
        });
    }
});

// Hide progress circle on success page
const observeSuccess = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        const successPage = document.getElementById('successPage');
        const progressCircle = document.getElementById('progressCircle');
        const progressDetails = document.getElementById('progressDetails');

        if (successPage && successPage.style.display === 'block') {
            if (progressCircle) progressCircle.style.display = 'none';
            if (progressDetails) progressDetails.style.display = 'none';
        }
    });
});

const successPage = document.getElementById('successPage');
if (successPage) {
    observeSuccess.observe(successPage, {
        attributes: true,
        attributeFilter: ['style']
    });
}
