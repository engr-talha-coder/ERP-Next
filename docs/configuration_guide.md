# Configuration Guide — facilities_ops

## Overview

This guide explains how to configure the `facilities_ops` module after installation.

---

## Module Structure

```
Facilities Ops
├── Masters
│   ├── Client Site
│   ├── Service Type
│   ├── Shift Template
│   ├── Service Checklist Template
│   ├── Billing Rule
│   └── SLA Matrix
├── Operations
│   ├── Service Contract
│   ├── Daily Service Plan
│   ├── Daily Service Task
│   ├── Service Request
│   ├── Client Signoff
│   └── Consumable Consumption Slip
├── Billing
│   └── Monthly Billing Summary
└── Fleet
    ├── Fleet Vehicle
    ├── Driver
    ├── Trip Request
    ├── Trip Sheet
    └── Fuel Log
```

---

## 1. Initial Masters Setup

### 1.1 Service Types

Navigate to **Facilities Ops → Service Type** and create records for each service offered:

| Field | Example |
|---|---|
| Service Type Name | Daily Office Cleaning |
| Service Category | Cleaning |
| Default Response Hours | 4 |
| Default Resolution Hours | 24 |

### 1.2 Shift Templates

Navigate to **Facilities Ops → Shift Template**:

| Field | Example |
|---|---|
| Shift Name | Morning Shift |
| Shift Type | Day |
| Start Time | 06:00:00 |
| End Time | 14:00:00 |

### 1.3 SLA Matrix

Set up SLA targets per service type and priority:

| Priority | Response (hrs) | Resolution (hrs) |
|---|---|---|
| Critical | 1 | 4 |
| High | 2 | 8 |
| Medium | 4 | 24 |
| Low | 8 | 48 |

### 1.4 Billing Rules

Create billing rules linked to service types:

- **Billing Basis**: Per Hour / Per Day / Fixed / Per Visit
- Link to a **Sales Taxes and Charges Template** for automatic tax application

---

## 2. Roles and Permissions

The following roles are created automatically via fixtures:

| Role | Access Level |
|---|---|
| Operations Manager | Full access to all Facilities Ops doctypes |
| Operations Planner | Create/edit Daily Service Plans |
| Site Supervisor | Execute tasks, sign off, log consumables |
| Transport Coordinator | Manage trip requests and fleet |
| Fleet Manager | Full fleet and driver management |
| Driver | Read-only fleet; create trip sheets and fuel logs |
| Client Portal User | Read-only access to their own records |

Assign roles in **HR → Employee → User** or via the User master.

---

## 3. Client Sites

For each physical site you manage:

1. Go to **Facilities Ops → Client Site → New**
2. Link to an existing **Customer**
3. Set a unique **Site Code** for internal reference
4. Fill in address and contact details
5. Set **Default Project**, **Default Cost Center**, and **Default Warehouse** to auto-populate on downstream documents

---

## 4. Service Contracts

1. Create a **Service Contract** linked to a Customer and Client Site
2. Add **Contract Lines** specifying each service type, quantity, rate, and billing rule
3. Submit the contract — status changes to **Active**
4. The contract drives Daily Service Plans and Monthly Billing Summaries

---

## 5. Daily Operations Workflow

```
Daily Service Plan (create & submit)
    ↓ (auto-creates)
Daily Service Tasks (one per plan line)
    ↓ (supervisor fills checklist)
Client Signoff (submit after service)
    ↓
Monthly Billing Summary (consolidates all tasks)
    ↓
Sales Invoice (generated from billing summary)
```

---

## 6. Service Requests

Service Requests follow a workflow:

```
Open → In Progress → [Pending Client] → Resolved → Closed
```

SLA tracking is automatic when an **SLA Matrix** is linked. The daily scheduler checks for breaches and sets `sla_breached = 1`.

---

## 7. Fleet Management

### Setup
1. Create **Fleet Vehicle** records with registration, specs, and document expiry dates
2. Create **Driver** records linked to Employee records
3. Set default vehicles and drivers per site

### Trip Flow
```
Trip Request (submit for approval)
    ↓ (Transport Coordinator approves)
Trip Sheet (driver fills odometer, time, passengers)
    ↓ (submit on completion)
Fuel Log (created separately per refuel event)
```

### Document Expiry Alerts
The daily scheduler sends email alerts 30 days before:
- Insurance expiry
- Road tax expiry
- Inspection expiry

---

## 8. Monthly Billing

1. At month end, create a **Monthly Billing Summary** per Customer/Site
2. Add billing lines from completed service tasks
3. Workflow: Draft → Review → Approved → Invoiced
4. Click **Create Sales Invoice** to generate an ERPNext Sales Invoice automatically

---

## 9. Custom Fields on Standard DocTypes

The app adds these fields to standard ERPNext doctypes:

### Employee
| Field | Type | Purpose |
|---|---|---|
| Default Client Site | Link → Client Site | Staff deployment site |
| Service Role | Select | Cleaner / Guard / Driver etc. |
| Is Site Staff | Check | Flag for facilities staff |
| Transport Eligible | Check | Can be assigned to trips |
| Uniform Size | Data | Uniform ordering |
| Employee Category | Select | Permanent / Contract / Casual |

### Asset
| Field | Type | Purpose |
|---|---|---|
| Client Site | Link → Client Site | Where asset is deployed |
| Ownership Type | Select | Owned / Leased / Client-Provided |
| Service Contract | Link → Service Contract | Linked contract |
| Asset Barcode | Data | For scanning/tracking |

---

## 10. Scheduler Events

| Event | Function | Frequency |
|---|---|---|
| Vehicle document expiry alerts | `fleet_vehicle.check_document_expiry` | Daily |
| SLA breach detection | `service_request.check_sla_breaches` | Daily |

Ensure the bench scheduler is running:
```bash
bench --site <site> enable-scheduler
```
