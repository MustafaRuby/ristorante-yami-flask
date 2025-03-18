// Main JavaScript file for handling orders functionality (both chef and admin views)

// Get configuration passed from the template
const isAdmin = window.pageConfig ? window.pageConfig.isAdmin : false;
const tavoloId = window.pageConfig ? window.pageConfig.tavoloId : null;

// Create HTML for order cards - used by the auto-refresh for chef view
function createOrderCard(ordine) {
    return `
        <div class="order-card">
            <div class="order-header">
                <h3>Tavolo #${ordine.tavolo_numero}</h3>
            </div>
            <div class="order-content">
                <img src="/static/${ordine.piatto.immagine}" alt="${ordine.piatto.nome}" class="order-image">
                <div class="order-details">
                    <div class="order-name">${ordine.piatto.nome}</div>
                    <div class="order-quantity">Quantità: ${ordine.quantita}</div>
                    <div class="order-status status-${ordine.stato.nome}">
                        ${ordine.stato.nome.charAt(0).toUpperCase() + ordine.stato.nome.slice(1)}
                    </div>
                    
                    <div class="status-actions">
                        ${getActionButtons(ordine)}
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Generate action buttons based on order state - used by the auto-refresh for chef view
function getActionButtons(ordine) {
    // Don't show action buttons for admin users
    if (isAdmin) {
        return '';
    }
    
    if (ordine.stato.nome === 'preparazione') {
        return `
            <form action="/update_order_status" method="POST" style="display: inline;">
                <input type="hidden" name="ordine_id" value="${ordine.id}">
                <input type="hidden" name="action" value="complete">
                <button type="submit" class="action-button complete-btn">Completa</button>
            </form>
            <form action="/update_order_status" method="POST" style="display: inline;">
                <input type="hidden" name="ordine_id" value="${ordine.id}">
                <input type="hidden" name="action" value="suspend">
                <button type="submit" class="action-button suspend-btn">Sospendi</button>
            </form>
        `;
    } else if (ordine.stato.nome === 'completato') {
        return `
            <form action="/update_order_status" method="POST">
                <input type="hidden" name="ordine_id" value="${ordine.id}">
                <input type="hidden" name="action" value="deliver">
                <button type="submit" class="action-button deliver-btn">Consegna</button>
            </form>
        `;
    }
    return '';
}

// Fetch orders data from the server and update the UI
async function updateOrders() {
    // Only update orders automatically if we're on the chef view
    if (!isAdmin) {
        try {
            const response = await fetch('/get_orders_data');
            if (!response.ok) throw new Error('Network response was not ok');
            const ordini = await response.json();
            
            const ordersGrid = document.querySelector('.orders-grid');
            if (ordersGrid) {
                ordersGrid.innerHTML = ordini.map(ordine => createOrderCard(ordine)).join('');
            }
        } catch (error) {
            console.error('Error fetching orders:', error);
        }
    }
}

// Initialize and set up auto-refresh
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the chef page by looking for specific elements
    const isChefPage = document.querySelector('.chef-header') && 
                      !document.querySelector('.tavolo-info');
    
    if (isChefPage && !isAdmin) {
        // Initial load
        updateOrders();
        
        // Set up interval for chef view only
        setInterval(updateOrders, 5000);
    }
});
