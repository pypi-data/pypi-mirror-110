
try {
  new Function("import('/hacsfiles/frontend/main-ef294d92.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-ef294d92.js';
  document.body.appendChild(el);
}
  