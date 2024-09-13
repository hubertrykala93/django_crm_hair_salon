document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('register-form');
    const formMessage = document.getElementById('form-message');

    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Zapobiega przeładowaniu strony

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        if (password !== confirmPassword) {
            formMessage.textContent = 'Passwords do not match.';
            formMessage.style.color = 'red';
            return;
        }

        try {
            const response = await fetch('/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }

            const result = await response.json();

            if (result.success) {
                formMessage.textContent = 'Registration successful!';
                formMessage.style.color = 'green';
                // Przekierowanie lub inna akcja po udanej rejestracji
                setTimeout(() => {
                    window.location.href = '/login/'; // Przykładowe przekierowanie
                }, 2000);
            } else {
                formMessage.textContent = result.error || 'An error occurred.';
                formMessage.style.color = 'red';
            }
        } catch (error) {
            formMessage.textContent = 'An error occurred: ' + error.message;
            formMessage.style.color = 'red';
        }
    });
});
