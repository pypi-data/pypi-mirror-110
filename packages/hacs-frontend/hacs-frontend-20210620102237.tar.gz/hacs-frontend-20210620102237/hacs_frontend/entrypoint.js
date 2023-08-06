
try {
  new Function("import('/hacsfiles/frontend/main-b9893c22.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-b9893c22.js';
  document.body.appendChild(el);
}
  