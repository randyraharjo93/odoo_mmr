# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    nomor_faktur_pajak = fields.Char(string='Nomor Faktur Pajak', size=19)
    faktur_pajak = fields.Many2one('faktur.pajak', string="Faktur Pajak", domain=[('state', '=', '0')])

    @api.multi
    def action_create_faktur(self):
        faktur_obj = self.env['faktur.pajak']
        date = fields.Date.context_today(self)

        for inv in self:
            if inv.type == 'out_invoice':
                vals = {
                    'date_used': date,
                    'invoice_id': inv.id,
                    'partner_id': inv.partner_id.id,
                    'pajak_type': 'out',
                    'dpp': inv.amount_untaxed or 0.0,
                    'tax_amount': inv.amount_tax or 0.0,
                    'currency_id': inv.currency_id.id,
                    'state': '1',
                    'company_id': inv.company_id.id,
                    }
                inv.faktur_pajak.write(vals)
            if inv.type == 'in_invoice':
                if inv.nomor_faktur_pajak:
                    kode_pt = inv.nomor_faktur_pajak[:3]
                    kode_cabang = inv.nomor_faktur_pajak[3:6]
                    tahun = inv.nomor_faktur_pajak[6:8]
                    nomor_fp = inv.nomor_faktur_pajak[-8:]
                    vals = {
                        'date_used': date,
                        'invoice_id': inv.id,
                        'partner_id': inv.partner_id.id,
                        'pajak_type': 'in',
                        'dpp': inv.amount_untaxed or 0.0,
                        'tax_amount': inv.amount_tax or 0.0,
                        'currency_id': inv.currency_id.id,
                        'state': '1',
                        'nomor_perusahaan': kode_pt,
                        'kode_cabang': kode_cabang,
                        'tahun_penerbit': tahun,
                        'nomor_urut': nomor_fp,
                        'company_id': inv.company_id.id,
                        }
                    # Find first if this number already used
                    if len(self.env['faktur.pajak'].search([('tahun_penerbit', '=', tahun), ('kode_cabang', '=', kode_cabang), ('nomor_urut', '=', nomor_fp)])) > 0:
                        raise UserError(_('Faktur Pajak with this number already exist.'))
                    faktur_obj.create(vals)

    @api.multi
    def action_invoice_open(self):
        for inv in self:
            inv.action_create_faktur()
        return super(AccountInvoice, self).action_invoice_open()
