from pathlib import Path
import re

root = Path('/home/ubuntu/retentio/client/src')

pages = root / 'pages/Pages.tsx'
text = pages.read_text()
text = text.replace("import { useState } from 'react';", "import { useEffect, useState } from 'react';")
text = text.replace("import { AnimatedHandsBackground, BackgroundVideo, GradientWaves } from '@/components/BackgroundSystems';", "import { BackgroundVideo, GradientWaves, NeuralPortalBackground } from '@/components/BackgroundSystems';")

landing = '''export function Landing(){
  const [,setLocation]=useLocation();
  return <main className="landing neural-portal-landing">
    <NeuralPortalBackground/>
    <div className="landing-top portal-top"><BrandMark/><span className="portal-status"><span className="status-pip"/> dimension online</span></div>
    <section className="portal-stage" aria-label="Retentio neural portal">
      <div className="portal-copy-panel">
        <p className="eyebrow portal-eyebrow">Retention intelligence / open the signal</p>
        <h1 className="portal-headline">Welcome to <span>Retentio.</span></h1>
        <p className="portal-subcopy">See the quiet signals behind customer behavior before they become churn.</p>
      </div>
      <button className="portal-cta" onClick={()=>setLocation('/signup')}>Get started <ArrowRight size={16}/></button>
    </section>
    <div className="portal-footer"><span>neural dimension / 001</span><span>move your cursor to reveal</span></div>
  </main>
}'''
text = re.sub(r"export function Landing\(\)\{[\s\S]*?\n\}\nexport function PublicLayout", landing + "\nexport function PublicLayout", text, count=1)

public_layout = '''export function PublicLayout({ children, dimmed=false }: { children:React.ReactNode; dimmed?:boolean }) { return <main className="public-layout"><BackgroundVideo dimmed={dimmed}/><div className="public-top"><BrandMark/><Link href="/">Back to home</Link></div>{children}</main> }'''
text = re.sub(r"export function PublicLayout\([\s\S]*?\nexport function SignUp", public_layout + "\nexport function SignUp", text, count=1)

signup = '''export function SignUp(){
  const {signup}=useAuth(); const [,setLocation]=useLocation(); const [form,setForm]=useState({businessName:'',name:'',email:'',password:'',confirm:''}); const [error,setError]=useState('');
  const description='Retentio reads the small changes in customer behavior that usually arrive before churn. Upload your data, find the accounts that need a conversation, and act while the signal is still quiet.';
  const [typed,setTyped]=useState('');
  useEffect(()=>{ let index=0; let timeout:number|undefined; const type=()=>{ if(index<=description.length){setTyped(description.slice(0,index)); index+=1; timeout=window.setTimeout(type,index===description.length+1?1600:30); } else {index=0; timeout=window.setTimeout(type,700);} }; type(); return()=>{if(timeout) window.clearTimeout(timeout)} },[]);
  const submit=async(e:React.FormEvent)=>{e.preventDefault(); if(!form.businessName||!form.name||!form.email||form.password.length<8||form.password!==form.confirm){setError('Add your details and make sure both passwords match (8+ characters).'); return;} await signup(form); setLocation('/predict');};
  return <div className="auth-grid signup-grid">
    <GlassCard className="auth-card signup-form-card"><p className="eyebrow">Create your observatory</p><h1>Keep the right customers close.</h1><p className="auth-intro">Retentio turns a simple customer export into a prioritized retention plan.</p><form onSubmit={submit}>{[['businessName','Business name'],['name','Full name'],['email','Work email'],['password','Password'],['confirm','Confirm password']].map(([key,label])=><label className="form-label" key={key}>{label}<input required type={key.includes('password')||key==='confirm'?'password':key==='email'?'email':'text'} value={form[key as keyof typeof form]} onChange={e=>setForm({...form,[key]:e.target.value})}/></label>)}{error&&<p className="form-error">{error}</p>}<button className="primary-button wide" type="submit">Create account <ArrowRight size={16}/></button></form><p className="switch-copy">Already have an account? <Link href="/login">Log in</Link></p></GlassCard>
    <GlassCard className="companion-card"><p className="eyebrow light">Retentio / live brief</p><h2>Your Retention Journey Starts Here</h2><div className="typewriter-copy"><span>{typed}</span><i aria-hidden="true"/></div><div className="companion-orbit"><span/><span/><span/></div></GlassCard>
  </div>
}'''
text = re.sub(r"export function SignUp\(\)\{[\s\S]*?\n\}\nconst facts", signup + "\nconst facts", text, count=1)

pages.write_text(text)

app = root / 'App.tsx'
app_text = app.read_text()
app_text = app_text.replace('<Route path="/signup"><PublicLayout><SignUp/></PublicLayout></Route><Route path="/login"><PublicLayout><Login/></PublicLayout></Route>', '<Route path="/signup"><PublicLayout><SignUp/></PublicLayout></Route><Route path="/login"><PublicLayout dimmed><Login/></PublicLayout></Route>')
app.write_text(app_text)

bg = root / 'components/BackgroundSystems.tsx'
bg_text = bg.read_text()
bg_text = bg_text.replace("export function BackgroundVideo() { return <div aria-hidden=\"true\" className=\"background-video\" style={{ backgroundImage: 'url(\"'+authAmbient+'\")' }}><div className=\"video-vignette\" /></div>; }", "export function BackgroundVideo({ dimmed=false }: { dimmed?: boolean }) { return <div aria-hidden=\"true\" className={dimmed ? 'background-video login-dim' : 'background-video'} style={{ backgroundImage: 'url(\"'+authAmbient+'\")' }}><div className=\"video-vignette\" /></div>; }")

portal = r'''\nconst neuralBrain = '/manus-storage/retentio-neural-brain_ccc27b5f.png';\n\nexport function NeuralPortalBackground(){\n  const canvasRef=useRef<HTMLCanvasElement>(null);\n  const sceneRef=useRef<HTMLDivElement>(null);\n  useEffect(()=>{\n    const canvas=canvasRef.current; const scene=sceneRef.current; if(!canvas||!scene) return; const ctx=canvas.getContext('2d'); if(!ctx) return;\n    let raf=0; let visible=true; const target={x:innerWidth*.5,y:innerHeight*.47}; const current={x:target.x,y:target.y};\n    const stars=Array.from({length:210},(_,i)=>({x:(i*83.17)%1,y:(i*47.31)%1,r:i%13===0?1.35:i%5===0?.9:.42,a:.22+(i%7)*.06,s:.12+(i%5)*.05}));\n    const resize=()=>{const dpr=Math.min(devicePixelRatio||1,2);canvas.width=innerWidth*dpr;canvas.height=innerHeight*dpr;canvas.style.width=innerWidth+'px';canvas.style.height=innerHeight+'px';ctx.setTransform(dpr,0,0,dpr,0,0)};\n    const move=(event:PointerEvent)=>{target.x=event.clientX;target.y=event.clientY;scene.style.setProperty('--portal-x',event.clientX+'px');scene.style.setProperty('--portal-y',event.clientY+'px');scene.style.setProperty('--portal-tilt',((event.clientX/innerWidth)-.5)*5+'deg')};\n    const visibility=()=>{visible=document.visibilityState==='visible'};\n    addEventListener('resize',resize); addEventListener('pointermove',move); document.addEventListener('visibilitychange',visibility); resize(); scene.style.setProperty('--portal-x',target.x+'px'); scene.style.setProperty('--portal-y',target.y+'px');\n    const frame=(ms:number)=>{if(visible){const t=ms/1000; const w=innerWidth,h=innerHeight; current.x+=(target.x-current.x)*.065; current.y+=(target.y-current.y)*.065; scene.style.setProperty('--portal-eased-x',current.x+'px'); scene.style.setProperty('--portal-eased-y',current.y+'px'); ctx.clearRect(0,0,w,h); ctx.fillStyle='#040713'; ctx.fillRect(0,0,w,h); const haze=ctx.createRadialGradient(w*.72,h*.38,0,w*.72,h*.38,w*.55); haze.addColorStop(0,'rgba(13,74,120,.18)'); haze.addColorStop(1,'rgba(1,4,15,0)'); ctx.fillStyle=haze; ctx.fillRect(0,0,w,h); stars.forEach((star,index)=>{const x=(star.x*w+(t*star.s*4+index*11))%w; const y=(star.y*h+Math.sin(t*.16+index)*2.5+h)%h; const pulse=star.a*(.68+.32*Math.sin(t*(.4+star.s)+index)); ctx.fillStyle='rgba(180,240,255,'+pulse+')'; ctx.beginPath(); ctx.arc(x,y,star.r,0,Math.PI*2); ctx.fill()}); const dust=ctx.createRadialGradient(w*.38,h*.63,0,w*.38,h*.63,w*.23); dust.addColorStop(0,'rgba(64,184,255,.1)'); dust.addColorStop(1,'rgba(64,184,255,0)'); ctx.fillStyle=dust; ctx.fillRect(0,0,w,h)} raf=requestAnimationFrame(frame)}; raf=requestAnimationFrame(frame);\n    return()=>{cancelAnimationFrame(raf);removeEventListener('resize',resize);removeEventListener('pointermove',move);document.removeEventListener('visibilitychange',visibility)}\n  },[]);\n  return <div ref={sceneRef} className="neural-portal-scene" aria-hidden="true"><canvas ref={canvasRef} className="neural-space-canvas"/><div className="neural-portal-lens"><svg className="portal-ribbon-svg" viewBox="0 0 620 620" preserveAspectRatio="none"><defs><clipPath id="neural-portal-clip"><path d="M328 36 C405 26 506 60 548 126 C584 184 530 222 555 292 C585 372 526 472 439 507 C365 537 304 584 224 552 C142 519 104 436 132 360 C154 300 107 245 143 176 C176 112 241 48 328 36 Z"/></clipPath><filter id="portal-glow"><feGaussianBlur stdDeviation="7"/></filter></defs><image href={neuralBrain} x="50" y="38" width="520" height="520" preserveAspectRatio="xMidYMid meet" clipPath="url(#neural-portal-clip)" className="portal-brain-image"/><path d="M328 36 C405 26 506 60 548 126 C584 184 530 222 555 292 C585 372 526 472 439 507 C365 537 304 584 224 552 C142 519 104 436 132 360 C154 300 107 245 143 176 C176 112 241 48 328 36 Z" className="portal-ribbon-halo"/><path d="M328 36 C405 26 506 60 548 126 C584 184 530 222 555 292 C585 372 526 472 439 507 C365 537 304 584 224 552 C142 519 104 436 132 360 C154 300 107 245 143 176 C176 112 241 48 328 36 Z" className="portal-ribbon-edge"/><path d="M338 52 C412 43 493 75 529 130 C556 173 510 224 536 292 C560 354 507 444 432 478 C360 511 304 551 239 525 C175 500 139 431 160 365 C180 304 139 254 166 193 C192 133 258 61 338 52 Z" className="portal-ribbon-edge portal-ribbon-edge-secondary"/></svg></div><div className="portal-cursor-halo"/></div>\n}\n'''
bg_text = re.sub(r"\nexport function AnimatedHandsBackground", portal + "\nexport function AnimatedHandsBackground", bg_text, count=1)
bg.write_text(bg_text)
''
