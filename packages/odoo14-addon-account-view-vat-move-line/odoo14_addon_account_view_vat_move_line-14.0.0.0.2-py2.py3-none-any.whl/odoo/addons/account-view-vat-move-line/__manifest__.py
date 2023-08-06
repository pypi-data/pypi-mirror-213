# -*- coding: utf-8 -*-
{
  'name': "Account Move Line VAT",

  'summary': """
    View VAT on account move line""",

  'author': "Talaios",
  'website': "https://talaios.coop",

  # Categories can be used to filter modules in modules listing
  # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
  # for the full list
  'category': 'manufacturing',
  'version': '14.0.0.0.2',

  # any module necessary for this one to work correctly
  'depends': [
    'base',
    'account',
  ],

  # always loaded
  'data': [
    'views/account_move_line_views.xml',
  ]
}