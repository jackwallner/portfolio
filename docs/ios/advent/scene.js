// The living scene: night sky, snow, the house, bell chimes and the frost you wipe away.
"use strict";
const REDUCE=matchMedia("(prefers-reduced-motion: reduce)").matches;

const THEMES=[
  {id:"midnight",name:"Midnight",wall:"#2a3a68",wall2:"#1a2548",roof:"#0f1630",trim:"#f3ead6",sh:"#b8364a",sh2:"#8c2435",num:"#f6d58a"},
  {id:"gingerbread",name:"Gingerbread",wall:"#a36a3c",wall2:"#7a4a27",roof:"#4f2f19",trim:"#fff8ec",sh:"#fbf4e6",sh2:"#e6d8c0",num:"#a3283a"},
  {id:"nordic",name:"Nordic",wall:"#b03d34",wall2:"#882a25",roof:"#241616",trim:"#fbf5ea",sh:"#22543f",sh2:"#173a2d",num:"#f6d58a"}
];

const ICON={
  selfcare:'<path d="M4 10h13v2.5a6.5 6.5 0 0 1-13 0z"/><path d="M17 11h1.5a2.3 2.3 0 0 1 0 4.6h-1.9" fill="none"/><path d="M8 3.2c-1 1.4 1 2.4 0 3.9M12.5 3.2c-1 1.4 1 2.4 0 3.9M3 21h15" fill="none"/>',
  family:'<circle cx="8" cy="6" r="3"/><path d="M2.5 21v-4.5a5.5 5.5 0 0 1 11 0V21z"/><circle cx="17.5" cy="10" r="2.3"/><path d="M14.6 21v-3a3.4 3.4 0 0 1 6.8 0v3z"/>',
  fitness:'<rect x="2" y="8.5" width="3" height="7" rx="1"/><rect x="19" y="8.5" width="3" height="7" rx="1"/><rect x="5.6" y="6" width="3" height="12" rx="1"/><rect x="15.4" y="6" width="3" height="12" rx="1"/><rect x="8.6" y="11" width="6.8" height="2"/>',
  music:'<path d="M9 17.5V5.2l11-2.6v12.6" fill="none"/><ellipse cx="6.2" cy="17.8" rx="3.1" ry="2.5"/><ellipse cx="17.2" cy="15.4" rx="3.1" ry="2.5"/>',
  puzzles:'<path d="M4 7.5h4.3a2.3 2.3 0 1 1 4.4 0H17v4.2a2.3 2.3 0 1 1 0 4.4V20H4z"/>',
  food:'<path d="M5.5 12.5h13L17 21H7z"/><path d="M4.6 11.4a3.4 3.4 0 0 1 2.5-5.4 5 5 0 0 1 9.8 0 3.4 3.4 0 0 1 2.5 5.4z"/><circle cx="12" cy="2.7" r="1.2"/>',
  humor:'<path fill-rule="evenodd" d="M12 2.5a9.5 9.5 0 1 0 0 19 9.5 9.5 0 0 0 0-19zM6.6 12.6h10.8a5.4 5.4 0 0 1-10.8 0zM8.6 7.4a1.4 1.4 0 1 0 0 2.8 1.4 1.4 0 0 0 0-2.8zm6.8 0a1.4 1.4 0 1 0 0 2.8 1.4 1.4 0 0 0 0-2.8z"/>',
  books:'<path d="M3 5.6c3-1.2 6-1 8.2.6v13.3C9 18 6 17.8 3 19z"/><path d="M21 5.6c-3-1.2-6-1-8.2.6v13.3C15 18 18 17.8 21 19z"/>'
};
function icon(cat,cls){return`<svg class="${cls||"ic"}" viewBox="0 0 24 24" aria-hidden="true">${ICON[cat]||""}</svg>`}

// House geometry, in a 400 by 720 design space that the page scales to fit.
function slot(i){
  if(i===0)return{x:177,y:92,w:46,h:46,kind:"round"};
  if(i<=20){const row=(i-1)>>2,col=(i-1)&3;return{x:60+col*78,y:176+row*80,w:46,h:58,kind:row%2?"rect":"arch"}}
  if(i===22)return{x:161,y:586,w:78,h:92,kind:"door"};
  return{x:i===21?60:294,y:596,w:46,h:60,kind:"arch"};
}
const WREATH='<svg class="wreath" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="18" r="11" fill="none" stroke="#1d5a3d" stroke-width="7.5"/><circle cx="20" cy="18" r="11" fill="none" stroke="#3b8f63" stroke-width="7.5" stroke-dasharray="2.5 5"/><circle cx="12" cy="11" r="1.7" fill="#e5384d"/><circle cx="29" cy="14" r="1.7" fill="#e5384d"/><circle cx="14" cy="27" r="1.7" fill="#e5384d"/><path d="M20 27l-7 8 7-3 7 3z" fill="#d42d43"/><circle cx="20" cy="27.5" r="2.7" fill="#e5384d"/></svg>';

function houseBG(t,lit,star){
  const roofY=x=>52+.674*Math.abs(x-200);
  let bulbs="",wire="M40 "+(roofY(40)+16);
  const cols=["#ff6b6b","#ffd166","#6bd5ff","#8be28b"];
  for(let x=52,i=0;x<=348;x+=14.8,i++){const y=roofY(x)+17+(i%2?1.5:0);wire+=` L${x.toFixed(1)} ${y.toFixed(1)}`;bulbs+=`<circle class="bulb" cx="${x.toFixed(1)}" cy="${(y+2.5).toFixed(1)}" r="3.1" fill="${cols[i%4]}" style="animation-delay:${(-i*.37).toFixed(2)}s"/>`}
  const smoke=lit?[0,1,2].map(i=>`<circle class="puff" cx="290" cy="54" r="7" style="animation-delay:${-i*1.6}s"/>`).join(""):"";
  return`<svg class="bg" viewBox="0 0 400 720" aria-hidden="true">
<defs>
<linearGradient id="wallg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${t.wall}"/><stop offset="1" stop-color="${t.wall2}"/></linearGradient>
<pattern id="siding" width="10" height="9" patternUnits="userSpaceOnUse"><rect width="10" height="1.2" fill="#000" opacity=".16"/><rect y="1.2" width="10" height="1" fill="#fff" opacity=".05"/></pattern>
<radialGradient id="shade" cx=".5" cy="1" r=".9"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></radialGradient>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>
</defs>
<ellipse cx="200" cy="684" rx="205" ry="13" fill="#3b4f8a" opacity=".3"/>
<g class="pine"><path d="M14 598l22 38H-8z" fill="#1c4a3a"/><path d="M14 620l27 42H-13z" fill="#173f31"/><path d="M14 646l31 44H-17z" fill="#12362a"/><path d="M14 598l8 14c-4-2-6 2-8-1s-5 3-8 1z" fill="#fff"/><path d="M14 620l11 17c-5-2-7 3-11 0s-7 2-11 0z" fill="#fff" opacity=".95"/><path d="M14 646l13 18c-6-2-8 3-13 0s-8 2-13 0z" fill="#fff" opacity=".95"/></g>
<rect x="276" y="66" width="28" height="60" fill="${t.wall}"/><rect x="276" y="66" width="28" height="60" fill="url(#siding)"/><rect x="271" y="58" width="38" height="11" rx="5.5" fill="#fff"/>
${smoke}
<path d="M44 682V160L200 56 356 160V682Z" fill="url(#wallg)"/>
<path d="M44 682V160L200 56 356 160V682Z" fill="url(#siding)"/>
<path d="M44 682V160L200 56 356 160V682Z" fill="url(#shade)"/>
<path d="M22 172L200 52 378 172" fill="none" stroke="${t.roof}" stroke-width="17" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M22 166L200 46 378 166" fill="none" stroke="#fff" stroke-width="15" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="11 13"/>
<path d="M20 163L200 42 380 163" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
<path d="${wire}" fill="none" stroke="#0a0f22" stroke-width="1" opacity=".7"/>
${bulbs}
<rect x="150" y="676" width="100" height="10" rx="3" fill="#cfd6ea"/><rect x="146" y="672" width="108" height="7" rx="3.5" fill="#fff"/>
<path d="M36 688c8-12 22-12 30-3 9-9 24-8 30 3z" fill="#fff"/><path d="M300 688c8-11 22-11 30-3 9-8 26-7 34 3z" fill="#fff"/>
<g class="snowman" transform="translate(-7 0)"><circle cx="384" cy="668" r="17" fill="#fff"/><circle cx="384" cy="644" r="12" fill="#fff"/><circle cx="384" cy="626" r="9" fill="#fff"/><path d="M373 635q11 6 22 0l1 5q-12 6-24 0z" fill="${t.sh}"/><path d="M391 638l5 13-5-1z" fill="${t.sh}"/><rect x="376" y="608" width="16" height="11" rx="1.5" fill="#141a33"/><rect x="372" y="617" width="24" height="3" rx="1.5" fill="#141a33"/><circle cx="381" cy="624" r="1.1" fill="#141a33"/><circle cx="387" cy="624" r="1.1" fill="#141a33"/><path d="M384 627l-9 2 9 1.4z" fill="#f08a2c"/><circle cx="384" cy="643" r="1.2" fill="#141a33"/><circle cx="384" cy="650" r="1.2" fill="#141a33"/></g>
${star?'<g class="topstar"><circle cx="200" cy="24" r="26" fill="#ffd978" opacity=".5" filter="url(#soft)"/><path d="M200 4l5.6 12.6 13.7 1.4-10.2 9.2 2.9 13.4L200 33.700l-12 6.900 2.900-13.400-10.200-9.200 13.700-1.400z" fill="#ffe08a" stroke="#fff3c9" stroke-width="1"/></g>':""}
</svg>`;
}

function miniHouse(t){return`<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M8 44V22L24 9l16 13v22z" fill="${t.wall}"/><path d="M5 23L24 7l19 16" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/><rect x="12" y="25" width="9" height="11" rx="1" fill="#ffc869" stroke="${t.trim}" stroke-width="1.5"/><path d="M27 44V31a4.500 4.500 0 0 1 9 0v13z" fill="${t.sh}" stroke="${t.trim}" stroke-width="1.5"/></svg>`}

// Sky and snow share one animation loop.
const scene={wind:0,flakes:[],stars:[],last:0};
function moonPhase(d){let p=((d-Date.UTC(2000,0,6,18,14))/864e5/29.530588853)%1;if(p<0)p+=1;return Math.min(.9,Math.max(.1,p))}
function drawMoon(){
  let p=moonPhase(Date.now());const wane=p>.5;if(wane)p=1-p;
  const r=27,rx=(r*Math.abs(Math.cos(2*Math.PI*p))).toFixed(2);
  document.getElementById("moon").innerHTML=`<defs><radialGradient id="mg" cx=".4" cy=".4"><stop offset="0" stop-color="#fffbe8"/><stop offset="1" stop-color="#e9dfb8"/></radialGradient></defs><circle cx="32" cy="32" r="${r}" fill="#1c2750" opacity=".55"/><g transform="translate(32 32)${wane?" scale(-1 1)":""}"><path d="M0-${r}A${r} ${r} 0 0 1 0 ${r}A${rx} ${r} 0 0 ${p<.25?0:1} 0-${r}Z" fill="url(#mg)"/></g>`;
}
function startScene(){
  const sn=document.getElementById("snow"),sx=sn.getContext("2d");
  const st=document.getElementById("stars"),tx=st.getContext("2d");
  const au=document.getElementById("aurora"),ax=au.getContext("2d");au.width=96;au.height=60;
  let W=0,H=0,dpr=1;
  function size(){
    dpr=Math.min(devicePixelRatio||1,2);W=innerWidth;H=innerHeight;
    for(const c of[sn,st]){c.width=W*dpr;c.height=H*dpr}
    const n=Math.round(Math.min(W*H/5200,260));
    scene.stars=Array.from({length:n},()=>({x:Math.random()*W,y:Math.random()*H*.75,r:.4+Math.random()*1.1,p:Math.random()*6.3,s:.4+Math.random()*1.6}));
    const m=Math.round(Math.min(W*H/7000,170));
    scene.flakes=Array.from({length:m},()=>flake(true));
  }
  function flake(any){const z=Math.random();return{x:Math.random()*W,y:any?Math.random()*H:-8,z,r:.7+z*z*3.2,v:14+z*46,p:Math.random()*6.3}}
  function aurora(t){
    ax.clearRect(0,0,96,60);
    for(let x=0;x<96;x++){
      const y0=4+7*Math.sin(x*.09+t*.25)+4*Math.sin(x*.23-t*.17);
      const h=26+10*Math.sin(x*.05+t*.2+1);
      const a=Math.max(0,.42+.5*Math.sin(x*.17+t*.4)*Math.sin(x*.06-t*.22)+.18*Math.sin(x*.5+t));
      const g=ax.createLinearGradient(0,y0,0,y0+h);
      g.addColorStop(0,"rgba(150,90,255,0)");g.addColorStop(.45,`rgba(120,120,255,${a*.55})`);g.addColorStop(.86,`rgba(70,255,175,${a})`);g.addColorStop(1,"rgba(70,255,175,0)");
      ax.fillStyle=g;ax.fillRect(x,y0,1,h);
    }
  }
  function frame(ms){
    const t=ms/1000,dt=Math.min(.05,t-scene.last||.016);scene.last=t;
    tx.setTransform(dpr,0,0,dpr,0,0);tx.clearRect(0,0,W,H);tx.fillStyle="#fff";
    for(const s of scene.stars){tx.globalAlpha=(.3+.7*(.5+.5*Math.sin(t*s.s+s.p)))*(1-s.y/H*.7);tx.beginPath();tx.arc(s.x,s.y,s.r,0,6.3);tx.fill()}
    aurora(t);
    scene.wind*=Math.pow(.25,dt);
    sx.setTransform(dpr,0,0,dpr,0,0);sx.clearRect(0,0,W,H);sx.fillStyle="#fff";
    for(const f of scene.flakes){
      f.y+=f.v*dt;f.x+=(Math.sin(t*.8+f.p)*10+scene.wind*(.4+f.z))*dt;
      if(f.y>H+8)Object.assign(f,flake(false));
      if(f.x<-10)f.x=W+10;else if(f.x>W+10)f.x=-10;
      sx.globalAlpha=.35+f.z*.55;sx.beginPath();sx.arc(f.x,f.y,f.r,0,6.3);sx.fill();
    }
    if(!REDUCE)requestAnimationFrame(frame);
  }
  size();drawMoon();addEventListener("resize",size);
  requestAnimationFrame(frame);
  // A tap on the open sky sends a gust through the snow.
  addEventListener("pointerdown",e=>{if(!e.target.closest("button,a,input,textarea,.veil"))scene.wind+=(e.clientX<innerWidth/2?1:-1)*420});
  if(matchMedia("(hover:hover)").matches)addEventListener("pointermove",e=>{const dx=e.clientX/innerWidth-.5,dy=e.clientY/innerHeight-.5;document.querySelector(".sky").style.transform=`translate(${(-dx*14).toFixed(1)}px,${(-dy*8).toFixed(1)}px)`});
}

// Bells, synthesized so the page ships no audio files.
const sound={
  ctx:null,on:true,
  bell(f,at,vol){
    const c=this.ctx,out=c.createGain();out.gain.value=vol;out.connect(c.destination);
    [[1,1,2.4],[2.76,.32,1.3],[5.4,.14,.7],[.5,.25,2.8]].forEach(([m,a,d])=>{
      const o=c.createOscillator(),g=c.createGain();o.type="sine";o.frequency.value=f*m;
      g.gain.setValueAtTime(0,at);g.gain.linearRampToValueAtTime(a,at+.006);g.gain.exponentialRampToValueAtTime(.0001,at+d);
      o.connect(g);g.connect(out);o.start(at);o.stop(at+d+.05);
    });
  },
  play(notes,gap,vol){
    if(!this.on)return;
    try{this.ctx=this.ctx||new(window.AudioContext||window.webkitAudioContext)();if(this.ctx.state==="suspended")this.ctx.resume();const t=this.ctx.currentTime+.02;notes.forEach((n,i)=>this.bell(n,t+i*gap,vol))}catch(e){}
  },
  // Each day rings a little higher up a pentatonic scale; the 24th gets the full run.
  chime(day){
    const scale=[523.25,587.33,659.25,783.99,880,1046.5,1174.66,1318.5,1567.98,1760];
    if(day===24)return this.play([0,2,4,5,7,9,7,9].map(i=>scale[i]),.16,.2);
    const i=(day-1)%6;this.play([scale[i],scale[i+2],scale[i+4]],.13,.2);
  },
  tick(){this.play([1760],0,.05)},
  star(n){this.play([[659.25,783.99,880,1046.5,1318.5][n-1]],0,.14)}
};

// Frost over a card. Wipe it clear with a finger, or tap to let it melt.
function frost(card,day,done){
  const c=document.createElement("canvas");c.className="frost";c.setAttribute("aria-hidden","true");card.appendChild(c);
  const W=card.clientWidth,H=card.clientHeight,dpr=Math.min(devicePixelRatio||1,2);
  c.width=W*dpr;c.height=H*dpr;const x=c.getContext("2d");x.scale(dpr,dpr);
  const g=x.createLinearGradient(0,0,W,H);g.addColorStop(0,"#f7fcff");g.addColorStop(.5,"#d3e6f6");g.addColorStop(1,"#eff7fd");
  x.fillStyle=g;x.fillRect(0,0,W,H);
  x.font=`600 ${Math.min(W*.55,210)}px "Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif`;x.textAlign="center";x.textBaseline="middle";
  x.fillStyle="rgba(76,118,170,.3)";x.fillText(day,W/2,H/2);
  x.lineCap="round";
  function fern(px,py,a,len,depth){
    if(depth<0||len<5)return;const ex=px+Math.cos(a)*len,ey=py+Math.sin(a)*len;
    x.strokeStyle="rgba(120,160,205,.35)";x.lineWidth=depth+1.2;x.beginPath();x.moveTo(px+1,py+1);x.lineTo(ex+1,ey+1);x.stroke();
    x.strokeStyle="rgba(255,255,255,.95)";x.lineWidth=depth+.6;x.beginPath();x.moveTo(px,py);x.lineTo(ex,ey);x.stroke();
    for(let k=1;k<=4;k++){const u=k/5,bx=px+(ex-px)*u,by=py+(ey-py)*u;fern(bx,by,a+.9,len*.36*(1-u*.4),depth-1);fern(bx,by,a-.9,len*.36*(1-u*.4),depth-1)}
  }
  for(let i=0;i<22;i++){
    const side=i%4,px=side===0?0:side===1?W:Math.random()*W,py=side===2?0:side===3?H:Math.random()*H;
    fern(px,py,Math.atan2(H/2-py,W/2-px)+(Math.random()-.5)*1.1,50+Math.random()*90,2);
  }
  for(let i=0;i<1100;i++){x.fillStyle=`rgba(255,255,255,${Math.random()*.6})`;x.fillRect(Math.random()*W,Math.random()*H,1.3,1.3)}
  x.globalCompositeOperation="destination-out";
  const seen=new Set(),GX=9,GY=12;let gone=false,last=null,moved=0,ticks=0;
  function dab(px,py){
    const rad=40,rg=x.createRadialGradient(px,py,rad*.35,px,py,rad);rg.addColorStop(0,"rgba(0,0,0,1)");rg.addColorStop(1,"rgba(0,0,0,0)");
    x.fillStyle=rg;x.beginPath();x.arc(px,py,rad,0,6.3);x.fill();
    seen.add((px/W*GX|0)+","+(py/H*GY|0));
  }
  function stroke(px,py){
    if(last){const d=Math.hypot(px-last[0],py-last[1]),n=Math.max(1,d/12|0);for(let i=1;i<=n;i++)dab(last[0]+(px-last[0])*i/n,last[1]+(py-last[1])*i/n);moved+=d;if(moved>ticks*46){ticks++;sound.tick()}}else dab(px,py);
    last=[px,py];if(seen.size>GX*GY*.4)melt();
  }
  function melt(){if(gone)return;gone=true;c.classList.add("melt");setTimeout(()=>c.remove(),800);done()}
  const at=e=>{const b=c.getBoundingClientRect();return[e.clientX-b.left,e.clientY-b.top]};
  c.addEventListener("pointerdown",e=>{c.setPointerCapture(e.pointerId);last=null;moved=0;ticks=0;stroke(...at(e));e.preventDefault()});
  c.addEventListener("pointermove",e=>{if(e.buttons||e.pointerType==="touch")stroke(...at(e))});
  c.addEventListener("pointerup",()=>{if(moved<10)melt();last=null});
  // A first stroke draws itself, so the frost shows what to do.
  const t0=performance.now()+450;
  (function hint(now){if(gone||moved>0)return;const u=(now-t0)/650;if(u>=0&&u<=1){const e=u*u*(3-2*u);last=null;dab(W*(.16+.68*e),H*(.3+.12*Math.sin(e*3.1)))}if(u<1)requestAnimationFrame(hint);else last=null})(performance.now());
  return melt;
}
