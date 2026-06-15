from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    name = fields.Char(string='Opportunity', default='New Caller')

    # Mapping Studio fields to Baano custom models
    location_id = fields.Many2one('baano.location_state', string='Location', tracking=True)
    hospital_id = fields.Many2one('baano.hospital', string='Hospital', tracking=True)
    doctor_id = fields.Many2one('baano.doctor', string='Physician', tracking=True)
    complain_id = fields.Many2one('baano.complain', string='Chief Complaints', tracking=True)
    enterprise_id = fields.Many2one('baano.enterprise', string='Enterprise/Company', tracking=True)
    site_id = fields.Many2one('baano.site', string='Site', tracking=True)

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    
    # Agent fields linked to HR Employees
    receiving_agent_id = fields.Many2one('hr.employee', string='Receiving Agent', tracking=True)
    responding_agent_id = fields.Many2one('hr.employee', string='Responding Agent', tracking=True)
    converting_agent_id = fields.Many2one('hr.employee', string='Converting Agent', tracking=True)
    enterprise_company_id = fields.Many2one('res.partner', string='Enterprise Company', domain=[('category_id.name', '=', 'Enterprise')], tracking=True)

    # Site City / Service Type
    service_type = fields.Selection([
        ('online', 'Online Consultation'),
        ('hospital', 'Hospital Booking'),
        ('enterprise', 'Enterprise'),
        ('home', 'Home Care')
    ], string='Service', tracking=True)
    state_city = fields.Char(string='State City', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') and vals.get('phone'):
                vals['name'] = vals.get('phone')
            elif not vals.get('name'):
                vals['name'] = "New Caller"
        return super().create(vals_list)

    def write(self, vals):
        if self.name == 'New Caller' or not self.name:
            phone = vals.get('phone') or self.phone
            if phone:
                vals['name'] = phone
        return super().write(vals)
