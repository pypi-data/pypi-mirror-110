import{_ as e,v as o,n as s,h as i,T as a}from"./c.3b87a103.js";import"./c.07ac4ee6.js";import"./index-7c27abab.js";let t=class extends i{render(){return a`
      <esphome-process-dialog
        .heading=${`Clean MQTT discovery topics for ${this.configuration}`}
        .type=${"clean-mqtt"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
      >
      </esphome-process-dialog>
    `}_handleClose(){this.parentNode.removeChild(this)}};e([o()],t.prototype,"configuration",void 0),t=e([s("esphome-clean-mqtt-dialog")],t);
