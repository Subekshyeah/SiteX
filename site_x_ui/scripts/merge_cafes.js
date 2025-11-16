const fs = require('fs');
const path = require('path');

function parseCsvLine(line) {
  const out = [];
  let cur = '';
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && i + 1 < line.length && line[i + 1] === '"') {
        cur += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (ch === ',' && !inQuotes) {
      out.push(cur);
      cur = '';
    } else {
      cur += ch;
    }
  }
  out.push(cur);
  return out;
}

function parseCsv(text) {
  const lines = text.split(/\r?\n/).filter((l) => l.trim().length > 0);
  if (lines.length === 0) return [];
  const headers = parseCsvLine(lines[0]).map((h) => h.trim());
  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const cols = parseCsvLine(lines[i]);
    if (cols.length === 0) continue;
    const row = {};
    for (let j = 0; j < headers.length; j++) {
      row[headers[j]] = (cols[j] ?? '').trim();
    }
    rows.push(row);
  }
  return rows;
}

function squaredDegDist(lat1, lon1, lat2, lon2) {
  const dx = lat1 - lat2;
  const dy = lon1 - lon2;
  return dx * dx + dy * dy;
}

function merge(cafeGeoPath, csvPath, outPath) {
  const cafeGeo = fs.existsSync(cafeGeoPath) ? JSON.parse(fs.readFileSync(cafeGeoPath, 'utf8')) : { type: 'FeatureCollection', features: [] };
  const csvText = fs.existsSync(csvPath) ? fs.readFileSync(csvPath, 'utf8') : '';
  const csvRows = csvText ? parseCsv(csvText) : [];

  // index existing features by coordinate for quick lookup
  const features = (cafeGeo.features || []).slice();

  const usedCsv = new Set();

  for (const row of csvRows) {
    const lat = parseFloat(row.lat ?? row.Lat ?? row.latitude ?? '');
    const lon = parseFloat(row.lng ?? row.Lng ?? row.lon ?? row.longitude ?? '');
    let matched = null;
    if (Number.isFinite(lat) && Number.isFinite(lon)) {
      let bestDist = Infinity;
      for (const f of features) {
        const geom = f.geometry;
        if (!geom) continue;
        if (geom.type === 'Point' && Array.isArray(geom.coordinates)) {
          const [fx, fy] = geom.coordinates; // lon, lat
          const dist = squaredDegDist(fy, fx, lat, lon);
          if (dist < bestDist) {
            bestDist = dist;
            matched = f;
          }
        }
      }
      // threshold squared ~ (0.0005)^2
      if (matched && bestDist < 0.0005 * 0.0005) {
        // merge properties: csv overrides existing properties where present
        matched.properties = Object.assign({}, matched.properties || {}, row);
        usedCsv.add(row);
        continue;
      }
    }

    // no match: create new feature if lat/lon present
    if (Number.isFinite(lat) && Number.isFinite(lon)) {
      const feat = {
        type: 'Feature',
        geometry: { type: 'Point', coordinates: [Number(lon), Number(lat)] },
        properties: row,
      };
      features.push(feat);
      usedCsv.add(row);
    } else {
      // cannot place this row; add to properties-less list? skip
    }
  }

  const out = { type: 'FeatureCollection', features };
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(out, null, 2), 'utf8');
  console.log('Merged', features.length, 'features ->', outPath);
}

if (require.main === module) {
  const cafeGeoPath = path.join(__dirname, '..', 'data', 'cafe.geojson');
  const csvPath = path.join(__dirname, '..', 'data', 'compact_summary_images.csv');
  const outPath = path.join(__dirname, '..', 'data', 'merged_cafes.geojson');
  merge(cafeGeoPath, csvPath, outPath);
}
