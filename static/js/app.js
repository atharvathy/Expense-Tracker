/**
 * ExpenseTracker Frontend Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    // State management
    let categoryChartInstance = null;
    let trendChartInstance = null;

    // DOM Elements
    const totalIncomeEl = document.getElementById('totalIncome');
    const totalExpenseEl = document.getElementById('totalExpense');
    const netBalanceEl = document.getElementById('netBalance');
    const savingsRateEl = document.getElementById('savingsRate');
    
    const budgetGridEl = document.getElementById('budgetGrid');
    const transactionsTableBody = document.getElementById('transactionsTableBody');
    const transCountEl = document.getElementById('transCount');
    const emptyStateEl = document.getElementById('emptyState');

    // Filter controls
    const searchInput = document.getElementById('searchInput');
    const filterType = document.getElementById('filterType');
    const filterCategory = document.getElementById('filterCategory');
    const btnResetFilters = document.getElementById('btnResetFilters');

    // Modals & Buttons
    const btnOpenAddModal = document.getElementById('btnOpenAddModal');
    const btnOpenBudgetModal = document.getElementById('btnOpenBudgetModal');

    const transactionModal = document.getElementById('transactionModal');
    const budgetModal = document.getElementById('budgetModal');

    const transactionForm = document.getElementById('transactionForm');
    const budgetForm = document.getElementById('budgetForm');

    // Initialize application
    initApp();

    function initApp() {
        // Set today's date in transaction form by default
        document.getElementById('date').value = new Date().toISOString().split('T')[0];

        // Event Listeners
        setupEventListeners();

        // Load data
        refreshAllData();
    }

    function setupEventListeners() {
        // Tab navigation between Page 1 (Dashboard) and Page 2 (Transactions)
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.page-view').forEach(v => v.classList.add('hidden'));

                tab.classList.add('active');
                const targetId = tab.dataset.target;
                const targetView = document.getElementById(targetId);
                if (targetView) {
                    targetView.classList.remove('hidden');
                }
            });
        });

        // Modals
        if (btnOpenAddModal) btnOpenAddModal.addEventListener('click', () => openTransactionModal());
        if (btnOpenBudgetModal) btnOpenBudgetModal.addEventListener('click', () => budgetModal.classList.remove('hidden'));

        document.querySelectorAll('.close-modal').forEach(btn => {
            btn.addEventListener('click', () => {
                transactionModal.classList.add('hidden');
                budgetModal.classList.add('hidden');
            });
        });

        // Close modal on background click
        [transactionModal, budgetModal].forEach(modal => {
            if (modal) {
                modal.addEventListener('click', (e) => {
                    if (e.target === modal) modal.classList.add('hidden');
                });
            }
        });

        // Filters
        let searchTimeout;
        searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(loadTransactions, 300);
        });
        filterType.addEventListener('change', loadTransactions);
        filterCategory.addEventListener('change', loadTransactions);

        btnResetFilters.addEventListener('click', () => {
            searchInput.value = '';
            filterType.value = 'All';
            filterCategory.value = 'All';
            loadTransactions();
        });

        // Form submissions
        transactionForm.addEventListener('submit', handleTransactionSubmit);
        budgetForm.addEventListener('submit', handleBudgetSubmit);
    }

    function refreshAllData() {
        loadSummary();
        loadBudgets();
        loadTransactions();
    }

    // ------------------ API CALLS & RENDERING ------------------ //

    async function loadSummary() {
        try {
            const res = await fetch('/api/summary');
            const data = await res.json();

            totalIncomeEl.textContent = `${data.total_income.toLocaleString('en-US', { minimumFractionDigits: 2 })}`;
            totalExpenseEl.textContent = `${data.total_expense.toLocaleString('en-US', { minimumFractionDigits: 2 })}`;
            
            const netFormatted = `${Math.abs(data.net_balance).toLocaleString('en-US', { minimumFractionDigits: 2 })}`;
            netBalanceEl.textContent = data.net_balance < 0 ? `-${netFormatted}` : netFormatted;
            netBalanceEl.className = `metric-value ${data.net_balance < 0 ? 'text-expense' : 'text-income'}`;

            savingsRateEl.textContent = `${data.savings_rate.toFixed(1)}%`;

            loadPlotlyCharts();
        } catch (err) {
            console.error('Failed to load summary', err);
        }
    }

    async function loadPlotlyCharts() {
        try {
            const res = await fetch('/api/plotly-charts');
            const charts = await res.json();

            if (charts.category_chart && window.Plotly) {
                Plotly.react('categoryChart', charts.category_chart.data, charts.category_chart.layout, { responsive: true, displayModeBar: false });
            }
            if (charts.trend_chart && window.Plotly) {
                Plotly.react('trendChart', charts.trend_chart.data, charts.trend_chart.layout, { responsive: true, displayModeBar: false });
            }
        } catch (err) {
            console.error('Failed to load Plotly charts', err);
        }
    }

    async function loadBudgets() {
        try {
            const res = await fetch('/api/budgets');
            const budgets = await res.json();

            budgetGridEl.innerHTML = '';
            if (budgets.length === 0) {
                budgetGridEl.innerHTML = '<p class="text-muted">No budget limits configured.</p>';
                return;
            }

            budgets.forEach(b => {
                let fillClass = 'fill-safe';
                if (b.percentage >= 100) fillClass = 'fill-over';
                else if (b.percentage >= 80) fillClass = 'fill-warn';

                const card = document.createElement('div');
                card.className = 'budget-item';
                card.innerHTML = `
                    <div class="budget-header">
                        <span>${escapeHtml(b.category)}</span>
                    </div>
                    <div class="budget-amounts">
                        Spent ${b.spent.toFixed(2)} of ${b.monthly_limit.toFixed(2)}
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill ${fillClass}" style="width: ${Math.min(b.percentage, 100)}%"></div>
                    </div>
                `;
                budgetGridEl.appendChild(card);
            });
        } catch (err) {
            console.error('Failed to load budgets', err);
        }
    }

    async function loadTransactions() {
        const queryParams = new URLSearchParams();
        if (filterType.value !== 'All') queryParams.append('type', filterType.value);
        if (filterCategory.value !== 'All') queryParams.append('category', filterCategory.value);
        if (searchInput.value.trim()) queryParams.append('search', searchInput.value.trim());

        try {
            const res = await fetch(`/api/transactions?${queryParams.toString()}`);
            const transactions = await res.json();

            transCountEl.textContent = `${transactions.length} item${transactions.length !== 1 ? 's' : ''}`;
            transactionsTableBody.innerHTML = '';

            if (transactions.length === 0) {
                emptyStateEl.classList.remove('hidden');
                return;
            } else {
                emptyStateEl.classList.add('hidden');
            }

            transactions.forEach(t => {
                const tr = document.createElement('tr');
                const isIncome = t.type === 'Income';
                const sign = isIncome ? '+' : '-';
                const amtClass = isIncome ? 'text-income' : 'text-expense';
                const tagClass = isIncome ? 'tag-income' : 'tag-expense';

                tr.innerHTML = `
                    <td>${t.date}</td>
                    <td>
                        <strong>${escapeHtml(t.title)}</strong>
                        ${t.note ? `<br><small class="text-muted">${escapeHtml(t.note)}</small>` : ''}
                    </td>
                    <td>${escapeHtml(t.category)}</td>
                    <td><small class="text-muted">${t.payment_method || 'Cash'}</small></td>
                    <td><span class="type-tag ${tagClass}">${t.type}</span></td>
                    <td class="text-right ${amtClass}"><strong>${sign}${t.amount.toFixed(2)}</strong></td>
                    <td class="text-center">
                        <div class="action-btns">
                            <button class="btn-action edit-btn" data-id="${t.id}" title="Edit"><i class="fa-solid fa-pen-to-square"></i></button>
                            <button class="btn-action delete delete-btn" data-id="${t.id}" title="Delete"><i class="fa-solid fa-trash-can"></i></button>
                        </div>
                    </td>
                `;
                transactionsTableBody.appendChild(tr);
            });

            // Bind edit/delete handlers
            document.querySelectorAll('.edit-btn').forEach(btn => {
                btn.addEventListener('click', () => editTransaction(btn.dataset.id));
            });
            document.querySelectorAll('.delete-btn').forEach(btn => {
                btn.addEventListener('click', () => deleteTransaction(btn.dataset.id));
            });

        } catch (err) {
            console.error('Failed to load transactions', err);
        }
    }

    // ------------------ CHARTS ------------------ //

    function renderCategoryChart(categoryData) {
        const ctx = document.getElementById('categoryChart').getContext('2d');
        const labels = Object.keys(categoryData);
        const values = Object.values(categoryData);

        const colors = [
            '#3b82f6', '#ef4444', '#10b981', '#f59e0b', 
            '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16', '#f97316'
        ];

        if (categoryChartInstance) {
            categoryChartInstance.destroy();
        }

        categoryChartInstance = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels.length ? labels : ['No Expense Data'],
                datasets: [{
                    data: values.length ? values : [1],
                    backgroundColor: values.length ? colors.slice(0, labels.length) : ['#e2e8f0'],
                    borderWidth: 0,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: { color: '#475569', font: { family: 'Outfit', size: 12.5, weight: '500' } }
                    }
                },
                cutout: '72%'
            }
        });
    }

    function renderTrendChart(monthlyTrend) {
        const ctx = document.getElementById('trendChart').getContext('2d');
        const months = Object.keys(monthlyTrend);
        const incomeData = months.map(m => monthlyTrend[m].income);
        const expenseData = months.map(m => monthlyTrend[m].expense);

        if (trendChartInstance) {
            trendChartInstance.destroy();
        }

        trendChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: months.length ? months : ['Current'],
                datasets: [
                    {
                        label: 'Income',
                        data: incomeData,
                        backgroundColor: '#10b981',
                        borderRadius: 6
                    },
                    {
                        label: 'Expense',
                        data: expenseData,
                        backgroundColor: '#f43f5e',
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        ticks: { color: '#64748b', font: { family: 'Outfit' } },
                        grid: { display: false }
                    },
                    y: {
                        ticks: { color: '#64748b', font: { family: 'Outfit' } },
                        grid: { color: 'rgba(0, 0, 0, 0.04)' }
                    }
                },
                plugins: {
                    legend: {
                        labels: { color: '#475569', font: { family: 'Outfit', size: 12.5, weight: '500' } }
                    }
                }
            }
        });
    }

    // ------------------ FORMS & MODAL CONTROLLERS ------------------ //

    function openTransactionModal(trans = null) {
        document.getElementById('modalTitle').innerHTML = trans 
            ? '<i class="fa-solid fa-pen-to-square"></i> Edit Transaction' 
            : '<i class="fa-solid fa-receipt"></i> Add Transaction';

        document.getElementById('transId').value = trans ? trans.id : '';
        document.getElementById('title').value = trans ? trans.title : '';
        document.getElementById('amount').value = trans ? trans.amount : '';
        document.getElementById('category').value = trans ? trans.category : 'Food & Dining';
        document.getElementById('date').value = trans ? trans.date : new Date().toISOString().split('T')[0];
        document.getElementById('paymentMethod').value = trans ? trans.payment_method : 'Cash';
        document.getElementById('note').value = trans ? trans.note : '';

        if (trans && trans.type === 'Income') {
            document.getElementById('typeIncome').checked = true;
        } else {
            document.getElementById('typeExpense').checked = true;
        }

        transactionModal.classList.remove('hidden');
    }

    async function editTransaction(id) {
        try {
            const res = await fetch(`/api/transactions/${id}`);
            if (res.ok) {
                const trans = await res.json();
                openTransactionModal(trans);
            }
        } catch (err) {
            showToast('Failed to fetch transaction details', 'error');
        }
    }

    async function deleteTransaction(id) {
        if (!confirm('Are you sure you want to delete this transaction?')) return;
        try {
            const res = await fetch(`/api/transactions/${id}`, { method: 'DELETE' });
            const data = await res.json();
            if (data.success) {
                showToast('Transaction deleted successfully', 'success');
                refreshAllData();
            } else {
                showToast(data.error || 'Failed to delete', 'error');
            }
        } catch (err) {
            showToast('Network error while deleting', 'error');
        }
    }

    async function handleTransactionSubmit(e) {
        e.preventDefault();
        const id = document.getElementById('transId').value;
        const type = document.querySelector('input[name="type"]:checked').value;
        const title = document.getElementById('title').value;
        const amount = document.getElementById('amount').value;
        const category = document.getElementById('category').value;
        const date = document.getElementById('date').value;
        const payment_method = document.getElementById('paymentMethod').value;
        const note = document.getElementById('note').value;

        const payload = { title, amount, type, category, date, payment_method, note };

        const url = id ? `/api/transactions/${id}` : '/api/transactions';
        const method = id ? 'PUT' : 'POST';

        try {
            const res = await fetch(url, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (data.success) {
                showToast(id ? 'Transaction updated' : 'Transaction added', 'success');
                transactionModal.classList.add('hidden');
                transactionForm.reset();
                refreshAllData();
            } else {
                showToast(data.error || 'Failed to save', 'error');
            }
        } catch (err) {
            showToast('Network error while saving transaction', 'error');
        }
    }

    async function handleBudgetSubmit(e) {
        e.preventDefault();
        const category = document.getElementById('budgetCategory').value;
        const limit = document.getElementById('budgetLimit').value;

        try {
            const res = await fetch('/api/budgets', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ category, limit })
            });
            const data = await res.json();
            if (data.success) {
                showToast(data.message, 'success');
                budgetModal.classList.add('hidden');
                budgetForm.reset();
                loadBudgets();
            } else {
                showToast(data.error || 'Failed to set budget', 'error');
            }
        } catch (err) {
            showToast('Network error while setting budget', 'error');
        }
    }

    async function handleImportSubmit(e) {
        e.preventDefault();
        const fileInput = document.getElementById('importFile');
        if (!fileInput.files.length) return;

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const res = await fetch('/api/import', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            if (data.success) {
                showToast(data.message, 'success');
                importModal.classList.add('hidden');
                importForm.reset();
                refreshAllData();
            } else {
                showToast(data.error || 'Import failed', 'error');
            }
        } catch (err) {
            showToast('Error uploading import file', 'error');
        }
    }

    // ------------------ UTILS ------------------ //

    function showToast(message, type = 'success') {
        const toastContainer = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <i class="fa-solid ${type === 'success' ? 'fa-circle-check text-income' : 'fa-triangle-exclamation text-expense'}"></i>
            <span>${escapeHtml(message)}</span>
        `;
        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3500);
    }

    function escapeHtml(str) {
        return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
});
