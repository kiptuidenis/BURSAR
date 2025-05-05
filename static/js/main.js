// CSRF Token setup for AJAX requests
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

// Add CSRF token to all fetch requests
function fetchWithCSRF(url, options = {}) {
    const defaultOptions = {
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    };
    return fetch(url, { ...defaultOptions, ...options });
}

// Budget Category Management
class BudgetManager {
    static async editCategory(categoryId) {
        try {
            const response = await fetchWithCSRF(`/budget/category/${categoryId}`);
            const category = await response.json();
            
            // Populate and show edit modal
            document.getElementById('categoryName').value = category.name;
            document.getElementById('dailyAmount').value = category.daily_amount;
            
            const modal = new bootstrap.Modal(document.getElementById('addCategoryModal'));
            modal.show();
            
            // Update form action and submit button text
            const form = document.getElementById('addCategoryForm');
            form.action = `/budget/category/${categoryId}`;
            form.querySelector('button[type="submit"]').textContent = 'Update Category';
        } catch (error) {
            console.error('Error fetching category:', error);
            alert('Failed to load category details');
        }
    }

    static async deleteCategory(categoryId) {
        if (!confirm('Are you sure you want to delete this category?')) return;

        try {
            const response = await fetchWithCSRF(`/budget/category/${categoryId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                window.location.reload();
            } else {
                throw new Error('Failed to delete category');
            }
        } catch (error) {
            console.error('Error deleting category:', error);
            alert('Failed to delete category');
        }
    }
}

// MPESA Integration
class MPESAManager {
    static async initiateTransfer(amount) {
        try {
            const response = await fetchWithCSRF('/mpesa/transfer', {
                method: 'POST',
                body: JSON.stringify({ amount })
            });

            const result = await response.json();
            
            if (result.success) {
                this.checkTransactionStatus(result.transactionId);
            } else {
                throw new Error(result.message || 'Transfer failed');
            }
        } catch (error) {
            console.error('Error initiating transfer:', error);
            alert('Failed to initiate MPESA transfer');
        }
    }

    static async checkTransactionStatus(transactionId) {
        try {
            const response = await fetchWithCSRF(`/mpesa/status/${transactionId}`);
            const status = await response.json();

            if (status.pending) {
                // Check again in 5 seconds
                setTimeout(() => this.checkTransactionStatus(transactionId), 5000);
            } else if (status.success) {
                alert('Transfer completed successfully');
                window.location.reload();
            } else {
                throw new Error(status.message || 'Transaction failed');
            }
        } catch (error) {
            console.error('Error checking transaction status:', error);
            alert('Failed to verify transaction status');
        }
    }
}

// Form Validation
document.addEventListener('DOMContentLoaded', () => {
    // Phone number validation
    const phoneInput = document.querySelector('input[type="tel"]');
    if (phoneInput) {
        phoneInput.addEventListener('input', (e) => {
            const value = e.target.value.replace(/\D/g, '');
            if (value.length > 9) {
                e.target.value = value.slice(0, 9);
            } else {
                e.target.value = value;
            }
        });
    }

    // Budget form validation
    const budgetForms = document.querySelectorAll('form[id$="CategoryForm"]');
    budgetForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const amountInput = form.querySelector('input[name="daily_amount"]');
            if (amountInput && parseFloat(amountInput.value) <= 0) {
                e.preventDefault();
                alert('Amount must be greater than 0');
            }
        });
    });
});

// Dashboard Initialization
function initializeDashboard() {
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));

    // Initialize charts if needed
    // Add chart initialization code here if you decide to add charts
}

// Export functionality for use in other scripts
window.BudgetManager = BudgetManager;
window.MPESAManager = MPESAManager;
window.initializeDashboard = initializeDashboard;