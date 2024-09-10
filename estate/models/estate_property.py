from odoo import fields, models, api
from datetime import date, timedelta
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Test inmobiliarias"

    name = fields.Char(required=True, copy=False)
    description = fields.Text(copy=False)
    postcode = fields.Char(copy=False)
    date_availability = fields.Date(string='Fecha de disponibilidad', default=lambda self: date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(required=True, copy=False)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientacion',
        selection=[('norte', 'Norte'), ('sur', 'Sur'), ('este', 'Este'), ('oeste', 'Oeste')],
        help="orientacion del jardin")
    active = fields.Boolean(string='Activo', default=True)
    state = fields.Selection(
        string='Estado',
        selection=[('nuevo', 'Nuevo'), ('oferta recibida', 'Oferta recibida'), ('oferta aceptada', 'Oferta aceptada'), ('vendido', 'Vendido'), ('cancelado', 'Cancelado')],
        help="Estado", copy=False, default='nuevo')
    type_ids = fields.Many2one("estate.property.type", string="Tipo")
    nombre = fields.Char(related="type_ids.nombre")
    user_id = fields.Many2one('res.users', string='Salesman', index=True, default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string="Buyer")
    tag_ids = fields.Many2many('estate.property.tag', string='Etiquetas')
    offer_ids = fields.One2many('estate.property.offer', 'id_property', string="ofertas")
    total_area = fields.Integer(compute="_compute_total")
    best_price = fields.Float(compute="_compute_price")

    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_price(self):
        for record in self:
            precios = record.offer_ids.mapped('price')
            mejor_precio = max(precios) if precios else 0
            record.best_price = mejor_precio

    @api.onchange("garden")
    def _onchange_jardin(self):
        if self.garden:
            # Si se marca el checkbox, establecer valores predeterminados
            self.garden_area = 10  # Valor por defecto para el área del jardín
            self.garden_orientation = 'norte'  # Valor por defecto para la orientación
        else:
            # Si se desmarca, limpiar los valores
            self.garden_area = 0
            self.garden_orientation = False

    def sold_property(self):
        for record in self:
            if self.state == "cancelado":
                # si la propiedad esta cancelada no se puede poner como vendida
                raise UserError("No puede vender una propiedad cancelada.")
            else:
                record.state = "vendido"
        return True

    def cancel_property(self):
        for record in self:
            if self.state == "vendido":
                # si la propiedad esta vendida no se puede poner como cancelada
                raise UserError("No puede cancelar una propiedad vendida.")
            else:
                record.state = "cancelado"
        return True

    
    
    