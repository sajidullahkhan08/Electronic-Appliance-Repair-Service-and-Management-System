// Request Form Logic
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('repair-form');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            
            try {
                const response = await fetch('/api/requests', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    alert('Request submitted successfully!');
                    form.reset();
                } else {
                    alert('Error submitting request');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error submitting request');
            }
        });
    }
});
