import{_ as e,k as s,e as a,o as i,T as t,a9 as o,b as n,q as r,i as l,n as c,H as d,m as h,E as p,F as m,aa as u,ab as v,V as g,W as y,X as _,d as f}from"./main-ef294d92.js";import{m as x}from"./c.8022cc27.js";import{u as k}from"./c.c68ff96b.js";import"./c.df97a59e.js";import"./c.773db748.js";import{s as b}from"./c.3f64a2cf.js";import"./c.94568445.js";import"./c.c05acf21.js";const $=()=>new Promise(e=>{var s;s=e,requestAnimationFrame(()=>setTimeout(s,0))});e([c("ha-expansion-panel")],(function(e,s){return{F:class extends s{constructor(...s){super(...s),e(this)}},d:[{kind:"field",decorators:[a({type:Boolean,reflect:!0})],key:"expanded",value:()=>!1},{kind:"field",decorators:[a({type:Boolean,reflect:!0})],key:"outlined",value:()=>!1},{kind:"field",decorators:[a()],key:"header",value:void 0},{kind:"field",decorators:[a()],key:"secondary",value:void 0},{kind:"field",decorators:[i(".container")],key:"_container",value:void 0},{kind:"method",key:"render",value:function(){return t`
      <div class="summary" @click=${this._toggleContainer}>
        <slot class="header" name="header">
          ${this.header}
          <slot class="secondary" name="secondary">${this.secondary}</slot>
        </slot>
        <ha-svg-icon
          .path=${o}
          class="summary-icon ${n({expanded:this.expanded})}"
        ></ha-svg-icon>
      </div>
      <div
        class="container ${n({expanded:this.expanded})}"
        @transitionend=${this._handleTransitionEnd}
      >
        <slot></slot>
      </div>
    `}},{kind:"method",key:"_handleTransitionEnd",value:function(){this._container.style.removeProperty("height")}},{kind:"method",key:"_toggleContainer",value:async function(){const e=!this.expanded;r(this,"expanded-will-change",{expanded:e}),e&&await $();const s=this._container.scrollHeight;this._container.style.height=s+"px",e||setTimeout(()=>{this._container.style.height="0px"},0),this.expanded=e,r(this,"expanded-changed",{expanded:this.expanded})}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        display: block;
      }

      :host([outlined]) {
        box-shadow: none;
        border-width: 1px;
        border-style: solid;
        border-color: var(
          --ha-card-border-color,
          var(--divider-color, #e0e0e0)
        );
        border-radius: var(--ha-card-border-radius, 4px);
        padding: 0 8px;
      }

      .summary {
        display: flex;
        padding: var(--expansion-panel-summary-padding, 0);
        min-height: 48px;
        align-items: center;
        cursor: pointer;
        overflow: hidden;
        font-weight: 500;
      }

      .summary-icon {
        transition: transform 150ms cubic-bezier(0.4, 0, 0.2, 1);
        margin-left: auto;
      }

      .summary-icon.expanded {
        transform: rotate(180deg);
      }

      .container {
        overflow: hidden;
        transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1);
        height: 0px;
      }

      .container.expanded {
        height: auto;
      }

      .header {
        display: block;
      }

      .secondary {
        display: block;
        color: var(--secondary-text-color);
        font-size: 12px;
      }
    `}}]}}),s);let w=e([c("hacs-update-dialog")],(function(e,s){class i extends s{constructor(...s){super(...s),e(this)}}return{F:i,d:[{kind:"field",decorators:[a()],key:"repository",value:void 0},{kind:"field",decorators:[a({type:Boolean})],key:"_updating",value:()=>!1},{kind:"field",decorators:[a()],key:"_error",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"_releaseNotes",value:()=>[]},{kind:"field",key:"_getRepository",value:()=>h((e,s)=>e.find(e=>e.id===s))},{kind:"method",key:"firstUpdated",value:async function(e){p(m(i.prototype),"firstUpdated",this).call(this,e);const s=this._getRepository(this.repositories,this.repository);s&&("commit"!==s.version_or_commit&&(this._releaseNotes=await u(this.hass,s.id),this._releaseNotes=this._releaseNotes.filter(e=>e.tag>s.installed_version)),this.hass.connection.subscribeEvents(e=>this._error=e.data,"hacs/error"))}},{kind:"method",key:"render",value:function(){if(!this.active)return t``;const e=this._getRepository(this.repositories,this.repository);return e?t`
      <hacs-dialog
        .active=${this.active}
        .title=${this.hacs.localize("dialog_update.title")}
        .hass=${this.hass}
      >
        <div class=${n({content:!0,narrow:this.narrow})}>
          <p class="message">
            ${this.hacs.localize("dialog_update.message",{name:e.name})}
          </p>
          <div class="version-container">
            <div class="version-element">
              <span class="version-number">${e.installed_version}</span>
              <small class="version-text">${this.hacs.localize("dialog_update.installed_version")}</small>
            </div>

            <span class="version-separator">
              <ha-svg-icon
                .path=${v}
              ></ha-svg-icon>
            </span>

            <div class="version-element">
                <span class="version-number">${e.available_version}</span>
                <small class="version-text">${this.hacs.localize("dialog_update.available_version")}</small>
              </div>
            </div>
          </div>

          ${this._releaseNotes.length>0?this._releaseNotes.map(s=>t`
                    <ha-expansion-panel
                      .header=${s.name&&s.name!==s.tag?`${s.tag}: ${s.name}`:s.tag}
                      outlined
                      ?expanded=${1===this._releaseNotes.length}
                    >
                      ${s.body?x.html(s.body,e):this.hacs.localize("dialog_update.no_info")}
                    </ha-expansion-panel>
                  `):""}
          ${e.can_install?"":t`<p class="error">
                  ${this.hacs.localize("confirm.home_assistant_version_not_correct").replace("{haversion}",this.hass.config.version).replace("{minversion}",e.homeassistant)}
                </p>`}
          ${"integration"===e.category?t`<p>${this.hacs.localize("dialog_install.restart")}</p>`:""}
          ${this._error?t`<div class="error">${this._error.message}</div>`:""}
        </div>
        <mwc-button
          slot="primaryaction"
          ?disabled=${!e.can_install}
          @click=${this._updateRepository}
          >${this._updating?t`<ha-circular-progress active size="small"></ha-circular-progress>`:this.hacs.localize("common.update")}</mwc-button
        >
        <div class="secondary" slot="secondaryaction">
          <hacs-link .url=${this._getChanglogURL()}
            ><mwc-button>${this.hacs.localize("dialog_update.changelog")}</mwc-button></hacs-link
          >
          <hacs-link .url="https://github.com/${e.full_name}"
            ><mwc-button>${this.hacs.localize("common.repository")}</mwc-button></hacs-link
          >
        </div>
      </hacs-dialog>
    `:t``}},{kind:"method",key:"_updateRepository",value:async function(){this._updating=!0;const e=this._getRepository(this.repositories,this.repository);e&&("commit"!==e.version_or_commit?await g(this.hass,e.id,e.available_version):await y(this.hass,e.id),"plugin"===e.category&&"storage"===this.hacs.status.lovelace_mode&&await k(this.hass,e,e.available_version),this._updating=!1,this.dispatchEvent(new Event("hacs-dialog-closed",{bubbles:!0,composed:!0})),"plugin"===e.category&&b(this,{title:this.hacs.localize("common.reload"),text:t`${this.hacs.localize("dialog.reload.description")}</br>${this.hacs.localize("dialog.reload.confirm")}`,dismissText:this.hacs.localize("common.cancel"),confirmText:this.hacs.localize("common.reload"),confirm:()=>{_.location.href=_.location.href}}))}},{kind:"method",key:"_getChanglogURL",value:function(){const e=this._getRepository(this.repositories,this.repository);if(e)return"commit"===e.version_or_commit?`https://github.com/${e.full_name}/compare/${e.installed_version}...${e.available_version}`:`https://github.com/${e.full_name}/releases`}},{kind:"get",static:!0,key:"styles",value:function(){return[f,l`
        .content {
          width: 360px;
          display: contents;
        }
        .error {
          color: var(--hacs-error-color, var(--google-red-500));
        }
        ha-expansion-panel {
          margin: 8px 0;
        }
        ha-expansion-panel[expanded] {
          padding-bottom: 16px;
        }

        .secondary {
          display: flex;
        }
        .message {
          text-align: center;
          margin: 0;
        }
        .version-container {
          margin: 24px 0 12px 0;
          width: 360px;
          min-width: 100%;
          max-width: 100%;
          display: flex;
          flex-direction: row;
        }
        .version-element {
          display: flex;
          flex-direction: column;
          flex: 1;
          padding: 0 12px;
          text-align: center;
        }
        .version-text {
          color: var(--secondary-text-color);
        }
        .version-number {
          font-size: 1.5rem;
          margin-bottom: 4px;
        }
      `]}}]}}),d);export{w as HacsUpdateDialog};
