// Calendar logic shared by the web page and scripts/test-web.mjs. Mirrors Shared/CalendarBuilder.swift.
"use strict";
const CATS=[["selfcare","Self care","s"],["family","Family fun","f"],["fitness","Fitness","x"],["music","Music","m"],["puzzles","Puzzles","p"],["food","Food","o"],["humor","Humor","h"],["books","Books","b"]];
const CAT_NAME=Object.fromEntries(CATS.map(c=>[c[0],c[1]]));
const CAT_CODE=Object.fromEntries(CATS.map(c=>[c[0],c[2]]));
const CODE_CAT=Object.fromEntries(CATS.map(c=>[c[2],c[0]]));
const TIERS=["none","low","medium","high"];
const TIER_NAME={none:"Free",low:"Low",medium:"Medium",high:"High"};
const QUOTA={none:{},low:{low:10},medium:{medium:6,low:8},high:{high:4,medium:6,low:6}};
const KIND_NAME={do:"Do",read:"Read",think:"Think"};
const ITEMS=window.ADVENT_ITEMS||[];
const BY_ID=Object.fromEntries(ITEMS.map(i=>[i.id,i]));

// Deterministic random, so a seed always gives the same calendar.
function rng(seed){let a=seed>>>0;return()=>{a=(a+0x6D2B79F5)>>>0;let t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return((t^(t>>>14))>>>0)/4294967296}}
function shuffle(arr,r){const a=arr.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(r()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function newSeed(){return Math.floor(Math.random()*2147483647)}

function pick(cats,budget,seed,exclude){
  exclude=exclude||new Set();
  const r=rng(seed);
  const allowed=TIERS.slice(0,TIERS.indexOf(budget)+1);
  const pool={};
  for(const t of allowed){pool[t]={};for(const c of cats){pool[t][c]=shuffle(ITEMS.filter(i=>i.category===c&&i.budget===t&&!exclude.has(i.id)),r)}}
  const chosen=[];
  const take=(t,n)=>{if(!pool[t])return n;const order=shuffle(cats,r);for(;;){let moved=false;for(const c of order){if(n<=0)return 0;const it=pool[t][c].pop();if(it){chosen.push(it);n--;moved=true}}if(!moved||n<=0)return n}};
  const q=QUOTA[budget];
  for(const t of ["high","medium","low"])if(q[t])take(t,q[t]);
  let need=take("none",24-chosen.length);
  for(const t of ["low","medium","high"])if(need>0)need=take(t,need);
  return arrange(chosen,r).map(i=>i.id);
}
// Spread categories so the same one rarely lands on back-to-back days.
function arrange(items,r){
  const a=shuffle(items,r);
  for(let i=1;i<a.length;i++){
    if(a[i].category!==a[i-1].category)continue;
    for(let j=i+1;j<a.length;j++){if(a[j].category!==a[i-1].category){[a[i],a[j]]=[a[j],a[i]];break}}
  }
  return a;
}
// The house front. Slot 0 is the attic window, 1 to 20 are four windows on each of five floors,
// 21 and 23 the ground floor windows, 22 the front door. Day 24 is always the front door.
function layout(seed){
  const r=rng((seed^0x9E3779B9)>>>0);
  const days=shuffle([...Array(23)].map((_,i)=>i+1),r);
  days.splice(22,0,24);
  return days;
}
// Ratings steer the doors that cannot be opened yet. A loved day brings one more of its kind,
// a disliked one swaps the next of its kind away. Returns the new days, or null when nothing changes.
function steer(cal,opened,day,stars,open){
  if(stars===3||cal.cats.length<2)return null;
  const days=cal.days.slice();const rated=BY_ID[days[day-1]];if(!rated)return null;
  const used=new Set(days);const r=rng((cal.seed^Math.imul(day,2654435761))>>>0);
  const future=[];for(let d=open+1;d<=24;d++)if(!opened[d])future.push(d);
  const fresh=(cat,tier)=>shuffle(ITEMS.filter(i=>i.category===cat&&i.budget===tier&&!used.has(i.id)),r)[0]||null;
  if(stars>=4){
    const count={};future.forEach(d=>{const c=BY_ID[days[d-1]].category;if(c!==rated.category)count[c]=(count[c]||0)+1});
    const top=Object.keys(count).sort((x,y)=>count[y]-count[x]||(x<y?-1:1))[0];if(!top)return null;
    const d=future.find(d=>BY_ID[days[d-1]].category===top);const it=fresh(rated.category,BY_ID[days[d-1]].budget);if(!it)return null;
    days[d-1]=it.id;return days;
  }
  const d=future.find(d=>BY_ID[days[d-1]].category===rated.category);if(!d)return null;
  for(const c of shuffle(cal.cats.filter(c=>c!==rated.category),r)){const it=fresh(c,BY_ID[days[d-1]].budget);if(it){days[d-1]=it.id;return days}}
  return null;
}

function b64e(s){const b=new TextEncoder().encode(s);let bin="";b.forEach(x=>bin+=String.fromCharCode(x));return btoa(bin).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"")}
function b64d(s){s=s.replace(/-/g,"+").replace(/_/g,"/");const bin=atob(s);return new TextDecoder().decode(Uint8Array.from(bin,c=>c.charCodeAt(0)))}
function encodeDays(ids){return ids.map(id=>{const[c,n]=id.split("-");return CAT_CODE[c]+parseInt(n,10)}).join(".")}
function decodeDays(s){return s.split(".").map(t=>{const c=CODE_CAT[t[0]];const n=t.slice(1).padStart(2,"0");return c+"-"+n})}
function hashKey(s){let h=5381;for(let i=0;i<s.length;i++)h=((h<<5)+h+s.charCodeAt(i))>>>0;return h.toString(36)}
