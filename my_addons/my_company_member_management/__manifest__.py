# auto_assign_sales_purchase/__manifest__.py
{
    'name': 'Company Member Management',
    'version': '1.0',
    'category': 'Customization',
    'summary': 'Automatically assign sales, purchase, and website groups to new users',
    'description': """
        This module automatically assigns the sales and purchase groups to newly created users.
    """,
    'author': 'He Zhongqing',
    'depends': ['base', 'sale', 'purchase', 'portal', 'website', 'auth_signup'],
    'data': [
        'security/res_users_security.xml',
        'security/record_rules.xml',
        'security/record_groups.xml',
        'security/ir.model.access.csv',
        'views/company_member_approval_views.xml',
        'views/res_users_views.xml',
        'views/portal_my_home_inherit.xml',
        'views/company_select_form.xml',
    ],
    'installable': True,
    'application': False,
}