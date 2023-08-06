import{g as r,A as e,_ as t,p as i,L as c,c as s,d as a,s as o,e as n,f as d}from"./c.3b87a103.js";import{f as l,s as p}from"./index-7c27abab.js";import{c as m}from"./c.880add99.js";function g(r,e,t){if(void 0!==e)return function(r,e,t){const i=r.constructor;if(!t){const r=`__${e}`;if(!(t=i.getPropertyDescriptor(e,r)))throw new Error("@ariaProperty must be used after a @property decorator")}const c=t;let s="";if(!c.set)throw new Error(`@ariaProperty requires a setter for ${e}`);const a={configurable:!0,enumerable:!0,set(r){if(""===s){const r=i.getPropertyOptions(e);s=r.attribute}this.hasAttribute(s)&&this.removeAttribute(s),c.set.call(this,r)}};return c.get&&(a.get=function(){return c.get.call(this)}),a}(r,e,t);throw new Error("@ariaProperty only supports TypeScript Decorators")}const u=new WeakMap,f=r((r=>t=>{const i=u.get(t);if(void 0===r&&t instanceof e){if(void 0!==i||!u.has(t)){const r=t.committer.name;t.committer.element.removeAttribute(r)}}else r!==i&&t.setValue(r);u.set(t,r)}));class h extends c{constructor(){super(...arguments),this.indeterminate=!1,this.progress=0,this.density=0,this.closed=!1}open(){this.closed=!1}close(){this.closed=!0}render(){const r={"mdc-circular-progress--closed":this.closed,"mdc-circular-progress--indeterminate":this.indeterminate},e=48+4*this.density,t={width:`${e}px`,height:`${e}px`};return s`
      <div
        class="mdc-circular-progress ${a(r)}"
        style="${o(t)}"
        role="progressbar"
        aria-label="${f(this.ariaLabel)}"
        aria-valuemin="0"
        aria-valuemax="1"
        aria-valuenow="${f(this.indeterminate?void 0:this.progress)}">
        ${this.renderDeterminateContainer()}
        ${this.renderIndeterminateContainer()}
      </div>`}renderDeterminateContainer(){const r=48+4*this.density,e=r/2,t=this.density>=-3?18+11*this.density/6:12.5+5*(this.density+3)/4,i=6.2831852*t,c=(1-this.progress)*i,a=this.density>=-3?4+this.density*(1/3):3+(this.density+3)*(1/6);return s`
      <div class="mdc-circular-progress__determinate-container">
        <svg class="mdc-circular-progress__determinate-circle-graphic"
             viewBox="0 0 ${r} ${r}">
          <circle class="mdc-circular-progress__determinate-track"
                  cx="${e}" cy="${e}" r="${t}"
                  stroke-width="${a}"></circle>
          <circle class="mdc-circular-progress__determinate-circle"
                  cx="${e}" cy="${e}" r="${t}"
                  stroke-dasharray="${6.2831852*t}"
                  stroke-dashoffset="${c}"
                  stroke-width="${a}"></circle>
        </svg>
      </div>`}renderIndeterminateContainer(){return s`
      <div class="mdc-circular-progress__indeterminate-container">
        <div class="mdc-circular-progress__spinner-layer">
          ${this.renderIndeterminateSpinnerLayer()}
        </div>
      </div>`}renderIndeterminateSpinnerLayer(){const r=48+4*this.density,e=r/2,t=this.density>=-3?18+11*this.density/6:12.5+5*(this.density+3)/4,i=6.2831852*t,c=.5*i,a=this.density>=-3?4+this.density*(1/3):3+(this.density+3)*(1/6);return s`
        <div class="mdc-circular-progress__circle-clipper mdc-circular-progress__circle-left">
          <svg class="mdc-circular-progress__indeterminate-circle-graphic"
               viewBox="0 0 ${r} ${r}">
            <circle cx="${e}" cy="${e}" r="${t}"
                    stroke-dasharray="${i}"
                    stroke-dashoffset="${c}"
                    stroke-width="${a}"></circle>
          </svg>
        </div>
        <div class="mdc-circular-progress__gap-patch">
          <svg class="mdc-circular-progress__indeterminate-circle-graphic"
               viewBox="0 0 ${r} ${r}">
            <circle cx="${e}" cy="${e}" r="${t}"
                    stroke-dasharray="${i}"
                    stroke-dashoffset="${c}"
                    stroke-width="${.8*a}"></circle>
          </svg>
        </div>
        <div class="mdc-circular-progress__circle-clipper mdc-circular-progress__circle-right">
          <svg class="mdc-circular-progress__indeterminate-circle-graphic"
               viewBox="0 0 ${r} ${r}">
            <circle cx="${e}" cy="${e}" r="${t}"
                    stroke-dasharray="${i}"
                    stroke-dashoffset="${c}"
                    stroke-width="${a}"></circle>
          </svg>
        </div>`}update(r){super.update(r),r.has("progress")&&(this.progress>1&&(this.progress=1),this.progress<0&&(this.progress=0))}}t([i({type:Boolean,reflect:!0})],h.prototype,"indeterminate",void 0),t([i({type:Number,reflect:!0})],h.prototype,"progress",void 0),t([i({type:Number,reflect:!0})],h.prototype,"density",void 0),t([i({type:Boolean,reflect:!0})],h.prototype,"closed",void 0),t([g,i({type:String,attribute:"aria-label"})],h.prototype,"ariaLabel",void 0);const y=n`.mdc-circular-progress__determinate-circle,.mdc-circular-progress__indeterminate-circle-graphic{stroke:#6200ee;stroke:var(--mdc-theme-primary, #6200ee)}.mdc-circular-progress__determinate-track{stroke:transparent}@keyframes mdc-circular-progress-container-rotate{to{transform:rotate(360deg)}}@keyframes mdc-circular-progress-spinner-layer-rotate{12.5%{transform:rotate(135deg)}25%{transform:rotate(270deg)}37.5%{transform:rotate(405deg)}50%{transform:rotate(540deg)}62.5%{transform:rotate(675deg)}75%{transform:rotate(810deg)}87.5%{transform:rotate(945deg)}100%{transform:rotate(1080deg)}}@keyframes mdc-circular-progress-color-1-fade-in-out{from{opacity:.99}25%{opacity:.99}26%{opacity:0}89%{opacity:0}90%{opacity:.99}to{opacity:.99}}@keyframes mdc-circular-progress-color-2-fade-in-out{from{opacity:0}15%{opacity:0}25%{opacity:.99}50%{opacity:.99}51%{opacity:0}to{opacity:0}}@keyframes mdc-circular-progress-color-3-fade-in-out{from{opacity:0}40%{opacity:0}50%{opacity:.99}75%{opacity:.99}76%{opacity:0}to{opacity:0}}@keyframes mdc-circular-progress-color-4-fade-in-out{from{opacity:0}65%{opacity:0}75%{opacity:.99}90%{opacity:.99}to{opacity:0}}@keyframes mdc-circular-progress-left-spin{from{transform:rotate(265deg)}50%{transform:rotate(130deg)}to{transform:rotate(265deg)}}@keyframes mdc-circular-progress-right-spin{from{transform:rotate(-265deg)}50%{transform:rotate(-130deg)}to{transform:rotate(-265deg)}}.mdc-circular-progress{display:inline-flex;position:relative;direction:ltr;transition:opacity 250ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-circular-progress__determinate-container,.mdc-circular-progress__indeterminate-circle-graphic,.mdc-circular-progress__indeterminate-container,.mdc-circular-progress__spinner-layer{position:absolute;width:100%;height:100%}.mdc-circular-progress__determinate-container{transform:rotate(-90deg)}.mdc-circular-progress__indeterminate-container{font-size:0;letter-spacing:0;white-space:nowrap;opacity:0}.mdc-circular-progress__determinate-circle-graphic,.mdc-circular-progress__indeterminate-circle-graphic{fill:transparent}.mdc-circular-progress__determinate-circle{transition:stroke-dashoffset 500ms 0ms cubic-bezier(0, 0, 0.2, 1)}.mdc-circular-progress__gap-patch{position:absolute;top:0;left:47.5%;box-sizing:border-box;width:5%;height:100%;overflow:hidden}.mdc-circular-progress__gap-patch .mdc-circular-progress__indeterminate-circle-graphic{left:-900%;width:2000%;transform:rotate(180deg)}.mdc-circular-progress__circle-clipper{display:inline-flex;position:relative;width:50%;height:100%;overflow:hidden}.mdc-circular-progress__circle-clipper .mdc-circular-progress__indeterminate-circle-graphic{width:200%}.mdc-circular-progress__circle-right .mdc-circular-progress__indeterminate-circle-graphic{left:-100%}.mdc-circular-progress--indeterminate .mdc-circular-progress__determinate-container{opacity:0}.mdc-circular-progress--indeterminate .mdc-circular-progress__indeterminate-container{opacity:1}.mdc-circular-progress--indeterminate .mdc-circular-progress__indeterminate-container{animation:mdc-circular-progress-container-rotate 1568.2352941176ms linear infinite}.mdc-circular-progress--indeterminate .mdc-circular-progress__spinner-layer{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-1{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-1-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-2{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-2-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-3{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-3-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-4{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-4-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__circle-left .mdc-circular-progress__indeterminate-circle-graphic{animation:mdc-circular-progress-left-spin 1333ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__circle-right .mdc-circular-progress__indeterminate-circle-graphic{animation:mdc-circular-progress-right-spin 1333ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--closed{opacity:0}:host{display:inline-flex}.mdc-circular-progress__determinate-track{stroke:transparent;stroke:var(--mdc-circular-progress-track-color, transparent)}`;let _=class extends h{};_.styles=y,_=t([d("mwc-circular-progress")],_);const b=r=>l("./wizard.html",{method:"post",body:new URLSearchParams(r)}),$=r=>l(`./info?configuration=${r}`),v=r=>l(`./delete?configuration=${r}`,{method:"post"}),w=r=>p("compile",{configuration:r}),k=async(r,e,t,i)=>{const c=await $(e);if(m[r.chipFamily]!==c.esp_platform)throw new Error(`Configuration does not match the platform of the connected device. Expected a ${c.esp_platform} device.`);let s;s="ESP32"===c.esp_platform?[{path:"./static/firmware/bootloader.bin",offset:4096},{path:"./static/firmware/partitions.bin",offset:32768},{path:"./static/firmware/ota.bin",offset:57344},{path:`./download.bin?configuration=${e}`,offset:65536}]:[{path:`./download.bin?configuration=${e}`,offset:0}];const a=s.map((async r=>{const e=new URL(r.path,location.href).toString(),t=await fetch(e);if(!t.ok)throw new Error(`Downlading firmware ${r.path} failed: ${t.status}`);return t.arrayBuffer()})),o=[];let n=0;for(const r of a){const e=await r;o.push(e),n+=e.byteLength}const d=await r.runStub();t&&await d.eraseFlash();let l=0,p=0;i(0);for(const r of s){const e=o.shift();await d.flashData(e,(r=>{const e=Math.floor((p+r)/n*100);e!==l&&(l=e,i(e))}),r.offset,!0),p+=e.byteLength}i(100)};export{g as a,b,w as c,v as d,k as f,$ as g,f as i};
