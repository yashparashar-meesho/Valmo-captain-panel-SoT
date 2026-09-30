/* DC Capacity — the behaviour behind the two capacity fields.
 *
 * Vendored rather than inlined into the screen's markup, the same way sa-map.js is:
 * the catalogue's seed stays reviewable markup, and this logic has one home to be
 * fixed in. The screen carries only the numbers it is judged against, as data-rec on
 * each card and data-total naming its cell in the action bar.
 *
 * Measured off the live panel, not documented anywhere:
 *   - the workable band is the recommendation +/- 20%
 *   - below it, the shortfall is simply recommendation - value
 *   - above it, live works out at roughly one extra pilot per 50 orders. That figure
 *     is fitted from sampled values and matches live at 1499 (5) and 1990 (15); it
 *     can be off by a pilot at the extremes.
 */
(function () {
  "use strict";

  var PER_PILOT = 50;
  var BAND = 0.2;

  var WARN = '<svg viewBox="0 0 14 14" fill="none" aria-hidden="true">' +
    '<path d="M7 1.6 13 12.4H1z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>' +
    '<path d="M7 5.6v3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>' +
    '<circle cx="7" cy="10.4" r="0.7" fill="currentColor"/></svg>';

  var GOOD = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">' +
    '<path d="M5 7.4 7.4 2c1 0 1.7.7 1.7 1.6v2.1h3.4c.8 0 1.4.7 1.2 1.5l-.8 4c-.1.6-.6 1-1.2 1H5z" fill="currentColor"/>' +
    '<rect x="1.9" y="7.2" width="2.4" height="6.4" rx="0.8" fill="currentColor" opacity=".55"/></svg>';

  function group(n) { return n.toLocaleString("en-IN"); }

  function wire(sec) {
    var rec = Number(sec.getAttribute("data-rec"));
    var input = sec.querySelector("input");
    var msg = sec.querySelector(".vp-dcc-msg");
    var total = document.getElementById(sec.getAttribute("data-total"));
    if (!rec || !input || !msg) return;

    var label = input.getAttribute("aria-label") || "";
    var noun = label.indexOf("deliver") > -1 ? "deliveries" : "pickups";
    /* live leaves the bar dashed until the captain actually changes something */
    var touched = false;

    function render() {
      var raw = String(input.value).trim();
      if (raw === "") {
        msg.hidden = true;
        if (touched && total) total.textContent = "-";
        return;
      }
      var n = Number(raw);
      if (!isFinite(n)) return;

      msg.hidden = false;
      if (touched && total) total.textContent = group(n) + " Orders/Day";

      if (n < rec * (1 - BAND)) {
        msg.className = "vp-dcc-msg";
        msg.innerHTML = WARN + "<span>Input is very low, you can do " +
          group(rec - n) + " more orders with your active pilots</span>";
      } else if (n > rec * (1 + BAND)) {
        var pilots = Math.max(1, Math.round((n - rec) / PER_PILOT));
        msg.className = "vp-dcc-msg";
        msg.innerHTML = WARN + "<span>Input is very high, you will need " + pilots +
          " extra pilot" + (pilots === 1 ? "" : "s") + " to do these " + noun + "</span>";
      } else {
        msg.className = "vp-dcc-msg good";
        msg.innerHTML = GOOD + "<span>Best capacity for you, your earnings will increase</span>";
      }
    }

    input.addEventListener("input", function () { touched = true; render(); });
    render();
  }

  function start() {
    Array.prototype.forEach.call(
      document.querySelectorAll(".vp-dcc-sec[data-rec]"), wire);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
