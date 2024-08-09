from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CompanyMemberApproval(models.Model):
    _name = 'company.member.approval'

    user_id = fields.Many2one('res.users', required=True)
    company_id = fields.Many2one('res.company', required=True)
    state = fields.Selection([('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
                             default='pending')
    approved_by = fields.Many2one('res.users', string="Approved By", readonly=True)

    # _sql_constraints = [
    #     ('unique_pending_approval', 'UNIQUE(user_id, company_id, state)',
    #      'You can only have one pending approval request per company.')
    # ]

    @api.model
    def get_pending_approvals(self):
        return self.search([
            ('company_id', '=', self.env.company.id),
            ('state', '=', 'pending')
        ])

    def action_approve(self):
        self.ensure_one()
        if self.state != 'pending':
            raise UserError(_("You can only approve pending requests."))
        if not self.env.user.has_group('my_company_member_management.group_company_admin'):
            raise UserError(_("You don't have the rights to approve this request."))
        if self.company_id != self.env.company:
            raise UserError(_("You can only approve requests for your own company."))

        self.write({
            'state': 'approved',
            'approved_by': self.env.user.id
        })
        self.user_id.sudo().write({
            'company_id': self.company_id.id,
            'company_ids': [(4, self.company_id.id)]
        })

    def action_reject(self):
        self.ensure_one()
        if self.state != 'pending':
            raise UserError(_("You can only reject pending requests."))
        if not self.env.user.has_group('my_company_member_management.group_company_admin'):
            raise UserError(_("You don't have the rights to reject this request."))
        if self.company_id != self.env.company:
            raise UserError(_("You can only reject requests for your own company."))

        self.write({
            'state': 'rejected',
        })