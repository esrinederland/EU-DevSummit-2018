import EsriMap = require("esri/Map");
import MapView = require("esri/views/MapView");

const map = new EsriMap({
  basemap: "dark-gray"
});

const view = new MapView({
  map: map,
  container: "viewDiv",
  center: [6.1, 52.5],
  zoom: 12
});

import Graphic = require("esri/Graphic");
import Point = require("esri/geometry/Point");

//Create a point
var point = new Point({
  x: 6.0920377,
  y: 52.5028158
});

// Create a symbol for drawing the point
var markerSymbol = {
  type: "simple-marker",
  outline: {
    width: 2,
    color: [255, 255, 255, 1]
  },
  color: [255, 170, 0, 1]
};

// Create a graphic and add the geometry and symbol to it
var pointGraphic = new Graphic({
  geometry: point,
  symbol: markerSymbol
});

view.graphics.add(pointGraphic);
