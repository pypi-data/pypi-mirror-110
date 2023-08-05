/*! For license information please see chunk.2549edd3c79c620b1aca.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[3684],{49706:(e,t,r)=>{"use strict";r.d(t,{Rb:()=>i,Zy:()=>a,h2:()=>s,PS:()=>o,l:()=>n,ht:()=>l,f0:()=>c,tj:()=>d,uo:()=>h,lC:()=>p,Kk:()=>u,iY:()=>f,ot:()=>m,gD:()=>y,AZ:()=>b});const i="hass:bookmark",a={alert:"hass:alert",alexa:"hass:amazon-alexa",air_quality:"hass:air-filter",automation:"hass:robot",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:cog",conversation:"hass:text-to-speech",counter:"hass:counter",device_tracker:"hass:account",fan:"hass:fan",google_assistant:"hass:google-assistant",group:"hass:google-circles-communities",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:toggle-switch-outline",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:form-textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",number:"hass:ray-vertex",persistent_notification:"hass:bell",person:"hass:account",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:palette",script:"hass:script-text",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer-outline",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weather:"hass:weather-cloudy",zone:"hass:map-marker-radius"},s={current:"hass:current-ac",carbon_dioxide:"mdi:molecule-co2",carbon_monoxide:"mdi:molecule-co",energy:"hass:flash",humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",pressure:"hass:gauge",power:"hass:flash",power_factor:"hass:angle-acute",signal_strength:"hass:wifi",timestamp:"hass:clock",voltage:"hass:sine-wave"},o=["climate","cover","configurator","input_select","input_number","input_text","lock","media_player","number","scene","script","timer","vacuum","water_heater"],n=["alarm_control_panel","automation","camera","climate","configurator","counter","cover","fan","group","humidifier","input_datetime","light","lock","media_player","person","remote","script","sun","timer","vacuum","water_heater","weather"],l=["input_number","input_select","input_text","number","scene"],c=["camera","configurator","scene"],d=["closed","locked","off"],h="on",p="off",u=new Set(["fan","input_boolean","light","switch","group","automation","humidifier"]),f=new Set(["camera","media_player"]),m="°C",y="°F",b=["ff0029","66a61e","377eb8","984ea3","00d2d5","ff7f00","af8d00","7f80cd","b3e900","c42e60","a65628","f781bf","8dd3c7","bebada","fb8072","80b1d3","fdb462","fccde5","bc80bd","ffed6f","c4eaff","cf8c00","1b9e77","d95f02","e7298a","e6ab02","a6761d","0097ff","00d067","f43600","4ba93b","5779bb","927acc","97ee3f","bf3947","9f5b00","f48758","8caed6","f2b94f","eff26e","e43872","d9b100","9d7a00","698cff","d9d9d9","00d27e","d06800","009f82","c49200","cbe8ff","fecddf","c27eb6","8cd2ce","c4b8d9","f883b0","a49100","f48800","27d0df","a04a9b"]},349:(e,t,r)=>{"use strict";function i(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}r.d(t,{m:()=>s});const a=new class{constructor(){i(this,"_storage",{}),i(this,"_listeners",{}),window.addEventListener("storage",(e=>{e.key&&this.hasKey(e.key)&&(this._storage[e.key]=e.newValue?JSON.parse(e.newValue):e.newValue,this._listeners[e.key]&&this._listeners[e.key].forEach((t=>t(e.oldValue?JSON.parse(e.oldValue):e.oldValue,this._storage[e.key]))))}))}addFromStorage(e){if(!this._storage[e]){const t=window.localStorage.getItem(e);t&&(this._storage[e]=JSON.parse(t))}}subscribeChanges(e,t){return this._listeners[e]?this._listeners[e].push(t):this._listeners[e]=[t],()=>{this.unsubscribeChanges(e,t)}}unsubscribeChanges(e,t){if(!(e in this._listeners))return;const r=this._listeners[e].indexOf(t);-1!==r&&this._listeners[e].splice(r,1)}hasKey(e){return e in this._storage}getValue(e){return this._storage[e]}setValue(e,t){this._storage[e]=t;try{window.localStorage.setItem(e,JSON.stringify(t))}catch(e){}}},s=(e,t,r)=>i=>{const s=String(i.key);e=e||String(i.key);const o=i.initializer?i.initializer():void 0;a.addFromStorage(e);const n=()=>a.hasKey(e)?a.getValue(e):o;return{kind:"method",placement:"prototype",key:i.key,descriptor:{set(r){((r,s)=>{let o;t&&(o=n()),a.setValue(e,s),t&&r.requestUpdate(i.key,o)})(this,r)},get:()=>n(),enumerable:!0,configurable:!0},finisher(o){if(t){const t=o.prototype.connectedCallback,n=o.prototype.disconnectedCallback;o.prototype.connectedCallback=function(){var r;t.call(this),this[`__unbsubLocalStorage${s}`]=(r=this,a.subscribeChanges(e,(e=>{r.requestUpdate(i.key,e)})))},o.prototype.disconnectedCallback=function(){n.call(this),this[`__unbsubLocalStorage${s}`]()},o.createProperty(i.key,{noAccessor:!0,...r})}}}}},27849:(e,t,r)=>{"use strict";r(39841);var i=r(50856);r(28426);class a extends(customElements.get("app-header-layout")){static get template(){return i.d`
      <style>
        :host {
          display: block;
          /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
          position: relative;
          z-index: 0;
        }

        #wrapper ::slotted([slot="header"]) {
          @apply --layout-fixed-top;
          z-index: 1;
        }

        #wrapper.initializing ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) {
          height: 100%;
        }

        :host([has-scrolling-region]) #wrapper ::slotted([slot="header"]) {
          position: absolute;
        }

        :host([has-scrolling-region])
          #wrapper.initializing
          ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) #wrapper #contentContainer {
          @apply --layout-fit;
          overflow-y: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
          position: relative;
        }

        #contentContainer {
          /* Create a stacking context here so that all children appear below the header. */
          position: relative;
          z-index: 0;
          /* Using 'transform' will cause 'position: fixed' elements to behave like
           'position: absolute' relative to this element. */
          transform: translate(0);
          margin-left: env(safe-area-inset-left);
          margin-right: env(safe-area-inset-right);
        }

        @media print {
          :host([has-scrolling-region]) #wrapper #contentContainer {
            overflow-y: visible;
          }
        }
      </style>

      <div id="wrapper" class="initializing">
        <slot id="headerSlot" name="header"></slot>

        <div id="contentContainer"><slot></slot></div>
        <slot id="fab" name="fab"></slot>
      </div>
    `}}customElements.define("ha-app-layout",a)},70379:(e,t,r)=>{"use strict";r.r(t);r(25230),r(53268),r(12730);var i=r(50424),a=r(55358),s=r(349),o=r(22311),n=r(40095),l=(r(48932),r(13997),r(69371)),c=(r(27849),r(11654)),d=r(47181);function h(){h=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var a=t.placement;if(t.kind===i&&("static"===a||"prototype"===a)){var s="static"===a?e:r;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],a={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,a)}),this),e.forEach((function(e){if(!f(e))return r.push(e);var t=this.decorateElement(e,a);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var s=this.decorateConstructor(r,t);return i.push.apply(i,s.finishers),s.finishers=i,s},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],a=e.decorators,s=a.length-1;s>=0;s--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var n=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,a[s])(n)||n);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var a=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[i])(a)||a);if(void 0!==s.finisher&&r.push(s.finisher),void 0!==s.elements){e=s.elements;for(var o=0;o<e.length-1;o++)for(var n=o+1;n<e.length;n++)if(e[o].key===e[n].key&&e[o].placement===e[n].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return g(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?g(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=b(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var a=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:r,placement:i,descriptor:Object.assign({},a)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(a,"get","The property descriptor of a field descriptor"),this.disallowProperty(a,"set","The property descriptor of a field descriptor"),this.disallowProperty(a,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function p(e){var t,r=b(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function u(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function f(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function b(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var a=h();if(i)for(var s=0;s<i.length;s++)a=i[s](a);var o=t((function(e){a.initializeInstanceElements(e,n.elements)}),r),n=a.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},i=0;i<e.length;i++){var a,s=e[i];if("method"===s.kind&&(a=t.find(r)))if(m(s.descriptor)||m(a.descriptor)){if(f(s)||f(a))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");a.descriptor=s.descriptor}else{if(f(s)){if(f(a))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");a.decorators=s.decorators}u(s,a)}else t.push(s)}return t}(o.d.map(p)),e);a.initializeClassElements(o.F,n.elements),a.runClassFinishers(o.F,n.finishers)}([(0,a.Mo)("ha-panel-media-browser")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,s.m)("mediaBrowseEntityId",!0)],key:"_entityId",value:()=>l.N8},{kind:"method",key:"render",value:function(){const e=this._entityId?this.hass.states[this._entityId]:void 0,t=this._entityId===l.N8?`${this.hass.localize("ui.components.media-browser.web-browser")}`:null!=e&&e.attributes.friendly_name?`${null==e?void 0:e.attributes.friendly_name}`:void 0;return i.dy`
      <ha-app-layout>
        <app-header fixed slot="header">
          <app-toolbar>
            <ha-menu-button
              .hass=${this.hass}
              .narrow=${this.narrow}
            ></ha-menu-button>
            <div main-title class="heading">
              <div>
                ${this.hass.localize("ui.components.media-browser.media-player-browser")}
              </div>
              <div class="secondary-text">${t||""}</div>
            </div>
            <mwc-button @click=${this._showSelectMediaPlayerDialog}>
              ${this.hass.localize("ui.components.media-browser.choose_player")}
            </mwc-button>
          </app-toolbar>
        </app-header>
        <div class="content">
          <ha-media-player-browse
            .hass=${this.hass}
            .entityId=${this._entityId}
            @media-picked=${this._mediaPicked}
          ></ha-media-player-browse>
        </div>
      </ha-app-layout>
    `}},{kind:"method",key:"_showSelectMediaPlayerDialog",value:function(){var e,t;e=this,t={mediaSources:this._mediaPlayerEntities,sourceSelectedCallback:e=>{this._entityId=e}},(0,d.B)(e,"show-dialog",{dialogTag:"hui-dialog-select-media-player",dialogImport:()=>Promise.all([r.e(3967),r.e(1662)]).then(r.bind(r,71662)),dialogParams:t})}},{kind:"method",key:"_mediaPicked",value:async function(e){const t=e.detail.item;if(this._entityId===l.N8){const e=await this.hass.callWS({type:"media_source/resolve_media",media_content_id:t.media_content_id});return i=this,a={sourceUrl:e.url,sourceType:e.mime_type,title:t.title},void(0,d.B)(i,"show-dialog",{dialogTag:"hui-dialog-web-browser-play-media",dialogImport:()=>Promise.all([r.e(3967),r.e(319),r.e(3132)]).then(r.bind(r,3212)),dialogParams:a})}var i,a;this.hass.callService("media_player","play_media",{entity_id:this._entityId,media_content_id:t.media_content_id,media_content_type:t.media_content_type})}},{kind:"get",key:"_mediaPlayerEntities",value:function(){return Object.values(this.hass.states).filter((e=>!("media_player"!==(0,o.N)(e)||!(0,n.e)(e,l.pu))))}},{kind:"get",static:!0,key:"styles",value:function(){return[c.Qx,i.iv`
        :host {
          --mdc-theme-primary: var(--app-header-text-color);
        }
        ha-media-player-browse {
          height: calc(100vh - var(--header-height));
        }
        :host([narrow]) app-toolbar mwc-button {
          width: 65px;
        }
        .heading {
          overflow: hidden;
          white-space: nowrap;
          margin-top: 4px;
        }
        .heading .secondary-text {
          font-size: 14px;
          overflow: hidden;
          text-overflow: ellipsis;
        }
      `]}}]}}),i.oi)}}]);
//# sourceMappingURL=chunk.2549edd3c79c620b1aca.js.map