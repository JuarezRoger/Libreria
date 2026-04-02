document.addEventListener('DOMContentLoaded', function () {
    const addBtn = document.getElementById('addDashboardBtn');
    const container = document.getElementById('dashboardsContainer');
    const template = document.getElementById('dashboardCardTemplate');

    function uid() {
        return 'd-' + Math.random().toString(36).slice(2, 9);
    }

    function addDashboard() {
        const node = template.content.cloneNode(true);
        const wrapper = node.querySelector('.dashboard-card');
        const id = uid();
        wrapper.setAttribute('data-id', id);

        // Attach remove handler
        const removeBtn = node.querySelector('.remove-dashboard-btn');
        removeBtn.addEventListener('click', function (e) {
            const card = e.target.closest('.dashboard-card');
            if (card) card.remove();
        });

        container.prepend(node);
    }

    addBtn.addEventListener('click', addDashboard);

    // Add one example dashboard on first load if none
    if (container.children.length === 0) {
        addDashboard();
    }
});
