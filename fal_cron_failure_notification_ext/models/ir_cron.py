from odoo import api, models
import datetime


class IrCron(models.Model):
    _inherit = "ir.cron"

    @api.model
    def _callback(self, model_name, method_name, args, job_id):
        res = super(IrCron, self)._callback(
            model_name, method_name, args, job_id)
        _error = ''
        if model_name in self.env:
            model = self.env[model_name]
            if not hasattr(model, method_name):
                _error = 'Method %s.%s does not exist.' % \
                    (model_name, method_name)
        else:
            _error = 'Model %r does not exist.' % model_name
        if _error:
            my_cron = self.browse(job_id)
            self.env['logs.action'].create({
                'name': my_cron.name,
                'method': my_cron.model,
                'object_action': my_cron.function,
                'exec_date': datetime.datetime.now(),
                'error_details': _error,
            })
        return res
