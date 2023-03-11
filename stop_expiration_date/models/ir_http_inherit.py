import datetime
from odoo import models
from odoo.http import request
from dateutil.relativedelta import relativedelta


class HttpInherit(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        ICP = request.env['ir.config_parameter'].sudo()
        User = request.env['res.users']

        if User.has_group('base.group_system'):
            warn_enterprise = 'admin'
        elif User.has_group('base.group_user'):
            warn_enterprise = 'user'
        else:
            warn_enterprise = False

        result = super(HttpInherit, self).session_info()
        result['support_url'] = "https://www.odoo.com/help"
        if warn_enterprise:
            result['warning'] = warn_enterprise
            result['expiration_date'] = str(datetime.datetime.now() + relativedelta(months=+1))
            result['expiration_reason'] = ICP.get_param('database.expiration_reason')

        return result


