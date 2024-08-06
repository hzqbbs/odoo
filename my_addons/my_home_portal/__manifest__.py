{
    'name': 'My Home Portal Module',
    'version': '1.0',
    'depends': ['portal', 'website', 'auth_signup'],
    'data': [
        'views/portal_my_home_inherit.xml',
        'views/company_select_form.xml',
    ],
    'installable': True,
    'application': False,
}