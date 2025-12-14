async function loadItems() {
  try {
    const res = await fetch('/api/items');
    const items = await res.json();
    const ul = document.getElementById('items');
    ul.innerHTML = '';
    if (items.length === 0) {
      ul.innerHTML = '<li>Aucun item trouvé</li>';
      return;
    }
    items.forEach(item => {
      const li = document.createElement('li');
      li.textContent = item.id + ' - ' + item.title + ': ' + (item.description || '(pas de description)');
      ul.appendChild(li);
    });
  } catch (e) {
    document.getElementById('items').innerHTML = '<li class=\"error\">Erreur: ' + e + '</li>';
  }
}
loadItems();
setInterval(loadItems, 5000);
