from pathlib import Path
import re

path = Path('/home/ubuntu/retentio/client/src/components/BackgroundSystems.tsx')
text = path.read_text()
start = text.index('export function NeuralPortalBackground')
end = text.index('export function AnimatedHandsBackground', start)
replacement = r'''export function NeuralPortalBackground(){
  const sceneRef=useRef<HTMLDivElement>(null);
  useEffect(()=>{
    const scene=sceneRef.current; if(!scene) return;
    let raf=0; let visible=true; const target={x:innerWidth*.68,y:innerHeight*.43}; const current={x:target.x,y:target.y};
    const stars=Array.from({length:220},(_,i)=>({x:(i*83.17)%1,y:(i*47.31)%1,r:i%13===0?1.35:i%5===0?.9:.42,a:.2+(i%7)*.055,s:.12+(i%5)*.05}));
    const canvas=document.createElement('canvas'); const ctx=canvas.getContext('2d'); if(!ctx) return;
    canvas.className='neural-space-canvas'; scene.prepend(canvas);
    const resize=()=>{const dpr=Math.min(devicePixelRatio||1,2); canvas.width=innerWidth*dpr;canvas.height=innerHeight*dpr;canvas.style.width=innerWidth+'px';canvas.style.height=innerHeight+'px';ctx.setTransform(dpr,0,0,dpr,0,0)};
    const move=(event:PointerEvent)=>{target.x=event.clientX;target.y=event.clientY; scene.style.setProperty('--portal-x',event.clientX+'px');scene.style.setProperty('--portal-y',event.clientY+'px');scene.style.setProperty('--portal-tilt',((event.clientX/innerWidth)-.5)*5+'deg')};
    const key=(event:KeyboardEvent)=>{if(event.key==='Tab'||event.key==='Enter'){target.x=innerWidth*.68;target.y=innerHeight*.43;scene.classList.add('portal-keyboard-focus')}else if(event.key==='Escape'){scene.classList.remove('portal-keyboard-focus')}};
    const visibility=()=>{visible=document.visibilityState==='visible'};
    addEventListener('resize',resize);addEventListener('pointermove',move);addEventListener('keydown',key);document.addEventListener('visibilitychange',visibility);resize();scene.style.setProperty('--portal-x',target.x+'px');scene.style.setProperty('--portal-y',target.y+'px');
    const frame=(ms:number)=>{if(visible){const t=ms/1000;const w=innerWidth,h=innerHeight;current.x+=(target.x-current.x)*.065;current.y+=(target.y-current.y)*.065;scene.style.setProperty('--portal-eased-x',current.x+'px');scene.style.setProperty('--portal-eased-y',current.y+'px');ctx.clearRect(0,0,w,h);ctx.fillStyle='#040713';ctx.fillRect(0,0,w,h);const haze=ctx.createRadialGradient(w*.72,h*.38,0,w*.72,h*.38,w*.55);haze.addColorStop(0,'rgba(13,74,120,.18)');haze.addColorStop(1,'rgba(1,4,15,0)');ctx.fillStyle=haze;ctx.fillRect(0,0,w,h);stars.forEach((star,index)=>{const x=(star.x*w+(t*star.s*4+index*11))%w;const y=(star.y*h+Math.sin(t*.16+index)*2.5+h)%h;const pulse=star.a*(.68+.32*Math.sin(t*(.4+star.s)+index));ctx.fillStyle='rgba(180,240,255,'+pulse+')';ctx.beginPath();ctx.arc(x,y,star.r,0,Math.PI*2);ctx.fill()})}raf=requestAnimationFrame(frame)};raf=requestAnimationFrame(frame);
    return()=>{cancelAnimationFrame(raf);removeEventListener('resize',resize);removeEventListener('pointermove',move);removeEventListener('keydown',key);document.removeEventListener('visibilitychange',visibility);canvas.remove()}
  },[]);
  return <div ref={sceneRef} className="neural-portal-scene" aria-hidden="true">
    <div className="hidden-neural-scene"><div className="portal-window"><div className="fixed-neural-world"><img src={neuralBrain} className="fixed-brain-image"/><div className="thought-bubble thought-a">“Am I even using this enough to justify the cost?”</div><div className="thought-bubble thought-b">“Their competitor just launched a cheaper plan...”</div><div className="thought-bubble thought-c">“I haven’t heard from them since I signed up.”</div><div className="thought-bubble thought-d">“This feature I need still isn’t here.”</div><div className="thought-bubble thought-e">“Support took 3 days to reply last time.”</div><div className="thought-bubble thought-f">“Do I still need this tool?”</div></div></div></div>
    <div className="portal-ribbon-layer"><svg className="portal-ribbon-svg" viewBox="0 0 560 560" preserveAspectRatio="none"><defs><linearGradient id="portal-gradient" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stopColor="#5CF6FF"/><stop offset="45%" stopColor="#4F9CFF"/><stop offset="100%" stopColor="#6A6CFF"/></linearGradient><filter id="portal-glow"><feGaussianBlur stdDeviation="7"/></filter></defs><path d="M292 25 C368 17 467 47 505 111 C540 170 489 211 514 276 C543 350 484 456 393 487 C317 513 267 552 188 520 C108 488 83 409 107 342 C132 274 81 226 118 151 C150 86 211 34 292 25 Z" className="portal-ribbon-halo"/><path d="M292 25 C368 17 467 47 505 111 C540 170 489 211 514 276 C543 350 484 456 393 487 C317 513 267 552 188 520 C108 488 83 409 107 342 C132 274 81 226 118 151 C150 86 211 34 292 25 Z" className="portal-ribbon-edge"/><path d="M299 43 C367 36 447 62 480 116 C506 163 466 210 490 274 C514 336 463 426 386 454 C314 480 270 518 204 491 C143 466 114 399 137 344 C158 284 119 233 145 169 C170 109 227 50 299 43 Z" className="portal-ribbon-edge portal-ribbon-edge-secondary"/></svg></div><div className="portal-cursor-halo"/>
  </div>
}

'''
path.write_text(text[:start] + replacement + text[end:])
