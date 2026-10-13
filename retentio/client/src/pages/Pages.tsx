/** Signal in the Dark: page compositions keep evidence close to the decision. */
import { useEffect, useState, useMemo, type ReactNode, type FormEvent } from 'react'; 
import { motion, AnimatePresence } from 'framer-motion'; 
import { ArrowRight, Check, Database, Download, LockKeyhole, Menu, Plus, Save, Sparkles, TrendingDown, TrendingUp } from 'lucide-react'; 
import { Link, useLocation } from 'wouter'; 
import { BackgroundVideo, GradientWaves, NeuralPortalBackground } from '@/components/BackgroundSystems'; 
import { BrandMark, DataTable, Dock, GlassCard, MiniChart, PageHeader, ProfileMenu, SearchField, StatusBadge, SummaryCard, UploadDropzone } from '@/components/AppUI'; 
import { useAuth } from '@/contexts/AuthContext';
import { dashboardApi, predictApi, customersApi, settingsApi } from '@/lib/api';
import type { CustomerRow, PredictResponse, DashboardSummary, DashboardTrend, CustomerDetail } from '@/lib/types';

export function Landing(){
  const [,setLocation]=useLocation();
  return <main className="landing neural-portal-landing">
    <NeuralPortalBackground/>
    <div className="landing-top portal-top"><BrandMark/></div>
    <section className="portal-stage" aria-label="Retentio neural portal">
      <div className="portal-copy-panel">
        <p className="eyebrow portal-eyebrow">Retention intelligence / open the signal</p>
        <h1 className="portal-headline">Welcome to <span>Retentio.</span></h1>
        <p className="portal-subcopy">See the quiet signals behind customer behavior before they become churn.</p>
      </div>
      <button className="portal-cta" onClick={()=>setLocation('/signup')}>Get started <ArrowRight size={16}/></button>
    </section>
  </main>
}

export function PublicLayout({ children, dimmed=false }: { children:ReactNode; dimmed?:boolean }) { 
  return <main className="public-layout"><BackgroundVideo dimmed={dimmed}/><div className="public-top"><BrandMark/><Link href="/">Back to home</Link></div>{children}</main> 
}

export function SignUp(){
  const {signup}=useAuth(); const [,setLocation]=useLocation(); const [form,setForm]=useState({businessName:'',name:'',email:'',password:'',confirm:''}); const [error,setError]=useState('');
  const description='Retentio reads the small changes in customer behavior that usually arrive before churn. Upload your data, find the accounts that need a conversation, and act while the signal is still quiet.';
  const [typed,setTyped]=useState('');
  useEffect(()=>{ let index=0; let timeout:number|undefined; const type=()=>{ if(index<=description.length){setTyped(description.slice(0,index)); index+=1; timeout=window.setTimeout(type,index===description.length+1?1600:30); } else {index=0; timeout=window.setTimeout(type,700);} }; type(); return()=>{if(timeout) window.clearTimeout(timeout)} },[]);
  const submit=async(e:FormEvent)=>{e.preventDefault(); if(!form.businessName||!form.name||!form.email||form.password.length<8||form.password!==form.confirm){setError('Add your details and make sure both passwords match (8+ characters).'); return;} try { await signup(form); setLocation('/predict'); } catch(err:any) { setError(err.message); }};
  return <div className="auth-grid signup-grid">
    <GlassCard className="auth-card signup-form-card"><p className="eyebrow">Create your observatory</p><h1>Keep the right customers close.</h1><p className="auth-intro">Retentio turns a simple customer export into a prioritized retention plan.</p><form onSubmit={submit}>{[['businessName','Business name'],['name','Full name'],['email','Work email'],['password','Password'],['confirm','Confirm password']].map(([key,label])=><label className="form-label" key={key}>{label}<input required type={key.includes('password')||key==='confirm'?'password':key==='email'?'email':'text'} value={form[key as keyof typeof form]} onChange={e=>setForm({...form,[key]:e.target.value})}/></label>)}{error&&<p className="form-error">{error}</p>}<button className="primary-button wide" type="submit">Create account <ArrowRight size={16}/></button></form><p className="switch-copy">Already have an account? <Link href="/login">Log in</Link></p></GlassCard>
    <GlassCard className="companion-card"><p className="eyebrow light">Retentio / live signal</p><h2>Your Retention Journey Starts Here</h2><div className="typewriter-copy"><span>{typed}</span><i aria-hidden="true"/></div><div className="companion-orbit"><span/><span/><span/></div></GlassCard>
  </div>
}

const facts=['A 5% lift in retention can increase profits by 25–95%.','Churn is often preceded by a small drop in usage, not a single dramatic event.','The best retention moment is usually before a customer says they are unhappy.','A clear benchmark turns a score into a decision.','Saved customers are proof that your follow-up changed the trajectory.','Customer history makes the next upload more useful than the last.','Small teams can act faster when the priority queue is visible.','Retention work compounds: one saved account can change a quarter.'];

export function Login(){ 
  const {login}=useAuth(); const [,setLocation]=useLocation(); const [email,setEmail]=useState('maya@northstar.co'); const [password,setPassword]=useState('retentio123'); const [fact,setFact]=useState(0); const [loading,setLoading]=useState(false); const [error,setError]=useState('');
  const submit=async(e:FormEvent)=>{e.preventDefault();setLoading(true);setError(''); try { await login(email,password); setLocation('/dashboard'); } catch (err:any) { setError(err.message); setLoading(false); } }; 
  return <div className="auth-grid login-grid"><GlassCard className="auth-card"><p className="eyebrow">Welcome back</p><h1>Resume the signal.</h1><p className="auth-intro">Your latest view of customer health is waiting.</p><form onSubmit={submit}><label className="form-label">Work email<input required type="email" value={email} onChange={e=>setEmail(e.target.value)}/></label><label className="form-label">Password<input required type="password" value={password} onChange={e=>setPassword(e.target.value)}/></label>{error&&<p className="form-error">{error}</p>}<button className="primary-button wide" disabled={loading}>{loading?'Reading your workspace…':<>Enter workspace <ArrowRight size={16}/></>}</button></form><p className="switch-copy">New to Retentio? <Link href="/signup">Create an account</Link></p></GlassCard><GlassCard className="fact-card"><div className="fact-top"><Sparkles size={18}/><span>Did you know?</span><span className="fact-count">0{fact+1} / 08</span></div><AnimatePresence mode="wait"><motion.p key={fact} initial={{opacity:0,y:10}} animate={{opacity:1,y:0}} exit={{opacity:0,y:-10}}>{facts[fact]}</motion.p></AnimatePresence><button className="text-button" onClick={()=>setFact((fact+1)%facts.length)}>Next insight <ArrowRight size={15}/></button></GlassCard></div> 
}

export function AuthenticatedLayout({ children }: {children:ReactNode}) { 
  return <main className="app-layout"><GradientWaves/><div className="app-shell"><div className="app-top"><BrandMark small/><ProfileMenu/></div>{children}</div><Dock/></main> 
}

export function Dashboard(){ 
  const {user}=useAuth();
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [trend, setTrend] = useState<DashboardTrend | null>(null);
  const [atRisk, setAtRisk] = useState<CustomerRow[]>([]);
  const [saved, setSaved] = useState<CustomerRow[]>([]);

  useEffect(() => {
    dashboardApi.summary().then(setSummary).catch(console.error);
    dashboardApi.trend().then(setTrend).catch(console.error);
    customersApi.atRisk().then(setAtRisk).catch(console.error);
    customersApi.saved().then(setSaved).catch(console.error);
  }, []);

  return <><PageHeader eyebrow="Workspace / overview" title="Make the next conversation count." description="A calm view of the customers who need your attention, before the signal becomes a goodbye." action={<button className="secondary-button"><Download size={15}/> Export report</button>}/>
  <div className="summary-grid">
    <SummaryCard label="Total customers" value={summary?.total_customers || 0} note="Total in system" tone="mint"/>
    <SummaryCard label="At risk" value={summary?.at_risk_count || 0} note="Requires attention" tone="risk"/>
    <SummaryCard label="Saved" value={summary?.saved_count || 0} note="Successfully retained" tone="saved"/>
    <SummaryCard label="Avg. risk score" value={summary?.avg_score?.toFixed(1) || '0'} note={`Benchmark set at ${user?.benchmark || 78}`} tone="blue"/>
  </div>
  <div className="dashboard-grid">
    <GlassCard className="chart-card">
      <div className="table-heading"><div><p className="eyebrow">Risk distribution</p><h2>Current customer health</h2></div><span className="chart-period">Overview</span></div>
      <div className="donut-wrap">
        <div className="donut"><div><strong>{summary?.avg_score?.toFixed(1) || '0'}</strong><span>avg score</span></div></div>
        <div className="legend">
          <span><i className="dot red"/> At risk <b>{summary?.at_risk_count || 0}</b></span>
          <span><i className="dot mint"/> Healthy <b>{Math.max(0, (summary?.total_customers || 0) - (summary?.at_risk_count || 0))}</b></span>
        </div>
      </div>
    </GlassCard>
    <GlassCard className="trend-card">
      <div className="table-heading"><div><p className="eyebrow">Retention movement</p><h2>Risk score trend</h2></div><TrendingDown className="trend-icon" size={20}/></div>
      <MiniChart points={trend?.points || []}/>
      <div className="chart-foot">
        <span>Average risk history</span>
      </div>
    </GlassCard>
  </div>
  <div className="dashboard-grid lower">
    <DataTable rows={atRisk}/>
    <DataTable rows={saved} saved/>
  </div></> 
}

export function Predict(){ 
  const {user}=useAuth();
  const [result,setResult]=useState<PredictResponse|null>(null); 
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const handleUpload = async (file: File) => {
    setLoading(true);
    setError('');
    try {
      const res = await predictApi.upload(file);
      setResult(res);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return <><PageHeader eyebrow="Workspace / predict" title="Turn a customer export into a plan." description="Upload recent data and Retentio will organize the signal by urgency." action={<a href={predictApi.templateUrl()} className="secondary-button" download><Download size={15}/> CSV template</a>}/>
  <UploadDropzone onUpload={handleUpload} isLoading={loading}/>
  {error && <p className="form-error" style={{marginTop: '1rem'}}>{error}</p>}
  {result&&<motion.div initial={{opacity:0,y:12}} animate={{opacity:1,y:0}} className="predict-results">
    <div className="result-banner">
      <div><span className="eyebrow">Ready to score</span><h2>{result.total_rows} rows processed.</h2><p>Calculated and classified customers against a benchmark of {user?.benchmark || 78}.</p></div>
    </div>
    <div className="dashboard-grid">
      <DataTable rows={result.at_risk}/>
      <DataTable rows={result.saved} saved/>
    </div>
  </motion.div>} 
  {!result&&!loading&&<div className="empty-state"><div className="empty-mark"><Plus size={20}/></div><h2>Your next signal starts with a CSV.</h2><p>When you upload, the results will appear here with clear at-risk and saved queues.</p></div>}</> 
}

export function Customers(){ 
  const [query,setQuery]=useState(''); 
  const [rows, setRows] = useState<CustomerRow[]>([]);
  const [detail, setDetail] = useState<CustomerDetail | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      customersApi.search(query).then(setRows).catch(console.error);
    }, 300);
    return () => clearTimeout(timer);
  }, [query]);

  const loadDetail = async (id: string) => {
    setLoadingDetail(true);
    try {
      const data = await customersApi.detail(id);
      setDetail(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingDetail(false);
    }
  };

  return <><PageHeader eyebrow="Workspace / customers" title="Stay close to the context." description="Search a customer to see the score, the history, and what changed."/>
  <div className="customer-toolbar"><SearchField value={query} onChange={setQuery}/><span>{rows.length} matching customers</span></div>
  <div className="customers-grid">
    <GlassCard className="table-card">
      <div className="table-heading"><div><p className="eyebrow">Search Results</p><h2>Customers</h2></div></div>
      <div className="data-table">
        <div className="table-row table-head"><span>Customer</span><span>Risk score</span><span>Status</span></div>
        {rows.map(row=>
          <div className="table-row" key={row.customer_id} onClick={() => loadDetail(row.customer_id)} style={{cursor: 'pointer'}}>
            <span><b>{row.name}</b><small>{row.customer_id} {row.meta ? `· ${row.meta}` : ''}</small></span>
            <span className="score-value">{row.score.toFixed(1)}</span>
            <StatusBadge status={row.status}/>
          </div>
        )}
      </div>
    </GlassCard>
    <GlassCard className="detail-card">
      <p className="eyebrow">Customer detail</p>
      {loadingDetail ? <p>Loading...</p> : detail ? (
        <div className="detail-content">
          <h2>{detail.name}</h2>
          <p>{detail.customer_id}</p>
          <div style={{marginTop: '1rem', display: 'flex', gap: '1rem', alignItems: 'center'}}>
            <StatusBadge status={detail.status}/>
            <strong style={{fontSize: '1.5rem'}}>{detail.current_score.toFixed(1)}</strong>
          </div>
          <h3 style={{marginTop: '2rem', marginBottom: '1rem'}}>History</h3>
          <div className="history-list">
            {detail.history.map((h, i) => (
              <div key={i} style={{display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid rgba(255,255,255,0.1)'}}>
                <span style={{color: 'rgba(255,255,255,0.5)'}}>{h.date}</span>
                <strong>{h.score.toFixed(1)}</strong>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="detail-empty">
          <Database size={24}/>
          <h2>Select a customer</h2>
          <p>Choose a row from the priority queue to inspect their score history and status changes.</p>
        </div>
      )}
    </GlassCard>
  </div></> 
}

export function Settings(){ 
  const {user, setUser}=useAuth(); 
  const [benchmark,setBenchmark]=useState(user?.benchmark||78); 
  const [profile, setProfile] = useState({ name: user?.name || '', business_name: user?.business_name || '' });
  const [savedState,setSavedState]=useState(false); 
  const [saving, setSaving] = useState(false);

  const saveBenchmark = async () => {
    setSaving(true);
    try {
      const updatedUser = await settingsApi.updateBenchmark(benchmark);
      setUser(updatedUser);
      setSavedState(true);
      setTimeout(() => setSavedState(false), 2000);
    } catch (e) {
      console.error(e);
    } finally {
      setSaving(false);
    }
  };

  const saveProfile = async () => {
    try {
      const updatedUser = await settingsApi.updateProfile(profile);
      setUser(updatedUser);
    } catch(e) {
      console.error(e);
    }
  };

  return <><PageHeader eyebrow="Workspace / settings" title="Tune the signal to your business." description="Set the benchmark and workspace details that shape every retention queue."/>
  <div className="settings-grid">
    <GlassCard>
      <p className="eyebrow">Workspace profile</p>
      <h2>Who is reading the signal?</h2>
      <div className="settings-form">
        <label className="form-label">Business name
          <input value={profile.business_name} onChange={e => setProfile({...profile, business_name: e.target.value})} onBlur={saveProfile}/>
        </label>
        <label className="form-label">Your name
          <input value={profile.name} onChange={e => setProfile({...profile, name: e.target.value})} onBlur={saveProfile}/>
        </label>
        <label className="form-label">Email
          <input disabled value={user?.email}/>
        </label>
      </div>
    </GlassCard>
    <GlassCard>
      <p className="eyebrow">Signal note / field guide</p>
      <h2>When should we raise a flag?</h2>
      <p className="settings-copy">Customers at or above this score appear in your priority queue.</p>
      <div className="benchmark-value"><strong>{benchmark}</strong><span>/ 100</span></div>
      <input className="range" type="range" min="70" max="90" value={benchmark} onChange={e=>setBenchmark(Number(e.target.value))}/>
      <div className="range-labels"><span>70 · focused</span><span>90 · selective</span></div>
      <button className="primary-button" onClick={saveBenchmark} disabled={saving}><Save size={15}/> {savedState?'Saved':'Save benchmark'}</button>
    </GlassCard>
  </div></> 
}

export function NotFound(){ 
  return <div className="not-found"><p className="eyebrow">404 / signal lost</p><h1>This route drifted off course.</h1><Link href="/" className="primary-button">Return home <ArrowRight size={16}/></Link></div> 
}
