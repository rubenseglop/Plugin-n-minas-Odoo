from odoo import models, fields, api


class Plus(models.Model):
    _name = 'nominas.plus'

    nombreplus = fields.Char('Nombre plus', required=True)
    comisionplus = fields.Integer('Euros', required=False)

    def name_get(self):
        res=[]
        for record in self:
            name = record.nombreplus
            res.append((record.id, name))
        return res