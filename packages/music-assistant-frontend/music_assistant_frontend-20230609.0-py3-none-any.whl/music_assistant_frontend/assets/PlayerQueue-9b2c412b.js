import{l as Y,J as Z,I as Q,r as M,c as k,o as ee,O as n,a7 as D,b as le,B as $,w as te,q as d,y as U,j as u,x as a,K as V,N as r,v as f,L as p,M as _,k as J,A as h,aq as T,S as ue}from"./index-11e01e27.js";import{_ as ae,s as oe}from"./ListviewItem.vue_vue_type_script_setup_true_lang-a96ef087.js";import{t as ie}from"./MediaItemThumb.vue_vue_type_style_index_0_lang-c919923a.js";import{V as O,L as g}from"./ProviderIcon.vue_vue_type_script_setup_true_lang-0ce5ab95.js";import{V as P,a as ne}from"./VTabs-63da40d9.js";import{V as F}from"./VAlert-1abda951.js";import{l as x,V as q}from"./VBtn-ba18d485.js";import{c as se,a as y,g as re}from"./VCard-4c75536f.js";import{V as de,b as G}from"./VToolbar-685b17bc.js";import{V as me}from"./VMenu-6f4b0d2a.js";import{V as C}from"./index-688be463.js";import{V as pe}from"./VDialog-06407d5a.js";import"./VLabel-9146de69.js";import"./VCheckboxBtn-7e157388.js";const ve=p("br",null,null,-1),fe={key:0},_e={key:0},ce={key:1},Ae=Y({__name:"PlayerQueue",setup(be){const{t:H}=Z(),B=Q(),E=M(0),s=M(),I=M(!1),c=M([]),e=k(()=>{if($.selectedPlayer)return n.queues[$.selectedPlayer.active_source]}),W=k(()=>{if(e.value)return e.value.current_item}),N=k(()=>e.value?c.value.slice(e.value.current_index):[]),S=k(()=>e.value?c.value.slice(0,e.value.current_index):[]),X=k(()=>E.value==1?S.value:N.value);ee(()=>{const l=n.subscribe_multi([D.QUEUE_UPDATED,D.QUEUE_ITEMS_UPDATED],t=>{var w;t.object_id==((w=e.value)==null?void 0:w.queue_id)&&(t.event==D.QUEUE_ITEMS_UPDATED?L():j())});le(l)});const L=async function(){e.value?($.topBarTitle=e.value.display_name,c.value=[],await n.getPlayerQueueItems(e.value.queue_id,l=>{console.log("chunk",l.length),c.value.push(...l)})):($.topBarTitle=void 0,c.value=[])},z=function(l){s.value=l,I.value=!0},R=function(l){A(),B.push({name:l.media_type,params:{itemId:l.item_id,provider:l.provider}})},b=function(l,t){A(),!(!l||!e.value)&&(t=="play_now"?n.queueCommandPlayIndex(e==null?void 0:e.value.queue_id,l.queue_item_id):t=="move_next"?n.queueCommandMoveNext(e==null?void 0:e.value.queue_id,l.queue_item_id):t=="up"?n.queueCommandMoveUp(e==null?void 0:e.value.queue_id,l.queue_item_id):t=="down"?n.queueCommandMoveDown(e==null?void 0:e.value.queue_id,l.queue_item_id):t=="delete"&&n.queueCommandDelete(e==null?void 0:e.value.queue_id,l.queue_item_id))},j=function(){$.topBarContextMenuItems=[{label:"settings.player_settings",labelArgs:[],action:()=>{B.push(`/settings/editplayer/${e.value.queue_id}`)},icon:"mdi-cog-outline"},{label:"queue_clear",labelArgs:[],action:()=>{n.queueCommandClear(e.value.queue_id)},icon:"mdi-cancel"},{label:e.value.shuffle_enabled?"shuffle_enabled":"shuffle_disabled",labelArgs:[],action:()=>{n.queueCommandShuffleToggle(e.value.queue_id)},icon:e.value.shuffle_enabled?"mdi-shuffle":"mdi-shuffle-disabled"},{label:"repeat_mode",labelArgs:[H(`repeatmode.${e.value.repeat_mode}`)],action:()=>{n.queueCommandRepeatToggle(e.value.queue_id)},icon:e.value.shuffle_enabled?"mdi-repeat":"mdi-repeat-off"},{label:e.value.crossfade_enabled?"crossfade_enabled":"crossfade_disabled",labelArgs:[],action:()=>{n.queueCommandCrossfadeToggle(e.value.queue_id)},icon:e.value.crossfade_enabled?"mdi-swap-horizontal-bold":"mdi-swap-horizontal"}]},A=function(){s.value=void 0,I.value=!1};return te(()=>e.value,l=>{l&&(L(),j())},{immediate:!0}),(l,t)=>{var w;return d(),U("section",null,[u(ne,{modelValue:E.value,"onUpdate:modelValue":t[0]||(t[0]=o=>E.value=o),"show-arrows":"",grow:""},{default:a(()=>[u(P,{value:0},{default:a(()=>[V(r(l.$t("queue_next_items")+" ("+N.value.length+")"),1)]),_:1}),u(P,{value:1},{default:a(()=>[V(r(l.$t("queue_previous_items")+" ("+S.value.length+")"),1)]),_:1})]),_:1},8,["modelValue"]),e.value&&((w=e.value)==null?void 0:w.radio_source.length)>0?(d(),f(F,{key:0,color:"primary",theme:"dark",icon:"mdi-radio-tower",prominent:"",style:{"margin-right":"10px"}},{default:a(()=>{var o,m,i,v;return[p("b",null,r(l.$t("queue_radio_enabled")),1),ve,V(" "+r(l.$t("queue_radio_based_on",[l.$t((o=e.value)==null?void 0:o.radio_source[0].media_type)]))+" ",1),p("b",null,[p("a",{onClick:t[1]||(t[1]=ge=>{var K;return e.value?R((K=e.value)==null?void 0:K.radio_source[0]):""})},r((m=e.value)==null?void 0:m.radio_source[0].name),1)]),((i=e.value)==null?void 0:i.radio_source.length)>1?(d(),U("span",fe," (+"+r(((v=e.value)==null?void 0:v.radio_source.length)-1)+")",1)):_("",!0)]}),_:1})):_("",!0),u(h(oe),{items:X.value,"item-size":60,"key-field":"queue_item_id","page-mode":""},{default:a(({item:o})=>{var m;return[(d(),f(ae,{key:o.uri,item:o.media_item,"show-disc-number":!1,"show-track-number":!1,"show-duration":!0,"show-library":!0,"show-menu":!0,"show-providers":!1,"show-album":!1,"show-checkboxes":!1,"is-selected":!1,"show-details":!1,"parent-item":o,"is-disabled":o.queue_item_id==((m=W.value)==null?void 0:m.queue_item_id),ripple:"",onMenu:i=>z(o),onClick:i=>b(o,"play_now"),onContextmenu:T(i=>z(o),["right","prevent"])},{append:a(()=>[l.$vuetify.display.mobile?_("",!0):(d(),U("div",_e,[u(O,{location:"bottom"},{activator:a(({props:i})=>[u(x,J({variant:"plain",ripple:""},i,{icon:"mdi-arrow-up",onClick:[v=>h(n).queueCommandMoveUp(e.value.queue_id,o.queue_item_id),t[2]||(t[2]=T(()=>{},["prevent"])),t[3]||(t[3]=T(()=>{},["stop"]))]}),null,16,["onClick"])]),default:a(()=>[p("span",null,r(l.$t("queue_move_up")),1)]),_:2},1024)])),l.$vuetify.display.mobile?_("",!0):(d(),U("div",ce,[u(O,{location:"bottom"},{activator:a(({props:i})=>[u(x,J({variant:"plain",ripple:""},i,{icon:"mdi-arrow-down",onClick:[v=>h(n).queueCommandMoveDown(e.value.queue_id,o.queue_item_id),t[4]||(t[4]=T(()=>{},["prevent"])),t[5]||(t[5]=T(()=>{},["stop"]))]}),null,16,["onClick"])]),default:a(()=>[p("span",null,r(l.$t("queue_move_down")),1)]),_:2},1024)]))]),_:2},1032,["item","parent-item","is-disabled","onMenu","onClick","onContextmenu"]))]}),_:1},8,["items"]),c.value.length==0?(d(),f(F,{key:1,type:"info",style:{margin:"20px"}},{default:a(()=>[V(r(l.$t("no_content")),1)]),_:1})):_("",!0),u(pe,{modelValue:I.value,"onUpdate:modelValue":t[13]||(t[13]=o=>I.value=o),fullscreen:l.$vuetify.display.mobile,"min-height":"80%",scrim:!0},{default:a(()=>[u(se,null,{default:a(()=>[u(de,{sense:"",dark:"",color:"primary"},{default:a(()=>[u(x,{icon:"mdi-play-circle-outline"}),s.value?(d(),f(G,{key:0,style:{"padding-left":"10px"}},{default:a(()=>{var o;return[p("b",null,r(h(ie)(((o=s.value)==null?void 0:o.name)||"",l.$vuetify.display.mobile?20:150)),1)]}),_:1})):(d(),f(G,{key:1,style:{"padding-left":"10px"}},{default:a(()=>{var o;return[p("b",null,r(l.$t("settings")),1),V(" | "+r((o=e.value)==null?void 0:o.display_name),1)]}),_:1})),u(x,{icon:"mdi-close",dark:"",onClick:t[6]||(t[6]=o=>A())})]),_:1}),s.value?(d(),f(re,{key:0},{default:a(()=>[u(me,null,{default:a(()=>{var o,m;return[u(g,{title:l.$t("play_now"),onClick:t[7]||(t[7]=i=>b(s.value,"play_now"))},{prepend:a(()=>[u(y,{style:{"padding-right":"10px"}},{default:a(()=>[u(q,{icon:"mdi-play-circle-outline"})]),_:1})]),_:1},8,["title"]),u(C),u(g,{title:l.$t("play_next"),onClick:t[8]||(t[8]=i=>b(s.value,"move_next"))},{prepend:a(()=>[u(y,{style:{"padding-right":"10px"}},{default:a(()=>[u(q,{icon:"mdi-skip-next-circle-outline"})]),_:1})]),_:1},8,["title"]),u(C),u(g,{title:l.$t("queue_move_up"),onClick:t[9]||(t[9]=i=>b(s.value,"up"))},{prepend:a(()=>[u(y,{style:{"padding-right":"10px"}},{default:a(()=>[u(q,{icon:"mdi-arrow-up"})]),_:1})]),_:1},8,["title"]),u(C),u(g,{title:l.$t("queue_move_down"),onClick:t[10]||(t[10]=i=>b(s.value,"down"))},{prepend:a(()=>[u(y,{style:{"padding-right":"10px"}},{default:a(()=>[u(q,{icon:"mdi-arrow-down"})]),_:1})]),_:1},8,["title"]),u(C),u(g,{title:l.$t("queue_delete"),onClick:t[11]||(t[11]=i=>b(s.value,"delete"))},{prepend:a(()=>[u(y,{style:{"padding-right":"10px"}},{default:a(()=>[u(q,{icon:"mdi-delete"})]),_:1})]),_:1},8,["title"]),u(C),((m=(o=s.value)==null?void 0:o.media_item)==null?void 0:m.media_type)==h(ue).TRACK?(d(),f(g,{key:0,title:l.$t("show_info"),onClick:t[12]||(t[12]=i=>{var v;return(v=s.value)!=null&&v.media_item?R(s.value.media_item):""})},{prepend:a(()=>[u(y,{style:{"padding-right":"10px"}},{default:a(()=>[u(q,{icon:"mdi-information-outline"})]),_:1})]),_:1},8,["title"])):_("",!0),u(C)]}),_:1})]),_:1})):_("",!0)]),_:1})]),_:1},8,["modelValue","fullscreen"])])}}});export{Ae as default};
