# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
import base64
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    mmr_written_amount_total = fields.Char(string='Written Amount Total')

    @api.model
    def create(self, vals):
        rec = super(AccountInvoice, self).create(vals)
        if rec.amount_total:
            def Terbilang(x):
                satuan=["","Satu","Dua","Tiga","Empat","Lima","Enam","Tujuh", "Delapan","Sembilan","Sepuluh","Sebelas"]
                n = int(x)
                if n >= 0 and n <= 11:
                    Hasil = " " + satuan[n]
                elif n >= 12 and n <= 19:
                    Hasil = Terbilang(n % 10) + " Belas"
                elif n >= 20 and n <= 99:
                    Hasil = Terbilang(n / 10) + " Puluh" + Terbilang(n % 10)
                elif n >= 100 and n <= 199:
                    Hasil = " Seratus" + Terbilang(n - 100)
                elif n >= 200 and n <= 999:
                    Hasil = Terbilang(n / 100) + " Ratus" + Terbilang(n % 100)
                elif n >= 1000 and n <= 1999:
                    Hasil = " Seribu" + Terbilang(n - 1000)
                elif n >= 2000 and n <= 999999:
                    Hasil = Terbilang(n / 1000) + " Ribu" + Terbilang(n % 1000)
                elif n >= 1000000 and n <= 999999999:
                    Hasil = Terbilang(n / 1000000) + " Juta" + Terbilang(n % 1000000)
                else:
                    Hasil = Terbilang(n / 1000000000) + " Milyar" + Terbilang(n % 100000000)
                return Hasil
            rec.mmr_written_amount_total = Terbilang(rec.amount_total)
        return rec

    @api.multi
    def write(self, vals):
        result = super(AccountInvoice, self).write(vals)
        if 'mmr_written_amount_total' not in vals:
            def Terbilang(x):
                satuan=["","Satu","Dua","Tiga","Empat","Lima","Enam","Tujuh", "Delapan","Sembilan","Sepuluh","Sebelas"]
                n = int(x)
                if n >= 0 and n <= 11:
                    Hasil = " " + satuan[n]
                elif n >= 12 and n <= 19:
                    Hasil = Terbilang(n % 10) + " Belas"
                elif n >= 20 and n <= 99:
                    Hasil = Terbilang(n / 10) + " Puluh" + Terbilang(n % 10)
                elif n >= 100 and n <= 199:
                    Hasil = " Seratus" + Terbilang(n - 100)
                elif n >= 200 and n <= 999:
                    Hasil = Terbilang(n / 100) + " Ratus" + Terbilang(n % 100)
                elif n >= 1000 and n <= 1999:
                    Hasil = " Seribu" + Terbilang(n - 1000)
                elif n >= 2000 and n <= 999999:
                    Hasil = Terbilang(n / 1000) + " Ribu" + Terbilang(n % 1000)
                elif n >= 1000000 and n <= 999999999:
                    Hasil = Terbilang(n / 1000000) + " Juta" + Terbilang(n % 1000000)
                else:
                    Hasil = Terbilang(n / 1000000000) + " Milyar" + Terbilang(n % 100000000)
                return Hasil
            self.mmr_written_amount_total = Terbilang(self.amount_total)
        return result
