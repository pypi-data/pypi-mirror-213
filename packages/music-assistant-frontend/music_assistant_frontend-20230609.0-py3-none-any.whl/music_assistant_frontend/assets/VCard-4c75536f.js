import{a as P,G as le,H as se,i as T,E as Q,c as ie,M as Fe,d as re,n as ue,w as ce,F as de,g as oe,N as He,V as te,x as ve,m as Ae,b as Ce,K as _e,R as we,O as Ve,u as Pe,f as Be,y as F,J as Ge,p as We,s as Ke,I as Ue,r as qe,v as Je,L as Qe}from"./VBtn-ba18d485.js";import{g as B,av as Xe,b3 as Ye,aw as Le,p as L,k as Ze,T as et,a8 as X,s as _,ab as Y,b1 as x,r as V,f as pe,c as S,b as Me,aa as tt,a9 as at,j as u,b4 as Oe,w as U,h as nt,n as lt,Q as q,a2 as me,F as ae,a as st,ak as it,ag as O,m as ge,d as fe,aK as Ie,i as rt}from"./index-11e01e27.js";function G(e){let i=arguments.length>1&&arguments[1]!==void 0?arguments[1]:"div",n=arguments.length>2?arguments[2]:void 0;return B()({name:n??Xe(Ye(e.replace(/__/g,"-"))),props:{tag:{type:String,default:i},...P()},setup(t,l){let{slots:a}=l;return()=>{var s;return Le(t.tag,{class:[e,t.class],style:t.style},(s=a.default)==null?void 0:s.call(a))}}})}const ut=L({transition:{type:[Boolean,String,Object],default:"fade-transition",validator:e=>e!==!0}},"transition"),K=(e,i)=>{let{slots:n}=i;const{transition:t,disabled:l,...a}=e,{component:s=et,...c}=typeof t=="object"?t:{};return Le(s,Ze(typeof t=="string"?{name:l?"":t}:c,a,{disabled:l}),n)},ne=Symbol.for("vuetify:list");function xt(){const e=X(ne,{hasPrepend:_(!1),updateHasPrepend:()=>null}),i={hasPrepend:_(!1),updateHasPrepend:n=>{n&&(i.hasPrepend.value=n)}};return Y(ne,i),e}function ct(){return X(ne,null)}const dt={open:e=>{let{id:i,value:n,opened:t,parents:l}=e;if(n){const a=new Set;a.add(i);let s=l.get(i);for(;s!=null;)a.add(s),s=l.get(s);return a}else return t.delete(i),t},select:()=>null},Te={open:e=>{let{id:i,value:n,opened:t,parents:l}=e;if(n){let a=l.get(i);for(t.add(i);a!=null&&a!==i;)t.add(a),a=l.get(a);return t}else t.delete(i);return t},select:()=>null},ot={open:Te.open,select:e=>{let{id:i,value:n,opened:t,parents:l}=e;if(!n)return t;const a=[];let s=l.get(i);for(;s!=null;)a.push(s),s=l.get(s);return new Set(a)}},ye=e=>{const i={select:n=>{let{id:t,value:l,selected:a}=n;if(t=x(t),e&&!l){const s=Array.from(a.entries()).reduce((c,y)=>{let[o,v]=y;return v==="on"?[...c,o]:c},[]);if(s.length===1&&s[0]===t)return a}return a.set(t,l?"on":"off"),a},in:(n,t,l)=>{let a=new Map;for(const s of n||[])a=i.select({id:s,value:!0,selected:new Map(a),children:t,parents:l});return a},out:n=>{const t=[];for(const[l,a]of n.entries())a==="on"&&t.push(l);return t}};return i},ze=e=>{const i=ye(e);return{select:t=>{let{selected:l,id:a,...s}=t;a=x(a);const c=l.has(a)?new Map([[a,l.get(a)]]):new Map;return i.select({...s,id:a,selected:c})},in:(t,l,a)=>{let s=new Map;return t!=null&&t.length&&(s=i.in(t.slice(0,1),l,a)),s},out:(t,l,a)=>i.out(t,l,a)}},vt=e=>{const i=ye(e);return{select:t=>{let{id:l,selected:a,children:s,...c}=t;return l=x(l),s.has(l)?a:i.select({id:l,selected:a,children:s,...c})},in:i.in,out:i.out}},mt=e=>{const i=ze(e);return{select:t=>{let{id:l,selected:a,children:s,...c}=t;return l=x(l),s.has(l)?a:i.select({id:l,selected:a,children:s,...c})},in:i.in,out:i.out}},gt=e=>{const i={select:n=>{let{id:t,value:l,selected:a,children:s,parents:c}=n;t=x(t);const y=new Map(a),o=[t];for(;o.length;){const r=o.shift();a.set(r,l?"on":"off"),s.has(r)&&o.push(...s.get(r))}let v=c.get(t);for(;v;){const r=s.get(v),d=r.every(m=>a.get(m)==="on"),g=r.every(m=>!a.has(m)||a.get(m)==="off");a.set(v,d?"on":g?"off":"indeterminate"),v=c.get(v)}return e&&!l&&Array.from(a.entries()).reduce((d,g)=>{let[m,k]=g;return k==="on"?[...d,m]:d},[]).length===0?y:a},in:(n,t,l)=>{let a=new Map;for(const s of n||[])a=i.select({id:s,value:!0,selected:new Map(a),children:t,parents:l});return a},out:(n,t)=>{const l=[];for(const[a,s]of n.entries())s==="on"&&!t.has(a)&&l.push(a);return l}};return i},H=Symbol.for("vuetify:nested"),Re={id:_(),root:{register:()=>null,unregister:()=>null,parents:V(new Map),children:V(new Map),open:()=>null,openOnSelect:()=>null,select:()=>null,opened:V(new Set),selected:V(new Map),selectedValues:V([])}},Nt=L({selectStrategy:[String,Function],openStrategy:[String,Object],opened:Array,selected:Array,mandatory:Boolean},"nested"),jt=e=>{let i=!1;const n=V(new Map),t=V(new Map),l=pe(e,"opened",e.opened,r=>new Set(r),r=>[...r.values()]),a=S(()=>{if(typeof e.selectStrategy=="object")return e.selectStrategy;switch(e.selectStrategy){case"single-leaf":return mt(e.mandatory);case"leaf":return vt(e.mandatory);case"independent":return ye(e.mandatory);case"single-independent":return ze(e.mandatory);case"classic":default:return gt(e.mandatory)}}),s=S(()=>{if(typeof e.openStrategy=="object")return e.openStrategy;switch(e.openStrategy){case"list":return ot;case"single":return dt;case"multiple":default:return Te}}),c=pe(e,"selected",e.selected,r=>a.value.in(r,n.value,t.value),r=>a.value.out(r,n.value,t.value));Me(()=>{i=!0});function y(r){const d=[];let g=r;for(;g!=null;)d.unshift(g),g=t.value.get(g);return d}const o=tt("nested"),v={id:_(),root:{opened:l,selected:c,selectedValues:S(()=>{const r=[];for(const[d,g]of c.value.entries())g==="on"&&r.push(d);return r}),register:(r,d,g)=>{d&&r!==d&&t.value.set(r,d),g&&n.value.set(r,[]),d!=null&&n.value.set(d,[...n.value.get(d)||[],r])},unregister:r=>{if(i)return;n.value.delete(r);const d=t.value.get(r);if(d){const g=n.value.get(d)??[];n.value.set(d,g.filter(m=>m!==r))}t.value.delete(r),l.value.delete(r)},open:(r,d,g)=>{o.emit("click:open",{id:r,value:d,path:y(r),event:g});const m=s.value.open({id:r,value:d,opened:new Set(l.value),children:n.value,parents:t.value,event:g});m&&(l.value=m)},openOnSelect:(r,d,g)=>{const m=s.value.select({id:r,value:d,selected:new Map(c.value),opened:new Set(l.value),children:n.value,parents:t.value,event:g});m&&(l.value=m)},select:(r,d,g)=>{o.emit("click:select",{id:r,value:d,path:y(r),event:g});const m=a.value.select({id:r,value:d,selected:new Map(c.value),children:n.value,parents:t.value,event:g});m&&(c.value=m),v.root.openOnSelect(r,d,g)},children:n,parents:t}};return Y(H,v),v.root},ft=(e,i)=>{const n=X(H,Re),t=Symbol(at()),l=S(()=>e.value??t),a={...n,id:l,open:(s,c)=>n.root.open(l.value,s,c),openOnSelect:(s,c)=>n.root.openOnSelect(l.value,s,c),isOpen:S(()=>n.root.opened.value.has(l.value)),parent:S(()=>n.root.parents.value.get(l.value)),select:(s,c)=>n.root.select(l.value,s,c),isSelected:S(()=>n.root.selected.value.get(x(l.value))==="on"),isIndeterminate:S(()=>n.root.selected.value.get(l.value)==="indeterminate"),isLeaf:S(()=>!n.root.children.value.get(l.value)),isGroupActivator:n.isGroupActivator};return!n.isGroupActivator&&n.root.register(l.value,n.id.value,i),Me(()=>{!n.isGroupActivator&&n.root.unregister(l.value)}),i&&Y(H,a),a},$t=()=>{const e=X(H,Re);Y(H,{...e,isGroupActivator:!0})};function yt(e){return{aspectStyles:S(()=>{const i=Number(e.aspectRatio);return i?{paddingBottom:String(1/i*100)+"%"}:void 0})}}const St=L({aspectRatio:[String,Number],contentClass:String,...P(),...le()},"v-responsive"),ht=B()({name:"VResponsive",props:St(),setup(e,i){let{slots:n}=i;const{aspectStyles:t}=yt(e),{dimensionStyles:l}=se(e);return T(()=>{var a;return u("div",{class:["v-responsive",e.class],style:[l.value,e.style]},[u("div",{class:"v-responsive__sizer",style:t.value},null),(a=n.additional)==null?void 0:a.call(n),n.default&&u("div",{class:["v-responsive__content",e.contentClass]},[n.default()])])}),{}}});function bt(e,i){if(!Oe)return;const n=i.modifiers||{},t=i.value,{handler:l,options:a}=typeof t=="object"?t:{handler:t,options:{}},s=new IntersectionObserver(function(){var r;let c=arguments.length>0&&arguments[0]!==void 0?arguments[0]:[],y=arguments.length>1?arguments[1]:void 0;const o=(r=e._observe)==null?void 0:r[i.instance.$.uid];if(!o)return;const v=c.some(d=>d.isIntersecting);l&&(!n.quiet||o.init)&&(!n.once||v||o.init)&&l(v,c,y),v&&n.once?xe(e,i):o.init=!0},a);e._observe=Object(e._observe),e._observe[i.instance.$.uid]={init:!1,observer:s},s.observe(e)}function xe(e,i){var t;const n=(t=e._observe)==null?void 0:t[i.instance.$.uid];n&&(n.observer.unobserve(e),delete e._observe[i.instance.$.uid])}const kt={mounted:bt,unmounted:xe},pt=kt,It=L({aspectRatio:[String,Number],alt:String,cover:Boolean,eager:Boolean,gradient:String,lazySrc:String,options:{type:Object,default:()=>({root:void 0,rootMargin:void 0,threshold:void 0})},sizes:String,src:{type:[String,Object],default:""},srcset:String,width:[String,Number],...P(),...ut()},"v-img"),Ne=B()({name:"VImg",directives:{intersect:pt},props:It(),emits:{loadstart:e=>!0,load:e=>!0,error:e=>!0},setup(e,i){let{emit:n,slots:t}=i;const l=_(""),a=V(),s=_(e.eager?"loading":"idle"),c=_(),y=_(),o=S(()=>e.src&&typeof e.src=="object"?{src:e.src.src,srcset:e.srcset||e.src.srcset,lazySrc:e.lazySrc||e.src.lazySrc,aspect:Number(e.aspectRatio||e.src.aspect||0)}:{src:e.src,srcset:e.srcset,lazySrc:e.lazySrc,aspect:Number(e.aspectRatio||0)}),v=S(()=>o.value.aspect||c.value/y.value||0);U(()=>e.src,()=>{r(s.value!=="idle")}),U(v,(f,b)=>{!f&&b&&a.value&&p(a.value)}),nt(()=>r());function r(f){if(!(e.eager&&f)&&!(Oe&&!f&&!e.eager)){if(s.value="loading",o.value.lazySrc){const b=new Image;b.src=o.value.lazySrc,p(b,null)}o.value.src&&lt(()=>{var b,I;if(n("loadstart",((b=a.value)==null?void 0:b.currentSrc)||o.value.src),(I=a.value)!=null&&I.complete){if(a.value.naturalWidth||g(),s.value==="error")return;v.value||p(a.value,null),d()}else v.value||p(a.value),m()})}}function d(){var f;m(),s.value="loaded",n("load",((f=a.value)==null?void 0:f.currentSrc)||o.value.src)}function g(){var f;s.value="error",n("error",((f=a.value)==null?void 0:f.currentSrc)||o.value.src)}function m(){const f=a.value;f&&(l.value=f.currentSrc||f.src)}let k=-1;function p(f){let b=arguments.length>1&&arguments[1]!==void 0?arguments[1]:100;const I=()=>{clearTimeout(k);const{naturalHeight:R,naturalWidth:M}=f;R||M?(c.value=M,y.value=R):!f.complete&&s.value==="loading"&&b!=null?k=window.setTimeout(I,b):(f.currentSrc.endsWith(".svg")||f.currentSrc.startsWith("data:image/svg+xml"))&&(c.value=1,y.value=1)};I()}const A=S(()=>({"v-img__img--cover":e.cover,"v-img__img--contain":!e.cover})),w=()=>{var I;if(!o.value.src||s.value==="idle")return null;const f=u("img",{class:["v-img__img",A.value],src:o.value.src,srcset:o.value.srcset,alt:e.alt,sizes:e.sizes,ref:a,onLoad:d,onError:g},null),b=(I=t.sources)==null?void 0:I.call(t);return u(K,{transition:e.transition,appear:!0},{default:()=>[q(b?u("picture",{class:"v-img__picture"},[b,f]):f,[[it,s.value==="loaded"]])]})},N=()=>u(K,{transition:e.transition},{default:()=>[o.value.lazySrc&&s.value!=="loaded"&&u("img",{class:["v-img__img","v-img__img--preload",A.value],src:o.value.lazySrc,alt:e.alt},null)]}),j=()=>t.placeholder?u(K,{transition:e.transition,appear:!0},{default:()=>[(s.value==="loading"||s.value==="error"&&!t.error)&&u("div",{class:"v-img__placeholder"},[t.placeholder()])]}):null,$=()=>t.error?u(K,{transition:e.transition,appear:!0},{default:()=>[s.value==="error"&&u("div",{class:"v-img__error"},[t.error()])]}):null,D=()=>e.gradient?u("div",{class:"v-img__gradient",style:{backgroundImage:`linear-gradient(${e.gradient})`}},null):null,z=_(!1);{const f=U(v,b=>{b&&(requestAnimationFrame(()=>{requestAnimationFrame(()=>{z.value=!0})}),f())})}return T(()=>q(u(ht,{class:["v-img",{"v-img--booting":!z.value},e.class],style:[{width:st(e.width==="auto"?c.value:e.width)},e.style],aspectRatio:v.value,"aria-label":e.alt,role:e.alt?"img":void 0},{additional:()=>u(ae,null,[u(w,null,null),u(N,null,null),u(D,null,null),u(j,null,null),u($,null,null)]),default:t.default}),[[me("intersect"),{handler:r,options:e.options},null,{once:!0}]])),{currentSrc:l,image:a,state:s,naturalWidth:c,naturalHeight:y}}}),At=L({start:Boolean,end:Boolean,icon:O,image:String,...P(),...Q(),...ie(),...Fe(),...re(),...ge(),...ue({variant:"flat"})},"v-avatar"),J=B()({name:"VAvatar",props:At(),setup(e,i){let{slots:n}=i;const{themeClasses:t}=fe(e),{colorClasses:l,colorStyles:a,variantClasses:s}=ce(e),{densityClasses:c}=de(e),{roundedClasses:y}=oe(e),{sizeClasses:o,sizeStyles:v}=He(e);return T(()=>u(e.tag,{class:["v-avatar",{"v-avatar--start":e.start,"v-avatar--end":e.end},t.value,l.value,c.value,y.value,o.value,s.value,e.class],style:[a.value,v.value,e.style]},{default:()=>{var r;return[e.image?u(Ne,{key:"image",src:e.image,alt:"",cover:!0},null):e.icon?u(te,{key:"icon",icon:e.icon},null):(r=n.default)==null?void 0:r.call(n),ve(!1,"v-avatar")]}})),{}}}),Ct=G("v-list-item-subtitle"),_t=G("v-list-item-title"),wt=L({active:{type:Boolean,default:void 0},activeClass:String,activeColor:String,appendAvatar:String,appendIcon:O,disabled:Boolean,lines:String,link:{type:Boolean,default:void 0},nav:Boolean,prependAvatar:String,prependIcon:O,ripple:{type:Boolean,default:!0},subtitle:[String,Number,Boolean],title:[String,Number,Boolean],value:null,onClick:Ie(),onClickOnce:Ie(),...Ae(),...P(),...Q(),...le(),...Ce(),...ie(),..._e(),...re(),...ge(),...ue({variant:"text"})},"v-list-item"),Dt=B()({name:"VListItem",directives:{Ripple:we},props:wt(),emits:{click:e=>!0},setup(e,i){let{attrs:n,slots:t,emit:l}=i;const a=Ve(e,n),s=S(()=>e.value??a.href.value),{select:c,isSelected:y,isIndeterminate:o,isGroupActivator:v,root:r,parent:d,openOnSelect:g}=ft(s,!1),m=ct(),k=S(()=>{var h;return e.active!==!1&&(e.active||((h=a.isActive)==null?void 0:h.value)||y.value)}),p=S(()=>e.link!==!1&&a.isLink.value),A=S(()=>!e.disabled&&e.link!==!1&&(e.link||a.isClickable.value||e.value!=null&&!!m)),w=S(()=>e.rounded||e.nav),N=S(()=>({color:k.value?e.activeColor??e.color:e.color,variant:e.variant}));U(()=>{var h;return(h=a.isActive)==null?void 0:h.value},h=>{h&&d.value!=null&&r.open(d.value,!0),h&&g(h)},{immediate:!0});const{themeClasses:j}=fe(e),{borderClasses:$}=Pe(e),{colorClasses:D,colorStyles:z,variantClasses:f}=ce(N),{densityClasses:b}=de(e),{dimensionStyles:I}=se(e),{elevationClasses:R}=Be(e),{roundedClasses:M}=oe(w),W=S(()=>e.lines?`v-list-item--${e.lines}-line`:void 0),Z=S(()=>({isActive:k.value,select:c,isSelected:y.value,isIndeterminate:o.value}));function Se(h){var E;l("click",h),!(v||!A.value)&&((E=a.navigate)==null||E.call(a,h),e.value!=null&&c(!y.value,h))}function je(h){(h.key==="Enter"||h.key===" ")&&(h.preventDefault(),Se(h))}return T(()=>{const h=p.value?"a":e.tag,E=!m||y.value||k.value,$e=t.title||e.title,De=t.subtitle||e.subtitle,he=!!(e.appendAvatar||e.appendIcon),Ee=!!(he||t.append),be=!!(e.prependAvatar||e.prependIcon),ee=!!(be||t.prepend);return m==null||m.updateHasPrepend(ee),q(u(h,{class:["v-list-item",{"v-list-item--active":k.value,"v-list-item--disabled":e.disabled,"v-list-item--link":A.value,"v-list-item--nav":e.nav,"v-list-item--prepend":!ee&&(m==null?void 0:m.hasPrepend.value),[`${e.activeClass}`]:e.activeClass&&k.value},j.value,$.value,E?D.value:void 0,b.value,R.value,W.value,M.value,f.value,e.class],style:[E?z.value:void 0,I.value,e.style],href:a.href.value,tabindex:A.value?0:void 0,onClick:Se,onKeydown:A.value&&!p.value&&je},{default:()=>{var ke;return[ve(A.value||k.value,"v-list-item"),ee&&u("div",{key:"prepend",class:"v-list-item__prepend"},[t.prepend?u(F,{key:"prepend-defaults",disabled:!be,defaults:{VAvatar:{density:e.density,image:e.prependAvatar},VIcon:{density:e.density,icon:e.prependIcon},VListItemAction:{start:!0}}},{default:()=>{var C;return[(C=t.prepend)==null?void 0:C.call(t,Z.value)]}}):u(ae,null,[e.prependAvatar&&u(J,{key:"prepend-avatar",density:e.density,image:e.prependAvatar},null),e.prependIcon&&u(te,{key:"prepend-icon",density:e.density,icon:e.prependIcon},null)])]),u("div",{class:"v-list-item__content","data-no-activator":""},[$e&&u(_t,{key:"title"},{default:()=>{var C;return[((C=t.title)==null?void 0:C.call(t,{title:e.title}))??e.title]}}),De&&u(Ct,{key:"subtitle"},{default:()=>{var C;return[((C=t.subtitle)==null?void 0:C.call(t,{subtitle:e.subtitle}))??e.subtitle]}}),(ke=t.default)==null?void 0:ke.call(t,Z.value)]),Ee&&u("div",{key:"append",class:"v-list-item__append"},[t.append?u(F,{key:"append-defaults",disabled:!he,defaults:{VAvatar:{density:e.density,image:e.appendAvatar},VIcon:{density:e.density,icon:e.appendIcon},VListItemAction:{end:!0}}},{default:()=>{var C;return[(C=t.append)==null?void 0:C.call(t,Z.value)]}}):u(ae,null,[e.appendIcon&&u(te,{key:"append-icon",density:e.density,icon:e.appendIcon},null),e.appendAvatar&&u(J,{key:"append-avatar",density:e.density,image:e.appendAvatar},null)])])]}}),[[me("ripple"),A.value&&e.ripple]])}),{}}});const Vt=B()({name:"VCardActions",props:P(),setup(e,i){let{slots:n}=i;return rt({VBtn:{variant:"text"}}),T(()=>{var t;return u("div",{class:["v-card-actions",e.class],style:e.style},[(t=n.default)==null?void 0:t.call(n)])}),{}}}),Pt=G("v-card-subtitle"),Bt=G("v-card-title"),Lt=L({appendAvatar:String,appendIcon:O,prependAvatar:String,prependIcon:O,subtitle:String,title:String,...P(),...Q()},"v-card-item"),Mt=B()({name:"VCardItem",props:Lt(),setup(e,i){let{slots:n}=i;return T(()=>{var o;const t=!!(e.prependAvatar||e.prependIcon),l=!!(t||n.prepend),a=!!(e.appendAvatar||e.appendIcon),s=!!(a||n.append),c=!!(e.title||n.title),y=!!(e.subtitle||n.subtitle);return u("div",{class:["v-card-item",e.class],style:e.style},[l&&u("div",{key:"prepend",class:"v-card-item__prepend"},[n.prepend?u(F,{key:"prepend-defaults",disabled:!t,defaults:{VAvatar:{density:e.density,icon:e.prependIcon,image:e.prependAvatar}}},n.prepend):t&&u(J,{key:"prepend-avatar",density:e.density,icon:e.prependIcon,image:e.prependAvatar},null)]),u("div",{class:"v-card-item__content"},[c&&u(Bt,{key:"title"},{default:()=>{var v;return[((v=n.title)==null?void 0:v.call(n))??e.title]}}),y&&u(Pt,{key:"subtitle"},{default:()=>{var v;return[((v=n.subtitle)==null?void 0:v.call(n))??e.subtitle]}}),(o=n.default)==null?void 0:o.call(n)]),s&&u("div",{key:"append",class:"v-card-item__append"},[n.append?u(F,{key:"append-defaults",disabled:!a,defaults:{VAvatar:{density:e.density,icon:e.appendIcon,image:e.appendAvatar}}},n.append):a&&u(J,{key:"append-avatar",density:e.density,icon:e.appendIcon,image:e.appendAvatar},null)])])}),{}}}),Ot=G("v-card-text"),Tt=L({appendAvatar:String,appendIcon:O,disabled:Boolean,flat:Boolean,hover:Boolean,image:String,link:{type:Boolean,default:void 0},prependAvatar:String,prependIcon:O,ripple:{type:Boolean,default:!0},subtitle:String,text:String,title:String,...Ae(),...P(),...Q(),...le(),...Ce(),...Ge(),...We(),...Ke(),...ie(),..._e(),...re(),...ge(),...ue({variant:"elevated"})},"v-card"),Et=B()({name:"VCard",directives:{Ripple:we},props:Tt(),setup(e,i){let{attrs:n,slots:t}=i;const{themeClasses:l}=fe(e),{borderClasses:a}=Pe(e),{colorClasses:s,colorStyles:c,variantClasses:y}=ce(e),{densityClasses:o}=de(e),{dimensionStyles:v}=se(e),{elevationClasses:r}=Be(e),{loaderClasses:d}=Ue(e),{locationStyles:g}=qe(e),{positionClasses:m}=Je(e),{roundedClasses:k}=oe(e),p=Ve(e,n),A=S(()=>e.link!==!1&&p.isLink.value),w=S(()=>!e.disabled&&e.link!==!1&&(e.link||p.isClickable.value));return T(()=>{const N=A.value?"a":e.tag,j=!!(t.title||e.title),$=!!(t.subtitle||e.subtitle),D=j||$,z=!!(t.append||e.appendAvatar||e.appendIcon),f=!!(t.prepend||e.prependAvatar||e.prependIcon),b=!!(t.image||e.image),I=D||f||z,R=!!(t.text||e.text);return q(u(N,{class:["v-card",{"v-card--disabled":e.disabled,"v-card--flat":e.flat,"v-card--hover":e.hover&&!(e.disabled||e.flat),"v-card--link":w.value},l.value,a.value,s.value,o.value,r.value,d.value,m.value,k.value,y.value,e.class],style:[c.value,v.value,g.value,e.style],href:p.href.value,onClick:w.value&&p.navigate,tabindex:e.disabled?-1:void 0},{default:()=>{var M;return[b&&u("div",{key:"image",class:"v-card__image"},[t.image?u(F,{key:"image-defaults",disabled:!e.image,defaults:{VImg:{cover:!0,src:e.image}}},t.image):u(Ne,{key:"image-img",cover:!0,src:e.image},null)]),u(Qe,{name:"v-card",active:!!e.loading,color:typeof e.loading=="boolean"?void 0:e.loading},{default:t.loader}),I&&u(Mt,{key:"item",prependAvatar:e.prependAvatar,prependIcon:e.prependIcon,title:e.title,subtitle:e.subtitle,appendAvatar:e.appendAvatar,appendIcon:e.appendIcon},{default:t.item,prepend:t.prepend,title:t.title,subtitle:t.subtitle,append:t.append}),R&&u(Ot,{key:"text"},{default:()=>{var W;return[((W=t.text)==null?void 0:W.call(t))??e.text]}}),(M=t.default)==null?void 0:M.call(t),t.actions&&u(Vt,null,{default:t.actions}),ve(w.value,"v-card")]}}),[[me("ripple"),w.value&&e.ripple]])}),{}}});export{pt as I,K as M,Dt as V,J as a,Pt as b,Et as c,_t as d,Ne as e,Bt as f,Ot as g,Vt as h,Ct as i,G as j,ft as k,ct as l,ut as m,xt as n,Nt as o,jt as p,$t as u};
