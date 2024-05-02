---
title: Dashboard
---


## Regenfall




```js
const world = await fetch("https://cdn.jsdelivr.net/npm/world-atlas@1/world/110m.json").then((response) => response.json());
const land = topojson.feature(world, world.objects.countries);

const countries = topojson.feature(world, world.objects.countries).features;
const switzerland = countries.find(d => d.id === "756");


// Assuming you're using D3 for additional adjustments
const projection = d3.geoMercator().fitSize([300, 300], switzerland);
const path = d3.geoPath(projection);
```

```js
const data = await FileAttachment("data/truncated.csv").csv({typed: true})
```

```js
Plot.plot({
    projection: projection,
    marks: [
        Plot.graticule(),
        Plot.geo(switzerland, {stroke: "var(--theme-foreground-faint)"}),
        Plot.dot(data, {x: "LONGITUDE", y: "LATITUDE",  stroke: "#f43f5e", size: "PRECIPITATION", fill: "var(--theme-foreground)", opacity: 0.6, radius: 2, title: "PRECIPITATION"})
    ]
})

```