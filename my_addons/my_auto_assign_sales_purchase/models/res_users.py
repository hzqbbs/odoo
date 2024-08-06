from odoo import models, api, _, fields
import logging

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def get_custom_users_domain(self):
        return [
            '|',
            ('groups_id', 'in', [self.env.ref('base.group_system').id]),
            ('company_id', '=', self.env.user.company_id.id)
        ]

    @api.model
    def action_users_custom(self):
        action = self.env.ref('my_auto_assign_sales_purchase.action_users_custom').read()[0]
        action['domain'] = self.get_custom_users_domain()
        return action

    @api.model
    def create(self, vals):
        _logger.info("Creating user with values: %s", vals)

        # 检查是否已有用户存在
        user_count = self.env['res.users'].search_count([])
        is_first_user = user_count == 0

        if is_first_user:
            vals['is_admin'] = True  # 设定管理员标志

        # 检查是否存在临时公司
        temporary_company = self.env['res.company'].search([('name', '=', 'Temporary Company')], limit=1)
        if not temporary_company:
            # 创建临时公司
            temporary_company = self.env['res.company'].create({
                'name': 'Temporary Company',
            })
            _logger.info("Created temporary company: %s", temporary_company.name)

        # 分配临时公司
        vals['company_id'] = temporary_company.id
        vals['company_ids'] = [(4, temporary_company.id)]

        # 创建用户
        user = super(ResUsers, self).create(vals)

        # 获取销售和采购组的引用
        sales_group = self.env.ref('sales_team.group_sale_salesman')
        purchase_group = self.env.ref('purchase.group_purchase_user')
        internal_user_group = self.env.ref('base.group_user')
        multi_company_group = self.env.ref('base.group_multi_company')  # 添加多公司管理组
        settings_group = self.env.ref('base.group_system')  # 确保用户有访问设置菜单的权限

        # 检查是否正确获取到组引用
        if not all([sales_group, purchase_group, internal_user_group, multi_company_group, settings_group]):
            _logger.error("Failed to retrieve one or more groups")
            return user

        _logger.info("Assigning groups to user: %s", user.name)

        # 移除所有用户类型组（以确保没有多个用户类型）
        user_types = self.env['res.groups'].search(
            [('category_id', '=', self.env.ref('base.module_category_user_type').id)])
        user.groups_id = [(3, group.id) for group in user_types]

        # 分配销售、采购、内部用户组和设置组给用户
        user.groups_id = [
            (4, internal_user_group.id),
            (4, sales_group.id),
            (4, purchase_group.id),
            (4, multi_company_group.id),
            (4, settings_group.id),
        ]

        _logger.info("User %s assigned to groups: %s", user.name, user.groups_id)

        return user

    def join_company(self, company_id):
        self.env['company.member.approval'].create({
            'user_id': self.id,
            'company_id': company_id,
            'state': 'pending'
        })
        # Send notification to admin for approval
        admin_user = self.env['res.users'].search([('is_admin', '=', True)], limit=1)
        if admin_user:
            # 使用Odoo内部通知功能发送通知
            admin_user.message_post(
                subject=_("New Company Member Approval Request"),
                body=_("A new member has requested to join your company. Please review the request."),
                message_type='notification',
                partner_ids=[admin_user.partner_id.id]
            )

    def approve_member(self, member_id):
        approval = self.env['company.member.approval'].browse(member_id)
        if approval and approval.state == 'pending':
            approval.state = 'approved'
            approval.user_id.write({'company_id': approval.company_id.id})
            approval.user_id.write({'company_ids': [(4, approval.company_id.id)]})
