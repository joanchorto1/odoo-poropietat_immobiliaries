from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string='Nom', required=True)
    description = fields.Text(string='Descripció')
    postal_code = fields.Char(string='Codi postal', required=True)
    availability_date = fields.Date(string='Data de disponibilitat', default=lambda self: fields.Date.today() + timedelta(days=30))
    expected_sale_price = fields.Float(string='Preu de venda esperat', digits=(10, 2))
    sale_price = fields.Float(string='Preu de venda', digits=(10, 2), readonly=True, copy=False)
    best_offer = fields.Float(string='Millor oferta', compute='_compute_best_offer', readonly=True, store=True)
    state = fields.Selection([('new', 'Nova'), ('offer_received', 'Oferta Rebuda'),('offer_accepted', 'Oferta Acceptada'),('sold', 'Venuda'),('cancelled', 'Cancel·lada')], string='Estat', default='new')
    num_bedrooms = fields.Integer(string='Nombre habitacions', required=True)
    property_type_id = fields.Many2one('estate.property.type', string='Tipus')
    tag_ids = fields.Many2many('estate.property.tag', string='Etiquetes')
    elevator = fields.Boolean(string='Ascensor', default=False)
    parking = fields.Boolean(string='Parking', default=False)
    renovated = fields.Boolean(string='Renovat', default=False)
    num_bathrooms = fields.Integer(string='Banys')
    surface_area = fields.Float(string='Superfície', required=True, digits=(10, 2))
    price_per_sqm = fields.Float(string='Preu per m2', compute='_compute_price_per_sqm', readonly=True, store=True)
    construction_year = fields.Integer(string='Any de construcció')
    energy_certificate = fields.Selection([('A', 'A'),('B', 'B'),('C', 'C'),('D', 'D'),('E', 'E'),('F', 'F'),('G', 'G')], string='Certificat energètic')
    active = fields.Boolean(default=True, invisible=True)
    offers = fields.One2many('estate.property.offer', 'property_id', string='Ofertes')
    buyer = fields.Many2one('res.partner', string='Comprador')
    salesman = fields.Many2one('res.users', string='Comercial', default=lambda self: self.env.user)

    @api.depends('offers.price', 'offers.state')
    def _compute_best_offer(self):
        for property_record in self:
            best_offer = 0.0
            for offer in property_record.offers.filtered(lambda o: o.state != 'rejected'):
                if offer.price > best_offer:
                    best_offer = offer.price
            property_record.best_offer = best_offer

    @api.depends('surface_area', 'expected_sale_price')
    def _compute_price_per_sqm(self):
        for property_record in self:
            if property_record.surface_area != 0:
                property_record.price_per_sqm = property_record.expected_sale_price / property_record.surface_area
            else:
                property_record.price_per_sqm = 0.0

    @api.depends('offers.state')
    def _compute_state(self):
        for property_record in self:
            if any(offer.state == 'offer_accepted' for offer in property_record.offers):
                property_record.state = 'offer_accepted'
            elif any(offer.state == 'offer_received' for offer in property_record.offers):
                property_record.state = 'offer_received'
            else:
                property_record.state = 'new'
                
    def write(self, vals):
        for property_record in self:
            if property_record.state == 'offer_accepted':
                raise UserError("No es pot modificar una propietat amb una oferta acceptada.")
        return super(EstateProperty, self).write(vals)

    
                