// Add input event listeners to OTP boxes for auto-focus and auto-submit
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

                // Auto-submit when all 6 digits are entered
                if (i === 6 && e.target.value.length === 1) {
                    // Check if all boxes are filled
                    let allFilled = true;
                    for (let j = 1; j <= 6; j++) {
                        if (!document.getElementById(`otp-${j}`).value) {
                            allFilled = false;
                            break;
                        }
                    }
                    if (allFilled) {
                        verifyOTP();
                    }
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
