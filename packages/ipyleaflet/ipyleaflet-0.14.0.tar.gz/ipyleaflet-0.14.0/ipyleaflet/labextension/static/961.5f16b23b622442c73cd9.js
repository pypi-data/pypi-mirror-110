(self.webpackChunkjupyter_leaflet=self.webpackChunkjupyter_leaflet||[]).push([[961],{4961:()=>{!function(e){function t(n){if(r[n])return r[n].exports;var o=r[n]={i:n,l:!1,exports:{}};return e[n].call(o.exports,o,o.exports,t),o.l=!0,o.exports}var r={};t.m=e,t.c=r,t.d=function(e,r,n){t.o(e,r)||Object.defineProperty(e,r,{configurable:!1,enumerable:!0,get:n})},t.n=function(e){var r=e&&e.__esModule?function(){return e.default}:function(){return e};return t.d(r,"a",r),r},t.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},t.p="/dist/",t(t.s=28)}([function(e,t,r){var n=r(4),o=r(38),i=r(39),s=n?n.toStringTag:void 0;e.exports=function(e){return null==e?void 0===e?"[object Undefined]":"[object Null]":s&&s in Object(e)?o(e):i(e)}},function(e,t){e.exports=function(e){return null!=e&&"object"==typeof e}},function(e,t){e.exports=function(e){var t=typeof e;return null!=e&&("object"==t||"function"==t)}},function(e,t,r){"use strict";function n(e,t,r){if(!l(r=r||{}))throw new Error("options is invalid");var n=r.bbox,o=r.id;if(void 0===e)throw new Error("geometry is required");if(t&&t.constructor!==Object)throw new Error("properties must be an Object");n&&function(e){if(!e)throw new Error("bbox is required");if(!Array.isArray(e))throw new Error("bbox must be an Array");if(4!==e.length&&6!==e.length)throw new Error("bbox must be an Array of 4 or 6 numbers");e.forEach((function(e){if(!u(e))throw new Error("bbox must only contain numbers")}))}(n),o&&function(e){if(!e)throw new Error("id is required");if(-1===["string","number"].indexOf(typeof e))throw new Error("id must be a number or a string")}(o);var i={type:"Feature"};return o&&(i.id=o),n&&(i.bbox=n),i.properties=t||{},i.geometry=e,i}function o(e,t,r){if(!e)throw new Error("coordinates is required");if(!Array.isArray(e))throw new Error("coordinates must be an Array");if(e.length<2)throw new Error("coordinates must be at least 2 numbers long");if(!u(e[0])||!u(e[1]))throw new Error("coordinates must contain numbers");return n({type:"Point",coordinates:e},t,r)}function i(e,t,r){if(!e)throw new Error("coordinates is required");if(e.length<2)throw new Error("coordinates must be an array of two or more positions");if(!u(e[0][1])||!u(e[0][1]))throw new Error("coordinates must contain numbers");return n({type:"LineString",coordinates:e},t,r)}function s(e,t){if(null==e)throw new Error("radians is required");if(t&&"string"!=typeof t)throw new Error("units must be a string");var r=c[t||"kilometers"];if(!r)throw new Error(t+" units is invalid");return e*r}function a(e){if(null==e)throw new Error("degrees is required");return e%360*Math.PI/180}function u(e){return!isNaN(e)&&null!==e&&!Array.isArray(e)}function l(e){return!!e&&e.constructor===Object}r.d(t,"b",(function(){return n})),r.d(t,"f",(function(){return o})),r.d(t,"e",(function(){return i})),r.d(t,"g",(function(){return s})),r.d(t,"a",(function(){return a})),r.d(t,"c",(function(){return u})),r.d(t,"d",(function(){return l}));var c={meters:6371008.8,metres:6371008.8,millimeters:6371008800,millimetres:6371008800,centimeters:637100880,centimetres:637100880,kilometers:6371.0088,kilometres:6371.0088,miles:3958.761333810546,nauticalmiles:6371008.8/1852,inches:6371008.8*39.37,yards:6371008.8/1.0936,feet:20902260.511392,radians:1,degrees:6371008.8/111325}},function(e,t,r){var n=r(5).Symbol;e.exports=n},function(e,t,r){var n=r(11),o="object"==typeof self&&self&&self.Object===Object&&self,i=n||o||Function("return this")();e.exports=i},function(e,t){e.exports=function(e,t){return e===t||e!=e&&t!=t}},function(e,t,r){var n=r(10),o=r(16);e.exports=function(e){return null!=e&&o(e.length)&&!n(e)}},function(e,t,r){var n=r(9);e.exports=function(e,t,r){"__proto__"==t&&n?n(e,t,{configurable:!0,enumerable:!0,value:r,writable:!0}):e[t]=r}},function(e,t,r){var n=r(35),o=function(){try{var e=n(Object,"defineProperty");return e({},"",{}),e}catch(e){}}();e.exports=o},function(e,t,r){var n=r(0),o=r(2);e.exports=function(e){if(!o(e))return!1;var t=n(e);return"[object Function]"==t||"[object GeneratorFunction]"==t||"[object AsyncFunction]"==t||"[object Proxy]"==t}},function(e,t,r){(function(t){var r="object"==typeof t&&t&&t.Object===Object&&t;e.exports=r}).call(t,r(37))},function(e,t,r){var n=r(13),o=r(45),i=r(46);e.exports=function(e,t){return i(o(e,t,n),e+"")}},function(e,t){e.exports=function(e){return e}},function(e,t){e.exports=function(e,t,r){switch(r.length){case 0:return e.call(t);case 1:return e.call(t,r[0]);case 2:return e.call(t,r[0],r[1]);case 3:return e.call(t,r[0],r[1],r[2])}return e.apply(t,r)}},function(e,t,r){var n=r(6),o=r(7),i=r(17),s=r(2);e.exports=function(e,t,r){if(!s(r))return!1;var a=typeof t;return!!("number"==a?o(r)&&i(t,r.length):"string"==a&&t in r)&&n(r[t],e)}},function(e,t){e.exports=function(e){return"number"==typeof e&&e>-1&&e%1==0&&e<=9007199254740991}},function(e,t){var r=/^(?:0|[1-9]\d*)$/;e.exports=function(e,t){var n=typeof e;return!!(t=null==t?9007199254740991:t)&&("number"==n||"symbol"!=n&&r.test(e))&&e>-1&&e%1==0&&e<t}},function(e,t,r){var n=r(51),o=r(52),i=r(19),s=r(54),a=r(17),u=r(56),l=Object.prototype.hasOwnProperty;e.exports=function(e,t){var r=i(e),c=!r&&o(e),p=!r&&!c&&s(e),f=!r&&!c&&!p&&u(e),h=r||c||p||f,d=h?n(e.length,String):[],m=d.length;for(var y in e)!t&&!l.call(e,y)||h&&("length"==y||p&&("offset"==y||"parent"==y)||f&&("buffer"==y||"byteLength"==y||"byteOffset"==y)||a(y,m))||d.push(y);return d}},function(e,t){var r=Array.isArray;e.exports=r},function(e,t){e.exports=function(e){return e.webpackPolyfill||(e.deprecate=function(){},e.paths=[],e.children||(e.children=[]),Object.defineProperty(e,"loaded",{enumerable:!0,get:function(){return e.l}}),Object.defineProperty(e,"id",{enumerable:!0,get:function(){return e.i}}),e.webpackPolyfill=1),e}},function(e,t){var r=Object.prototype;e.exports=function(e){var t=e&&e.constructor;return e===("function"==typeof t&&t.prototype||r)}},function(e,t,r){var n=r(0),o=r(1),i=r(63);e.exports=function(e){if(!o(e))return!1;var t=n(e);return"[object Error]"==t||"[object DOMException]"==t||"string"==typeof e.message&&"string"==typeof e.name&&!i(e)}},function(e,t){e.exports=function(e,t){return function(r){return e(t(r))}}},function(e,t){e.exports=function(e,t){for(var r=-1,n=null==e?0:e.length,o=Array(n);++r<n;)o[r]=t(e[r],r,e);return o}},function(e,t){e.exports=/<%=([\s\S]+?)%>/g},function(e,t,r){var n=r(75);e.exports=function(e){return null==e?"":n(e)}},function(e,t,r){"use strict";function n(e,t,r){if(null!==e)for(var o,i,s,a,u,l,c,p,f=0,h=0,d=e.type,m="FeatureCollection"===d,y="Feature"===d,v=m?e.features.length:1,g=0;g<v;g++){u=(p=!!(c=m?e.features[g].geometry:y?e.geometry:e)&&"GeometryCollection"===c.type)?c.geometries.length:1;for(var b=0;b<u;b++){var _=0,j=0;if(null!==(a=p?c.geometries[b]:c)){l=a.coordinates;var x=a.type;switch(f=!r||"Polygon"!==x&&"MultiPolygon"!==x?0:1,x){case null:break;case"Point":if(!1===t(l,h,g,_,j))return!1;h++,_++;break;case"LineString":case"MultiPoint":for(o=0;o<l.length;o++){if(!1===t(l[o],h,g,_,j))return!1;h++,"MultiPoint"===x&&_++}"LineString"===x&&_++;break;case"Polygon":case"MultiLineString":for(o=0;o<l.length;o++){for(i=0;i<l[o].length-f;i++){if(!1===t(l[o][i],h,g,_,j))return!1;h++}"MultiLineString"===x&&_++,"Polygon"===x&&j++}"Polygon"===x&&_++;break;case"MultiPolygon":for(o=0;o<l.length;o++){for("MultiPolygon"===x&&(j=0),i=0;i<l[o].length;i++){for(s=0;s<l[o][i].length-f;s++){if(!1===t(l[o][i][s],h,g,_,j))return!1;h++}j++}_++}break;case"GeometryCollection":for(o=0;o<a.geometries.length;o++)if(!1===n(a.geometries[o],t,r))return!1;break;default:throw new Error("Unknown Geometry Type")}}}}}function o(e,t){var r,n,o,i,s,a,u,l,c,p,f=0,h="FeatureCollection"===e.type,d="Feature"===e.type,m=h?e.features.length:1;for(r=0;r<m;r++){for(a=h?e.features[r].geometry:d?e.geometry:e,l=h?e.features[r].properties:d?e.properties:{},c=h?e.features[r].bbox:d?e.bbox:void 0,p=h?e.features[r].id:d?e.id:void 0,s=(u=!!a&&"GeometryCollection"===a.type)?a.geometries.length:1,o=0;o<s;o++)if(null!==(i=u?a.geometries[o]:a))switch(i.type){case"Point":case"LineString":case"MultiPoint":case"Polygon":case"MultiLineString":case"MultiPolygon":if(!1===t(i,f,l,c,p))return!1;break;case"GeometryCollection":for(n=0;n<i.geometries.length;n++)if(!1===t(i.geometries[n],f,l,c,p))return!1;break;default:throw new Error("Unknown Geometry Type")}else if(!1===t(null,f,l,c,p))return!1;f++}}function i(e,t,r){var n=r;return o(e,(function(e,o,i,s,a){n=0===o&&void 0===r?e:t(n,e,o,i,s,a)})),n}function s(e,t){!function(e,t){o(e,(function(e,r,n,o,i){var s,a=null===e?null:e.type;switch(a){case null:case"Point":case"LineString":case"Polygon":return!1!==t(Object(u.b)(e,n,{bbox:o,id:i}),r,0)&&void 0}switch(a){case"MultiPoint":s="Point";break;case"MultiLineString":s="LineString";break;case"MultiPolygon":s="Polygon"}for(var l=0;l<e.coordinates.length;l++){var c={type:s,coordinates:e.coordinates[l]};if(!1===t(Object(u.b)(c,n),r,l))return!1}}))}(e,(function(e,r,o){var i=0;if(e.geometry){var s,a=e.geometry.type;if("Point"!==a&&"MultiPoint"!==a)return!1!==n(e,(function(n,a,l,c,p){if(void 0!==s){var f=Object(u.e)([s,n],e.properties);if(!1===t(f,r,o,p,i))return!1;i++,s=n}else s=n}))&&void 0}}))}function a(e,t,r){var n=r,o=!1;return s(e,(function(e,i,s,a,u){n=!1===o&&void 0===r?e:t(n,e,i,s,a,u),o=!0})),n}r.d(t,"a",(function(){return i})),r.d(t,"b",(function(){return a}));var u=r(3)},function(e,t,r){e.exports=r(29)},function(e,t,r){"use strict";function n(e){return e&&e.__esModule?e:{default:e}}r(30);var o=n(r(31)),i=n(r(79)),s=n(r(80)),a=r(85),u=function(e){if(e&&e.__esModule)return e;var t={};if(null!=e)for(var r in e)Object.prototype.hasOwnProperty.call(e,r)&&(t[r]=e[r]);return t.default=e,t}(a),l=n(r(86)),c=r(87),p=r(88),f={imports:{numberFormat:c.numberFormat},interpolate:/{{([\s\S]+?)}}/g},h=(0,o.default)(p.controlTemplate,f),d=(0,o.default)(p.resultsTemplate,f),m=(0,o.default)(p.pointPopupTemplate,f),y=(0,o.default)(p.linePopupTemplate,f),v=(0,o.default)(p.areaPopupTemplate,f);L.Control.Measure=L.Control.extend({_className:"leaflet-control-measure",options:{units:{},position:"topright",primaryLengthUnit:"feet",secondaryLengthUnit:"miles",primaryAreaUnit:"acres",activeColor:"#ABE67E",completedColor:"#C8F2BE",captureZIndex:1e4,popupOptions:{className:"leaflet-measure-resultpopup",autoPanPadding:[10,10]}},initialize:function(e){L.setOptions(this,e);var t=this.options,r=t.activeColor,n=t.completedColor;this._symbols=new l.default({activeColor:r,completedColor:n}),this.options.units=L.extend({},i.default,this.options.units)},onAdd:function(e){return this._map=e,this._latlngs=[],this._initLayout(),e.on("click",this._collapse,this),this._layer=L.layerGroup().addTo(e),this._container},onRemove:function(e){e.off("click",this._collapse,this),e.removeLayer(this._layer)},_initLayout:function(){var e=this._className,t=this._container=L.DomUtil.create("div",e+" leaflet-bar");t.innerHTML=h({model:{className:e}}),t.setAttribute("aria-haspopup",!0),L.DomEvent.disableClickPropagation(t),L.DomEvent.disableScrollPropagation(t);var r=this.$toggle=(0,a.selectOne)(".js-toggle",t);this.$interaction=(0,a.selectOne)(".js-interaction",t);var n=(0,a.selectOne)(".js-start",t),o=(0,a.selectOne)(".js-cancel",t),i=(0,a.selectOne)(".js-finish",t);this.$startPrompt=(0,a.selectOne)(".js-startprompt",t),this.$measuringPrompt=(0,a.selectOne)(".js-measuringprompt",t),this.$startHelp=(0,a.selectOne)(".js-starthelp",t),this.$results=(0,a.selectOne)(".js-results",t),this.$measureTasks=(0,a.selectOne)(".js-measuretasks",t),this._collapse(),this._updateMeasureNotStarted(),L.Browser.android||(L.DomEvent.on(t,"mouseenter",this._expand,this),L.DomEvent.on(t,"mouseleave",this._collapse,this)),L.DomEvent.on(r,"click",L.DomEvent.stop),L.Browser.touch?L.DomEvent.on(r,"click",this._expand,this):L.DomEvent.on(r,"focus",this._expand,this),L.DomEvent.on(n,"click",L.DomEvent.stop),L.DomEvent.on(n,"click",this._startMeasure,this),L.DomEvent.on(o,"click",L.DomEvent.stop),L.DomEvent.on(o,"click",this._finishMeasure,this),L.DomEvent.on(i,"click",L.DomEvent.stop),L.DomEvent.on(i,"click",this._handleMeasureDoubleClick,this)},_expand:function(){u.hide(this.$toggle),u.show(this.$interaction)},_collapse:function(){this._locked||(u.hide(this.$interaction),u.show(this.$toggle))},_updateMeasureNotStarted:function(){u.hide(this.$startHelp),u.hide(this.$results),u.hide(this.$measureTasks),u.hide(this.$measuringPrompt),u.show(this.$startPrompt)},_updateMeasureStartedNoPoints:function(){u.hide(this.$results),u.show(this.$startHelp),u.show(this.$measureTasks),u.hide(this.$startPrompt),u.show(this.$measuringPrompt)},_updateMeasureStartedWithPoints:function(){u.hide(this.$startHelp),u.show(this.$results),u.show(this.$measureTasks),u.hide(this.$startPrompt),u.show(this.$measuringPrompt)},_startMeasure:function(){this._locked=!0,this._measureVertexes=L.featureGroup().addTo(this._layer),this._captureMarker=L.marker(this._map.getCenter(),{clickable:!0,zIndexOffset:this.options.captureZIndex,opacity:0}).addTo(this._layer),this._setCaptureMarkerIcon(),this._captureMarker.on("mouseout",this._handleMapMouseOut,this).on("dblclick",this._handleMeasureDoubleClick,this).on("click",this._handleMeasureClick,this),this._map.on("mousemove",this._handleMeasureMove,this).on("mouseout",this._handleMapMouseOut,this).on("move",this._centerCaptureMarker,this).on("resize",this._setCaptureMarkerIcon,this),L.DomEvent.on(this._container,"mouseenter",this._handleMapMouseOut,this),this._updateMeasureStartedNoPoints(),this._map.fire("measurestart",null,!1)},_finishMeasure:function(){var e=L.extend({},this._resultsModel,{points:this._latlngs});this._locked=!1,L.DomEvent.off(this._container,"mouseover",this._handleMapMouseOut,this),this._clearMeasure(),this._captureMarker.off("mouseout",this._handleMapMouseOut,this).off("dblclick",this._handleMeasureDoubleClick,this).off("click",this._handleMeasureClick,this),this._map.off("mousemove",this._handleMeasureMove,this).off("mouseout",this._handleMapMouseOut,this).off("move",this._centerCaptureMarker,this).off("resize",this._setCaptureMarkerIcon,this),this._layer.removeLayer(this._measureVertexes).removeLayer(this._captureMarker),this._measureVertexes=null,this._updateMeasureNotStarted(),this._collapse(),this._map.fire("measurefinish",e,!1)},_clearMeasure:function(){this._latlngs=[],this._resultsModel=null,this._measureVertexes.clearLayers(),this._measureDrag&&this._layer.removeLayer(this._measureDrag),this._measureArea&&this._layer.removeLayer(this._measureArea),this._measureBoundary&&this._layer.removeLayer(this._measureBoundary),this._measureDrag=null,this._measureArea=null,this._measureBoundary=null},_centerCaptureMarker:function(){this._captureMarker.setLatLng(this._map.getCenter())},_setCaptureMarkerIcon:function(){this._captureMarker.setIcon(L.divIcon({iconSize:this._map.getSize().multiplyBy(2)}))},_getMeasurementDisplayStrings:function(e){function t(e,t,o,i,s){if(t&&n[t]){var a=r(e,n[t],i,s);return o&&n[o]&&(a=a+" ("+r(e,n[o],i,s)+")"),a}return r(e,null,i,s)}function r(e,t,r,n){var o=L.extend({factor:1,decimals:0},t);return[(0,c.numberFormat)(e*o.factor,o.decimals,r||".",n||","),{acres:"Acres",feet:"Feet",kilometers:"Kilometers",hectares:"Hectares",meters:"Meters",miles:"Miles",sqfeet:"Sq Feet",sqmeters:"Sq Meters",sqmiles:"Sq Miles"}[o.display]||o.display].join(" ")}var n=this.options.units;return{lengthDisplay:t(e.length,this.options.primaryLengthUnit,this.options.secondaryLengthUnit,this.options.decPoint,this.options.thousandsSep),areaDisplay:t(e.area,this.options.primaryAreaUnit,this.options.secondaryAreaUnit,this.options.decPoint,this.options.thousandsSep)}},_updateResults:function(){var e=(0,s.default)(this._latlngs),t=this._resultsModel=L.extend({},e,this._getMeasurementDisplayStrings(e),{pointCount:this._latlngs.length});this.$results.innerHTML=d({model:t})},_handleMeasureMove:function(e){this._measureDrag?this._measureDrag.setLatLng(e.latlng):this._measureDrag=L.circleMarker(e.latlng,this._symbols.getSymbol("measureDrag")).addTo(this._layer),this._measureDrag.bringToFront()},_handleMeasureDoubleClick:function(){var e=this._latlngs,t=void 0,r=void 0;if(this._finishMeasure(),e.length){e.length>2&&e.push(e[0]);var n=(0,s.default)(e);1===e.length?(t=L.circleMarker(e[0],this._symbols.getSymbol("resultPoint")),r=m({model:n})):2===e.length?(t=L.polyline(e,this._symbols.getSymbol("resultLine")),r=y({model:L.extend({},n,this._getMeasurementDisplayStrings(n))})):(t=L.polygon(e,this._symbols.getSymbol("resultArea")),r=v({model:L.extend({},n,this._getMeasurementDisplayStrings(n))}));var o=L.DomUtil.create("div","");o.innerHTML=r;var i=(0,a.selectOne)(".js-zoomto",o);i&&(L.DomEvent.on(i,"click",L.DomEvent.stop),L.DomEvent.on(i,"click",(function(){t.getBounds?this._map.fitBounds(t.getBounds(),{padding:[20,20],maxZoom:17}):t.getLatLng&&this._map.panTo(t.getLatLng())}),this));var u=(0,a.selectOne)(".js-deletemarkup",o);u&&(L.DomEvent.on(u,"click",L.DomEvent.stop),L.DomEvent.on(u,"click",(function(){this._layer.removeLayer(t)}),this)),t.addTo(this._layer),t.bindPopup(o,this.options.popupOptions),t.getBounds?t.openPopup(t.getBounds().getCenter()):t.getLatLng&&t.openPopup(t.getLatLng())}},_handleMeasureClick:function(e){var t=this._map.mouseEventToLatLng(e.originalEvent),r=this._latlngs[this._latlngs.length-1],n=this._symbols.getSymbol("measureVertex");r&&t.equals(r)||(this._latlngs.push(t),this._addMeasureArea(this._latlngs),this._addMeasureBoundary(this._latlngs),this._measureVertexes.eachLayer((function(e){e.setStyle(n),e._path&&e._path.setAttribute("class",n.className)})),this._addNewVertex(t),this._measureBoundary&&this._measureBoundary.bringToFront(),this._measureVertexes.bringToFront()),this._updateResults(),this._updateMeasureStartedWithPoints()},_handleMapMouseOut:function(){this._measureDrag&&(this._layer.removeLayer(this._measureDrag),this._measureDrag=null)},_addNewVertex:function(e){L.circleMarker(e,this._symbols.getSymbol("measureVertexActive")).addTo(this._measureVertexes)},_addMeasureArea:function(e){e.length<3?this._measureArea&&(this._layer.removeLayer(this._measureArea),this._measureArea=null):this._measureArea?this._measureArea.setLatLngs(e):this._measureArea=L.polygon(e,this._symbols.getSymbol("measureArea")).addTo(this._layer)},_addMeasureBoundary:function(e){e.length<2?this._measureBoundary&&(this._layer.removeLayer(this._measureBoundary),this._measureBoundary=null):this._measureBoundary?this._measureBoundary.setLatLngs(e):this._measureBoundary=L.polyline(e,this._symbols.getSymbol("measureBoundary")).addTo(this._layer)}}),L.Map.mergeOptions({measureControl:!1}),L.Map.addInitHook((function(){this.options.measureControl&&(this.measureControl=(new L.Control.Measure).addTo(this))})),L.control.measure=function(e){return new L.Control.Measure(e)}},function(e,t){},function(e,t,r){var n=r(32),o=r(62),i=r(65),s=r(66),a=r(67),u=r(22),l=r(15),c=r(68),p=r(25),f=r(71),h=r(26),d=/\b__p \+= '';/g,m=/\b(__p \+=) '' \+/g,y=/(__e\(.*?\)|\b__t\)) \+\n'';/g,v=/\$\{([^\\}]*(?:\\.[^\\}]*)*)\}/g,g=/($^)/,b=/['\n\r\u2028\u2029\\]/g;e.exports=function(e,t,r){var _=f.imports._.templateSettings||f;r&&l(e,t,r)&&(t=void 0),e=h(e),t=n({},t,_,s);var j,x,M=n({},t.imports,_.imports,s),w=c(M),L=i(M,w),O=0,k=t.interpolate||g,P="__p += '",C=RegExp((t.escape||g).source+"|"+k.source+"|"+(k===p?v:g).source+"|"+(t.evaluate||g).source+"|$","g"),E="sourceURL"in t?"//# sourceURL="+t.sourceURL+"\n":"";e.replace(C,(function(t,r,n,o,i,s){return n||(n=o),P+=e.slice(O,s).replace(b,a),r&&(j=!0,P+="' +\n__e("+r+") +\n'"),i&&(x=!0,P+="';\n"+i+";\n__p += '"),n&&(P+="' +\n((__t = ("+n+")) == null ? '' : __t) +\n'"),O=s+t.length,t})),P+="';\n";var S=t.variable;S||(P="with (obj) {\n"+P+"\n}\n"),P=(x?P.replace(d,""):P).replace(m,"$1").replace(y,"$1;"),P="function("+(S||"obj")+") {\n"+(S?"":"obj || (obj = {});\n")+"var __t, __p = ''"+(j?", __e = _.escape":"")+(x?", __j = Array.prototype.join;\nfunction print() { __p += __j.call(arguments, '') }\n":";\n")+P+"return __p\n}";var A=o((function(){return Function(w,E+"return "+P).apply(void 0,L)}));if(A.source=P,u(A))throw A;return A}},function(e,t,r){var n=r(33),o=r(44),i=r(50),s=o((function(e,t,r,o){n(t,i(t),e,o)}));e.exports=s},function(e,t,r){var n=r(34),o=r(8);e.exports=function(e,t,r,i){var s=!r;r||(r={});for(var a=-1,u=t.length;++a<u;){var l=t[a],c=i?i(r[l],e[l],l,r,e):void 0;void 0===c&&(c=e[l]),s?o(r,l,c):n(r,l,c)}return r}},function(e,t,r){var n=r(8),o=r(6),i=Object.prototype.hasOwnProperty;e.exports=function(e,t,r){var s=e[t];i.call(e,t)&&o(s,r)&&(void 0!==r||t in e)||n(e,t,r)}},function(e,t,r){var n=r(36),o=r(43);e.exports=function(e,t){var r=o(e,t);return n(r)?r:void 0}},function(e,t,r){var n=r(10),o=r(40),i=r(2),s=r(42),a=/^\[object .+?Constructor\]$/,u=Function.prototype,l=Object.prototype,c=u.toString,p=l.hasOwnProperty,f=RegExp("^"+c.call(p).replace(/[\\^$.*+?()[\]{}|]/g,"\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g,"$1.*?")+"$");e.exports=function(e){return!(!i(e)||o(e))&&(n(e)?f:a).test(s(e))}},function(e,t){var r;r=function(){return this}();try{r=r||Function("return this")()||(0,eval)("this")}catch(e){"object"==typeof window&&(r=window)}e.exports=r},function(e,t,r){var n=r(4),o=Object.prototype,i=o.hasOwnProperty,s=o.toString,a=n?n.toStringTag:void 0;e.exports=function(e){var t=i.call(e,a),r=e[a];try{e[a]=void 0;var n=!0}catch(e){}var o=s.call(e);return n&&(t?e[a]=r:delete e[a]),o}},function(e,t){var r=Object.prototype.toString;e.exports=function(e){return r.call(e)}},function(e,t,r){var n=r(41),o=function(){var e=/[^.]+$/.exec(n&&n.keys&&n.keys.IE_PROTO||"");return e?"Symbol(src)_1."+e:""}();e.exports=function(e){return!!o&&o in e}},function(e,t,r){var n=r(5)["__core-js_shared__"];e.exports=n},function(e,t){var r=Function.prototype.toString;e.exports=function(e){if(null!=e){try{return r.call(e)}catch(e){}try{return e+""}catch(e){}}return""}},function(e,t){e.exports=function(e,t){return null==e?void 0:e[t]}},function(e,t,r){var n=r(12),o=r(15);e.exports=function(e){return n((function(t,r){var n=-1,i=r.length,s=i>1?r[i-1]:void 0,a=i>2?r[2]:void 0;for(s=e.length>3&&"function"==typeof s?(i--,s):void 0,a&&o(r[0],r[1],a)&&(s=i<3?void 0:s,i=1),t=Object(t);++n<i;){var u=r[n];u&&e(t,u,n,s)}return t}))}},function(e,t,r){var n=r(14),o=Math.max;e.exports=function(e,t,r){return t=o(void 0===t?e.length-1:t,0),function(){for(var i=arguments,s=-1,a=o(i.length-t,0),u=Array(a);++s<a;)u[s]=i[t+s];s=-1;for(var l=Array(t+1);++s<t;)l[s]=i[s];return l[t]=r(u),n(e,this,l)}}},function(e,t,r){var n=r(47),o=r(49)(n);e.exports=o},function(e,t,r){var n=r(48),o=r(9),i=r(13),s=o?function(e,t){return o(e,"toString",{configurable:!0,enumerable:!1,value:n(t),writable:!0})}:i;e.exports=s},function(e,t){e.exports=function(e){return function(){return e}}},function(e,t){var r=Date.now;e.exports=function(e){var t=0,n=0;return function(){var o=r(),i=16-(o-n);if(n=o,i>0){if(++t>=800)return arguments[0]}else t=0;return e.apply(void 0,arguments)}}},function(e,t,r){var n=r(18),o=r(60),i=r(7);e.exports=function(e){return i(e)?n(e,!0):o(e)}},function(e,t){e.exports=function(e,t){for(var r=-1,n=Array(e);++r<e;)n[r]=t(r);return n}},function(e,t,r){var n=r(53),o=r(1),i=Object.prototype,s=i.hasOwnProperty,a=i.propertyIsEnumerable,u=n(function(){return arguments}())?n:function(e){return o(e)&&s.call(e,"callee")&&!a.call(e,"callee")};e.exports=u},function(e,t,r){var n=r(0),o=r(1);e.exports=function(e){return o(e)&&"[object Arguments]"==n(e)}},function(e,t,r){(function(e){var n=r(5),o=r(55),i="object"==typeof t&&t&&!t.nodeType&&t,s=i&&"object"==typeof e&&e&&!e.nodeType&&e,a=s&&s.exports===i?n.Buffer:void 0,u=(a?a.isBuffer:void 0)||o;e.exports=u}).call(t,r(20)(e))},function(e,t){e.exports=function(){return!1}},function(e,t,r){var n=r(57),o=r(58),i=r(59),s=i&&i.isTypedArray,a=s?o(s):n;e.exports=a},function(e,t,r){var n=r(0),o=r(16),i=r(1),s={};s["[object Float32Array]"]=s["[object Float64Array]"]=s["[object Int8Array]"]=s["[object Int16Array]"]=s["[object Int32Array]"]=s["[object Uint8Array]"]=s["[object Uint8ClampedArray]"]=s["[object Uint16Array]"]=s["[object Uint32Array]"]=!0,s["[object Arguments]"]=s["[object Array]"]=s["[object ArrayBuffer]"]=s["[object Boolean]"]=s["[object DataView]"]=s["[object Date]"]=s["[object Error]"]=s["[object Function]"]=s["[object Map]"]=s["[object Number]"]=s["[object Object]"]=s["[object RegExp]"]=s["[object Set]"]=s["[object String]"]=s["[object WeakMap]"]=!1,e.exports=function(e){return i(e)&&o(e.length)&&!!s[n(e)]}},function(e,t){e.exports=function(e){return function(t){return e(t)}}},function(e,t,r){(function(e){var n=r(11),o="object"==typeof t&&t&&!t.nodeType&&t,i=o&&"object"==typeof e&&e&&!e.nodeType&&e,s=i&&i.exports===o&&n.process,a=function(){try{return s&&s.binding&&s.binding("util")}catch(e){}}();e.exports=a}).call(t,r(20)(e))},function(e,t,r){var n=r(2),o=r(21),i=r(61),s=Object.prototype.hasOwnProperty;e.exports=function(e){if(!n(e))return i(e);var t=o(e),r=[];for(var a in e)("constructor"!=a||!t&&s.call(e,a))&&r.push(a);return r}},function(e,t){e.exports=function(e){var t=[];if(null!=e)for(var r in Object(e))t.push(r);return t}},function(e,t,r){var n=r(14),o=r(12),i=r(22),s=o((function(e,t){try{return n(e,void 0,t)}catch(e){return i(e)?e:new Error(e)}}));e.exports=s},function(e,t,r){var n=r(0),o=r(64),i=r(1),s=Function.prototype,a=Object.prototype,u=s.toString,l=a.hasOwnProperty,c=u.call(Object);e.exports=function(e){if(!i(e)||"[object Object]"!=n(e))return!1;var t=o(e);if(null===t)return!0;var r=l.call(t,"constructor")&&t.constructor;return"function"==typeof r&&r instanceof r&&u.call(r)==c}},function(e,t,r){var n=r(23)(Object.getPrototypeOf,Object);e.exports=n},function(e,t,r){var n=r(24);e.exports=function(e,t){return n(t,(function(t){return e[t]}))}},function(e,t,r){var n=r(6),o=Object.prototype,i=o.hasOwnProperty;e.exports=function(e,t,r,s){return void 0===e||n(e,o[r])&&!i.call(s,r)?t:e}},function(e,t){var r={"\\":"\\","'":"'","\n":"n","\r":"r","\u2028":"u2028","\u2029":"u2029"};e.exports=function(e){return"\\"+r[e]}},function(e,t,r){var n=r(18),o=r(69),i=r(7);e.exports=function(e){return i(e)?n(e):o(e)}},function(e,t,r){var n=r(21),o=r(70),i=Object.prototype.hasOwnProperty;e.exports=function(e){if(!n(e))return o(e);var t=[];for(var r in Object(e))i.call(e,r)&&"constructor"!=r&&t.push(r);return t}},function(e,t,r){var n=r(23)(Object.keys,Object);e.exports=n},function(e,t,r){var n=r(72),o={escape:r(77),evaluate:r(78),interpolate:r(25),variable:"",imports:{_:{escape:n}}};e.exports=o},function(e,t,r){var n=r(73),o=r(26),i=/[&<>"']/g,s=RegExp(i.source);e.exports=function(e){return(e=o(e))&&s.test(e)?e.replace(i,n):e}},function(e,t,r){var n=r(74)({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"});e.exports=n},function(e,t){e.exports=function(e){return function(t){return null==e?void 0:e[t]}}},function(e,t,r){var n=r(4),o=r(24),i=r(19),s=r(76),a=n?n.prototype:void 0,u=a?a.toString:void 0;e.exports=function e(t){if("string"==typeof t)return t;if(i(t))return o(t,e)+"";if(s(t))return u?u.call(t):"";var r=t+"";return"0"==r&&1/t==-Infinity?"-0":r}},function(e,t,r){var n=r(0),o=r(1);e.exports=function(e){return"symbol"==typeof e||o(e)&&"[object Symbol]"==n(e)}},function(e,t){e.exports=/<%-([\s\S]+?)%>/g},function(e,t){e.exports=/<%([\s\S]+?)%>/g},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={acres:{factor:24711e-8,display:"acres",decimals:2},feet:{factor:3.2808,display:"feet",decimals:0},kilometers:{factor:.001,display:"kilometers",decimals:2},hectares:{factor:1e-4,display:"hectares",decimals:2},meters:{factor:1,display:"meters",decimals:0},miles:{factor:3.2808/5280,display:"miles",decimals:2},sqfeet:{factor:10.7639,display:"sqfeet",decimals:0},sqmeters:{factor:1,display:"sqmeters",decimals:0},sqmiles:{factor:3.86102e-7,display:"sqmiles",decimals:2}}},function(e,t,r){"use strict";function n(e){return e&&e.__esModule?e:{default:e}}function o(e){return e<10?"0"+e.toString():e.toString()}function i(e,t,r){var n=Math.abs(e),i=Math.floor(n),s=Math.floor(60*(n-i)),a=Math.round(3600*(n-i-s/60)*100)/100,u=n===e?t:r;return o(i)+"&deg; "+o(s)+"' "+o(a)+'" '+u}Object.defineProperty(t,"__esModule",{value:!0}),t.default=function(e){var t=e[e.length-1],r=e.map((function(e){return[e.lat,e.lng]})),n=L.polyline(r),o=L.polygon(r),u=1e3*(0,s.default)(n.toGeoJSON(),{units:"kilometers"}),l=(0,a.default)(o.toGeoJSON());return{lastCoord:{dd:{x:t.lng,y:t.lat},dms:{x:i(t.lng,"E","W"),y:i(t.lat,"N","S")}},length:u,area:l}};var s=n(r(81)),a=n(r(84))},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n=r(82),o=r(27),i=r(3);t.default=function(e,t){if(t=t||{},!Object(i.d)(t))throw new Error("options is invalid");if(!e)throw new Error("geojson is required");return Object(o.b)(e,(function(e,r){var o=r.geometry.coordinates;return e+Object(n.a)(o[0],o[1],t)}),0)}},function(e,t,r){"use strict";var n=r(83),o=r(3);t.a=function(e,t,r){if(r=r||{},!Object(o.d)(r))throw new Error("options is invalid");var i=r.units,s=Object(n.a)(e),a=Object(n.a)(t),u=Object(o.a)(a[1]-s[1]),l=Object(o.a)(a[0]-s[0]),c=Object(o.a)(s[1]),p=Object(o.a)(a[1]),f=Math.pow(Math.sin(u/2),2)+Math.pow(Math.sin(l/2),2)*Math.cos(c)*Math.cos(p);return Object(o.g)(2*Math.atan2(Math.sqrt(f),Math.sqrt(1-f)),i)}},function(e,t,r){"use strict";function n(e){if(!e)throw new Error("coord is required");if("Feature"===e.type&&null!==e.geometry&&"Point"===e.geometry.type)return e.geometry.coordinates;if("Point"===e.type)return e.coordinates;if(Array.isArray(e)&&e.length>=2&&void 0===e[0].length&&void 0===e[1].length)return e;throw new Error("coord must be GeoJSON Point or an Array of numbers")}r.d(t,"a",(function(){return n})),r(3)},function(e,t,r){"use strict";function n(e){var t,r=0;switch(e.type){case"Polygon":return o(e.coordinates);case"MultiPolygon":for(t=0;t<e.coordinates.length;t++)r+=o(e.coordinates[t]);return r;case"Point":case"MultiPoint":case"LineString":case"MultiLineString":return 0;case"GeometryCollection":for(t=0;t<e.geometries.length;t++)r+=n(e.geometries[t]);return r}}function o(e){var t=0;if(e&&e.length>0){t+=Math.abs(i(e[0]));for(var r=1;r<e.length;r++)t-=Math.abs(i(e[r]))}return t}function i(e){var t,r,n,o,i,a,l=0,c=e.length;if(c>2){for(a=0;a<c;a++)a===c-2?(n=c-2,o=c-1,i=0):a===c-1?(n=c-1,o=0,i=1):(n=a,o=a+1,i=a+2),t=e[n],r=e[o],l+=(s(e[i][0])-s(t[0]))*Math.sin(s(r[1]));l=l*u*u/2}return l}function s(e){return e*Math.PI/180}Object.defineProperty(t,"__esModule",{value:!0});var a=r(27),u=6378137;t.default=function(e){return Object(a.a)(e,(function(e,t){return e+n(t)}),0)}},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.selectOne=function(e,t){return t||(t=document),t.querySelector(e)},t.selectAll=function(e,t){return t||(t=document),Array.prototype.slice.call(t.querySelectorAll(e))},t.hide=function(e){if(e)return e.setAttribute("style","display:none;"),e},t.show=function(e){if(e)return e.removeAttribute("style"),e}},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n=function(){function e(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}return function(t,r,n){return r&&e(t.prototype,r),n&&e(t,n),t}}(),o={activeColor:"#ABE67E",completedColor:"#C8F2BE"},i=function(){function e(t){(function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")})(this,e),this._options=L.extend({},o,this._options,t)}return n(e,[{key:"getSymbol",value:function(e){return{measureDrag:{clickable:!1,radius:4,color:this._options.activeColor,weight:2,opacity:.7,fillColor:this._options.activeColor,fillOpacity:.5,className:"layer-measuredrag"},measureArea:{clickable:!1,stroke:!1,fillColor:this._options.activeColor,fillOpacity:.2,className:"layer-measurearea"},measureBoundary:{clickable:!1,color:this._options.activeColor,weight:2,opacity:.9,fill:!1,className:"layer-measureboundary"},measureVertex:{clickable:!1,radius:4,color:this._options.activeColor,weight:2,opacity:1,fillColor:this._options.activeColor,fillOpacity:.7,className:"layer-measurevertex"},measureVertexActive:{clickable:!1,radius:4,color:this._options.activeColor,weight:2,opacity:1,fillColor:this._options.activeColor,fillOpacity:1,className:"layer-measurevertex active"},resultArea:{clickable:!0,color:this._options.completedColor,weight:2,opacity:.9,fillColor:this._options.completedColor,fillOpacity:.2,className:"layer-measure-resultarea"},resultLine:{clickable:!0,color:this._options.completedColor,weight:3,opacity:.9,fill:!1,className:"layer-measure-resultline"},resultPoint:{clickable:!0,radius:4,color:this._options.completedColor,weight:2,opacity:1,fillColor:this._options.completedColor,fillOpacity:.7,className:"layer-measure-resultpoint"}}[e]}}]),e}();t.default=i},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.numberFormat=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:2,r=arguments.length>2&&void 0!==arguments[2]?arguments[2]:".",n=arguments.length>3&&void 0!==arguments[3]?arguments[3]:",",o=e<0?"-":"",i=Math.abs(+e||0),s=parseInt(i.toFixed(t),10)+"",a=s.length>3?s.length%3:0;return[o,a?s.substr(0,a)+n:"",s.substr(a).replace(/(\d{3})(?=\d)/g,"$1"+n),t?""+r+Math.abs(i-s).toFixed(t).slice(2):""].join("")}},function(e,t,r){"use strict";function n(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var o=r(89);Object.defineProperty(t,"controlTemplate",{enumerable:!0,get:function(){return n(o).default}});var i=r(90);Object.defineProperty(t,"resultsTemplate",{enumerable:!0,get:function(){return n(i).default}});var s=r(91);Object.defineProperty(t,"pointPopupTemplate",{enumerable:!0,get:function(){return n(s).default}});var a=r(92);Object.defineProperty(t,"linePopupTemplate",{enumerable:!0,get:function(){return n(a).default}});var u=r(93);Object.defineProperty(t,"areaPopupTemplate",{enumerable:!0,get:function(){return n(u).default}})},function(e,t,r){e.exports='<a class="{{ model.className }}-toggle js-toggle" href=# title="Measure distances and areas">Measure</a> <div class="{{ model.className }}-interaction js-interaction"> <div class="js-startprompt startprompt"> <h3>Measure distances and areas</h3> <ul class=tasks> <a href=# class="js-start start">Create a new measurement</a> </ul> </div> <div class=js-measuringprompt> <h3>Measure distances and areas</h3> <p class=js-starthelp>Start creating a measurement by adding points to the map</p> <div class="js-results results"></div> <ul class="js-measuretasks tasks"> <li><a href=# class="js-cancel cancel">Cancel</a></li> <li><a href=# class="js-finish finish">Finish measurement</a></li> </ul> </div> </div> '},function(e,t,r){e.exports='<div class=group> <p class="lastpoint heading">Last point</p> <p>{{ model.lastCoord.dms.y }} <span class=coorddivider>/</span> {{ model.lastCoord.dms.x }}</p> <p>{{ numberFormat(model.lastCoord.dd.y, 6) }} <span class=coorddivider>/</span> {{ numberFormat(model.lastCoord.dd.x, 6) }}</p> </div> <% if (model.pointCount > 1) { %> <div class=group> <p><span class=heading>Path distance</span> {{ model.lengthDisplay }}</p> </div> <% } %> <% if (model.pointCount > 2) { %> <div class=group> <p><span class=heading>Area</span> {{ model.areaDisplay }}</p> </div> <% } %> '},function(e,t,r){e.exports='<h3>Point location</h3> <p>{{ model.lastCoord.dms.y }} <span class=coorddivider>/</span> {{ model.lastCoord.dms.x }}</p> <p>{{ numberFormat(model.lastCoord.dd.y, 6) }} <span class=coorddivider>/</span> {{ numberFormat(model.lastCoord.dd.x, 6) }}</p> <ul class=tasks> <li><a href=# class="js-zoomto zoomto">Center on this location</a></li> <li><a href=# class="js-deletemarkup deletemarkup">Delete</a></li> </ul> '},function(e,t,r){e.exports='<h3>Linear measurement</h3> <p>{{ model.lengthDisplay }}</p> <ul class=tasks> <li><a href=# class="js-zoomto zoomto">Center on this line</a></li> <li><a href=# class="js-deletemarkup deletemarkup">Delete</a></li> </ul> '},function(e,t,r){e.exports='<h3>Area measurement</h3> <p>{{ model.areaDisplay }}</p> <p>{{ model.lengthDisplay }} Perimeter</p> <ul class=tasks> <li><a href=# class="js-zoomto zoomto">Center on this area</a></li> <li><a href=# class="js-deletemarkup deletemarkup">Delete</a></li> </ul> '}])}}]);