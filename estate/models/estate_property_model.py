from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from datetime import timedelta

class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Model for Real-Estate Properties"

    STATE_SELECTION = [
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    state = fields.Selection(STATE_SELECTION, string="State", required=True, default="new", copy=False)

    # New fields for buyer and salesperson
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)

    # Computed field for total area
    total_area = fields.Integer(compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # One2many field for property offers
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # Computed field for best offer
    best_offer = fields.Float(compute="_compute_best_offer")

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped("price"))
            else:
                record.best_offer = 0.0

    # Onchange method for garden field
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # Business logic for canceling a property
    def action_cancel(self):
        for record in self:
            if record.state not in ('new', 'offer_received'):
                raise UserError("You can only cancel properties in 'New' or 'Offer Received' state.")
            record.state = 'canceled'

    # Business logic for setting a property as sold
    def action_set_sold(self):
        for record in self:
            if record.state != 'offer_accepted':
                raise UserError("You can only set properties as 'Sold' when in 'Offer Accepted' state.")
            record.state = 'sold'

    # Python constraint to check selling price cannot be lower than 90% of the expected price
    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if not tools.float_is_zero(record.expected_price, precision_digits=2) and \
               not tools.float_is_zero(record.selling_price, precision_digits=2) and \
               record.selling_price < 0.9 * record.expected_price:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price.")


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
