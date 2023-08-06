# -*- coding: utf-8 -*-
from odoo import models, fields

class chips(models.Model):
    _inherit = 'account.move.line'
    
    partner_vat = fields.Char('NIF', related='partner_id.vat')
   