A **full implementation design document** for an **ERPNext + Frappe solution** for a **Services / Facilities Provider firm** that manages **multiple client offices/sites** and wants to implement **HR/Payroll, Asset Management, Inventory, Daily Services, Transport/Fleet, and Finance**. The design uses **standard ERPNext modules** where they already exist and a **custom Frappe app** for operational flows that are unique to facilities management. ERPNext officially provides modules for **Accounting, Human Resources, Stock, Asset Management, Projects, and Support**, and Frappe provides the underlying capability to create **custom DocTypes, custom fields, workflows, Web Forms, Client Scripts, and Server Scripts** for site-specific business processes. [\[docs.frappe.io\]](https://docs.frappe.io/hr/payroll-entry), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/stock-entry), [\[manualpt.a...aerp.co.ao\]](https://manualpt.angolaerp.co.ao/docs/user/manual/en), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/asset-movement), [\[mycampus.amrita.edu\]](https://mycampus.amrita.edu/Frappe%20/documentation_frappe), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/videos/learn), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/manual/en/support/articles/automating-issue-assignments-to-support-team-in-erpnext)

***

# ERPNext Implementation Design Document

## For a Multi-Client Services / Facilities Provider Firm

***

# 1) Solution scope

This implementation covers the following business areas:

*   **HR / Payroll** for employees, attendance, leave, expense claims, salary structures, payroll entries, salary slips, and payroll-linked accounting. ERPNext’s HR module explicitly includes employee data, attendance, performance, leaves, appraisals, and payroll processing, while Payroll Entry supports bulk payroll creation and accounting accrual. [\[deepwiki.com\]](https://deepwiki.com/frappe/frappe/9.2-server-scripts-and-safe-execution), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes), [\[bing.com\]](https://bing.com/search?q=site%3adocs.frappe.io+web+form+frappe+official+docs)
*   **Asset Management** for office equipment, tools, cleaning machines, generators, IT devices, and optionally vehicles as fixed assets, including movement, depreciation, and maintenance. ERPNext supports asset depreciation, allocation/movement, and maintenance tracking through Asset, Asset Movement, and Asset Maintenance. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/stock-entry), [\[github.com\]](https://github.com/frappe/erpnext/wiki/Migration-Guide-to-ERPNext-version-15), [\[thirvusoft.com\]](https://www.thirvusoft.com/blog/erpnext/whats-new-in-erpnext-v15293-features-and-enhancements)
*   **Inventory Management** for consumables, janitorial supplies, pantry items, stationery, PPE, spare parts, and site/warehouse transfers. ERPNext Stock supports warehouse hierarchies, stock movements, serials/batches, and stock entries such as Material Issue, Material Receipt, and Material Transfer. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/exporting-customizations), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/manual/en/human-resources)
*   **Finance** for ledgers, invoicing, taxes, vendor payments, customer collections, and payroll-linked accounting. ERPNext officially positions Accounting as handling accounts, transactions, taxes, billing, journals, ledgers, and reports, and Payment Entry is the standard mechanism for collecting or disbursing funds against invoices and related records. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/stock-entry), [\[docs.frappe.io\]](https://docs.frappe.io/hr/payroll-entry), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/tutorial/create-a-doctype)
*   **Daily Services** and **Transport/Fleet** as **custom operational applications** built on Frappe using custom DocTypes, workflows, automation, and web forms because these service-delivery processes are not covered by a dedicated standard ERPNext module. Frappe’s framework documentation confirms that custom business entities should be modeled as DocTypes and extended using Workflows, Web Forms, Client Scripts, and Server Scripts. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[mycampus.amrita.edu\]](https://mycampus.amrita.edu/Frappe%20/documentation_frappe), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/videos/learn), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/manual/en/support/articles/automating-issue-assignments-to-support-team-in-erpnext), [\[docs.frappe.io\]](https://docs.frappe.io/framework/v13/user/en/web-forms)

***

# 2) High-level architecture

## Standard ERPNext modules to enable

Enable the following standard ERPNext modules:

*   **Human Resources / Payroll** [\[deepwiki.com\]](https://deepwiki.com/frappe/frappe/9.2-server-scripts-and-safe-execution), [\[bing.com\]](https://bing.com/search?q=site%3adocs.frappe.io+web+form+frappe+official+docs)
*   **Assets** [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/stock-entry), [\[github.com\]](https://github.com/frappe/erpnext/wiki/Migration-Guide-to-ERPNext-version-15)
*   **Stock / Inventory** [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/exporting-customizations)
*   **Accounting / Finance** [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/stock-entry), [\[docs.frappe.io\]](https://docs.frappe.io/hr/payroll-entry)
*   **Selling** for contract billing and client invoices, since ERPNext Selling covers quotations, sales orders, and order-to-invoice tracking. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events), [\[manualpt.a...aerp.co.ao\]](https://manualpt.angolaerp.co.ao/docs/user/manual/en)
*   **Projects** so each client site or contract can be mapped to a Project and/or Cost Center for profitability analysis, because ERPNext Projects integrates with billing and cost centers. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events), [\[docs.frappe.io\]](https://docs.frappe.io/framework/v14/user/en/desk/scripting/server-script)
*   **Support** if you want ticketing or issue handling, because ERPNext Support includes issue tracking and maintenance scheduling. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events), [\[erpnext.com\]](https://erpnext.com/homepage)

## Custom Frappe app to build

Create a custom app, for example:

```text
facilities_ops
```

This app will contain custom business objects for:

*   Client Site Management
*   Service Contracts
*   Daily Service Planning and Execution
*   Site Complaints / Service Requests
*   Client Signoff
*   Consumable Consumption
*   Transport / Fleet Operations
*   Billing Summary Consolidation

Using a custom app is the correct architectural choice because Frappe DocTypes are the core mechanism for defining custom data models, and customizations can be exported into an app for version control and deployment. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/maintenance-schedule), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v12/user/manual/en/asset/asset-movement)

***

# 3) Organization and financial design

## Company structure

Set up your legal entity/company in ERPNext and create:

*   **Departments** such as Operations, HR, Finance, Procurement, Transport, and Stores. ERPNext HR uses employee masters with organizational dimensions like department, branch, and designation. [\[deepwiki.com\]](https://deepwiki.com/frappe/frappe/9.2-server-scripts-and-safe-execution), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes)
*   **Branches** if your organization operates by city or business region, because Payroll Entry can be filtered by branch and related organizational categories. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes)
*   **Cost Centers** for profitability tracking. Payroll Entry can post payroll expense to cost centers, and the ERPNext manual states Projects also integrate with billing and cost centers. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events)
*   **Projects** for each client contract or client site if you need operational and financial visibility by location. ERPNext Projects supports project/task management and is integrated with billing and cost centers. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events), [\[docs.frappe.io\]](https://docs.frappe.io/framework/v14/user/en/desk/scripting/server-script)

## Recommended profitability model

Use:

*   **1 Cost Center per client site**, or
*   **1 Project per client site + 1 Cost Center per client site**, depending on reporting depth needed.

This will allow payroll, inventory consumption, transport cost, and other operational costs to be analyzed against the revenue generated for the same site. ERPNext explicitly supports payroll cost-center posting, and Projects are designed for linked billing and cost management. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events)

***

# 4) Master data model

This section defines the **exact data architecture**.

***

## 4.1 Standard ERPNext master records

You should use standard ERPNext records for the following:

*   **Customer** = client company. ERPNext Selling and Accounts use Customer as the standard party for receivables and sales invoices. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/tutorial/create-a-doctype)
*   **Supplier** = vendor for consumables, services, fuel, vehicle maintenance, etc. ERPNext Buying and Accounting use Supplier as the procurement/payables party. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/tutorial/create-a-doctype)
*   **Employee** = all staff including site staff, drivers, supervisors, office staff, and technicians. ERPNext HR maintains the employee database and payroll details. [\[deepwiki.com\]](https://deepwiki.com/frappe/frappe/9.2-server-scripts-and-safe-execution), [\[bing.com\]](https://bing.com/search?q=site%3adocs.frappe.io+web+form+frappe+official+docs)
*   **Item** = both stock items and service items. ERPNext’s services-company guide notes that service items should be created as **non-stock items** by unchecking “Maintain Stock.” [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events)
*   **Warehouse** = central warehouse, site warehouse, and optional vehicle store. ERPNext Stock supports warehouse hierarchies and stock movements. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/exporting-customizations)
*   **Asset** = fixed assets, equipment, and optionally vehicles. ERPNext Asset handles depreciation, movement, and maintenance. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/stock-entry), [\[github.com\]](https://github.com/frappe/erpnext/wiki/Migration-Guide-to-ERPNext-version-15), [\[thirvusoft.com\]](https://www.thirvusoft.com/blog/erpnext/whats-new-in-erpnext-v15293-features-and-enhancements)
*   **Bank Account / Cash Account** = required for Payment Entry and payroll disbursement. ERPNext Payment Entry requires bank/cash accounts and party mapping. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/tutorial/create-a-doctype), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes)

***

## 4.2 Custom master DocTypes to create

Below are the custom masters I recommend.

***

### A. `Client Site`

**Purpose:** Represents one client-managed office/site/location under a Customer. This is a custom DocType because a facilities provider typically serves multiple physical sites for the same client, and standard Customer alone is not granular enough. Frappe DocTypes are the correct way to model such custom business entities. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/maintenance-schedule)

**Naming**

```text
SITE-.YYYY.-.#####
```

**Fields**

*   `site_name` (Data, mandatory)
*   `customer` (Link → Customer, mandatory)
*   `site_code` (Data, unique)
*   `site_type` (Select: Office / Factory / Warehouse / Branch / Shared Workspace)
*   `address_line_1` (Data)
*   `address_line_2` (Data)
*   `city` (Data)
*   `region` (Data)
*   `country` (Link → Country)
*   `geo_coordinates` (Geolocation / Data)
*   `client_site_manager` (Data)
*   `client_approver_email` (Data)
*   `service_hours` (Data)
*   `default_project` (Link → Project)
*   `default_cost_center` (Link → Cost Center)
*   `default_warehouse` (Link → Warehouse)
*   `active` (Check)

**Permissions**

*   Operations Manager: full access
*   Site Supervisor: read/write limited to assigned site
*   Finance: read only
*   Client Portal User: read limited portal access

**Connections**

*   Service Contract
*   Daily Service Plan
*   Service Request
*   Consumable Consumption Slip
*   Trip Sheet
*   Sales Invoice

Frappe supports custom links/actions and connection dashboards for DocTypes. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v12/user/manual/en/support/maintenance-schedule), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/asset-movement)

***

### B. `Service Type`

**Purpose:** Master list of service categories offered. This is a business-defined operational master and should therefore be a custom DocType. Frappe explicitly uses DocTypes as the model/view layer for custom entities. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/maintenance-schedule)

**Fields**

*   `service_type_name`
*   `billing_method` (Fixed / Per Visit / Per Resource / Per Hour / Per Unit)
*   `default_service_item` (Link → Item)
*   `requires_checklist` (Check)
*   `requires_client_signoff` (Check)
*   `sla_hours` (Float)
*   `is_transport_related` (Check)
*   `is_daily_recurring` (Check)

***

### C. `Shift Template`

**Purpose:** Defines standard shifts used for site staffing and daily planning. This is best modeled as a custom DocType because it carries site-service specific operational logic. Frappe supports custom DocTypes and form customization for these cases. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/asset-movement)

**Fields**

*   `shift_name`
*   `start_time`
*   `end_time`
*   `days_of_week`
*   `default_headcount`
*   `break_minutes`
*   `site_type_applicability`

***

### D. `Service Checklist Template`

**Purpose:** Template for housekeeping rounds, pantry refill, reception checklist, technical inspection, etc. A checklist template is not a standard ERPNext core document, so it should be modeled as a custom DocType. Frappe’s metadata-driven model is built for this. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/maintenance-schedule)

**Fields**

*   `template_name`
*   `service_type` (Link → Service Type)
*   `site_type` (optional)
*   `is_active` (Check)

**Child table:** `Service Checklist Item`

*   `check_item`
*   `response_type` (Check / Text / Numeric / Rating / Photo)
*   `is_mandatory`
*   `sequence`

***

### E. `Billing Rule`

**Purpose:** Stores rules for consolidating fixed contract fees, transport charges, variable service calls, and consumable pass-throughs into a monthly invoice. This is a custom commercial master built on Frappe’s custom data model capability. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/asset-movement)

**Fields**

*   `billing_rule_name`
*   `billing_frequency` (Monthly / Weekly / Per Event)
*   `invoice_grouping` (By Site / By Customer / By Contract)
*   `include_consumables` (Check)
*   `include_transport` (Check)
*   `include_variable_jobs` (Check)
*   `rounding_policy`
*   `default_tax_template` (Link → Sales Taxes and Charges Template)

***

### F. `SLA Matrix`

**Purpose:** Maps priority and service type to response/resolution targets and escalation rules. This is a custom operational governance object, suitable for a custom DocType. Frappe supports this directly. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[mycampus.amrita.edu\]](https://mycampus.amrita.edu/Frappe%20/documentation_frappe), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/manual/en/support/articles/automating-issue-assignments-to-support-team-in-erpnext)

**Fields**

*   `priority` (Low / Medium / High / Critical)
*   `service_type`
*   `response_time_hours`
*   `resolution_time_hours`
*   `escalate_to_role`
*   `is_active`

***

# 5) Transactional custom DocTypes to implement

These are the **core operational records** for your facilities business.

***

## 5.1 `Service Contract`

**Purpose:** Defines the client agreement for one site or group of sites, including included services, billing, SLA, manpower, and contract period. This is a custom contract object and should be modeled as a DocType, while billing itself can later generate standard ERPNext sales records. Frappe custom DocTypes are intended for such extensions. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v12/user/manual/en/asset/asset-movement)

**Naming**

```text
SC-.YYYY.-.#####
```

**Fields**

*   `customer` (Link → Customer, mandatory)
*   `client_site` (Link → Client Site, mandatory)
*   `contract_start_date`
*   `contract_end_date`
*   `billing_rule` (Link → Billing Rule)
*   `default_project` (Link → Project)
*   `default_cost_center` (Link → Cost Center)
*   `fixed_monthly_fee` (Currency)
*   `currency`
*   `contract_status` (Draft / Active / Suspended / Expired / Terminated)
*   `client_reference_no`
*   `notes`
*   `service_level_template` (Link → SLA Matrix)
*   `requires_monthly_signoff` (Check)

**Child table:** `Service Contract Line`

*   `service_type`
*   `service_item` (Link → Item; usually a non-stock service item as recommended for services businesses) [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events)
*   `billing_method`
*   `rate`
*   `quantity`
*   `included_in_fixed_fee`
*   `shift_template`
*   `headcount_required`
*   `checklist_template`

**Workflow**

*   Draft
*   Under Review
*   Approved
*   Active
*   Suspended
*   Expired
*   Closed

Using a Workflow here is appropriate because ERPNext Workflows support multi-step approval states and override the normal draft/submit pattern where needed. [\[mycampus.amrita.edu\]](https://mycampus.amrita.edu/Frappe%20/documentation_frappe)

***

## 5.2 `Daily Service Plan`

**Purpose:** Generates the operational plan for a given site/date/shift. This extends beyond ERPNext’s standard maintenance scheduling and is better modeled as a custom operational schedule. Frappe custom DocTypes and workflows are intended for these site-specific processes. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[mycampus.amrita.edu\]](https://mycampus.amrita.edu/Frappe%20/documentation_frappe)

**Naming**

```text
DSP-.YY.-.MM.-.##### 
```

**Fields**

*   `service_date`
*   `client_site`
*   `service_contract`
*   `shift_template`
*   `supervisor` (Link → Employee)
*   `planned_start_time`
*   `planned_end_time`
*   `status` (Draft / Scheduled / In Progress / Completed / Closed / Missed)
*   `project`
*   `cost_center`
*   `remarks`

**Child table:** `Daily Service Plan Line`

*   `service_type`
*   `assigned_employee`
*   `assigned_driver` (optional)
*   `assigned_vehicle` (Link → Fleet Vehicle or Asset)
*   `checklist_template`
*   `expected_duration_minutes`
*   `requires_consumables`
*   `requires_signoff`

**Workflow**

*   Draft
*   Scheduled
*   Assigned
*   In Progress
*   Awaiting Signoff
*   Completed
*   Closed
*   Escalated

Workflows are well suited here because ERPNext allows state transitions, conditional approvals, and notification of next-step actors. [\[mycampus.amrita.edu\]](https://mycampus.amrita.edu/Frappe%20/documentation_frappe)

**Automation**

*   On submit / approval, auto-create **Daily Service Tasks** using a Server Script or custom app controller. Frappe supports server-side automation on DocType events. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/manual/en/support/articles/automating-issue-assignments-to-support-team-in-erpnext), [\[docs.frappe.io\]](https://docs.frappe.io/helpdesk/lesson-3-agents-teams)

***

## 5.3 `Daily Service Task`

**Purpose:** Actual executable unit of work for staff or supervisors. This should be a submittable custom DocType because it records operational evidence and closure. Frappe custom DocTypes support submittable records and event logic. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[docs.frappe.io\]](https://docs.frappe.io/helpdesk/lesson-3-agents-teams)

**Naming**

```text
DST-.YY.-.MM.-.##### 
```

**Fields**

*   `daily_service_plan` (Link)
*   `client_site`
*   `service_contract`
*   `service_type`
*   `assigned_employee`
*   `assigned_supervisor`
*   `start_time_actual`
*   `end_time_actual`
*   `task_status` (Open / In Progress / Awaiting Signoff / Completed / Rejected / Missed)
*   `priority`
*   `is_billable` (Check)
*   `billable_item` (Link → Item)
*   `billable_qty`
*   `checklist_template`
*   `customer_feedback` (Small Text)
*   `photo_before` (Attach / Image)
*   `photo_after` (Attach / Image)
*   `exception_notes`

**Child table:** `Daily Service Task Checklist Response`

*   `check_item`
*   `response_value`
*   `photo`
*   `is_passed`
*   `remarks`

**Workflow**

*   Open
*   Accepted
*   In Progress
*   Awaiting Signoff
*   Completed
*   Returned
*   Escalated
*   Closed

**Automation**

*   Client Script for mandatory photos/checklist completion before moving to “Awaiting Signoff.” Frappe Form Scripts / Client Scripts support field validation and contextual actions. [\[docs.frappe.io\]](https://docs.frappe.io/framework/v13/user/en/web-forms)
*   Server Script for SLA breach timestamping and escalation assignment. Server Scripts can run on document events and update records automatically. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/manual/en/support/articles/automating-issue-assignments-to-support-team-in-erpnext), [\[docs.frappe.io\]](https://docs.frappe.io/framework/v13/user/en/basics/doctypes/customize)

***

## 5.4 `Service Request`

**Purpose:** Reactive service issue or complaint raised by the client or site team. This can be modeled either as a custom DocType or mapped to ERPNext Support’s Issue concept, since ERPNext Support already tracks customer issues and requests. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events)

**Recommended approach:**  
Create a custom `Service Request` but keep a design that can later integrate with standard Issue / Support if needed.

**Fields**

*   `request_date`
*   `customer`
*   `client_site`
*   `request_source` (Portal / Phone / Email / Internal / WhatsApp)
*   `service_type`
*   `priority`
*   `reported_by`
*   `contact_number`
*   `description`
*   `status` (New / Assigned / In Progress / Awaiting Client / Resolved / Closed / Rejected)
*   `assigned_team`
*   `assigned_to`
*   `sla_due_at`
*   `linked_daily_service_task`
*   `linked_trip_request`
*   `is_billable`
*   `billable_item`
*   `resolution_summary`
*   `client_closure_confirmation` (Check)

**Workflow**

*   New
*   Triage
*   Assigned
*   In Progress
*   Awaiting Client
*   Resolved
*   Closed
*   Escalated

**Assignment**
Use **Assignment Rule** to auto-route by priority, service type, or site, because Frappe/ERPNext Assignment Rules support conditional routing, round-robin, load balancing, and workload-based assignment. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/workflows), [\[docs.frappe.io\]](https://docs.frappe.io/framework/v14/user/en/web-form/customization)

**Web intake**
Expose this via **Web Form** for clients/site teams, because Frappe Web Forms can create records for a DocType with client-side validation and custom behaviors. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/videos/learn), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/erpnext-for-services-organization), [\[frappe.io\]](https://frappe.io/erpnext/modules)

***

## 5.5 `Client Signoff`

**Purpose:** Captures evidence that the client representative approved a daily job, service request closure, or monthly service summary. This is a custom confirmation object suitable for a custom DocType. Frappe’s metadata and workflow model supports this cleanly. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[mycampus.amrita.edu\]](https://mycampus.amrita.edu/Frappe%20/documentation_frappe)

**Fields**

*   `signoff_type` (Task / Request / Monthly Summary / Visit)
*   `reference_doctype`
*   `reference_name`
*   `customer`
*   `client_site`
*   `client_contact_name`
*   `client_contact_email`
*   `signoff_date_time`
*   `feedback_rating`
*   `feedback_notes`
*   `signature_image` (Attach / Image)
*   `is_approved`

This can also be presented to clients using Web Forms or a portal page, since Frappe Web Forms are designed for web-based data capture into DocTypes. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/videos/learn), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/erpnext-for-services-organization)

***

## 5.6 `Consumable Consumption Slip`

**Purpose:** Records material issued and consumed at a client site for operational costing and/or billing recovery. This complements standard Stock Entry because Stock Entry records movement, while this custom slip captures site-level attribution and billing context. ERPNext Stock Entry already supports stock movement across warehouses and issue/receipt logic. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/exporting-customizations), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events)

**Fields**

*   `posting_date`
*   `client_site`
*   `service_contract`
*   `warehouse`
*   `linked_task`
*   `linked_request`
*   `requested_by`
*   `approved_by`
*   `is_billable_to_client`
*   `status` (Draft / Approved / Issued / Closed)

**Child table:** `Consumable Consumption Item`

*   `item_code`
*   `uom`
*   `qty_requested`
*   `qty_issued`
*   `rate`
*   `amount`
*   `stock_entry_reference`

**Automation**

*   On approval, create or link a standard **Stock Entry** of type Material Issue or Material Transfer as applicable. ERPNext Stock Entry supports Material Issue, Receipt, and Transfer. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/exporting-customizations)

***

## 5.7 `Fleet Vehicle`

**Purpose:** Operational fleet master. Although vehicles can be registered as standard ERPNext Assets, this custom DocType adds transport-specific operational fields while linking back to the Asset record. ERPNext Assets support depreciation, movement, and maintenance, and Frappe custom DocTypes allow an operational layer on top. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/stock-entry), [\[github.com\]](https://github.com/frappe/erpnext/wiki/Migration-Guide-to-ERPNext-version-15), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement)

**Fields**

*   `vehicle_code`
*   `vehicle_number`
*   `asset` (Link → Asset)
*   `vehicle_type`
*   `make_model`
*   `ownership_type` (Owned / Leased / Rented)
*   `driver_default`
*   `fuel_type`
*   `capacity`
*   `odometer_current`
*   `registration_expiry`
*   `insurance_expiry`
*   `fitness_expiry`
*   `status` (Active / Under Maintenance / Inactive)

***

## 5.8 `Driver`

**Purpose:** Driver operational master if you want a separate transport role layer beyond standard Employee. Since all drivers are also employees, this can either be a custom DocType linked to Employee or custom fields on Employee. Frappe customization supports either approach via custom fields or custom DocTypes. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/asset-movement), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement)

**Fields**

*   `employee` (Link → Employee)
*   `license_number`
*   `license_expiry`
*   `allowed_vehicle_types`
*   `default_shift`
*   `medical_expiry`
*   `status`

***

## 5.9 `Trip Request`

**Purpose:** Request for transport support for staff movement, supplies movement, site visits, or emergency response. This is not a standard ERPNext transport object, so it belongs in the custom app. Frappe’s workflow and assignment capabilities make it a good fit. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[mycampus.amrita.edu\]](https://mycampus.amrita.edu/Frappe%20/documentation_frappe), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/workflows)

**Fields**

*   `request_date`
*   `requested_by`
*   `client_site`
*   `trip_type` (Staff Pickup / Site Visit / Material Delivery / Client Meeting / Emergency)
*   `from_location`
*   `to_location`
*   `required_start`
*   `estimated_end`
*   `passenger_count`
*   `purpose`
*   `priority`
*   `status`
*   `approver`
*   `assigned_vehicle`
*   `assigned_driver`

**Workflow**

*   Draft
*   Pending Approval
*   Approved
*   Allocated
*   In Transit
*   Completed
*   Cancelled

***

## 5.10 `Trip Sheet`

**Purpose:** Execution record for an approved trip. This is the operational evidence document for vehicle utilization and costing. Frappe custom DocTypes and submissions are well suited for this purpose. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[docs.frappe.io\]](https://docs.frappe.io/helpdesk/lesson-3-agents-teams)

**Fields**

*   `trip_request`
*   `client_site`
*   `vehicle`
*   `driver`
*   `departure_datetime`
*   `arrival_datetime`
*   `start_odometer`
*   `end_odometer`
*   `distance_km`
*   `fuel_consumed`
*   `fuel_cost`
*   `toll_cost`
*   `parking_cost`
*   `other_cost`
*   `is_billable`
*   `billable_item`
*   `project`
*   `cost_center`
*   `status`

**Automation**

*   Compute `distance_km = end_odometer - start_odometer`
*   Push approved billable amounts into Monthly Billing Summary
*   Raise maintenance alert if odometer reaches threshold

This automation can be handled in Server Scripts or the custom app’s Python controller, since Frappe supports document-event execution and safe scripting. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/manual/en/support/articles/automating-issue-assignments-to-support-team-in-erpnext), [\[docs.frappe.io\]](https://docs.frappe.io/helpdesk/lesson-3-agents-teams), [\[docs.frappe.io\]](https://docs.frappe.io/framework/v13/user/en/basics/doctypes/customize)

***

## 5.11 `Fuel Log`

**Purpose:** Records fueling events for cost analysis and vehicle monitoring. This is a custom transport operation record. Frappe custom DocTypes are designed for this. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/maintenance-schedule)

**Fields**

*   `vehicle`
*   `driver`
*   `date_time`
*   `odometer`
*   `fuel_qty`
*   `fuel_rate`
*   `fuel_amount`
*   `vendor`
*   `invoice_no`
*   `is_linked_to_trip`
*   `trip_sheet`

***

## 5.12 `Monthly Billing Summary`

**Purpose:** Consolidates all billable contract lines, variable services, transport, and consumable recovery into a reviewable pre-invoice record. Standard ERPNext handles the actual Sales Invoice, while this custom layer performs business-specific aggregation. Frappe custom DocTypes are ideal for this type of business orchestration. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v12/user/manual/en/asset/asset-movement)

**Fields**

*   `billing_month`
*   `customer`
*   `client_site` (optional)
*   `service_contract`
*   `project`
*   `cost_center`
*   `status` (Draft / Under Review / Approved / Invoiced)
*   `sales_invoice` (Link → Sales Invoice)
*   `total_contract_fee`
*   `total_variable_services`
*   `total_transport`
*   `total_consumables`
*   `total_penalties`
*   `net_billable_amount`

**Child table:** `Monthly Billing Summary Line`

*   `line_type` (Fixed Fee / Variable Service / Transport / Consumable / Penalty)
*   `reference_doctype`
*   `reference_name`
*   `description`
*   `item`
*   `qty`
*   `rate`
*   `amount`

**Workflow**

*   Draft
*   Finance Review
*   Approved
*   Invoiced
*   Closed

***

# 6) Standard ERPNext transaction design by module

***

## 6.1 HR / Payroll design

ERPNext HR maintains employee records, attendance, leave, expense claims, and payroll. Payroll processing in ERPNext is driven by **Salary Components**, **Salary Structure**, **Salary Structure Assignment**, **Payroll Entry**, and **Salary Slips**. [\[deepwiki.com\]](https://deepwiki.com/frappe/frappe/9.2-server-scripts-and-safe-execution), [\[bing.com\]](https://bing.com/search?q=site%3adocs.frappe.io+web+form+frappe+official+docs), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes)

### Standard HR DocTypes to use

*   Employee [\[deepwiki.com\]](https://deepwiki.com/frappe/frappe/9.2-server-scripts-and-safe-execution)
*   Attendance [\[deepwiki.com\]](https://deepwiki.com/frappe/frappe/9.2-server-scripts-and-safe-execution), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes)
*   Leave Application [\[deepwiki.com\]](https://deepwiki.com/frappe/frappe/9.2-server-scripts-and-safe-execution)
*   Expense Claim [\[deepwiki.com\]](https://deepwiki.com/frappe/frappe/9.2-server-scripts-and-safe-execution)
*   Salary Component [\[bing.com\]](https://bing.com/search?q=site%3adocs.frappe.io+web+form+frappe+official+docs)
*   Salary Structure [\[bing.com\]](https://bing.com/search?q=site%3adocs.frappe.io+web+form+frappe+official+docs)
*   Salary Structure Assignment [\[bing.com\]](https://bing.com/search?q=site%3adocs.frappe.io+web+form+frappe+official+docs), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes)
*   Payroll Entry [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes)
*   Salary Slip [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes), [\[bing.com\]](https://bing.com/search?q=site%3adocs.frappe.io+web+form+frappe+official+docs)

### Custom fields to add on Employee

Use **Customize Form** / **Custom Field** for site-specific HR needs because Frappe explicitly supports site-specific custom fields and property overrides on standard DocTypes. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/asset-movement), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/manual/en/asset/asset-maintenance)

Add:

*   `default_client_site`
*   `default_cost_center`
*   `service_role` (Cleaner / Supervisor / Pantry / Reception / Driver / Technician)
*   `is_site_staff`
*   `transport_eligible`
*   `uniform_size`
*   `employee_category` (Permanent / Contract / Temporary)

### Payroll process

1.  Attendance finalized by site/HR. ERPNext Payroll Entry can validate attendance and optionally use timesheet-based calculations. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes)
2.  Salary Structures assigned. ERPNext Payroll Setup explicitly uses Salary Structure and Salary Structure Assignment before Payroll Entry. [\[bing.com\]](https://bing.com/search?q=site%3adocs.frappe.io+web+form+frappe+official+docs)
3.  Payroll Entry created by payroll frequency, optionally filtered by branch/department/designation/project. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes)
4.  Salary Slips created in bulk. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes)
5.  Salary Slips submitted; ERPNext books payroll accrual to Payroll Payable and expense heads. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes)
6.  Salary payment executed through Payment Entry / bank disbursement. Payroll Entry documentation describes the payment stage after accrual. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/basics/doctypes), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/tutorial/create-a-doctype)

***

## 6.2 Asset Management design

ERPNext Asset covers fixed asset registration, depreciation, and movements, while Asset Movement tracks transfer, issue, receipt, and custodian/location updates, and Asset Maintenance schedules and tracks preventive or calibration tasks. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/stock-entry), [\[github.com\]](https://github.com/frappe/erpnext/wiki/Migration-Guide-to-ERPNext-version-15), [\[thirvusoft.com\]](https://www.thirvusoft.com/blog/erpnext/whats-new-in-erpnext-v15293-features-and-enhancements)

### Standard Asset DocTypes to use

*   Asset
*   Asset Movement
*   Asset Maintenance
*   Asset Repair / maintenance logs where needed    [\[github.com\]](https://github.com/frappe/erpnext/wiki/Migration-Guide-to-ERPNext-version-15), [\[thirvusoft.com\]](https://www.thirvusoft.com/blog/erpnext/whats-new-in-erpnext-v15293-features-and-enhancements)

### Custom fields on Asset

*   `client_site`
*   `ownership_type` (Company Owned / Client Owned Managed by Us)
*   `service_contract`
*   `operational_status`
*   `asset_barcode`
*   `maintenance_vendor`

### Asset process

*   New assets created from purchases and capitalized in standard Asset records. ERPNext supports asset capitalization/decapitalization and depreciation. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/stock-entry)
*   Assets moved via **Asset Movement** when transferred to a site or issued to an employee. ERPNext Asset Movement changes location/custodian based on purpose and requires submission. [\[github.com\]](https://github.com/frappe/erpnext/wiki/Migration-Guide-to-ERPNext-version-15)
*   Assets requiring preventive maintenance are scheduled through **Asset Maintenance**, which supports periodicity, assignment, due dates, and ToDo generation. [\[thirvusoft.com\]](https://www.thirvusoft.com/blog/erpnext/whats-new-in-erpnext-v15293-features-and-enhancements), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/introduction)

***

## 6.3 Inventory Management design

ERPNext Stock manages warehouses, item quantities, and stock entries across receipts, issues, and transfers. The official Stock Entry documentation lists supported purposes such as Material Receipt, Material Issue, Material Transfer, and others. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/exporting-customizations), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events)

### Standard inventory DocTypes to use

*   Item
*   Warehouse
*   Stock Entry
*   Material Request if desired for requisitions
*   Purchase Order / Purchase Invoice for buying flows    [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/exporting-customizations), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events)

### Warehouse structure

*   `Central Warehouse`
*   `Site Warehouse - [Site Code]`
*   `Transit Warehouse` (optional)
*   `Vehicle Store - [Vehicle No]` (optional)

### Item categories

*   Pantry Supplies
*   Housekeeping Consumables
*   Technical Spares
*   PPE
*   Stationery
*   Tools
*   Billable Consumables

### Core stock movements

*   Purchase Receipt into Central Warehouse
*   Material Transfer to Site Warehouse
*   Material Issue to Task / Site Team
*   Return from site when unused  
    ERPNext Stock Entry explicitly supports Material Receipt, Material Issue, and Material Transfer for such purposes. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/exporting-customizations)

***

## 6.4 Finance / Accounting design

ERPNext Accounting is the financial core for invoicing, journals, ledgers, taxes, and reports, while Payment Entry records receipts, payments, advances, and internal transfers. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/stock-entry), [\[docs.frappe.io\]](https://docs.frappe.io/hr/payroll-entry), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/tutorial/create-a-doctype)

### Standard finance DocTypes to use

*   Sales Invoice
*   Purchase Invoice
*   Journal Entry
*   Payment Entry
*   Cost Center
*   Bank Account / Mode of Payment    [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/tutorial/create-a-doctype), [\[docs.frappe.io\]](https://docs.frappe.io/hr/payroll-entry)

### Revenue model

*   Fixed monthly site management fee
*   Variable service jobs
*   Consumable recovery
*   Transport / trip-based charges
*   Emergency visit charges
*   Penalties / SLA credits  
    ERPNext’s services-business guidance recommends non-stock service items for service billing, and standard Selling/Accounting flows can be used for invoicing. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events)

### Collections model

Customer collections should be posted via **Payment Entry**, because ERPNext Payment Entry is the documented mechanism for receiving payment against Sales Invoices and related transactions. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/tutorial/create-a-doctype)

***

# 7) Workflow design (exact implementation)

***

## 7.1 Service Contract workflow

```text
Draft → Under Review → Approved → Active → Suspended → Expired/Closed
```

**Approvers**

*   Operations Manager reviews scope
*   Finance Manager approves billing/commercials
*   Senior Management or authorized role activates

ERPNext Workflows support custom states, transitions, document status mappings, and notifications to the next possible actors. [\[mycampus.amrita.edu\]](https://mycampus.amrita.edu/Frappe%20/documentation_frappe)

***

## 7.2 Daily Service Plan workflow

```text
Draft → Scheduled → Assigned → In Progress → Awaiting Signoff → Completed → Closed
                              ↘ Escalated
```

**Transition rules**

*   Only Operations Planner can move Draft → Scheduled
*   Only Supervisor can move Assigned → In Progress
*   Only Assigned staff/supervisor can complete task evidence
*   Client Signoff or Supervisor override required for “Completed”  
    Workflows in ERPNext can encode role-based transitions and state changes. [\[mycampus.amrita.edu\]](https://mycampus.amrita.edu/Frappe%20/documentation_frappe)

***

## 7.3 Service Request workflow

```text
New → Triage → Assigned → In Progress → Awaiting Client → Resolved → Closed
              ↘ Escalated
```

**Assignment**

*   Auto-assign by site/service type/priority using **Assignment Rule** or Server Script. Assignment Rules support conditions, round-robin, and load balancing. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/workflows), [\[docs.frappe.io\]](https://docs.frappe.io/framework/v14/user/en/web-form/customization)

***

## 7.4 Trip Request workflow

```text
Draft → Pending Approval → Approved → Allocated → In Transit → Completed
                                      ↘ Cancelled
```

**Approvers**

*   Site Supervisor or Department Manager
*   Transport Coordinator allocates driver/vehicle

Use Workflow for approvals and Server Scripts for auto-allocation proposals where relevant. Frappe supports both. [\[mycampus.amrita.edu\]](https://mycampus.amrita.edu/Frappe%20/documentation_frappe), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/manual/en/support/articles/automating-issue-assignments-to-support-team-in-erpnext)

***

## 7.5 Monthly Billing Summary workflow

```text
Draft → Finance Review → Approved → Invoiced → Closed
```

**Transitions**

*   Operations confirms billable operational lines
*   Finance validates rates and tax treatment
*   Invoice created in standard ERPNext Sales Invoice and linked back

This design keeps operational aggregation in the custom app while preserving standard accounting records in ERPNext. ERPNext’s service-company guidance and Accounting/Selling modules support this pattern. [\[docs.frappe.io\]](https://docs.frappe.io/hr/payroll-entry), [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/guides/app-development/executing-code-on-doctype-events)

***

# 8) Web Forms, automation, and custom scripting

Frappe provides **Web Forms** for website/portal submission into DocTypes, **Client Scripts** for form-side validation and behaviors, and **Server Scripts** for event-driven back-end automation. These are the key tools to operationalize your custom facilities workflows without hardcoding everything from scratch. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/videos/learn), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/erpnext-for-services-organization), [\[docs.frappe.io\]](https://docs.frappe.io/framework/v13/user/en/web-forms), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/manual/en/support/articles/automating-issue-assignments-to-support-team-in-erpnext), [\[docs.frappe.io\]](https://docs.frappe.io/framework/v13/user/en/basics/doctypes/customize)

## Recommended Web Forms

Create Web Forms for:

*   Client Service Request submission
*   Client Signoff
*   Site Consumable Request
*   Driver / Trip Request intake (optional)

## Recommended Client Scripts

Use Client Scripts for:

*   auto-filling site defaults when `client_site` is selected
*   mandatory photo/checklist enforcement on Daily Service Task
*   calculating transport kilometers on Trip Sheet
*   hiding/showing billing fields depending on `is_billable`

## Recommended Server Scripts or app logic

Use Server Scripts or controller hooks for:

*   generate Daily Service Tasks from Daily Service Plan
*   create ToDo / assignment when service request is raised
*   compute SLA breach and escalation
*   push approved consumable issues into Stock Entry
*   compile Monthly Billing Summary lines from tasks, trips, and consumption slips
*   create reminders for expiring vehicle documents or asset maintenance due dates

Frappe’s documentation explicitly supports document-event server scripts, API scripts, and client-side scripts attached to forms and web forms. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/manual/en/support/articles/automating-issue-assignments-to-support-team-in-erpnext), [\[docs.frappe.io\]](https://docs.frappe.io/framework/assignments-and-todos), [\[docs.frappe.io\]](https://docs.frappe.io/framework/v13/user/en/web-forms), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/erpnext-for-services-organization)

***

# 9) Role and permission model

Use Frappe’s role-based security model to restrict module and record access. The framework documentation highlights built-in role-based permissions as a core feature. [\[youtube.com\]](https://www.youtube.com/watch?v=sehbIxQ0w0Y)

## Roles to create

*   System Manager
*   HR Manager
*   Payroll Officer
*   Finance Manager
*   Accounts User
*   Store Manager
*   Procurement User
*   Operations Manager
*   Operations Planner
*   Site Supervisor
*   Technician / Field Staff
*   Transport Coordinator
*   Fleet Manager
*   Driver
*   Client Portal User

## Record-level restrictions

*   Site Supervisors should only access records for assigned Client Sites
*   Drivers should only access their own trip sheets / vehicle logs
*   Client users should only access portal-safe forms and signoff records
*   Payroll data should be restricted to payroll roles only

Where native permissions are insufficient, Frappe also supports **Permission Query** logic via Server Scripts for additional filtering. [\[docs.frappe.io\]](https://docs.frappe.io/framework/assignments-and-todos), [\[docs.frappe.io\]](https://docs.frappe.io/framework/v13/user/en/basics/doctypes/customize)

***

# 10) Reporting and dashboards to build

ERPNext and Frappe include dashboards, lists, and report-building capabilities, and ERPNext specifically highlights dashboards and KPI tracking across business processes. [\[docs.frappe.io\]](https://docs.frappe.io/helpdesk/assignment-rule), [\[youtube.com\]](https://www.youtube.com/watch?v=sehbIxQ0w0Y)

## HR / Payroll reports

*   Headcount by site
*   Attendance % by site
*   Payroll cost by site
*   Overtime by site
*   Driver deployment summary

## Inventory reports

*   Stock by warehouse/site
*   Consumable usage by client site
*   Consumable recovery vs cost
*   Reorder risk items

## Asset reports

*   Assets by site
*   Assets issued to employees
*   Maintenance due list
*   Asset downtime / repair log
*   Vehicle documents expiry

## Operations reports

*   Planned vs completed daily services
*   Missed tasks by site
*   SLA breaches
*   Client signoff %
*   Open service requests by priority
*   Resolution time by service type

## Finance reports

*   Revenue by client/site
*   Gross margin by client/site
*   Receivables aging
*   Transport cost vs recovery
*   Consumable recovery vs actual cost

***

# 11) Recommended implementation sequence

## Phase 1 — Core ERP setup

*   Company, Chart of Accounts, Users, Roles, Permissions, Customers, Suppliers, Employees, Cost Centers, Projects, Warehouses, Items, Asset Categories. ERPNext documentation identifies these as foundational business records across HR, Accounts, Stock, and Assets. [\[docs.frappe.io\]](https://docs.frappe.io/hr/payroll-entry), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/stock-entry)

## Phase 2 — Standard modules live

*   HR / Payroll
*   Stock
*   Assets
*   Accounting / Selling  
    This aligns with ERPNext’s documented core modules and will establish the master and transactional backbone first. [\[docs.frappe.io\]](https://docs.frappe.io/hr/payroll-entry), [\[manualpt.a...aerp.co.ao\]](https://manualpt.angolaerp.co.ao/docs/user/manual/en)

## Phase 3 — Custom facilities app

*   Client Site
*   Service Contract
*   Daily Service Plan / Task
*   Service Request
*   Client Signoff
*   Consumable Consumption Slip
*   Fleet / Transport  
    This is where Frappe DocTypes, Workflows, Web Forms, and scripts are used for the custom operations layer. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v14/user/manual/en/asset/asset-movement), [\[mycampus.amrita.edu\]](https://mycampus.amrita.edu/Frappe%20/documentation_frappe), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/videos/learn), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v13/user/manual/en/support/articles/automating-issue-assignments-to-support-team-in-erpnext)

## Phase 4 — Billing consolidation

*   Monthly Billing Summary
*   Sales Invoice integration
*   Payment collection  
    This phase connects custom operations to standard ERPNext finance flows. ERPNext service-item billing and Payment Entry support this pattern. [\[docs.frappe.io\]](https://docs.frappe.io/framework/user/en/tutorial/create-a-doctype)

## Phase 5 — Dashboards, reporting, UAT, go-live

*   Report validation
*   Pilot by 1–2 sites
*   Security review
*   Training and SOP handover

***

# 12) Final recommended document structure for your implementation team

If you are converting this into a working implementation project, I recommend your internal implementation pack include:

1.  **Business process map**
2.  **Master data template**
3.  **DocType field dictionary**
4.  **Workflow matrix**
5.  **Role/permission matrix**
6.  **Integration/automation specs**
7.  **Reports & dashboards list**
8.  **UAT scenarios**
9.  **Go-live checklist**

This is consistent with how Frappe/ERPNext implementations usually separate standard module configuration from custom-app specifications and exportable customizations. Frappe documentation explicitly supports app-based customizations and exported custom objects. [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/v12/user/manual/en/asset/asset-movement), [\[docs.frappe.io\]](https://docs.frappe.io/erpnext/asset-movement)

***

# 13) Next step I recommend

The design above is the **implementation blueprint**. The best next step is to convert it into a **field-level functional specification** for your consultants/developers.

I can do that next in one of these formats:

### Option A — **DocType-by-DocType field dictionary**

A detailed spec for every custom DocType with:

*   field name
*   label
*   field type
*   link target
*   mandatory/hidden/default rules
*   role access
*   automation notes

### Option B — **Workflow & role matrix**

A full matrix showing:

*   who creates
*   who approves
*   who can edit
*   who can close
*   notifications/escalations

### Option C — **Development-ready technical spec**

A more technical document covering:

*   custom app modules
*   naming series
*   child tables
*   APIs
*   server script logic
*   web form design
*   reports and dashboards

If you want, I can do **Option A next** and produce the **complete field dictionary for every custom DocType**.
