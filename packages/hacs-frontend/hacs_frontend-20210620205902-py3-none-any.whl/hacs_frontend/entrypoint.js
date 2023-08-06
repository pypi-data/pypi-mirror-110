
try {
  new Function("import('/hacsfiles/frontend/main-22e9dfb2.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-22e9dfb2.js';
  document.body.appendChild(el);
}
  