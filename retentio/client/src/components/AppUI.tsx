/** Signal in the Dark: reusable instrument-console primitives for all product surfaces. */
import { motion } from 'framer-motion'; 
import { Activity, BarChart3, ChevronRight, CircleUserRound, Database, Gauge, LogOut, Search, Settings2, UploadCloud } from 'lucide-react'; 
import { Link, useLocation } from 'wouter'; 
import { useAuth } from '@/contexts/AuthContext';
import { useRef, type ReactNode } from 'react';
import type { CustomerRow, TrendPoint } from '@/lib/types';

export function GlassCard({ children, className='' }: { children: ReactNode; className?: string }) { 
  return <div className={`glass-panel ${className}`}>{children}</div>; 
}

export function StatusBadge({ status }: { status: 'At Risk' | 'Saved' | string }) { 
  return <span className={status === 'At Risk' ? 'status-badge risk' : 'status-badge saved'}>{status}</span>; 
}

export function BrandMark({ small=false }: { small?: boolean }) { 
  return <Link href="/" className="brand-mark"><img src="/retentio_logo.png" alt="Retentio" className={small ? 'h-7 w-7' : 'h-9 w-9'} onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }} /><span>RETENTIO</span></Link>; 
}

const nav = [
  { href:'/dashboard', label:'Overview', icon:Gauge }, 
  { href:'/predict', label:'Predict', icon:Activity }, 
  { href:'/customers', label:'Customers', icon:Database }, 
  { href:'/settings', label:'Settings', icon:Settings2 }
];

export function Dock() { 
  const [location] = useLocation(); 
  return <nav className="dock" aria-label="Primary navigation">{nav.map(({href,label,icon:Icon}) => <Link key={href} href={href} className={location===href ? 'dock-item active' : 'dock-item'}><Icon size={18}/><span>{label}</span></Link>)}</nav>; 
}

export function ProfileMenu() { 
  const { user, logout } = useAuth(); 
  const [, setLocation] = useLocation(); 
  return <div className="profile-menu"><div className="profile-avatar"><CircleUserRound size={18}/></div><div className="profile-copy"><span>{user?.name || 'Workspace'}</span><small>{user?.business_name || 'Retentio demo'}</small></div><button aria-label="Log out" onClick={() => { logout(); setLocation('/'); }}><LogOut size={16}/></button></div>; 
}

export function PageHeader({ eyebrow, title, description, action }: { eyebrow:string; title:string; description:string; action?: ReactNode }) { 
  return <header className="page-header"><div><p className="eyebrow">{eyebrow}</p><h1>{title}</h1><p className="page-description">{description}</p></div>{action}</header>; 
}

export function SummaryCard({ label, value, note, tone='neutral' }: { label:string; value:string | number; note:string; tone?:string }) { 
  return <motion.div initial={{opacity:0,y:12}} animate={{opacity:1,y:0}} className={`summary-card tone-${tone}`}><div className="summary-label">{label}</div><strong>{value}</strong><span>{note}</span></motion.div>; 
}

export function MiniChart({ bars=false, points=[] }: { bars?:boolean; points?: TrendPoint[] }) { 
  if (points.length > 0) {
    const maxScore = Math.max(...points.map(p => p.avg_score), 1);
    return <div className={bars ? 'mini-chart bars' : 'mini-chart'}>{points.map((p, i) => <span key={i} style={{ height: `${(p.avg_score / maxScore) * 100}%` }} title={p.date} />)}</div>;
  }
  return <div className={bars ? 'mini-chart bars' : 'mini-chart'}>{Array.from({length: bars ? 12 : 28}, (_,i) => <span key={i} style={{ height: `${bars ? 24+(i*17)%60 : 20+(i*13)%70}%` }} />)}</div>; 
}

export function DataTable({ rows, saved=false }: { rows: CustomerRow[]; saved?:boolean }) { 
  return <GlassCard className="table-card"><div className="table-heading"><div><p className="eyebrow">{saved ? 'Recovered signal' : 'Priority queue'}</p><h2>{saved ? 'Saved customers' : 'At-risk customers'}</h2></div><button className="quiet-button">View all <ChevronRight size={15}/></button></div><div className="data-table"><div className="table-row table-head"><span>Customer</span><span>Risk score</span><span>Status</span></div>{rows.map(row=><div className="table-row" key={row.customer_id}><span><b>{row.name}</b><small>{row.customer_id} {row.meta ? `· ${row.meta}` : ''}</small></span><span className="score-value">{row.score.toFixed(1)}</span><StatusBadge status={row.status}/></div>)}</div></GlassCard>; 
}

export function SearchField({ value, onChange }: { value:string; onChange:(v:string)=>void }) { 
  return <label className="search-field"><Search size={16}/><input value={value} onChange={e=>onChange(e.target.value)} placeholder="Search by customer or ID" /></label>; 
}

export function UploadDropzone({ onUpload, isLoading }: { onUpload:(file: File)=>void; isLoading?: boolean }) { 
  const fileInputRef = useRef<HTMLInputElement>(null);
  return (
    <GlassCard className="upload-card">
      <div className="upload-icon"><UploadCloud size={24}/></div>
      <div><p className="eyebrow">Customer export</p><h2>Drop a CSV to surface the signal</h2><p>Use your latest customer export. Retentio validates the columns before scoring.</p></div>
      <input type="file" accept=".csv" className="hidden" ref={fileInputRef} style={{display: 'none'}} onChange={(e) => { if (e.target.files?.[0]) { onUpload(e.target.files[0]); } }} />
      <button className="primary-button" disabled={isLoading} onClick={() => fileInputRef.current?.click()}>
        {isLoading ? 'Uploading...' : 'Choose CSV'} <ChevronRight size={16}/>
      </button>
      <span className="upload-note">CSV only · up to 10 MB</span>
    </GlassCard>
  ); 
}
