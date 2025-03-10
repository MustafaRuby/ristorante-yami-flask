## Schema del database

[Tavolo]: ID_tavolo (PK) [INT], numero_tavolo [INT], password [VARCHAR(100)]

//Ci sono 100 tavoli

[Piatto]: ID_piatto (PK) [INT], nome [VARCHAR(100)], ingredienti [VARCHAR(500)], nome_immagine [VARCHAR(500)]

[Stato]: ID_Stato (PK) [INT], nome [VARCHAR(2)]

[Ordine]: ID_ordine (PK) [INT], ID_piatto (FK1) [INT], ID_tavolo (FK2) [INT], ID_stato (FK3) [INT],  quantita [INT]

[Chef]: ID_chef (PK) [INT], nome [VARCHAR], password

//Stato può essere "preparazione", e indica che l'ordine non è ancora stato completato. Se stato è "completato" significa che è finito il piatto. Se stato è "consegnato" indica che è stato consegnato al tavolo il piatto.

