// Tracking Page Logic
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('tracking-form');
    const resultDiv = document.getElementById('tracking-result');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const trackingId = form.querySelector('input').value;
            
            try {
                const response = await fetch(`/api/tracking/${trackingId}`);
                
                if (response.ok) {
                    const data = await response.json();
                    resultDiv.innerHTML = `
                        <h3>Repair Status</h3>
                        <p>Status: ${data.status}</p>
                        <p>Date: ${data.date}</p>
                        <p>Details: ${data.details}</p>
                    `;
                } else {
                    resultDiv.innerHTML = '<p>Repair request not found</p>';
                }
            } catch (error) {
                console.error('Error:', error);
                resultDiv.innerHTML = '<p>Error fetching tracking information</p>';
            }
        });
    }
});
