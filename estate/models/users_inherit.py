from odoo import fields, models


class UsersInherit(models.Model):

    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property", "salesperson_id", string="Properties"
    )
