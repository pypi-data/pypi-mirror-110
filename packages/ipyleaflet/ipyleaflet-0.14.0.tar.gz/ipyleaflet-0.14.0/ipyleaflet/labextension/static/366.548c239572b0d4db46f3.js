(self.webpackChunkjupyter_leaflet=self.webpackChunkjupyter_leaflet||[]).push([[366],{5202:(n,e,t)=>{(e=t(3645)(!1)).push([n.id,".leaflet-sbs-range {\n    position: absolute;\n    top: 50%;\n    width: 100%;\n    z-index: 999;\n}\n.leaflet-sbs-divider {\n    position: absolute;\n    top: 0;\n    bottom: 0;\n    left: 50%;\n    margin-left: -2px;\n    width: 4px;\n    background-color: #fff;\n    pointer-events: none;\n    z-index: 999;\n}\n",""]),n.exports=e},8102:(n,e,t)=>{var i=t(3645),a=t(1667),r=t(9161);e=i(!1);var s=a(r);e.push([n.id,".leaflet-sbs-range {\n    -webkit-appearance: none;\n    display: inline-block!important;\n    vertical-align: middle;\n    height: 0;\n    padding: 0;\n    margin: 0;\n    border: 0;\n    background: rgba(0, 0, 0, 0.25);\n    min-width: 100px;\n    cursor: pointer;\n    pointer-events: none;\n    z-index: 999;\n}\n.leaflet-sbs-range::-ms-fill-upper {\n    background: transparent;\n}\n.leaflet-sbs-range::-ms-fill-lower {\n    background: rgba(255, 255, 255, 0.25);\n}\n/* Browser thingies */\n\n.leaflet-sbs-range::-moz-range-track {\n    opacity: 0;\n}\n.leaflet-sbs-range::-ms-track {\n    opacity: 0;\n}\n.leaflet-sbs-range::-ms-tooltip {\n    display: none;\n}\n/* For whatever reason, these need to be defined\n * on their own so dont group them */\n\n.leaflet-sbs-range::-webkit-slider-thumb {\n    -webkit-appearance: none;\n    margin: 0;\n    padding: 0;\n    background: #fff;\n    height: 40px;\n    width: 40px;\n    border-radius: 20px;\n    cursor: ew-resize;\n    pointer-events: auto;\n    border: 1px solid #ddd;\n    background-image: url("+s+");\n    background-position: 50% 50%;\n    background-repeat: no-repeat;\n    background-size: 40px 40px;\n}\n.leaflet-sbs-range::-ms-thumb {\n    margin: 0;\n    padding: 0;\n    background: #fff;\n    height: 40px;\n    width: 40px;\n    border-radius: 20px;\n    cursor: ew-resize;\n    pointer-events: auto;\n    border: 1px solid #ddd;\n    background-image: url("+s+");\n    background-position: 50% 50%;\n    background-repeat: no-repeat;\n    background-size: 40px 40px;\n}\n.leaflet-sbs-range::-moz-range-thumb {\n    padding: 0;\n    right: 0    ;\n    background: #fff;\n    height: 40px;\n    width: 40px;\n    border-radius: 20px;\n    cursor: ew-resize;\n    pointer-events: auto;\n    border: 1px solid #ddd;\n    background-image: url("+s+");\n    background-position: 50% 50%;\n    background-repeat: no-repeat;\n    background-size: 40px 40px;\n}\n.leaflet-sbs-range:disabled::-moz-range-thumb {\n    cursor: default;\n}\n.leaflet-sbs-range:disabled::-ms-thumb {\n    cursor: default;\n}\n.leaflet-sbs-range:disabled::-webkit-slider-thumb {\n    cursor: default;\n}\n.leaflet-sbs-range:disabled {\n    cursor: default;\n}\n.leaflet-sbs-range:focus {\n    outline: none!important;\n}\n.leaflet-sbs-range::-moz-focus-outer {\n    border: 0;\n}\n\n",""]),n.exports=e},9161:(n,e,t)=>{"use strict";t.r(e),t.d(e,{default:()=>i});const i=t.p+"69fbc9c24b3665b801445c9bccc7017d.png"},665:(n,e,t)=>{var i,a,r=t(5881);function s(n,e,t,i){e.split(" ").forEach((function(e){r.DomEvent.on(n,e,t,i)}))}function o(n,e,t,i){e.split(" ").forEach((function(e){r.DomEvent.off(n,e,t,i)}))}function l(n){return"oninput"in n?"input":"change"}function p(){i=this._map.dragging.enabled(),a=this._map.tap&&this._map.tap.enabled(),this._map.dragging.disable(),this._map.tap&&this._map.tap.disable()}function d(n){this._refocusOnMap(n),i&&this._map.dragging.enable(),a&&this._map.tap.enable()}function u(n){return"undefined"===n?[]:Array.isArray(n)?n:[n]}t(9791),t(3230),r.Control.SplitMap=r.Control.extend({options:{thumbSize:42,padding:0},initialize:function(n,e,t){this._leftLayers=u(n),this._rightLayers=u(e),this._updateClip(),r.setOptions(this,t)},getPosition:function(){var n=this._range.value,e=(.5-n)*(2*this.options.padding+this.options.thumbSize);return this._map.getSize().x*n+e},setPosition:function(){},includes:r.Mixin.Events,addTo:function(n){this.remove(),this._map=n;var e=this._container=r.DomUtil.create("div","leaflet-sbs",n._controlContainer);this._divider=r.DomUtil.create("div","leaflet-sbs-divider",e);var t=this._range=r.DomUtil.create("input","leaflet-sbs-range",e);return t.type="range",t.min=0,t.max=1,t.step="any",t.value=.5,t.style.paddingLeft=t.style.paddingRight=this.options.padding+"px",this._addEvents(),this._updateClip(),this},remove:function(){return this._map?(this._leftLayers.forEach((n=>{n.getContainer?n.getContainer().style.clip="":n.getPane().style.clip=""})),this._rightLayers.forEach((n=>{n.getContainer?n.getContainer().style.clip="":n.getPane().style.clip=""})),this._removeEvents(),r.DomUtil.remove(this._container),this._map=null,this):this},_updateClip:function(){if(!this._map)return this;var n=this._map,e=n.containerPointToLayerPoint([0,0]),t=n.containerPointToLayerPoint(n.getSize()),i=e.x+this.getPosition(),a=this.getPosition();this._divider.style.left=a+"px",this.fire("dividermove",{x:a});var r="rect("+[e.y,i,t.y,e.x].join("px,")+"px)",s="rect("+[e.y,t.x,t.y,i].join("px,")+"px)";this._leftLayers.forEach((n=>{n.getContainer?n.getContainer().style.clip=r:n.getPane().style.clip=r})),this._rightLayers.forEach((n=>{n.getContainer?n.getContainer().style.clip=s:n.getPane().style.clip=s}))},_addEvents:function(){var n=this._range,e=this._map;e&&n&&(e.on("move",this._updateClip,this),e.on("layeradd layerremove",this._updateLayers,this),s(n,l(n),this._updateClip,this),s(n,r.Browser.touch?"touchstart":"mousedown",p,this),s(n,r.Browser.touch?"touchend":"mouseup",d,this))},_removeEvents:function(){var n=this._range,e=this._map;n&&(o(n,l(n),this._updateClip,this),o(n,r.Browser.touch?"touchstart":"mousedown",p,this),o(n,r.Browser.touch?"touchend":"mouseup",d,this)),e&&(e.off("layeradd layerremove",this._updateLayers,this),e.off("move",this._updateClip,this))}}),r.control.splitMap=function(n,e,t){return new r.Control.SplitMap(n,e,t)},n.exports=r.Control.SplitMap},9791:(n,e,t)=>{var i=t(3379),a=t(5202);"string"==typeof(a=a.__esModule?a.default:a)&&(a=[[n.id,a,""]]);i(a,{insert:"head",singleton:!1}),n.exports=a.locals||{}},3230:(n,e,t)=>{var i=t(3379),a=t(8102);"string"==typeof(a=a.__esModule?a.default:a)&&(a=[[n.id,a,""]]);i(a,{insert:"head",singleton:!1}),n.exports=a.locals||{}}}]);