import{l as y,J as k,I as B,r as l,c as b,o as V,w as g,q as o,y as x,j as r,x as u,v as m,M as c,A as C,O as q,B as f,S as M}from"./index-11e01e27.js";import{_ as N,s as O}from"./ListviewItem.vue_vue_type_script_setup_true_lang-a96ef087.js";import{h as P}from"./MediaItemThumb.vue_vue_type_style_index_0_lang-c919923a.js";import{l as T,k as D}from"./VBtn-ba18d485.js";import{V as E}from"./VContainer-b3bc5698.js";import"./ProviderIcon.vue_vue_type_script_setup_true_lang-0ce5ab95.js";import"./VCard-4c75536f.js";import"./VMenu-6f4b0d2a.js";import"./index-688be463.js";import"./VLabel-9146de69.js";import"./VCheckboxBtn-7e157388.js";/* empty css              */const K=y({__name:"BrowseView",props:{path:{}},setup(d){const t=d,{t:h}=k(),i=B(),a=l(),s=l(!1),w=b(()=>{if(t.path){const e=t.path.substring(0,t.path.lastIndexOf("/")+1);return e.endsWith("://")?"":e}return""}),n=async function(){s.value=!0,a.value=await q.browse(t.path),!a.value||!t.path?f.topBarTitle=void 0:f.topBarTitle=P(a.value,h),s.value=!1};V(()=>{n()}),g(()=>t.path,()=>{n()});const v=function(e){e.media_type===M.FOLDER?i.push({name:"browse",query:{path:e.path}}):i.push({name:e.media_type,params:{itemId:e.item_id,provider:e.provider}})};return(e,F)=>(o(),x("section",null,[r(E,null,{default:u(()=>{var p;return[s.value?(o(),m(D,{key:0,indeterminate:""})):c("",!0),t.path?(o(),m(T,{key:1,variant:"plain",icon:"mdi-arrow-left",to:{name:"browse",query:{path:w.value}}},null,8,["to"])):c("",!0),r(C(O),{items:((p=a.value)==null?void 0:p.items)||[],"item-size":66,"key-field":"uri","page-mode":""},{default:u(({item:_})=>[r(N,{item:_,"show-library":!1,"show-menu":!1,"show-providers":!1,"is-selected":!1,onClick:v},null,8,["item"])]),_:1},8,["items"])]}),_:1})]))}});export{K as default};
