import{_ as t,q as e,a as i,p as r,o as a,i as s,L as o,R as c,h as n,c as d,b as l,d as p,e as h,r as m,n as g,f as _,T as v,s as u,g as y,j as w,k as f,l as b,m as x,x as k}from"./c.85c06825.js";import{f as $,c as C,u as z}from"./index-98a3f8c8.js";class L extends o{constructor(){super(...arguments),this.value="",this.group=null,this.tabindex=-1,this.disabled=!1,this.twoline=!1,this.activated=!1,this.graphic=null,this.multipleGraphics=!1,this.hasMeta=!1,this.noninteractive=!1,this.selected=!1,this.shouldRenderRipple=!1,this._managingList=null,this.boundOnClick=this.onClick.bind(this),this._firstChanged=!0,this._skipPropRequest=!1,this.rippleHandlers=new c((()=>(this.shouldRenderRipple=!0,this.ripple))),this.listeners=[{target:this,eventNames:["click"],cb:()=>{this.onClick()}},{target:this,eventNames:["mouseenter"],cb:this.rippleHandlers.startHover},{target:this,eventNames:["mouseleave"],cb:this.rippleHandlers.endHover},{target:this,eventNames:["focus"],cb:this.rippleHandlers.startFocus},{target:this,eventNames:["blur"],cb:this.rippleHandlers.endFocus},{target:this,eventNames:["mousedown","touchstart"],cb:t=>{const e=t.type;this.onDown("mousedown"===e?"mouseup":"touchend",t)}}]}get text(){const t=this.textContent;return t?t.trim():""}render(){const t=this.renderText(),e=this.graphic?this.renderGraphic():n``,i=this.hasMeta?this.renderMeta():n``;return n`
      ${this.renderRipple()}
      ${e}
      ${t}
      ${i}`}renderRipple(){return this.shouldRenderRipple?n`
      <mwc-ripple
        .activated=${this.activated}>
      </mwc-ripple>`:this.activated?n`<div class="fake-activated-ripple"></div>`:""}renderGraphic(){const t={multi:this.multipleGraphics};return n`
      <span class="mdc-deprecated-list-item__graphic material-icons ${d(t)}">
        <slot name="graphic"></slot>
      </span>`}renderMeta(){return n`
      <span class="mdc-deprecated-list-item__meta material-icons">
        <slot name="meta"></slot>
      </span>`}renderText(){const t=this.twoline?this.renderTwoline():this.renderSingleLine();return n`
      <span class="mdc-deprecated-list-item__text">
        ${t}
      </span>`}renderSingleLine(){return n`<slot></slot>`}renderTwoline(){return n`
      <span class="mdc-deprecated-list-item__primary-text">
        <slot></slot>
      </span>
      <span class="mdc-deprecated-list-item__secondary-text">
        <slot name="secondary"></slot>
      </span>
    `}onClick(){this.fireRequestSelected(!this.selected,"interaction")}onDown(t,e){const i=()=>{window.removeEventListener(t,i),this.rippleHandlers.endPress()};window.addEventListener(t,i),this.rippleHandlers.startPress(e)}fireRequestSelected(t,e){if(this.noninteractive)return;const i=new CustomEvent("request-selected",{bubbles:!0,composed:!0,detail:{source:e,selected:t}});this.dispatchEvent(i)}connectedCallback(){super.connectedCallback(),this.noninteractive||this.setAttribute("mwc-list-item","");for(const t of this.listeners)for(const e of t.eventNames)t.target.addEventListener(e,t.cb,{passive:!0})}disconnectedCallback(){super.disconnectedCallback();for(const t of this.listeners)for(const e of t.eventNames)t.target.removeEventListener(e,t.cb);this._managingList&&(this._managingList.debouncedLayout?this._managingList.debouncedLayout(!0):this._managingList.layout(!0))}firstUpdated(){const t=new Event("list-item-rendered",{bubbles:!0,composed:!0});this.dispatchEvent(t)}}t([e("slot")],L.prototype,"slotElement",void 0),t([i("mwc-ripple")],L.prototype,"ripple",void 0),t([r({type:String})],L.prototype,"value",void 0),t([r({type:String,reflect:!0})],L.prototype,"group",void 0),t([r({type:Number,reflect:!0})],L.prototype,"tabindex",void 0),t([r({type:Boolean,reflect:!0}),a((function(t){t?this.setAttribute("aria-disabled","true"):this.setAttribute("aria-disabled","false")}))],L.prototype,"disabled",void 0),t([r({type:Boolean,reflect:!0})],L.prototype,"twoline",void 0),t([r({type:Boolean,reflect:!0})],L.prototype,"activated",void 0),t([r({type:String,reflect:!0})],L.prototype,"graphic",void 0),t([r({type:Boolean})],L.prototype,"multipleGraphics",void 0),t([r({type:Boolean})],L.prototype,"hasMeta",void 0),t([r({type:Boolean,reflect:!0}),a((function(t){t?(this.removeAttribute("aria-checked"),this.removeAttribute("mwc-list-item"),this.selected=!1,this.activated=!1,this.tabIndex=-1):this.setAttribute("mwc-list-item","")}))],L.prototype,"noninteractive",void 0),t([r({type:Boolean,reflect:!0}),a((function(t){const e=this.getAttribute("role"),i="gridcell"===e||"option"===e||"row"===e||"tab"===e;i&&t?this.setAttribute("aria-selected","true"):i&&this.setAttribute("aria-selected","false"),this._firstChanged?this._firstChanged=!1:this._skipPropRequest||this.fireRequestSelected(t,"property")}))],L.prototype,"selected",void 0),t([s()],L.prototype,"shouldRenderRipple",void 0),t([s()],L.prototype,"_managingList",void 0);const A=l`:host{cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent;height:48px;display:flex;position:relative;align-items:center;justify-content:flex-start;overflow:hidden;padding:0;padding-left:var(--mdc-list-side-padding, 16px);padding-right:var(--mdc-list-side-padding, 16px);outline:none;height:48px;color:rgba(0,0,0,.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host:focus{outline:none}:host([activated]){color:#6200ee;color:var(--mdc-theme-primary, #6200ee);--mdc-ripple-color: var( --mdc-theme-primary, #6200ee )}:host([activated]) .mdc-deprecated-list-item__graphic{color:#6200ee;color:var(--mdc-theme-primary, #6200ee)}:host([activated]) .fake-activated-ripple::before{position:absolute;display:block;top:0;bottom:0;left:0;right:0;width:100%;height:100%;pointer-events:none;z-index:1;content:"";opacity:0.12;opacity:var(--mdc-ripple-activated-opacity, 0.12);background-color:#6200ee;background-color:var(--mdc-ripple-color, var(--mdc-theme-primary, #6200ee))}.mdc-deprecated-list-item__graphic{flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;display:inline-flex}.mdc-deprecated-list-item__graphic ::slotted(*){flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;width:100%;height:100%;text-align:center}.mdc-deprecated-list-item__meta{width:var(--mdc-list-item-meta-size, 24px);height:var(--mdc-list-item-meta-size, 24px);margin-left:auto;margin-right:0;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-hint-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-item__meta.multi{width:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:var(--mdc-list-item-meta-size, 24px);line-height:var(--mdc-list-item-meta-size, 24px)}.mdc-deprecated-list-item__meta ::slotted(.material-icons),.mdc-deprecated-list-item__meta ::slotted(mwc-icon){line-height:var(--mdc-list-item-meta-size, 24px) !important}.mdc-deprecated-list-item__meta ::slotted(:not(.material-icons):not(mwc-icon)){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-caption-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.75rem;font-size:var(--mdc-typography-caption-font-size, 0.75rem);line-height:1.25rem;line-height:var(--mdc-typography-caption-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-caption-font-weight, 400);letter-spacing:0.0333333333em;letter-spacing:var(--mdc-typography-caption-letter-spacing, 0.0333333333em);text-decoration:inherit;text-decoration:var(--mdc-typography-caption-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-caption-text-transform, inherit)}[dir=rtl] .mdc-deprecated-list-item__meta,.mdc-deprecated-list-item__meta[dir=rtl]{margin-left:0;margin-right:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:100%;height:100%}.mdc-deprecated-list-item__text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden}.mdc-deprecated-list-item__text ::slotted([for]),.mdc-deprecated-list-item__text[for]{pointer-events:none}.mdc-deprecated-list-item__primary-text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;margin-bottom:-20px;display:block}.mdc-deprecated-list-item__primary-text::before{display:inline-block;width:0;height:32px;content:"";vertical-align:0}.mdc-deprecated-list-item__primary-text::after{display:inline-block;width:0;height:20px;content:"";vertical-align:-20px}.mdc-deprecated-list-item__secondary-text{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;display:block}.mdc-deprecated-list-item__secondary-text::before{display:inline-block;width:0;height:20px;content:"";vertical-align:0}.mdc-deprecated-list--dense .mdc-deprecated-list-item__secondary-text{font-size:inherit}* ::slotted(a),a{color:inherit;text-decoration:none}:host([twoline]){height:72px}:host([twoline]) .mdc-deprecated-list-item__text{align-self:flex-start}:host([disabled]),:host([noninteractive]){cursor:default;pointer-events:none}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*){opacity:.38}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__primary-text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__secondary-text ::slotted(*){color:#000;color:var(--mdc-theme-on-surface, #000)}.mdc-deprecated-list-item__secondary-text ::slotted(*){color:rgba(0, 0, 0, 0.54);color:var(--mdc-theme-text-secondary-on-background, rgba(0, 0, 0, 0.54))}.mdc-deprecated-list-item__graphic ::slotted(*){background-color:transparent;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-icon-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-group__subheader ::slotted(*){color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 40px);height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 40px);line-height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 40px) !important}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){border-radius:50%}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic,:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic,:host([graphic=control]) .mdc-deprecated-list-item__graphic{margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 16px)}[dir=rtl] :host([graphic=avatar]) .mdc-deprecated-list-item__graphic,:host([graphic=avatar]) .mdc-deprecated-list-item__graphic[dir=rtl],[dir=rtl] :host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=medium]) .mdc-deprecated-list-item__graphic[dir=rtl],[dir=rtl] :host([graphic=large]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic[dir=rtl],[dir=rtl] :host([graphic=control]) .mdc-deprecated-list-item__graphic,:host([graphic=control]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 16px);margin-right:0}:host([graphic=icon]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 24px);height:var(--mdc-list-item-graphic-size, 24px);margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 32px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 24px);line-height:var(--mdc-list-item-graphic-size, 24px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 24px) !important}[dir=rtl] :host([graphic=icon]) .mdc-deprecated-list-item__graphic,:host([graphic=icon]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 32px);margin-right:0}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:56px}:host([graphic=medium]:not([twoLine])),:host([graphic=large]:not([twoLine])){height:72px}:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 56px);height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic.multi,:host([graphic=large]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(*),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 56px);line-height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 56px) !important}:host([graphic=large]){padding-left:0px}`;let R=class extends L{};R.styles=A,R=t([p("mwc-list-item")],R);const P=k`
  <svg width="24" height="24" viewBox="0 0 24 24" slot="meta">
    <path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" />
  </svg>
`,M=k`
  <svg width="24" height="24" viewBox="0 0 24 24" slot="meta">
    <path d="M11,18H13V16H11V18M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,6A4,4 0 0,0 8,10H10A2,2 0 0,1 12,8A2,2 0 0,1 14,10C14,12 11,11.75 11,15H13C13,12.75 16,12.5 16,10A4,4 0 0,0 12,6Z" />
  </svg>
`;let S=class extends _{constructor(){super(...arguments),this._writeProgress=0,this._state="pick_option"}render(){let t,e,i=!1;return"pick_option"===this._state?(t="Pick Install Target",e=v`
        <mwc-list-item
          twoline
          hasMeta
          .port=${"OTA"}
          @click=${this._handleLegacyOption}
        >
          <span>Install wirelessly</span>
          <span slot="secondary">Requires the device to be online</span>
          ${P}
        </mwc-list-item>

        ${this._error?v`<div class="error">${this._error}</div>`:""}

        <mwc-list-item twoline hasMeta @click=${this._handleBrowserInstall}>
          <span>Install via the browser</span>
          <span slot="secondary">
            ${u?"For devices connected to this computer":y?"Your browser is not supported.":"Dashboard needs to opened via HTTPS"}
          </span>
          ${u?P:M}
        </mwc-list-item>

        <mwc-list-item twoline hasMeta @click=${this._showServerPorts}>
          <span>Install via the server</span>
          <span slot="secondary"
            >For devices connected to server running dashboard</span
          >
          ${P}
        </mwc-list-item>

        <mwc-list-item twoline hasMeta @click=${this._showCompileDialog}>
          <span>Download</span>
          <span slot="secondary"
            >Install it yourself using your preferred method</span
          >
          ${P}
        </mwc-list-item>

        <mwc-button
          no-attention
          slot="secondaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      `):"pick_server_port"===this._state?(t="Pick Server Port",e=v`
        ${this._ports.map((t=>v`
            <mwc-list-item
              twoline
              hasMeta
              .port=${t.port}
              @click=${this._handleLegacyOption}
            >
              <span>${t.desc}</span>
              <span slot="secondary">${t.port}</span>
              ${P}
            </mwc-list-item>
          `))}

        <mwc-button
          no-attention
          slot="secondaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      `):"connecting_webserial"===this._state?(e=this._renderProgress("Connecting"),i=!0):"prepare_installation"===this._state?(e=this._renderProgress("Preparing installation"),i=!0):"installing"===this._state?(e=this._renderProgress(v`
          Installing<br /><br />
          This will take
          ${"ESP8266"===this._configuration.esp_platform?"a minute":"2 minutes"}.<br />
          Keep this page visible to prevent slow down
        `,this._writeProgress>3?this._writeProgress:void 0),i=!0):"done"===this._state&&(e=this._error?this._renderMessage("👀",this._error,!0):this._renderMessage("🎉","Configuration installed!",!0)),v`
      <mwc-dialog
        open
        heading=${t}
        scrimClickAction
        @closed=${this._handleClose}
        .hideActions=${i}
      >
        ${e}
      </mwc-dialog>
    `}_renderProgress(t,e){return v`
      <div class="center">
        <div>
          <mwc-circular-progress
            active
            ?indeterminate=${void 0===e}
            .progress=${void 0!==e?e/100:void 0}
            density="8"
          ></mwc-circular-progress>
          ${void 0!==e?v`<div class="progress-pct">${e}%</div>`:""}
        </div>
        ${t}
      </div>
    `}_renderMessage(t,e,i){return v`
      <div class="center">
        <div class="icon">${t}</div>
        ${e}
      </div>
      ${i&&v`
        <mwc-button
          slot="primaryAction"
          dialogAction="ok"
          label="Close"
        ></mwc-button>
      `}
    `}firstUpdated(t){super.firstUpdated(t),$("./serial-ports").then((t=>t.filter((t=>"OTA"!==t.port)))).then((t=>{this._ports=t}))}updated(t){super.updated(t)}_showServerPorts(){this.style.setProperty("--mdc-dialog-min-width",`${this.shadowRoot.querySelector("mwc-list-item").clientWidth+4}px`),this._state="pick_server_port"}_showCompileDialog(){var t;t=this.filename,C.open({target:{dataset:{filename:t}}}),this._close()}_handleLegacyOption(t){var e;(t=>{const e=document.querySelector(".nav-wrapper select"),i=window.M.FormSelect.getInstance(e);i&&i.destroy(),e.value=t,window.M.FormSelect.init(e,{})})(t.target.port),this._close(),e=this.filename,z.open({target:{dataset:{filename:e}}})}async _handleBrowserInstall(){if(!u||!y)return void window.open("https://esphome.io/guides/getting_started_hassio.html#webserial","_blank");this._error=void 0;const t=w(this.filename);let e;try{e=await f(console)}catch(t){return}try{try{this._configuration=await t}catch(t){return this._state="done",void(this._error="Error fetching configuration information")}const i=b(this.filename);this._state="connecting_webserial";try{await e.initialize()}catch(t){return console.error(t),this._state="pick_option",this._error="Failed to initialize.",void(e.connected&&(this._error+=" Try resetting your device or holding the BOOT button while selecting your serial port until it starts preparing the installation."))}this._state="prepare_installation";try{await i}catch(t){return this._error=v`
          Failed to prepare configuration<br /><br />
          <button class="link" @click=${this._showCompileDialog}>
            See what went wrong.
          </button>
        `,void(this._state="done")}this._state="installing";try{await x(e,this.filename,!1,(t=>{this._writeProgress=t}))}catch(t){return this._error="Installation failed",void(this._state="done")}await e.hardReset(),this._state="done"}finally{(null==e?void 0:e.connected)&&(console.log("Disconnecting esp"),await e.disconnect())}}_close(){this.shadowRoot.querySelector("mwc-dialog").close()}async _handleClose(){this.parentNode.removeChild(this)}};S.styles=h`
    :host {
      --mdc-dialog-max-width: 390px;
      --mdc-theme-primary: #03a9f4;
    }
    a {
      color: var(--mdc-theme-primary);
    }
    mwc-button[no-attention] {
      --mdc-theme-primary: #444;
      --mdc-theme-on-primary: white;
    }
    mwc-list-item {
      margin: 0 -20px;
    }
    svg {
      fill: currentColor;
    }
    .center {
      text-align: center;
    }
    mwc-circular-progress {
      margin-bottom: 16px;
    }
    .progress-pct {
      position: absolute;
      top: 50px;
      left: 0;
      right: 0;
    }
    .icon {
      font-size: 50px;
      line-height: 80px;
      color: black;
    }
    button.link {
      background: none;
      color: var(--mdc-theme-primary);
      border: none;
      padding: 0;
      font: inherit;
      text-align: left;
      text-decoration: underline;
      cursor: pointer;
    }
    .show-ports {
      margin-top: 16px;
    }
    .error {
      padding: 8px 24px;
      background-color: #fff59d;
      margin: 0 -24px;
    }
  `,t([m()],S.prototype,"filename",void 0),t([m()],S.prototype,"_ports",void 0),t([m()],S.prototype,"_writeProgress",void 0),t([m()],S.prototype,"_configuration",void 0),t([m()],S.prototype,"_state",void 0),t([m()],S.prototype,"_error",void 0),S=t([g("esphome-install-dialog")],S);
