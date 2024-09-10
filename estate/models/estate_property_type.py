from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property.type"
    _description = "Tipo de inmueble"

    nombre = fields.Char(required=True)