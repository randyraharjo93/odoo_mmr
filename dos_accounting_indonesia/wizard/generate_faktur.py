# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class generate_faktur_pajak(models.TransientModel):
    _name = 'generate.faktur.pajak'
    _description = "Generate Faktur Pajak"

    nomor_perusahaan = fields.Char(string='Nomor Perusahaan', size=3, required=True, default='010')
    kode_cabang = fields.Char(string='Kode Cabang', size=3, required=True, default='001')
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
                'kode_cabang': self.kode_cabang,
                'state': '0',
                'pajak_type': self.pajak_type,
                'company_id': self.env.user.company_id.id,
            }
            pajak_obj.create(vals)
            awal += 1
        return {'type': 'ir.actions.act_window_close'}
