// Add input event listeners to OTP boxes for auto-focus only (NO auto-submit)
document.addEventListener('DOMContentLoaded', () => {
    for (let i = 1; i <= 6; i++) {
        const box = document.getElementById(`otp-${i}`);
        if (box) {
            box.addEventListener('input', (e) => {
                // Remove any non-digit characters
                e.target.value = e.target.value.replace(/\D/g, '');

                // Auto-focus to next box
                if (e.target.value.length === 1 && i < 6) {
                    document.getElementById(`otp-${i + 1}`).focus();
                }
            });

            // Handle backspace to go to previous box
            box.addEventListener('keydown', (e) => {
                if (e.key === 'Backspace' && !e.target.value && i > 1) {
                    document.getElementById(`otp-${i - 1}`).focus();
                }
            });
        }
    }
});
