# auto_assign_sales_purchase/__manifest__.py
{
    'name': 'Auto Assign Sales and Purchase Groups',
    'version': '1.0',
    'category': 'Customization',
    'summary': 'Automatically assign sales, purchase, and website groups to new users',
    'description': """
        This module automatically assigns the sales and purchase groups to newly created users.
    """,
    'author': 'He Zhongqing',
    'depends': ['base', 'sale', 'purchase', 'website'],
    'data': [
        'views/company_member_approval_views.xml',
        'views/res_users_views.xml',
        'security/ir.model.access.csv',
        'security/res_users_security.xml',
        'security/record_rules.xml',
    ],
    'installable': True,
    'application': False,
}