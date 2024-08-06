from odoo import models, fields


class CompanyMemberApproval(models.Model):
    _name = 'company.member.approval'
    _description = 'Company Member Approval'

    user_id = fields.Many2one('res.users', string='User', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending', string='Status')