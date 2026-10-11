/* Switches between promoted versions on one page. See .vsw in wireframe.css.
 *
 * Several designs for the same problem belong at one URL: comparing them
 * means flicking between them in the same spot, and separate tabs lose both
 * the alignment and the thread of the argument.
 *
 * Keyboard: 1-9 jump to a version, left/right step through them. The current
 * one is written to the hash, so a link can point at a specific version and
 * a reload keeps your place.
 */
(function () {
  var bar = document.querySelector(".vsw");
  if (!bar) return;
  var buttons = [].slice.call(bar.querySelectorAll("button[data-v]"));
  if (!buttons.length) return;

  function show(v) {
    var found = false;
    buttons.forEach(function (b) {
      var on = b.getAttribute("data-v") === v;
      b.classList.toggle("on", on);
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (on) found = true;
    });
    if (!found) return;
    document.querySelectorAll(".vsw-pane").forEach(function (p) {
      p.hidden = p.id !== v;
    });
    var t = bar.querySelector(".vsw-t");
    var active = buttons.filter(function (b) { return b.classList.contains("on"); })[0];
    if (t && active && active.dataset.title) t.textContent = active.dataset.title;
    // replaceState, not a hash assignment: a hash jump would scroll the page
    // to the pane and lose the reader's position, which is the one thing
    // comparing two designs depends on.
    if (history.replaceState) history.replaceState(null, "", "#" + v);
  }

  buttons.forEach(function (b) {
    b.addEventListener("click", function () { show(b.getAttribute("data-v")); });
  });

  document.addEventListener("keydown", function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var tag = (e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || e.target.isContentEditable) return;
    var i = buttons.findIndex(function (b) { return b.classList.contains("on"); });
    if (/^[1-9]$/.test(e.key) && buttons[+e.key - 1]) {
      show(buttons[+e.key - 1].getAttribute("data-v"));
    } else if (e.key === "ArrowRight" && buttons[i + 1]) {
      show(buttons[i + 1].getAttribute("data-v"));
    } else if (e.key === "ArrowLeft" && buttons[i - 1]) {
      show(buttons[i - 1].getAttribute("data-v"));
    } else { return; }
    e.preventDefault();
  });

  var start = location.hash.slice(1);
  show(buttons.some(function (b) { return b.getAttribute("data-v") === start; })
       ? start : buttons[0].getAttribute("data-v"));
  // A hash in the URL makes the browser scroll to that pane on load, which
  // pushes the switcher off the top and clips the rail. The hash is for
  // choosing a version, not for jumping to one.
  window.scrollTo(0, 0);
})();
