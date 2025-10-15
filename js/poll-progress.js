// Poll Progress Circle Functionality
// Tracks completion of required form fields and displays progress

function updateProgressCircle() {
    const form = document.querySelector('form[id$="Form"]'); // Matches any form ending with "Form"
    if (!form) return;

    const formSections = document.querySelectorAll('.form-section');
    const sectionStatus = [];
    let completedSections = 0;
    let totalRequiredSections = 0;
    let currentSectionName = '';

    formSections.forEach((section) => {
        const h3 = section.querySelector('h3');
        if (!h3) return;

        const sectionName = h3.textContent.trim();

        // Check for required fields in this section
        const requiredInputs = section.querySelectorAll('[required], .checkbox-group[data-group]');

        if (requiredInputs.length === 0) return; // Skip sections without required fields

        totalRequiredSections++;
        let sectionComplete = true;

        requiredInputs.forEach((input) => {
            // Handle single-choice checkbox groups
            if (input.classList.contains('checkbox-group') && input.hasAttribute('data-group')) {
                const groupName = input.getAttribute('data-group');
                const checked = input.querySelectorAll('input[type="checkbox"]:checked');
                if (checked.length === 0) {
                    sectionComplete = false;
                }
            }
            // Handle regular required fields
            else if (input.hasAttribute('required')) {
                if (input.type === 'checkbox' || input.type === 'radio') {
                    const name = input.name;
                    const anyChecked = section.querySelector(`[name="${name}"]:checked`);
                    if (!anyChecked) {
                        sectionComplete = false;
                    }
                } else {
                    if (!input.value.trim()) {
                        sectionComplete = false;
                    }
                }
            }
        });

        if (sectionComplete) {
            completedSections++;
            sectionStatus.push({ name: sectionName, completed: true });
        } else {
            sectionStatus.push({ name: sectionName, completed: false });
            if (!currentSectionName) {
                currentSectionName = sectionName;
            }
        }
    });

    // Calculate progress percentage
    const progressPercentage = totalRequiredSections > 0 ?
        Math.round((completedSections / totalRequiredSections) * 100) : 0;

    // Update circle progress
    const circumference = 2 * Math.PI * 45; // radius = 45 for 100px circle
    const offset = circumference - (progressPercentage / 100) * circumference;
    const progressRing = document.getElementById('progressRing');
    const progressPercent = document.getElementById('progressPercent');
    const progressCircle = document.getElementById('progressCircle');

    if (progressRing) {
        progressRing.style.strokeDashoffset = offset;
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
