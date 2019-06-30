from odoo import models, api, _
from odoo.exceptions import UserError


class ValidateAccountMove(models.TransientModel):
    _name = "unvalidate.account.move"
    _description = "Unvalidate Account Move"

    @api.multi
    def unvalidate_move(self):
        context = dict(self._context or {})
        moves = self.env['account.move'].browse(context.get('active_ids'))
        move_to_unpost = self.env['account.move']
        for move in moves:
            if move.state == 'posted':
                move_to_unpost += move
        if not move_to_unpost:
            raise UserError(_('There is no journal items in posted state to draft.'))
        move_to_unpost.button_cancel()
        return {'type': 'ir.actions.act_window_close'}
