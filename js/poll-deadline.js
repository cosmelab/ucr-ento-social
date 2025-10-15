// Poll Deadline Enforcement
// Disables polls after October 17, 2025 at 11:59 PM Pacific Time

(function() {
    // Set deadline: October 17, 2025 at 23:59:59 Pacific Time
    const deadline = new Date('2025-10-17T23:59:59-07:00');
    const now = new Date();

    // Check if deadline has passed
    if (now > deadline) {
        // Disable the form
        const form = document.querySelector('form');
        if (form) {
            // Disable all form inputs
            const inputs = form.querySelectorAll('input, textarea, select, button');
            inputs.forEach(input => {
                input.disabled = true;
                input.style.cursor = 'not-allowed';
                input.style.opacity = '0.5';
            });

            // Hide the submit button
            const submitBtn = form.querySelector('.submit-btn');
            if (submitBtn) {
                submitBtn.style.display = 'none';
            }

            // Show deadline passed message
            const pollForm = document.getElementById('pollForm');
            if (pollForm) {
                const deadlineMessage = document.createElement('div');
                deadlineMessage.className = 'message error';
                deadlineMessage.style.display = 'block';
                deadlineMessage.style.marginTop = '2rem';
                deadlineMessage.innerHTML = `
                    <h3 style="margin-bottom: 1rem;">⏰ Poll Closed</h3>
                    <p>This poll closed on October 17, 2025 at 11:59 PM.</p>
                    <p style="margin-top: 1rem;">Thank you to everyone who participated! Results will be shared at our first event in November.</p>
                    <div style="margin-top: 2rem;">
                        <a href="polls.html" class="action-button">Back to Polls</a>
                    </div>
                `;
                pollForm.insertBefore(deadlineMessage, pollForm.firstChild);
            }

            // Hide progress circle
            const progressCircle = document.getElementById('progressCircle');
            if (progressCircle) {
                progressCircle.style.display = 'none';
            }
        }
    }
})();
