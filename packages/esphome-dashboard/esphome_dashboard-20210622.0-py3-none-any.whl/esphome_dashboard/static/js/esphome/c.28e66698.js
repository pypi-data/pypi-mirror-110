import{i as t,_ as o,v as e,r as s,n as i,h as a,T as c}from"./c.3b87a103.js";import{g as r}from"./c.5dd5b8c9.js";import"./c.07ac4ee6.js";import{m as n}from"./c.880add99.js";const l=(t,o)=>{import("./c.fea0d4bc.js");const e=document.createElement("esphome-logs-dialog");e.configuration=t,e.target=o,document.body.append(e)};let p=class extends a{render(){return this._ports?c`
      <mwc-dialog
        open
        heading=${"Show Logs"}
        scrimClickAction
        @closed=${this._handleClose}
      >
        <mwc-list-item
          twoline
          hasMeta
          dialogAction="close"
          .port=${"OTA"}
          @click=${this._pickPort}
        >
          <span>Connect wirelessly</span>
          <span slot="secondary">Requires the device to be online</span>
          ${n}
        </mwc-list-item>

        ${this._ports.map((t=>c`
            <mwc-list-item
              twoline
              hasMeta
              dialogAction="close"
              .port=${t.port}
              @click=${this._pickPort}
            >
              <span>${t.desc}</span>
              <span slot="secondary">${t.port}</span>
              ${n}
            </mwc-list-item>
          `))}

        <mwc-button
          no-attention
          slot="secondaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      </mwc-dialog>
    `:c``}firstUpdated(t){super.firstUpdated(t),r().then((t=>{this._ports=t}))}_pickPort(t){l(this.configuration,t.currentTarget.port)}_handleClose(){this.parentNode.removeChild(this)}};p.styles=t`
    :host {
      --mdc-theme-primary: #03a9f4;
    }

    mwc-list-item {
      margin: 0 -20px;
    }
  `,o([e()],p.prototype,"configuration",void 0),o([s()],p.prototype,"_ports",void 0),p=o([i("esphome-logs-target-dialog")],p);var d=Object.freeze({__proto__:null});export{d as l,l as o};
