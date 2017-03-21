# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    nomor_faktur_pajak = fields.Char(string='Nomor Faktur Pajak', size=16)
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
                    }
                inv.faktur_pajak.write(vals)
            if inv.type == 'in_invoice':
                if inv.nomor_faktur_pajak:
                    kode_pt = inv.nomor_faktur_pajak[:3]
                    tahun = inv.nomor_faktur_pajak[4:6]
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
                        'tahun_penerbit': tahun,
                        'nomor_urut': nomor_fp,
                        }
                    faktur_obj.create(vals)

    @api.multi
    def action_invoice_open(self):
        for inv in self:
            inv.action_create_faktur()
        return super(AccountInvoice, self).action_invoice_open()
