app_name = "facilities_ops"
app_title = "Facilities Ops"
app_publisher = "Facilities Ops"
app_description = "Facilities Operations Management for ERPNext v15"
app_email = "admin@facilitiesops.com"
app_license = "MIT"

app_include_css = []
app_include_js = []

fixtures = [
    {
        "dt": "Role",
        "filters": [
            [
                "name",
                "in",
                [
                    "Operations Manager",
                    "Operations Planner",
                    "Site Supervisor",
                    "Transport Coordinator",
                    "Fleet Manager",
                    "Driver",
                    "Client Portal User",
                ],
            ]
        ],
    },
    {"dt": "Workflow State"},
    {"dt": "Workflow Action Master"},
    {
        "dt": "Workflow",
        "filters": [
            [
                "document_type",
                "in",
                [
                    "Service Contract",
                    "Daily Service Plan",
                    "Service Request",
                    "Trip Request",
                    "Monthly Billing Summary",
                ],
            ]
        ],
    },
    {"dt": "Custom Field", "filters": [["module", "=", "Facilities Ops"]]},
    {"dt": "Workspace", "filters": [["name", "in", ["Facilities Ops"]]]},
]

after_install = "facilities_ops.setup.install.after_install"

doc_events = {}

scheduler_events = {
    "daily": [
        "facilities_ops.facilities_ops.doctype.fleet_vehicle.fleet_vehicle.check_document_expiry",
        "facilities_ops.facilities_ops.doctype.service_request.service_request.check_sla_breaches",
    ],
}
