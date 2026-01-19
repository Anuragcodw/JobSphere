let jobMap = null;   // global reference (important)

function initJobMap(lat, lon) {

    // ===== 1. FORCE NUMBER =====
    lat = Number(lat);
    lon = Number(lon);

    if (Number.isNaN(lat) || Number.isNaN(lon)) {
        console.warn("Invalid coordinates for map:", lat, lon);
        return;
    }

    const mapContainer = document.getElementById("job-map");
    if (!mapContainer) {
        console.warn("No #job-map element found.");
        return;
    }

    // ===== 2. DESTROY OLD MAP (SAFE WAY) =====
    if (jobMap) {
        jobMap.off();
        jobMap.remove();
        jobMap = null;
    }

    // Leaflet internal cleanup (CRITICAL)
    if (mapContainer._leaflet_id) {
        mapContainer._leaflet_id = null;
    }

    mapContainer.innerHTML = "";

    // ===== 3. CREATE MAP (USE ID STRING, NOT ELEMENT) =====
    jobMap = L.map("job-map", {
        center: [lat, lon],
        zoom: 13,
        zoomControl: true,
        attributionControl: true
    });

    // ===== 4. TILE LAYER =====
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        crossOrigin: true
    }).addTo(jobMap);

    // ===== 5. MARKER =====
    const marker = L.marker([lat, lon]).addTo(jobMap);

    const directionsUrl =
        `https://www.google.com/maps/dir/?api=1&destination=${lat},${lon}`;

    marker.bindPopup(`
        <div style="font-size:0.85rem;">
            <strong>Job location</strong><br>
            <a href="${directionsUrl}" target="_blank"
               style="color:#3b82f6;text-decoration:none;">
                🧭 Open directions in Google Maps
            </a>
        </div>
    `);

    // ===== 6. FORCE PROPER RENDER (THIS FIXES BLANK MAP) =====
    setTimeout(() => {
        jobMap.invalidateSize(true);
        jobMap.setView([lat, lon], 13);
    }, 500);
}
