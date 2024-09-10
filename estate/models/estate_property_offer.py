from odoo import fields, models, api
from datetime import date, timedelta

class EstateProperty(models.Model):
    _name = "estate.property.offer"
    _description = "Ofertas a la propiedad"

    price = fields.Float(required=True, copy=False)
    estado = fields.Selection(
        string='',
        selection=[('aceptado', 'Aceptado'), ('rechazado', 'Rechazado')],
        help="Estatus de la oferta", copy=False)
    socio_id = fields.Many2one('res.partner', string="Partner")
    id_property = fields.Many2one('estate.property', string='Propiedad')
    validity = fields.Integer(default=2)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity","create_date")
    def _compute_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                # Sumar 10 días a la fecha de inicio
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = False
                
    @api.depends("validity","create_date")
    def _inverse_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                # Calcular la diferencia en días
                diferencia = (record.date_deadline - record.create_date.date()).days
                record.validity = diferencia
            else:
                record.validity = 0

    def action_confirm(self):
        for record in self:
            record.estado = "aceptado"
        return True

    def action_refused(self):
        for record in self:
            record.estado = "rechazado"
        return True
    
    