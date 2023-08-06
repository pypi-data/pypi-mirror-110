import{_ as e,H as t,e as i,m as o,T as s,n as r}from"./main-b9893c22.js";import{m as d}from"./c.852db58c.js";import"./c.4fc2ddbf.js";import"./c.a55930e9.js";import"./c.66753414.js";import"./c.50e12a96.js";let a=e([r("hacs-generic-dialog")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({type:Boolean})],key:"markdown",value:()=>!1},{kind:"field",decorators:[i()],key:"repository",value:void 0},{kind:"field",decorators:[i()],key:"header",value:void 0},{kind:"field",decorators:[i()],key:"content",value:void 0},{kind:"field",key:"_getRepository",value:()=>o((e,t)=>null==e?void 0:e.find(e=>e.id===t))},{kind:"method",key:"render",value:function(){if(!this.active)return s``;const e=this._getRepository(this.repositories,this.repository);return s`
      <hacs-dialog .active=${this.active} .narrow=${this.narrow} .hass=${this.hass}>
        <div slot="header">${this.header||""}</div>
        ${this.markdown?this.repository?d.html(this.content||"",e):d.html(this.content||""):this.content||""}
      </hacs-dialog>
    `}}]}}),t);export{a as HacsGenericDialog};
