// Admin Panel Shared Logic
document.addEventListener('DOMContentLoaded', function() {
    console.log('Admin JS loaded');
    
    // Check if user is logged in
    const token = localStorage.getItem('auth_token');
    if (!token && window.location.pathname.includes('/admin/') && !window.location.pathname.includes('login')) {
        window.location.href = '/admin/login.html';
    }
    
    // Logout functionality
    const logoutLink = document.getElementById('logout');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            localStorage.removeItem('auth_token');
            window.location.href = '/admin/login.html';
        });
    }
    
    // Load stats overview
    const statsContainer = document.getElementById('stats-overview');
    if (statsContainer) {
        loadStats();
    }
    
    // Load requests table
    const requestsTable = document.getElementById('requests-table');
    if (requestsTable) {
        loadRequests();
    }
    
    // Load customers table
    const customersTable = document.getElementById('customers-table');
    if (customersTable) {
        loadCustomers();
    }
    
    // Load home services table
    const homeServicesTable = document.getElementById('home-services-table');
    if (homeServicesTable) {
        loadHomeServices();
    }
});

async function loadStats() {
    try {
        const response = await fetch('/api/admin/stats', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            const container = document.getElementById('stats-overview');
            container.innerHTML = `
                <div class="stat-card">
                    <h3>Total Requests</h3>
                    <div class="value">${data.total_requests}</div>
                </div>
                <div class="stat-card">
                    <h3>Pending Requests</h3>
                    <div class="value">${data.pending_requests}</div>
                </div>
                <div class="stat-card">
                    <h3>Total Customers</h3>
                    <div class="value">${data.total_customers}</div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function loadRequests() {
    // Implementation for loading requests
    console.log('Loading requests...');
}

async function loadCustomers() {
    // Implementation for loading customers
    console.log('Loading customers...');
}

async function loadHomeServices() {
    // Implementation for loading home services
    console.log('Loading home services...');
}
