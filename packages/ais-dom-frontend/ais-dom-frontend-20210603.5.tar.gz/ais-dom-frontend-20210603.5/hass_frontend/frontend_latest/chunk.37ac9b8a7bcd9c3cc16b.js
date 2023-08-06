/*! For license information please see chunk.37ac9b8a7bcd9c3cc16b.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[392],{65660:(e,t,n)=>{"use strict";n(65233);const o=n(50856).d`
<custom-style>
  <style is="custom-style">
    [hidden] {
      display: none !important;
    }
  </style>
</custom-style>
<custom-style>
  <style is="custom-style">
    html {

      --layout: {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      };

      --layout-inline: {
        display: -ms-inline-flexbox;
        display: -webkit-inline-flex;
        display: inline-flex;
      };

      --layout-horizontal: {
        @apply --layout;

        -ms-flex-direction: row;
        -webkit-flex-direction: row;
        flex-direction: row;
      };

      --layout-horizontal-reverse: {
        @apply --layout;

        -ms-flex-direction: row-reverse;
        -webkit-flex-direction: row-reverse;
        flex-direction: row-reverse;
      };

      --layout-vertical: {
        @apply --layout;

        -ms-flex-direction: column;
        -webkit-flex-direction: column;
        flex-direction: column;
      };

      --layout-vertical-reverse: {
        @apply --layout;

        -ms-flex-direction: column-reverse;
        -webkit-flex-direction: column-reverse;
        flex-direction: column-reverse;
      };

      --layout-wrap: {
        -ms-flex-wrap: wrap;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
      };

      --layout-wrap-reverse: {
        -ms-flex-wrap: wrap-reverse;
        -webkit-flex-wrap: wrap-reverse;
        flex-wrap: wrap-reverse;
      };

      --layout-flex-auto: {
        -ms-flex: 1 1 auto;
        -webkit-flex: 1 1 auto;
        flex: 1 1 auto;
      };

      --layout-flex-none: {
        -ms-flex: none;
        -webkit-flex: none;
        flex: none;
      };

      --layout-flex: {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      };

      --layout-flex-2: {
        -ms-flex: 2;
        -webkit-flex: 2;
        flex: 2;
      };

      --layout-flex-3: {
        -ms-flex: 3;
        -webkit-flex: 3;
        flex: 3;
      };

      --layout-flex-4: {
        -ms-flex: 4;
        -webkit-flex: 4;
        flex: 4;
      };

      --layout-flex-5: {
        -ms-flex: 5;
        -webkit-flex: 5;
        flex: 5;
      };

      --layout-flex-6: {
        -ms-flex: 6;
        -webkit-flex: 6;
        flex: 6;
      };

      --layout-flex-7: {
        -ms-flex: 7;
        -webkit-flex: 7;
        flex: 7;
      };

      --layout-flex-8: {
        -ms-flex: 8;
        -webkit-flex: 8;
        flex: 8;
      };

      --layout-flex-9: {
        -ms-flex: 9;
        -webkit-flex: 9;
        flex: 9;
      };

      --layout-flex-10: {
        -ms-flex: 10;
        -webkit-flex: 10;
        flex: 10;
      };

      --layout-flex-11: {
        -ms-flex: 11;
        -webkit-flex: 11;
        flex: 11;
      };

      --layout-flex-12: {
        -ms-flex: 12;
        -webkit-flex: 12;
        flex: 12;
      };

      /* alignment in cross axis */

      --layout-start: {
        -ms-flex-align: start;
        -webkit-align-items: flex-start;
        align-items: flex-start;
      };

      --layout-center: {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      };

      --layout-end: {
        -ms-flex-align: end;
        -webkit-align-items: flex-end;
        align-items: flex-end;
      };

      --layout-baseline: {
        -ms-flex-align: baseline;
        -webkit-align-items: baseline;
        align-items: baseline;
      };

      /* alignment in main axis */

      --layout-start-justified: {
        -ms-flex-pack: start;
        -webkit-justify-content: flex-start;
        justify-content: flex-start;
      };

      --layout-center-justified: {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      };

      --layout-end-justified: {
        -ms-flex-pack: end;
        -webkit-justify-content: flex-end;
        justify-content: flex-end;
      };

      --layout-around-justified: {
        -ms-flex-pack: distribute;
        -webkit-justify-content: space-around;
        justify-content: space-around;
      };

      --layout-justified: {
        -ms-flex-pack: justify;
        -webkit-justify-content: space-between;
        justify-content: space-between;
      };

      --layout-center-center: {
        @apply --layout-center;
        @apply --layout-center-justified;
      };

      /* self alignment */

      --layout-self-start: {
        -ms-align-self: flex-start;
        -webkit-align-self: flex-start;
        align-self: flex-start;
      };

      --layout-self-center: {
        -ms-align-self: center;
        -webkit-align-self: center;
        align-self: center;
      };

      --layout-self-end: {
        -ms-align-self: flex-end;
        -webkit-align-self: flex-end;
        align-self: flex-end;
      };

      --layout-self-stretch: {
        -ms-align-self: stretch;
        -webkit-align-self: stretch;
        align-self: stretch;
      };

      --layout-self-baseline: {
        -ms-align-self: baseline;
        -webkit-align-self: baseline;
        align-self: baseline;
      };

      /* multi-line alignment in main axis */

      --layout-start-aligned: {
        -ms-flex-line-pack: start;  /* IE10 */
        -ms-align-content: flex-start;
        -webkit-align-content: flex-start;
        align-content: flex-start;
      };

      --layout-end-aligned: {
        -ms-flex-line-pack: end;  /* IE10 */
        -ms-align-content: flex-end;
        -webkit-align-content: flex-end;
        align-content: flex-end;
      };

      --layout-center-aligned: {
        -ms-flex-line-pack: center;  /* IE10 */
        -ms-align-content: center;
        -webkit-align-content: center;
        align-content: center;
      };

      --layout-between-aligned: {
        -ms-flex-line-pack: justify;  /* IE10 */
        -ms-align-content: space-between;
        -webkit-align-content: space-between;
        align-content: space-between;
      };

      --layout-around-aligned: {
        -ms-flex-line-pack: distribute;  /* IE10 */
        -ms-align-content: space-around;
        -webkit-align-content: space-around;
        align-content: space-around;
      };

      /*******************************
                Other Layout
      *******************************/

      --layout-block: {
        display: block;
      };

      --layout-invisible: {
        visibility: hidden !important;
      };

      --layout-relative: {
        position: relative;
      };

      --layout-fit: {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-scroll: {
        -webkit-overflow-scrolling: touch;
        overflow: auto;
      };

      --layout-fullbleed: {
        margin: 0;
        height: 100vh;
      };

      /* fixed position */

      --layout-fixed-top: {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
      };

      --layout-fixed-right: {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
      };

      --layout-fixed-bottom: {
        position: fixed;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-fixed-left: {
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
      };

    }
  </style>
</custom-style>`;o.setAttribute("style","display: none;"),document.head.appendChild(o.content);var i=document.createElement("style");i.textContent="[hidden] { display: none !important; }",document.head.appendChild(i)},43835:(e,t,n)=>{"use strict";n(65660),n(54242),n(70019)},70019:(e,t,n)=>{"use strict";n(65233);const o=n(50856).d`<custom-style>
  <style is="custom-style">
    html {

      /* Shared Styles */
      --paper-font-common-base: {
        font-family: 'Roboto', 'Noto', sans-serif;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-code: {
        font-family: 'Roboto Mono', 'Consolas', 'Menlo', monospace;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-expensive-kerning: {
        text-rendering: optimizeLegibility;
      };

      --paper-font-common-nowrap: {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      };

      /* Material Font Styles */

      --paper-font-display4: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 112px;
        font-weight: 300;
        letter-spacing: -.044em;
        line-height: 120px;
      };

      --paper-font-display3: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 56px;
        font-weight: 400;
        letter-spacing: -.026em;
        line-height: 60px;
      };

      --paper-font-display2: {
        @apply --paper-font-common-base;

        font-size: 45px;
        font-weight: 400;
        letter-spacing: -.018em;
        line-height: 48px;
      };

      --paper-font-display1: {
        @apply --paper-font-common-base;

        font-size: 34px;
        font-weight: 400;
        letter-spacing: -.01em;
        line-height: 40px;
      };

      --paper-font-headline: {
        @apply --paper-font-common-base;

        font-size: 24px;
        font-weight: 400;
        letter-spacing: -.012em;
        line-height: 32px;
      };

      --paper-font-title: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 20px;
        font-weight: 500;
        line-height: 28px;
      };

      --paper-font-subhead: {
        @apply --paper-font-common-base;

        font-size: 16px;
        font-weight: 400;
        line-height: 24px;
      };

      --paper-font-body2: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-body1: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 400;
        line-height: 20px;
      };

      --paper-font-caption: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 12px;
        font-weight: 400;
        letter-spacing: 0.011em;
        line-height: 20px;
      };

      --paper-font-menu: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 13px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-button: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.018em;
        line-height: 24px;
        text-transform: uppercase;
      };

      --paper-font-code2: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 700;
        line-height: 20px;
      };

      --paper-font-code1: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 500;
        line-height: 20px;
      };

    }

  </style>
</custom-style>`;o.setAttribute("style","display: none;"),document.head.appendChild(o.content)},21384:(e,t,n)=>{"use strict";n.d(t,{t:()=>c});n(56646);var o=n(42687),i=n(74460);let s={},l={};function r(e,t){s[e]=l[e.toLowerCase()]=t}function a(e){return s[e]||l[e.toLowerCase()]}class c extends HTMLElement{static get observedAttributes(){return["id"]}static import(e,t){if(e){let n=a(e);return n&&t?n.querySelector(t):n}return null}attributeChangedCallback(e,t,n,o){t!==n&&this.register()}get assetpath(){if(!this.__assetpath){const e=window.HTMLImports&&HTMLImports.importForElement?HTMLImports.importForElement(this)||document:this.ownerDocument,t=(0,o.Kk)(this.getAttribute("assetpath")||"",e.baseURI);this.__assetpath=(0,o.iY)(t)}return this.__assetpath}register(e){if(e=e||this.id){if(i.XN&&void 0!==a(e))throw r(e,null),new Error(`strictTemplatePolicy: dom-module ${e} re-registered`);this.id=e,r(e,this),(t=this).querySelector("style")&&console.warn("dom-module %s has style outside template",t.id)}var t}}c.prototype.modules=s,customElements.define("dom-module",c)},33367:(e,t,n)=>{"use strict";n.d(t,{w:()=>c});var o=n(81850);let i={attached:!0,detached:!0,ready:!0,created:!0,beforeRegister:!0,registered:!0,attributeChanged:!0,behaviors:!0};function s(e,t){if(!e)return t=t;t=(0,o.x)(t),Array.isArray(e)||(e=[e]);let n=t.prototype.behaviors;return t=l(e=r(e,null,n),t),n&&(e=n.concat(e)),t.prototype.behaviors=e,t}function l(e,t){for(let n=0;n<e.length;n++){let o=e[n];o&&(t=Array.isArray(o)?l(o,t):a(o,t))}return t}function r(e,t,n){t=t||[];for(let o=e.length-1;o>=0;o--){let i=e[o];i?Array.isArray(i)?r(i,t):t.indexOf(i)<0&&(!n||n.indexOf(i)<0)&&t.unshift(i):console.warn("behavior is null, check for missing or 404 import")}return t}function a(e,t){class n extends t{static get properties(){return e.properties}static get observers(){return e.observers}created(){super.created(),e.created&&e.created.call(this)}_registered(){super._registered(),e.beforeRegister&&e.beforeRegister.call(Object.getPrototypeOf(this)),e.registered&&e.registered.call(Object.getPrototypeOf(this))}_applyListeners(){if(super._applyListeners(),e.listeners)for(let t in e.listeners)this._addMethodEventListenerToNode(this,t,e.listeners[t])}_ensureAttributes(){if(e.hostAttributes)for(let t in e.hostAttributes)this._ensureAttribute(t,e.hostAttributes[t]);super._ensureAttributes()}ready(){super.ready(),e.ready&&e.ready.call(this)}attached(){super.attached(),e.attached&&e.attached.call(this)}detached(){super.detached(),e.detached&&e.detached.call(this)}attributeChanged(t,n,o){super.attributeChanged(t,n,o),e.attributeChanged&&e.attributeChanged.call(this,t,n,o)}}n.generatedFrom=e;for(let t in e)if(!(t in i)){let o=Object.getOwnPropertyDescriptor(e,t);o&&Object.defineProperty(n.prototype,t,o)}return n}const c=function(e,t){e||console.warn("Polymer's Class function requires `info` argument");const n=e.behaviors?s(e.behaviors,HTMLElement):(0,o.x)(HTMLElement),i=a(e,t?t(n):n);return i.is=e.is,i}},72419:(e,t,n)=>{"use strict";var o=n(18691);let i;i=o.E._mutablePropertyChange;Boolean},9672:(e,t,n)=>{"use strict";var o=n(33367);n(56646);const i=function(e){let t;return t="function"==typeof e?e:i.Class(e),customElements.define(t.is,t),t};i.Class=o.w},87156:(e,t,n)=>{"use strict";n.d(t,{Ku:()=>l,vz:()=>c});n(56646),n(74460);var o=n(20723);n(93252),n(78956);const i=Element.prototype,s=i.matches||i.matchesSelector||i.mozMatchesSelector||i.msMatchesSelector||i.oMatchesSelector||i.webkitMatchesSelector,l=function(e,t){return s.call(e,t)};class r{constructor(e){this.node=e}observeNodes(e){return new o.o(this.node,e)}unobserveNodes(e){e.disconnect()}notifyObserver(){}deepContains(e){if(this.node.contains(e))return!0;let t=e,n=e.ownerDocument;for(;t&&t!==n&&t!==this.node;)t=t.parentNode||t.host;return t===this.node}getOwnerRoot(){return this.node.getRootNode()}getDistributedNodes(){return"slot"===this.node.localName?this.node.assignedNodes({flatten:!0}):[]}getDestinationInsertionPoints(){let e=[],t=this.node.assignedSlot;for(;t;)e.push(t),t=t.assignedSlot;return e}importNode(e,t){return(this.node instanceof Document?this.node:this.node.ownerDocument).importNode(e,t)}getEffectiveChildNodes(){return o.o.getFlattenedNodes(this.node)}queryDistributedElements(e){let t=this.getEffectiveChildNodes(),n=[];for(let o,i=0,s=t.length;i<s&&(o=t[i]);i++)o.nodeType===Node.ELEMENT_NODE&&l(o,e)&&n.push(o);return n}get activeElement(){let e=this.node;return void 0!==e._activeElement?e._activeElement:e.activeElement}}class a{constructor(e){this.event=e}get rootTarget(){return this.event.composedPath()[0]}get localTarget(){return this.event.target}get path(){return this.event.composedPath()}}r.prototype.cloneNode,r.prototype.appendChild,r.prototype.insertBefore,r.prototype.removeChild,r.prototype.replaceChild,r.prototype.setAttribute,r.prototype.removeAttribute,r.prototype.querySelector,r.prototype.querySelectorAll,r.prototype.parentNode,r.prototype.firstChild,r.prototype.lastChild,r.prototype.nextSibling,r.prototype.previousSibling,r.prototype.firstElementChild,r.prototype.lastElementChild,r.prototype.nextElementSibling,r.prototype.previousElementSibling,r.prototype.childNodes,r.prototype.children,r.prototype.classList,r.prototype.textContent,r.prototype.innerHTML,function(e,t){for(let n=0;n<t.length;n++){let o=t[n];e[o]=function(){return this.node[o].apply(this.node,arguments)}}}(r.prototype,["cloneNode","appendChild","insertBefore","removeChild","replaceChild","setAttribute","removeAttribute","querySelector","querySelectorAll"]),function(e,t){for(let n=0;n<t.length;n++){let o=t[n];Object.defineProperty(e,o,{get:function(){return this.node[o]},configurable:!0})}}(r.prototype,["parentNode","firstChild","lastChild","nextSibling","previousSibling","firstElementChild","lastElementChild","nextElementSibling","previousElementSibling","childNodes","children","classList"]),function(e,t){for(let n=0;n<t.length;n++){let o=t[n];Object.defineProperty(e,o,{get:function(){return this.node[o]},set:function(e){this.node[o]=e},configurable:!0})}}(r.prototype,["textContent","innerHTML"]);const c=function(e){if(!(e=e||document).__domApi){let t;t=e instanceof Event?new a(e):new r(e),e.__domApi=t}return e.__domApi}},37692:(e,t,n)=>{"use strict";n(52521)},21683:(e,t,n)=>{"use strict";n.d(t,{Wc:()=>a,YA:()=>c});n(56646);let o=0,i=0,s=[],l=0,r=document.createTextNode("");new window.MutationObserver((function(){const e=s.length;for(let t=0;t<e;t++){let e=s[t];if(e)try{e()}catch(e){setTimeout((()=>{throw e}))}}s.splice(0,e),i+=e})).observe(r,{characterData:!0});const a={after:e=>({run:t=>window.setTimeout(t,e),cancel(e){window.clearTimeout(e)}}),run:(e,t)=>window.setTimeout(e,t),cancel(e){window.clearTimeout(e)}},c={run:e=>(r.textContent=l++,s.push(e),o++),cancel(e){const t=e-i;if(t>=0){if(!s[t])throw new Error("invalid async handle: "+e);s[t]=null}}}},81668:(e,t,n)=>{"use strict";n.d(t,{NH:()=>H,ys:()=>z,BP:()=>L});n(56646);var o=n(21683),i=n(78956),s=n(74460);let l="string"==typeof document.head.style.touchAction,r="__polymerGestures",a="__polymerGesturesHandled",c="__polymerGesturesTouchAction",p=["mousedown","mousemove","mouseup","click"],u=[0,1,4,2],f=function(){try{return 1===new MouseEvent("test",{buttons:1}).buttons}catch(e){return!1}}();function d(e){return p.indexOf(e)>-1}let h=!1;function m(e){if(!d(e)&&"touchend"!==e)return l&&h&&s.f6?{passive:!0}:void 0}!function(){try{let e=Object.defineProperty({},"passive",{get(){h=!0}});window.addEventListener("test",null,e),window.removeEventListener("test",null,e)}catch(e){}}();let y=navigator.userAgent.match(/iP(?:[oa]d|hone)|Android/);const g=[],x={button:!0,input:!0,keygen:!0,meter:!0,output:!0,textarea:!0,progress:!0,select:!0},_={button:!0,command:!0,fieldset:!0,input:!0,keygen:!0,optgroup:!0,option:!0,select:!0,textarea:!0};function b(e){let t=Array.prototype.slice.call(e.labels||[]);if(!t.length){t=[];let n=e.getRootNode();if(e.id){let o=n.querySelectorAll(`label[for = ${e.id}]`);for(let e=0;e<o.length;e++)t.push(o[e])}}return t}let w=function(e){let t=e.sourceCapabilities;var n;if((!t||t.firesTouchEvents)&&(e[a]={skip:!0},"click"===e.type)){let t=!1,o=e.composedPath&&e.composedPath();if(o)for(let e=0;e<o.length;e++){if(o[e].nodeType===Node.ELEMENT_NODE)if("label"===o[e].localName)g.push(o[e]);else if(n=o[e],x[n.localName]){let n=b(o[e]);for(let e=0;e<n.length;e++)t=t||g.indexOf(n[e])>-1}if(o[e]===k.mouse.target)return}if(t)return;e.preventDefault(),e.stopPropagation()}};function v(e){let t=y?["click"]:p;for(let n,o=0;o<t.length;o++)n=t[o],e?(g.length=0,document.addEventListener(n,w,!0)):document.removeEventListener(n,w,!0)}function E(e){let t=e.type;if(!d(t))return!1;if("mousemove"===t){let t=void 0===e.buttons?1:e.buttons;return e instanceof window.MouseEvent&&!f&&(t=u[e.which]||0),Boolean(1&t)}return 0===(void 0===e.button?0:e.button)}let k={mouse:{target:null,mouseIgnoreJob:null},touch:{x:0,y:0,id:-1,scrollDecided:!1}};function T(e,t,n){e.movefn=t,e.upfn=n,document.addEventListener("mousemove",t),document.addEventListener("mouseup",n)}function P(e){document.removeEventListener("mousemove",e.movefn),document.removeEventListener("mouseup",e.upfn),e.movefn=null,e.upfn=null}document.addEventListener("touchend",(function(e){k.mouse.mouseIgnoreJob||v(!0),k.mouse.target=e.composedPath()[0],k.mouse.mouseIgnoreJob=i.d.debounce(k.mouse.mouseIgnoreJob,o.Wc.after(2500),(function(){v(),k.mouse.target=null,k.mouse.mouseIgnoreJob=null}))}),!!h&&{passive:!0});const C={},N=[];function O(e){if(e.composedPath){const t=e.composedPath();return t.length>0?t[0]:e.target}return e.target}function M(e){let t,n=e.type,o=e.currentTarget[r];if(!o)return;let i=o[n];if(i){if(!e[a]&&(e[a]={},"touch"===n.slice(0,5))){let t=(e=e).changedTouches[0];if("touchstart"===n&&1===e.touches.length&&(k.touch.id=t.identifier),k.touch.id!==t.identifier)return;l||"touchstart"!==n&&"touchmove"!==n||function(e){let t=e.changedTouches[0],n=e.type;if("touchstart"===n)k.touch.x=t.clientX,k.touch.y=t.clientY,k.touch.scrollDecided=!1;else if("touchmove"===n){if(k.touch.scrollDecided)return;k.touch.scrollDecided=!0;let n=function(e){let t="auto",n=e.composedPath&&e.composedPath();if(n)for(let e,o=0;o<n.length;o++)if(e=n[o],e[c]){t=e[c];break}return t}(e),o=!1,i=Math.abs(k.touch.x-t.clientX),s=Math.abs(k.touch.y-t.clientY);e.cancelable&&("none"===n?o=!0:"pan-x"===n?o=s>i:"pan-y"===n&&(o=i>s)),o?e.preventDefault():D("track")}}(e)}if(t=e[a],!t.skip){for(let n,o=0;o<N.length;o++)n=N[o],i[n.name]&&!t[n.name]&&n.flow&&n.flow.start.indexOf(e.type)>-1&&n.reset&&n.reset();for(let o,s=0;s<N.length;s++)o=N[s],i[o.name]&&!t[o.name]&&(t[o.name]=!0,o[n](e))}}}function H(e,t,n){return!!C[t]&&(function(e,t,n){let o=C[t],i=o.deps,s=o.name,l=e[r];l||(e[r]=l={});for(let t,n,o=0;o<i.length;o++)t=i[o],y&&d(t)&&"click"!==t||(n=l[t],n||(l[t]=n={_count:0}),0===n._count&&e.addEventListener(t,M,m(t)),n[s]=(n[s]||0)+1,n._count=(n._count||0)+1);e.addEventListener(t,n),o.touchAction&&L(e,o.touchAction)}(e,t,n),!0)}function z(e,t,n){return!!C[t]&&(function(e,t,n){let o=C[t],i=o.deps,s=o.name,l=e[r];if(l)for(let t,n,o=0;o<i.length;o++)t=i[o],n=l[t],n&&n[s]&&(n[s]=(n[s]||1)-1,n._count=(n._count||1)-1,0===n._count&&e.removeEventListener(t,M,m(t)));e.removeEventListener(t,n)}(e,t,n),!0)}function A(e){N.push(e);for(let t=0;t<e.emits.length;t++)C[e.emits[t]]=e}function L(e,t){l&&e instanceof HTMLElement&&o.YA.run((()=>{e.style.touchAction=t})),e[c]=t}function S(e,t,n){let o=new Event(t,{bubbles:!0,cancelable:!0,composed:!0});if(o.detail=n,e.dispatchEvent(o),o.defaultPrevented){let e=n.preventer||n.sourceEvent;e&&e.preventDefault&&e.preventDefault()}}function D(e){let t=function(e){for(let t,n=0;n<N.length;n++){t=N[n];for(let n,o=0;o<t.emits.length;o++)if(n=t.emits[o],n===e)return t}return null}(e);t.info&&(t.info.prevent=!0)}function j(e,t,n,o){t&&S(t,e,{x:n.clientX,y:n.clientY,sourceEvent:n,preventer:o,prevent:function(e){return D(e)}})}function Y(e,t,n){if(e.prevent)return!1;if(e.started)return!0;let o=Math.abs(e.x-t),i=Math.abs(e.y-n);return o>=5||i>=5}function I(e,t,n){if(!t)return;let o,i=e.moves[e.moves.length-2],s=e.moves[e.moves.length-1],l=s.x-e.x,r=s.y-e.y,a=0;i&&(o=s.x-i.x,a=s.y-i.y),S(t,"track",{state:e.state,x:n.clientX,y:n.clientY,dx:l,dy:r,ddx:o,ddy:a,sourceEvent:n,hover:function(){return function(e,t){let n=document.elementFromPoint(e,t),o=n;for(;o&&o.shadowRoot&&!window.ShadyDOM;){let i=o;if(o=o.shadowRoot.elementFromPoint(e,t),i===o)break;o&&(n=o)}return n}(n.clientX,n.clientY)}})}function R(e,t,n){let o=Math.abs(t.clientX-e.x),i=Math.abs(t.clientY-e.y),s=O(n||t);!s||_[s.localName]&&s.hasAttribute("disabled")||(isNaN(o)||isNaN(i)||o<=25&&i<=25||function(e){if("click"===e.type){if(0===e.detail)return!0;let t=O(e);if(!t.nodeType||t.nodeType!==Node.ELEMENT_NODE)return!0;let n=t.getBoundingClientRect(),o=e.pageX,i=e.pageY;return!(o>=n.left&&o<=n.right&&i>=n.top&&i<=n.bottom)}return!1}(t))&&(e.prevent||S(s,"tap",{x:t.clientX,y:t.clientY,sourceEvent:t,preventer:n}))}A({name:"downup",deps:["mousedown","touchstart","touchend"],flow:{start:["mousedown","touchstart"],end:["mouseup","touchend"]},emits:["down","up"],info:{movefn:null,upfn:null},reset:function(){P(this.info)},mousedown:function(e){if(!E(e))return;let t=O(e),n=this;T(this.info,(function(e){E(e)||(j("up",t,e),P(n.info))}),(function(e){E(e)&&j("up",t,e),P(n.info)})),j("down",t,e)},touchstart:function(e){j("down",O(e),e.changedTouches[0],e)},touchend:function(e){j("up",O(e),e.changedTouches[0],e)}}),A({name:"track",touchAction:"none",deps:["mousedown","touchstart","touchmove","touchend"],flow:{start:["mousedown","touchstart"],end:["mouseup","touchend"]},emits:["track"],info:{x:0,y:0,state:"start",started:!1,moves:[],addMove:function(e){this.moves.length>2&&this.moves.shift(),this.moves.push(e)},movefn:null,upfn:null,prevent:!1},reset:function(){this.info.state="start",this.info.started=!1,this.info.moves=[],this.info.x=0,this.info.y=0,this.info.prevent=!1,P(this.info)},mousedown:function(e){if(!E(e))return;let t=O(e),n=this,o=function(e){let o=e.clientX,i=e.clientY;Y(n.info,o,i)&&(n.info.state=n.info.started?"mouseup"===e.type?"end":"track":"start","start"===n.info.state&&D("tap"),n.info.addMove({x:o,y:i}),E(e)||(n.info.state="end",P(n.info)),t&&I(n.info,t,e),n.info.started=!0)};T(this.info,o,(function(e){n.info.started&&o(e),P(n.info)})),this.info.x=e.clientX,this.info.y=e.clientY},touchstart:function(e){let t=e.changedTouches[0];this.info.x=t.clientX,this.info.y=t.clientY},touchmove:function(e){let t=O(e),n=e.changedTouches[0],o=n.clientX,i=n.clientY;Y(this.info,o,i)&&("start"===this.info.state&&D("tap"),this.info.addMove({x:o,y:i}),I(this.info,t,n),this.info.state="track",this.info.started=!0)},touchend:function(e){let t=O(e),n=e.changedTouches[0];this.info.started&&(this.info.state="end",this.info.addMove({x:n.clientX,y:n.clientY}),I(this.info,t,n))}}),A({name:"tap",deps:["mousedown","click","touchstart","touchend"],flow:{start:["mousedown","touchstart"],end:["click","touchend"]},emits:["tap"],info:{x:NaN,y:NaN,prevent:!1},reset:function(){this.info.x=NaN,this.info.y=NaN,this.info.prevent=!1},mousedown:function(e){E(e)&&(this.info.x=e.clientX,this.info.y=e.clientY)},click:function(e){E(e)&&R(this.info,e)},touchstart:function(e){const t=e.changedTouches[0];this.info.x=t.clientX,this.info.y=t.clientY},touchend:function(e){R(this.info,e.changedTouches[0],e)}})},87529:(e,t,n)=>{"use strict";n(56646)},74460:(e,t,n)=>{"use strict";n.d(t,{sM:()=>i,v1:()=>s,f6:()=>l,XN:()=>r,ZN:()=>a});n(56646);var o=n(42687);window.ShadyDOM,Boolean(!window.ShadyCSS||window.ShadyCSS.nativeCss),window.customElements.polyfillWrapFlushCallback;let i=(0,o.iY)(document.baseURI||window.location.href);let s=window.Polymer&&window.Polymer.sanitizeDOMValue||void 0;let l=!1;let r=!1;let a=!1},52521:(e,t,n)=>{"use strict";n.d(t,{Uv:()=>x,GJ:()=>_});n(56646);var o=n(40729),i=n(18691),s=n(74460);let l=null;function r(){return l}r.prototype=Object.create(HTMLTemplateElement.prototype,{constructor:{value:r,writable:!0}});const a=(0,o.q)(r),c=(0,i.E)(a);const p=(0,o.q)(class{});class u extends p{constructor(e){super(),this._configureProperties(e),this.root=this._stampTemplate(this.__dataHost);let t=this.children=[];for(let e=this.root.firstChild;e;e=e.nextSibling)t.push(e),e.__templatizeInstance=this;this.__templatizeOwner&&this.__templatizeOwner.__hideTemplateChildren__&&this._showHideChildren(!0);let n=this.__templatizeOptions;(e&&n.instanceProps||!n.instanceProps)&&this._enableProperties()}_configureProperties(e){if(this.__templatizeOptions.forwardHostProp)for(let e in this.__hostProps)this._setPendingProperty(e,this.__dataHost["_host_"+e]);for(let t in e)this._setPendingProperty(t,e[t])}forwardHostProp(e,t){this._setPendingPropertyOrPath(e,t,!1,!0)&&this.__dataHost._enqueueClient(this)}_addEventListenerToNode(e,t,n){if(this._methodHost&&this.__templatizeOptions.parentModel)this._methodHost._addEventListenerToNode(e,t,(e=>{e.model=this,n(e)}));else{let o=this.__dataHost.__dataHost;o&&o._addEventListenerToNode(e,t,n)}}_showHideChildren(e){let t=this.children;for(let n=0;n<t.length;n++){let o=t[n];if(Boolean(e)!=Boolean(o.__hideTemplateChildren__))if(o.nodeType===Node.TEXT_NODE)e?(o.__polymerTextContent__=o.textContent,o.textContent=""):o.textContent=o.__polymerTextContent__;else if("slot"===o.localName)if(e)o.__polymerReplaced__=document.createComment("hidden-slot"),o.parentNode.replaceChild(o.__polymerReplaced__,o);else{const e=o.__polymerReplaced__;e&&e.parentNode.replaceChild(o,e)}else o.style&&(e?(o.__polymerDisplay__=o.style.display,o.style.display="none"):o.style.display=o.__polymerDisplay__);o.__hideTemplateChildren__=e,o._showHideChildren&&o._showHideChildren(e)}}_setUnmanagedPropertyToNode(e,t,n){e.__hideTemplateChildren__&&e.nodeType==Node.TEXT_NODE&&"textContent"==t?e.__polymerTextContent__=n:super._setUnmanagedPropertyToNode(e,t,n)}get parentModel(){let e=this.__parentModel;if(!e){let t;e=this;do{e=e.__dataHost.__dataHost}while((t=e.__templatizeOptions)&&!t.parentModel);this.__parentModel=e}return e}dispatchEvent(e){return!0}}u.prototype.__dataHost,u.prototype.__templatizeOptions,u.prototype._methodHost,u.prototype.__templatizeOwner,u.prototype.__hostProps;const f=(0,i.E)(u);function d(e){let t=e.__dataHost;return t&&t._methodHost||t}function h(e,t,n){let o=n.mutableData?f:u,i=class extends o{};return i.prototype.__templatizeOptions=n,i.prototype._bindTemplate(e),function(e,t,n,o){let i=n.hostProps||{};for(let t in o.instanceProps){delete i[t];let n=o.notifyInstanceProp;n&&e.prototype._addPropertyEffect(t,e.prototype.PROPERTY_EFFECT_TYPES.NOTIFY,{fn:g(t,n)})}if(o.forwardHostProp&&t.__dataHost)for(let t in i)e.prototype._addPropertyEffect(t,e.prototype.PROPERTY_EFFECT_TYPES.NOTIFY,{fn:function(e,t,n){e.__dataHost._setPendingPropertyOrPath("_host_"+t,n[t],!0,!0)}})}(i,e,t,n),i}function m(e,t,n){let o=n.forwardHostProp;if(o){let i=t.templatizeTemplateClass;if(!i){let e=n.mutableData?c:a;i=t.templatizeTemplateClass=class extends e{};let s=t.hostProps;for(let e in s)i.prototype._addPropertyEffect("_host_"+e,i.prototype.PROPERTY_EFFECT_TYPES.PROPAGATE,{fn:y(e,o)}),i.prototype._createNotifyingProperty("_host_"+e)}!function(e,t){l=e,Object.setPrototypeOf(e,t.prototype),new t,l=null}(e,i),e.__dataProto&&Object.assign(e.__data,e.__dataProto),e.__dataTemp={},e.__dataPending=null,e.__dataOld=null,e._enableProperties()}}function y(e,t){return function(e,n,o){t.call(e.__templatizeOwner,n.substring("_host_".length),o[n])}}function g(e,t){return function(e,n,o){t.call(e.__templatizeOwner,e,n,o[n])}}function x(e,t,n){if(s.XN&&!d(e))throw new Error("strictTemplatePolicy: template owner not trusted");if(n=n||{},e.__templatizeOwner)throw new Error("A <template> can only be templatized once");e.__templatizeOwner=t;let o=(t?t.constructor:u)._parseTemplate(e),i=o.templatizeInstanceClass;i||(i=h(e,o,n),o.templatizeInstanceClass=i),m(e,o,n);let l=class extends i{};return l.prototype._methodHost=d(e),l.prototype.__dataHost=e,l.prototype.__templatizeOwner=t,l.prototype.__hostProps=o.hostProps,l=l,l}function _(e,t){let n;for(;t;)if(n=t.__templatizeInstance){if(n.__dataHost==e)return n;t=n.__dataHost}else t=t.parentNode;return null}},28426:(e,t,n)=>{"use strict";n.d(t,{H3:()=>i});var o=n(36608);n(50856);const i=(0,o.SH)(HTMLElement)},65233:(e,t,n)=>{"use strict";var o=n(81850);n(9672),n(37692),n(9024),n(42173),n(26047),n(37961),n(5618),n(72419),n(50856);(0,o.x)(HTMLElement).prototype}}]);
//# sourceMappingURL=chunk.37ac9b8a7bcd9c3cc16b.js.map