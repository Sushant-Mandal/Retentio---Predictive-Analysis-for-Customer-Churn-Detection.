from pathlib import Path
import re

pages = Path('/home/ubuntu/retentio/client/src/pages/Pages.tsx')
text = pages.read_text()
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
start = text.index('export function Landing')
end = text.index('export function PublicLayout', start)
text = text[:start] + landing + '\n' + text[end:]

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
start = text.index('export function SignUp')
end = text.index('const facts', start)
text = text[:start] + signup + '\n' + text[end:]
pages.write_text(text)
