/* Turn the Service Area screens' baked map into a real Leaflet map.

   The screens position everything - the BEU boundary, neighbouring DC areas, pincode
   cells, DC pins, shipment dots - in a 0-100 coordinate space over a baked raster of a
   known bounding box. That means the geography is already there; this file only has to
   project it back to lat/lng and hand it to Leaflet.

   Nothing here is required for the page to render. If Leaflet is missing, or tiles
   cannot be reached, the original raster and its overlays stay exactly as they are -
   which is why the raster is hidden only after the map is actually up. */
(function () {
  "use strict";

  // the bbox the raster was baked from
  var W = 77.6419, E = 77.7313, N = 12.9572, S = 12.9048;

  function toLatLng(x, y) {           // x,y in 0..100
    return [N - (y / 100) * (N - S), W + (x / 100) * (E - W)];
  }

  function parsePath(d) {
    var rings = [], cur = [];
    d.replace(/([MLZ])\s*([-\d.]+)?[, ]?\s*([-\d.]+)?/gi, function (_, cmd, a, b) {
      if (cmd.toUpperCase() === "Z") { if (cur.length) { rings.push(cur); cur = []; } }
      else if (a !== undefined && b !== undefined) { cur.push(toLatLng(parseFloat(a), parseFloat(b))); }
      return "";
    });
    if (cur.length) rings.push(cur);
    return rings;
  }

  function pct(el, prop) {
    var v = el.style[prop];
    return v && v.indexOf("%") > -1 ? parseFloat(v) : null;
  }

  function build(area) {
    if (typeof L === "undefined") return;            // library absent - keep the raster
    if (area.getAttribute("data-leaflet") === "1") return;
    area.setAttribute("data-leaflet", "1");

    var host = document.createElement("div");
    host.className = "vp-leaflet";
    area.insertBefore(host, area.firstChild);

    var map = L.map(host, {
      zoomControl: false, attributionControl: false,
      scrollWheelZoom: true, dragging: true
    });
    map.fitBounds([[S, W], [N, E]], { animate: false });

    // OpenStreetMap's own tiles. CARTO's Voyager style is a closer match for the Google
    // basemap live renders, but it now refuses to serve without an API key, and every
    // other close-styled provider (Stadia, Mapbox, Thunderforest) wants one too. Keyless
    // and dependable beats prettier-but-broken; the attribution line names OSM.
    var tiles = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19, crossOrigin: true
    }).addTo(map);

    // only stand down the raster once tiles have actually painted
    tiles.on("load", function () { area.classList.add("vp-leaflet-on"); });

    // --- the SVG boundary shapes
    function shapeFor(p) {
      var rings = parsePath(p.getAttribute("d") || "").filter(function (r) { return r.length > 2; });
      if (!rings.length) return null;
      return L.polygon(rings.length > 1 ? rings : rings[0], {
        color: p.getAttribute("stroke") || "#3b4fc4",
        // the source SVG uses vector-effect="non-scaling-stroke", so its stroke-width
        // is already in screen pixels - scaling it up was what thickened every outline
        weight: Math.max(0.8, parseFloat(p.getAttribute("stroke-width") || 1)),
        fillColor: p.getAttribute("fill") || "transparent",
        fillOpacity: 1, interactive: false, dashArray: p.getAttribute("stroke-dasharray") || null,
        vpBase: p.hasAttribute("data-area")
      });
    }

    function addShapes(svg, target) {
      if (!svg) return;
      Array.prototype.forEach.call(svg.querySelectorAll("path"), function (p) {
        var shape = shapeFor(p);
        if (!shape) return;
        // A path carrying data-area is one revision of the boundary in the Area Update
        // History; only the selected revision is on screen, so follow that rather than
        // stacking every revision on the map.
        if (p.hasAttribute("data-area")) {
          function sync() {
            var on = getComputedStyle(p).display !== "none";
            if (!on) { target.removeLayer ? target.removeLayer(shape) : map.removeLayer(shape); return; }
            shape.addTo(target);
            // the current area stays put; a revision being compared against it is drawn
            // over the top, the way live stacks the orange boundary on the blue one.
            if (p.getAttribute("data-area") !== "0") shape.bringToFront();
          }
          sync();
          // the serviceable area reads on top of the neighbouring DC areas
          if (shape._map) shape.bringToFront();
          new MutationObserver(sync).observe(p, { attributes: true, attributeFilter: ["style", "class"] });
        } else {
          shape.addTo(target);
        }
      });
    }
    // the overlay that sits straight on the map is always on; the ones inside a layer
    // belong to that layer and follow its checkbox
    var svg = null;
    Array.prototype.forEach.call(area.children, function (el) {
      if (!svg && el.classList && el.classList.contains("vp-mapoverlay")) svg = el;
    });
    addShapes(svg, map);

    // frame the way live does: on the serviceable area, not the whole baked bbox
    var main = svg && svg.querySelector('path[data-area="0"]');
    if (main) {
      var ring = parsePath(main.getAttribute("d") || "")[0];
      if (ring && ring.length > 2) map.fitBounds(L.latLngBounds(ring).pad(0.35), { animate: false });
    }

    function toMarker(el, group) {
      var x = pct(el, "left"), y = pct(el, "top");
      if (x === null || y === null) return;
      var box = el.getBoundingClientRect();
      var clone = el.cloneNode(true);
      clone.style.left = ""; clone.style.top = ""; clone.style.position = "static";
      L.marker(toLatLng(x, y), {
        interactive: false,
        icon: L.divIcon({
          html: clone.outerHTML, className: "vp-leaflet-pin",
          iconSize: [box.width || 12, box.height || 12],
          iconAnchor: [(box.width || 12) / 2, (box.height || 12) / 2]
        })
      }).addTo(group);
    }

    // pins that sit straight on the map, outside any toggled layer (the captain's own DC)
    var loose = L.layerGroup().addTo(map);
    Array.prototype.forEach.call(area.children, function (el) {
      if (el.classList && (el.classList.contains("vp-dcpin") ||
          el.classList.contains("vp-shipdot") || el.classList.contains("vp-shiptri"))) {
        toMarker(el, loose);
        el.style.visibility = "hidden";
      }
    });

    // --- pins and dots, each layer mirrored so the existing checkboxes keep working
    Array.prototype.forEach.call(area.querySelectorAll(".vp-lyr"), function (lyr) {
      var group = L.layerGroup();
      // measure while the layer is on screen, otherwise a hidden row has no size
      var wasHidden = getComputedStyle(lyr).display === "none";
      if (wasHidden) { lyr.style.visibility = "hidden"; lyr.style.display = "block"; }
      Array.prototype.forEach.call(lyr.children, function (el) {
        if (el.classList && el.classList.contains("vp-mapoverlay")) addShapes(el, group);
        else toMarker(el, group);
      });
      if (wasHidden) { lyr.style.display = "none"; lyr.style.visibility = ""; }
      function sync() {
        var on = getComputedStyle(lyr).display !== "none";
        if (on) { group.addTo(map); } else { map.removeLayer(group); }
      }
      sync();
      new MutationObserver(sync).observe(lyr, { attributes: true, attributeFilter: ["style", "class"] });
    });

    // the zoom buttons the screens already draw
    var zin = area.querySelector(".vp-mapzoom .zin"), zout = area.querySelector(".vp-mapzoom .zout");
    if (zin) zin.onclick = function () { map.zoomIn(); };
    if (zout) zout.onclick = function () { map.zoomOut(); };

    map.on("layeradd", function () {
      Array.prototype.forEach.call(area.querySelectorAll('path[data-area]'), function () {});
    });
    window.addEventListener("resize", function () { map.invalidateSize(); });
    setTimeout(function () {
      map.invalidateSize();
      map.eachLayer(function (l) { if (l.options && l.options.vpBase && l.bringToFront) l.bringToFront(); });
    }, 120);
  }

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll(".vp-maparea"), build);
  }
  window.vpInitServiceAreaMap = init;
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
