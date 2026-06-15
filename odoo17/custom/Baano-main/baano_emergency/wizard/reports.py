from odoo import api, fields, models, _
from odoo.exceptions import UserError

class BaanoReportWizard(models.TransientModel):
    _name = 'baano.report.wizard'
    _description = 'Report Date Range Wizard'

    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    report_type = fields.Selection([
        ('Disease Types', 'Disease Types'),
        ('Handled Cases', 'Handled Cases'),
        ('Labs', 'Labs'),
        ('Prescriptions', 'Prescriptions'),
    ], string='Report Type', required=True)

    def action_print_report(self):
        """
        Generate the selected PDF report immediately,
        bypassing the layout configuration dialog.
        """
        self.ensure_one()
        domain = [
            ('appointment_date', '>=', self.from_date),
            ('appointment_date', '<=', self.to_date),
        ]
        appointments = self.env['baano.appointment'].search(domain)
        if not appointments:
            raise UserError(_("No appointments found in the given date range."))

        # Map report types to their XML IDs
        report_map = {
            'Disease Types': 'baano_emergency.action_disease_types_report',
            'Handled Cases': 'baano_emergency.action_handled_cases_report',
            'Labs':           'baano_emergency.action_lab_test_cases_report',
            'Prescriptions': 'baano_emergency.action_prescription_summary_report',
        }

        xml_id = report_map.get(self.report_type)
        if not xml_id:
            raise UserError(_("Unknown report type: %s") % self.report_type)

        report = self.env.ref(xml_id)
        if not report:
            raise UserError(_("Cannot find report action %s") % xml_id)

        # Call report_action with config=False to skip the layout wizard
        return report.report_action(appointments.ids, data=None, config=False)
