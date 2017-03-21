# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class generate_faktur_pajak(models.TransientModel):
    _name = 'generate.faktur.pajak'
    _description = "Generate Faktur Pajak"

    nomor_faktur_awal = fields.Char(string='Nomor Faktur Awal', size=20)
    nomor_faktur_akhir = fields.Char(string='Nomor Faktur Akhir', size=20)
    strip = fields.Char(string='Strip', size=3, default='-')
    dot = fields.Char(string='Dot', size=3, default='.')
    strip2 = fields.Char(string='Strip', size=3, default='-')
    dot2 = fields.Char(string='Dot', size=3, default='.')
    nomor_perusahaan = fields.Char(string='Nomor Perusahaan', size=3, required=True, default='010')
    nomor_awal = fields.Char(string='Nomor Faktur Awal', size=8, required=True)
    nomor_akhir = fields.Char(string='Nomor Faktur Akhir', size=8, required=True)
    tahun = fields.Char(string='Tahun Penerbit', size=2, required=True, default=lambda self: fields.Date.from_string(fields.Date.context_today(self)).strftime('%y'))
    pajak_type = fields.Selection([('in', 'Faktur Pajak Masukan'), ('out', 'Faktur Pajak Keluaran')], string='Type', default='out')

    @api.multi
    def generate_faktur(self, vals):
        pajak_obj = self.env['faktur.pajak']
        awal = int(self.nomor_awal)
        akhir = int(self.nomor_akhir)
        while (awal <= akhir):
            vals = {
                'nomor_perusahaan': self.nomor_perusahaan,
                'tahun_penerbit': self.tahun,
                'nomor_urut': '%08d' % awal,
                'state': '0',
                'pajak_type': self.pajak_type,
                }
            pajak_obj.create(vals)
            awal += 1
        return {'type': 'ir.actions.act_window_close'}
