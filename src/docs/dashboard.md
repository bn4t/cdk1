---
title: Dashboard
---

```js
const data = FileAttachment("data/agri4cast.csv").csv({typed: true})
console.log(data)
```

## Regenfall

```js

Plot.dot(data, {x: (d) => d.YEAR*366+d.DOY, y: "RAIN", tip: true}).plot()

```

## Wind

```js
Plot.dot(data, {x: (d) => d.YEAR*366+d.DOY, y: "WIND", stroke: "GRID_NO"}).plot()

```