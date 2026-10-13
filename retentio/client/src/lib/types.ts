/**
 * lib/types.ts
 * ===========
 * TypeScript types that mirror the FastAPI backend Pydantic schemas.
 * Keep in sync with backend/schemas/*.py
 */

// ── Auth / User ──────────────────────────────────────────────────────────────

export interface User {
  name: string;
  business_name: string;
  email: string;
  benchmark: number;
  created_at?: string | null;
}

export interface TokenResponse {
  token: string;
  user: User;
}

// ── Customer ─────────────────────────────────────────────────────────────────

export interface CustomerRow {
  customer_id: string;
  name: string;
  score: number;
  meta?: string | null;
  status: string;
}

export interface ScoreHistoryEntry {
  date: string;
  score: number;
}

export interface CustomerDetail {
  customer_id: string;
  name: string;
  current_score: number;
  status: string;
  history: ScoreHistoryEntry[];
}

// ── Prediction ────────────────────────────────────────────────────────────────

export interface PredictResponse {
  total_rows: number;
  at_risk: CustomerRow[];
  saved: CustomerRow[];
  saved_message?: string | null;
}

// ── Dashboard ─────────────────────────────────────────────────────────────────

export interface DashboardSummary {
  total_customers: number;
  at_risk_count: number;
  saved_count: number;
  avg_score: number;
}

export interface TrendPoint {
  date: string;
  avg_score: number;
  at_risk_count: number;
}

export interface DashboardTrend {
  points: TrendPoint[];
}

// ── Settings ──────────────────────────────────────────────────────────────────

export interface ProfileUpdate {
  business_name?: string;
  name?: string;
}

export interface BenchmarkUpdate {
  benchmark: number;
}

// ── API Error ─────────────────────────────────────────────────────────────────

export interface ApiError {
  detail: string;
}
