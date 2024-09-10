from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property.tag"
    _description = "Etiquetas"

    etiqueta = fields.Char(string='etiqueta')