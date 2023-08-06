import{i as t,_ as o,v as e,r as s,n as i,h as r,T as n}from"./c.3b87a103.js";import"./c.1d39cb1f.js";import{o as a}from"./index-7db316db.js";import{o as l}from"./c.6a89748f.js";import"./c.2472ed8e.js";import"./c.14b31b51.js";import"./c.4d1ff8c6.js";let c=class extends r{render(){return n`
      <esphome-process-dialog
        .heading=${`Install ${this.configuration}`}
        .type=${"upload"}
        .spawnParams=${{configuration:this.configuration,port:this.target}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${"OTA"===this.target?"":n`
              <a
                href="https://esphome.io/guides/faq.html#i-can-t-get-flashing-over-usb-to-work"
                slot="secondaryAction"
                target="_blank"
                >❓</a
              >
            `}
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        ${void 0===this._result||0===this._result?"":n`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_openEdit(){a(this.configuration)}_handleProcessDone(t){this._result=t.detail}_handleRetry(){l(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};c.styles=t`
    a[slot="secondaryAction"] {
      text-decoration: none;
      line-height: 32px;
    }
  `,o([e()],c.prototype,"configuration",void 0),o([e()],c.prototype,"target",void 0),o([s()],c.prototype,"_result",void 0),c=o([i("esphome-install-server-dialog")],c);
