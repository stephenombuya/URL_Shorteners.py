// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    setupFormValidation();
    setupCopyButtons();
    initializeCharts();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form validation
function setupFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Copy to clipboard functionality
function setupCopyButtons() {
    const copyButtons = document.querySelectorAll('.copy-btn');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const textToCopy = this.getAttribute('data-copy');
            if (textToCopy) {
                try {
                    await navigator.clipboard.writeText(textToCopy);
                    showNotification('Copied to clipboard!', 'success');
                    
                    // Change button text temporarily
                    const originalText = this.innerHTML;
                    this.innerHTML = '✅ Copied!';
                    setTimeout(() => {
                        this.innerHTML = originalText;
                    }, 2000);
                } catch (err) {
                    showNotification('Failed to copy', 'error');
                }
            }
        });
    });
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification-toast`;
    notification.innerHTML = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.animation = 'slideIn 0.5s ease';
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.5s ease';
        setTimeout(() => {
            notification.remove();
        }, 500);
    }, 3000);
}

// URL shortening with AJAX
async function shortenUrl(longUrl, service, customCode = null) {
    const formData = new FormData();
    formData.append('long_url', longUrl);
    formData.append('service', service);
    if (customCode) formData.append('custom_code', customCode);
    
    showLoadingSpinner();
    
    try {
        const response = await fetch('/shorten', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) {
            showNotification(data.error, 'error');
            return null;
        }
        
        showNotification('URL shortened successfully!', 'success');
        return data;
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
        return null;
    } finally {
        hideLoadingSpinner();
    }
}

// Loading spinner
function showLoadingSpinner() {
    const spinner = document.createElement('div');
    spinner.id = 'loadingSpinner';
    spinner.className = 'spinner-overlay';
    spinner.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(spinner);
}

function hideLoadingSpinner() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) spinner.remove();
}

// Fetch analytics data
async function fetchAnalytics(shortCode) {
    showLoadingSpinner();
    
    try {
        const response = await fetch(`/api/analytics/${shortCode}`);
        const data = await response.json();
        
        if (data.error) {
            showNotification(data.error, 'error');
            return null;
        }
        
        return data;
    } catch (error) {
        showNotification('Error fetching analytics', 'error');
        return null;
    } finally {
        hideLoadingSpinner();
    }
}

// Initialize charts for analytics
function initializeCharts() {
    // This will be called when analytics page loads
    const chartCanvas = document.getElementById('hourlyChart');
    if (chartCanvas && window.hourlyData) {
        const ctx = chartCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: window.hourlyLabels || [],
                datasets: [{
                    label: 'Clicks',
                    data: window.hourlyData || [],
                    borderColor: 'rgb(102, 126, 234)',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Hourly Click Distribution'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }
}

// QR code download functionality
function downloadQRCode() {
    const qrImage = document.getElementById('qrCode');
    if (qrImage && qrImage.src) {
        const link = document.createElement('a');
        link.download = 'qrcode.png';
        link.href = qrImage.src;
        link.click();
        showNotification('QR Code downloaded!', 'success');
    }
}

// URL validation
function isValidUrl(string) {
    try {
        const url = new URL(string);
        return url.protocol === 'http:' || url.protocol === 'https:';
    } catch (_) {
        return false;
    }
}

// Real-time URL validation
function setupRealtimeValidation() {
    const urlInput = document.getElementById('longUrl');
    if (urlInput) {
        urlInput.addEventListener('input', function() {
            const url = this.value;
            const validationFeedback = document.getElementById('urlValidation');
            
            if (url && !isValidUrl(url)) {
                this.classList.add('is-invalid');
                if (validationFeedback) {
                    validationFeedback.textContent = 'Please enter a valid URL starting with http:// or https://';
                }
            } else {
                this.classList.remove('is-invalid');
                if (validationFeedback) {
                    validationFeedback.textContent = '';
                }
            }
        });
    }
}

// Auto-refresh history
function autoRefreshHistory() {
    const historyTable = document.getElementById('historyTable');
    if (historyTable) {
        setInterval(async () => {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                updateHistoryTable(data);
            } catch (error) {
                console.error('Error refreshing history:', error);
            }
        }, 30000); // Refresh every 30 seconds
    }
}

// Update history table dynamically
function updateHistoryTable(data) {
    const tbody = document.querySelector('#historyTable tbody');
    if (tbody && data.urls) {
        tbody.innerHTML = '';
        data.urls.forEach(url => {
            const row = tbody.insertRow();
            row.insertCell(0).textContent = url.code;
            row.insertCell(1).textContent = url.long_url.substring(0, 50) + '...';
            row.insertCell(2).textContent = url.clicks;
            row.insertCell(3).innerHTML = `<a href="/analytics/${url.code}" class="btn btn-sm btn-info">View</a>`;
        });
    }
}

// Export data as CSV
function exportToCSV(data, filename = 'analytics.csv') {
    if (!data || !data.length) {
        showNotification('No data to export', 'warning');
        return;
    }
    
    const headers = Object.keys(data[0]);
    const csvRows = [];
    
    csvRows.push(headers.join(','));
    
    for (const row of data) {
        const values = headers.map(header => {
            const escaped = ('' + row[header]).replace(/"/g, '\\"');
            return `"${escaped}"`;
        });
        csvRows.push(values.join(','));
    }
    
    const blob = new Blob(csvRows.join('\n'), { type: 'text/csv' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    URL.revokeObjectURL(link.href);
    
    showNotification('Data exported successfully!', 'success');
}

// Search/filter functionality
function setupSearchFilter() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const filter = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('#historyTable tbody tr');
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }
}

// Pagination
function setupPagination() {
    const itemsPerPage = 10;
    let currentPage = 1;
    const tableRows = document.querySelectorAll('#historyTable tbody tr');
    const totalPages = Math.ceil(tableRows.length / itemsPerPage);
    
    function showPage(page) {
        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        
        tableRows.forEach((row, index) => {
            row.style.display = (index >= start && index < end) ? '' : 'none';
        });
        
        updatePaginationControls(page, totalPages);
    }
    
    function updatePaginationControls(page, total) {
        const paginationDiv = document.getElementById('pagination');
        if (paginationDiv) {
            paginationDiv.innerHTML = `
                <button onclick="changePage(${page - 1})" ${page === 1 ? 'disabled' : ''}>Previous</button>
                <span>Page ${page} of ${total}</span>
                <button onclick="changePage(${page + 1})" ${page === total ? 'disabled' : ''}>Next</button>
            `;
        }
    }
    
    window.changePage = function(page) {
        if (page >= 1 && page <= totalPages) {
            currentPage = page;
            showPage(currentPage);
        }
    };
    
    if (tableRows.length > 0) {
        showPage(1);
    }
}

// Dark mode toggle
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDarkMode = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDarkMode);
    
    showNotification(isDarkMode ? 'Dark mode enabled' : 'Light mode enabled', 'info');
}

// Check for saved dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// Initialize all features
document.addEventListener('DOMContentLoaded', () => {
    setupRealtimeValidation();
    autoRefreshHistory();
    setupSearchFilter();
    setupPagination();
    
    // Add dark mode toggle button if not exists
    if (!document.querySelector('#darkModeToggle')) {
        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'darkModeToggle';
        toggleBtn.innerHTML = '🌙';
        toggleBtn.className = 'btn btn-secondary';
        toggleBtn.style.position = 'fixed';
        toggleBtn.style.bottom = '20px';
        toggleBtn.style.right = '20px';
        toggleBtn.style.zIndex = '1000';
        toggleBtn.onclick = toggleDarkMode;
        document.body.appendChild(toggleBtn);
    }
});

// Export functions for global use
window.shortenUrl = shortenUrl;
window.downloadQRCode = downloadQRCode;
window.exportToCSV = exportToCSV;
window.fetchAnalytics = fetchAnalytics;
window.showNotification = showNotification;
