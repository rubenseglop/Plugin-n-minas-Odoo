from odoo import models, fields, api


class Nominas(models.Model):
    _name = 'nominas.nominas'

    empleado = fields.Many2one('nominas.empleados', 'Empleado')
    dias = fields.Selection(selection=[('M', '1 mes'), ('Q', '15 dias')], default='M')
    nominaorigen = fields.Integer('Nómina', compute='_traenomina')
    nominatotal = fields.Integer('Nomina Total', compute='_calculo')

    def name_get(self):
        res=[]
        for record in self:
            name = record.empleado
            res.append((record.id, name))
        return res

    @api.one
    @api.depends('empleado','nominaorigen','dias')

    def _traenomina(self):
        cursor = self.env.cr
        cargoselect: int = int(self.empleado)
        if cargoselect is False:
            self.totalnomina = 6
        else:
            cursor.execute(
                "select salariobase+comisionplus from nominas_empleados inner join nominas_cargo on nominas_empleados.cargo = nominas_cargo.id inner join nominas_plus on nominas_empleados.plus = nominas_plus.id where nominas_empleados.id =%s",(cargoselect,))
            for x in cursor.fetchall():
                self.nominaorigen = int(x[0])
                self.nominatotal = int(x[0]/2)
                if (self.dias == 'M'):
                    self.nominatotal = int(x[0])

    def _calculo(self):
        if (self.dias == 'Q'):
            self.nominatotal = self.nominaorigen / 2
        else:
            self.nominatotal = self.nominaorigen