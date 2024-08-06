from odoo import http
from odoo.http import request


class MyCompany(http.Controller):

    @http.route('/company/select', type='http', auth='user', website=True)
    def company_select_form(self, **kw):
        companies = request.env['res.company'].sudo().search([])
        return request.render('my_home_portal.company_select_form', {'companies': companies})

    @http.route('/company/select/submit', type='http', auth='user', methods=['POST'], website=True)
    def company_select_submit(self, **kw):
        user = request.env.user
        company_id = kw.get('company_id')
        company_name = kw.get('company_name')

        if company_id:
            # 用户选择加入现有公司
            existing_company = request.env['res.company'].sudo().browse(int(company_id))
            user.sudo().write({'company_id': existing_company.id, 'company_ids': [(4, existing_company.id)]})
        elif company_name:
            # 用户选择创建新公司
            new_company = request.env['res.company'].sudo().create({
                'name': company_name,
            })
            user.sudo().write({'company_id': new_company.id, 'company_ids': [(4, new_company.id)]})

        return request.redirect('/my/home')
