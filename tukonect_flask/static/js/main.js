// Main JavaScript for Tukonect

document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme toggle
    initializeThemeToggle();
    
    // Initialize hide/show tabs functionality
    initializeTabsToggle();
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Message form auto-resize
    const messageTextareas = document.querySelectorAll('textarea[name="content"]');
    messageTextareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // Connection request handling
    const connectionButtons = document.querySelectorAll('.connection-btn');
    connectionButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const userId = this.dataset.userId;
            const action = this.dataset.action;
            
            if (action === 'send') {
                sendConnectionRequest(userId);
            } else if (action === 'accept') {
                acceptConnection(this.dataset.connectionId);
            } else if (action === 'reject') {
                rejectConnection(this.dataset.connectionId);
            }
        });
    });

    // Event participation handling
    const eventButtons = document.querySelectorAll('.event-btn');
    eventButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const eventId = this.dataset.eventId;
            const action = this.dataset.action;
            
            if (action === 'join') {
                joinEvent(eventId);
            } else if (action === 'leave') {
                leaveEvent(eventId);
            }
        });
    });
});

// Send connection request
function sendConnectionRequest(userId) {
    fetch(`/send-connection/${userId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            showAlert('Connection request sent!', 'success');
            location.reload();
        } else {
            showAlert('Error sending connection request', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error sending connection request', 'danger');
    });
}

// Accept connection
function acceptConnection(connectionId) {
    fetch(`/accept-connection/${connectionId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            showAlert('Connection accepted!', 'success');
            location.reload();
        } else {
            showAlert('Error accepting connection', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error accepting connection', 'danger');
    });
}

// Reject connection
function rejectConnection(connectionId) {
    fetch(`/reject-connection/${connectionId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            showAlert('Connection rejected', 'info');
            location.reload();
        } else {
            showAlert('Error rejecting connection', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error rejecting connection', 'danger');
    });
}

// Join event
function joinEvent(eventId) {
    fetch(`/join-event/${eventId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            showAlert('You are now attending this event!', 'success');
            location.reload();
        } else {
            showAlert('Error joining event', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error joining event', 'danger');
    });
}

// Leave event
function leaveEvent(eventId) {
    fetch(`/leave-event/${eventId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            showAlert('You have left this event', 'info');
            location.reload();
        } else {
            showAlert('Error leaving event', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error leaving event', 'danger');
    });
}

// Show alert message
function showAlert(message, type) {
    const alertContainer = document.querySelector('.container');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    alertContainer.insertBefore(alertDiv, alertContainer.firstChild);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

// Search functionality
function initializeSearch() {
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const searchableItems = document.querySelectorAll(this.dataset.target);
            
            searchableItems.forEach(function(item) {
                const text = item.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
}

// Initialize search on page load
document.addEventListener('DOMContentLoaded', initializeSearch);

// Theme toggle functionality
function initializeThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    
    if (!themeToggle || !themeIcon) return;
    
    // Get saved theme or default to light
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    
    // Add click event listener
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
        localStorage.setItem('theme', newTheme);
    });
}

function setTheme(theme) {
    const themeIcon = document.getElementById('themeIcon');
    
    if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeIcon.className = 'fas fa-sun';
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        themeIcon.className = 'fas fa-moon';
    }
}

// Collapse/Expand Sidebar functionality
function initializeTabsToggle() {
    const toggleButton = document.getElementById('toggleTabs');
    const toggleIcon = document.getElementById('toggleIcon');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    
    if (!toggleButton || !toggleIcon || !sidebar || !mainContent) return;
    
    // Get saved state or default to expanded
    const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    setSidebarState(isCollapsed);
    
    // Add click event listener
    toggleButton.addEventListener('click', function() {
        const currentlyCollapsed = sidebar.classList.contains('collapsed');
        const newState = !currentlyCollapsed;
        setSidebarState(newState);
        localStorage.setItem('sidebarCollapsed', newState.toString());
    });
}

function setSidebarState(collapsed) {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const toggleIcon = document.getElementById('toggleIcon');
    
    if (collapsed) {
        sidebar.classList.add('collapsed');
        mainContent.classList.add('sidebar-collapsed');
        toggleIcon.className = 'fas fa-chevron-right';
    } else {
        sidebar.classList.remove('collapsed');
        mainContent.classList.remove('sidebar-collapsed');
        toggleIcon.className = 'fas fa-chevron-left';
    }
}


