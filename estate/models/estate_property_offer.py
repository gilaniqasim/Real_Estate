from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Model for Real-Estate Property Offers"

    property_id = fields.Many2one("estate.property", string="Property", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    price = fields.Float(required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Status", required=True, default="draft")

    # Business logic for accepting an offer
    def action_accept(self):
        for record in self:
            if record.state != 'draft':
                raise UserError("You can only accept offers in 'Draft' state.")
            record.state = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

    # Business logic for refusing an offer
    def action_refuse(self):
        for record in self:
            if record.state != 'draft':
                raise UserError("You can only refuse offers in 'Draft' state.")
            record.state = 'refused'

    # SQL Constraints
    _sql_constraints = [
        ('price_positive', 'CHECK (price >= 0)', 'The offer price must be positive.'),
    ]
