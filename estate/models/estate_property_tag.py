from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Model for Real-Estate Property Tags"

    name = fields.Char(string="Tag Name", required=True, translate=True)
    color = fields.Integer(string="Color Index", default=0)

    # SQL Constraint
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'Tag name must be unique!'),
    ]
