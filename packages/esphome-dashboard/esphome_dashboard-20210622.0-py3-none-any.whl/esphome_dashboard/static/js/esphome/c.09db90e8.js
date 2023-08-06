import{_ as o,v as i,r as t,n as e,h as s,T as a}from"./c.3b87a103.js";import"./c.07ac4ee6.js";import{o as n,b as l}from"./index-7c27abab.js";let c=class extends s{render(){const o=void 0===this._valid?"":this._valid?"✅":"❌";return a`
      <esphome-process-dialog
        .heading=${`Validate ${this.configuration} ${o}`}
        .type=${"validate"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Install"
          @click=${this._openInstall}
        ></mwc-button>
      </esphome-process-dialog>
    `}_openEdit(){n(this.configuration)}_openInstall(){l(this.configuration)}_handleProcessDone(o){this._valid=0==o.detail}_handleClose(){this.parentNode.removeChild(this)}};o([i()],c.prototype,"configuration",void 0),o([t()],c.prototype,"_valid",void 0),c=o([e("esphome-validate-dialog")],c);
