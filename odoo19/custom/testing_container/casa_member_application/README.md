# CASA New Member Application (Odoo 19)

Implements the public new-member workflow specified in `new member form.xlsx`.

## Main flow

1. Applicant opens `/new-member` without logging in.
2. Page 1 creates a staged application and CRM lead, then emails a six-digit OTP and private resume link.
3. Each page saves independently. Applicants with branches receive dynamically generated branch blocks; standalone applicants skip the branch page.
4. The summary page supports editing and submission. Submission performs CIPC, NCR and trading-name duplicate checks against applications, existing members and CRM leads.
5. CASA officers move the application to Under Review, enter the Pastel account and payment terms, attach the welcome invoice and certificate, and approve or decline it.
6. Approval alone creates the affiliation (when “Other” is selected), member entity, branches, MFSA/CASA numbers and portal access. `Date of Last Update` is set to the approval date, and the welcome email sends the invoice and certificate.

No member/entity/branch record is created from a draft or submitted application.

## Installation

Add the module directory to the Odoo 19 addons path, update the Apps list, and install **CASA New Member Application**. Assign CASA staff the **CASA Membership / Membership Officer** access privilege.

Configure an outgoing mail server and verify `web.base.url`, because OTP, resume, status and portal invitation links are sent by email.

## Validation

The addon includes post-install tests for staging, approval-only record creation, membership numbering, annual-update date, Pastel enforcement, branch reconciliation, OTP expiry and public website rendering.
