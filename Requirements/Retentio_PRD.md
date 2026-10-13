# Product Requirements Document (PRD)
## Product Name: Retentio
### Customer Churn Prediction Platform

**Version:** 1.0
**Status:** Draft
**Date:** August 19, 2026

---

## 1. Overview

Retentio is a web-based application that helps businesses identify customers who are at risk of churning (leaving). Using a machine learning model trained on customer behavior data, Retentio assigns each customer a **Risk Score (0–100)**. Customers scoring above a configurable benchmark (default: 78) are flagged as **"At Risk."** On subsequent data uploads, customers whose scores drop below the benchmark are automatically reclassified as **"Saved,"** allowing businesses to track the effectiveness of their retention efforts over time.

---

## 2. Problem Statement

Businesses lose revenue when they fail to notice early warning signs of customer disengagement. Most small-to-mid-sized businesses lack the tools or expertise to build predictive churn models themselves, and existing enterprise solutions are often expensive, complex, or require deep technical integration. There is a need for a simple, upload-based tool that gives businesses actionable churn insights without requiring a data science team or live system integration.

---

## 3. Goals & Objectives

| Goal | Description |
|---|---|
| G1 | Allow businesses to upload customer data and receive churn risk scores |
| G2 | Flag high-risk customers clearly and immediately |
| G3 | Track customers over time — detect who moves from "At Risk" to "Saved" |
| G4 | Provide a simple, visually engaging dashboard for churn insights |
| G5 | Allow businesses to customize their own risk benchmark |
| G6 | Deliver the above through an intuitive, low-friction web interface |

### Non-Goals (Out of Scope for v1)
- Real-time/continuous data ingestion (API/webhook integration) — reserved for a future version.
- Automated email/SMS alerts to end customers.
- Multi-user role management (admin/team roles) within a single business account.
- Native mobile application.

---

## 4. Target Users

- **Primary:** Small-to-mid-sized business owners, customer success teams, and marketing/retention teams who manage customer relationship data but lack in-house ML capability.
- **Secondary:** Students/analysts evaluating churn trends for reporting purposes.

---

## 5. User Stories

| ID | As a... | I want to... | So that... |
|---|---|---|---|
| US1 | Business owner | Sign up and create an account | I can start using Retentio for my business |
| US2 | Returning user | Log in and see a dashboard summary | I can quickly understand my churn situation |
| US3 | New user | Upload a customer CSV | I can get churn risk scores for my customers |
| US4 | User | See a clear list of "At Risk" customers | I know who to focus retention efforts on |
| US5 | User | Re-upload updated data later | I can see which at-risk customers were "Saved" |
| US6 | User | Search for a specific customer | I can view their individual risk history |
| US7 | User | Adjust the risk benchmark | I can tailor sensitivity to my business needs |
| US8 | User | Update my name/business name | I can keep my account information accurate |

---

## 6. Core Features

### 6.1 Landing Page
Animated introductory page with sequential text reveals ("Losing Customers?" → "Predict Customer Churn Before It Happens" → "Let's Get Started!"), leading to a Sign Up / Login card.

### 6.2 Authentication
- **Sign Up:** New businesses create an account; redirected to the Predict Page.
- **Login:** Returning users log in; redirected to the Dashboard Page. Login page displays rotating "Did you know?" business/churn facts every 7 seconds.
- Both entry points grant full navigation access to all pages (Dashboard, Predict, Customers, Settings).

### 6.3 Dashboard
Displays summary cards (Total Customers, At Risk Count, Saved Count, Average Risk Score) and visual charts (risk distribution, trend over time).

### 6.4 Predict Page (Core ML Feature)
- CSV upload (drag & drop or file picker).
- Success confirmation via toast/popup.
- "Calculate" button triggers ML scoring.
- Results rendered below upload section:
  - **At Risk table** — customers scoring ≥ benchmark.
  - **Saved table** — customers who previously were "At Risk" and have since dropped below benchmark.
  - If no customers qualify as "Saved" on a given upload, the table displays: *"No customers saved yet."*

### 6.5 Customer Detail Page
Search customers by name or Customer ID; view individual score history (trend chart), current status, and status change timeline.

### 6.6 Settings Page
- Edit user name and business name.
- Adjust risk benchmark threshold (slider, e.g., 70–90).
- Save with confirmation toast.

---

## 7. Functional Requirements

| ID | Requirement |
|---|---|
| FR1 | System must allow CSV upload and validate required columns |
| FR2 | System must run the ML model and generate a risk score (0–100) per customer |
| FR3 | System must classify customers as "At Risk" if score ≥ benchmark |
| FR4 | System must persist customer risk history across uploads |
| FR5 | System must reclassify a previously "At Risk" customer as "Saved" if their new score drops below benchmark |
| FR6 | System must display "No customers saved yet" if no status changes occurred |
| FR7 | System must allow benchmark threshold adjustment per business account |
| FR8 | System must support customer search by name or ID |
| FR9 | System must support Sign Up and Login with redirect logic as defined |
| FR10 | Authenticated users must have unrestricted navigation across all pages |

---

## 8. Non-Functional Requirements

| Category | Requirement |
|---|---|
| Usability | Simple upload-first flow; no technical/ML knowledge required from the user |
| Performance | CSV processing and scoring should complete within a few seconds for typical file sizes |
| Reliability | Customer history must persist accurately across sessions and uploads |
| Scalability | Should handle a growing customer base per business without major rework |
| Maintainability | ML model and preprocessing logic should be swappable/retrainable independently of the API layer |

*(Detailed security, performance benchmarks, and infrastructure requirements will be covered in the separate Technical Architecture and Security & Access documents.)*

---

## 9. Success Metrics

| Metric | Target |
|---|---|
| Upload-to-result time | Under a few seconds for standard file sizes |
| Correct status classification | Model accuracy/F1-score benchmarked during training (Step 3 of build plan) |
| User task completion | User can go from Sign Up → Upload → View Results without confusion (usability testing) |
| Retention insight value | Business can clearly distinguish "At Risk" vs "Saved" customers across uploads |

---

## 10. Assumptions & Constraints

- Businesses will manually export and upload their customer data as CSV; no live data integration in v1.
- Historical customer status tracking (At Risk / Saved) depends on `customer_id` remaining consistent across uploads.
- The ML model is trained on a general churn dataset (e.g., Telco Churn) and may require retraining/fine-tuning for specific industries in the future.

---

## 11. Dependencies

- ML model and preprocessing pipeline (FastAPI backend, XGBoost).
- MongoDB for persistent customer status/history tracking.
- Frontend stack: React.js, Tailwind CSS, shadcn/ui, lucide-react, Recharts, Axios.

---

## 12. Related Documents
- Technical Architecture Document *(separate)*
- Security & Access Document *(separate)*
- Frontend Specification Document *(separate)*
- Feature Ticket List *(separate)*
