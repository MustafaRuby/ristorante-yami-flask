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

function getActionButtons(ordine) {
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

async function updateOrders() {
    try {
        const response = await fetch('/get_orders_data');
        if (!response.ok) throw new Error('Network response was not ok');
        const ordini = await response.json();
        
        const ordersGrid = document.querySelector('.orders-grid');
        ordersGrid.innerHTML = ordini.map(ordine => createOrderCard(ordine)).join('');
    } catch (error) {
        console.error('Error fetching orders:', error);
    }
}

// Aggiorna gli ordini ogni 5 secondi
setInterval(updateOrders, 5000);
