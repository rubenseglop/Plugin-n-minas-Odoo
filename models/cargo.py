from odoo import models, fields, api


class Cargo(models.Model):
    _name = 'nominas.cargo'

    nombrecargo = fields.Char('Cargo', required=True)
    salariobase = fields.Integer('Salario base', required=False)

    def name_get(self):
        res=[]
        for record in self:
            name = record.nombrecargo
            res.append((record.id, name))
        return res