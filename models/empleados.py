from odoo import models, fields, api


class Empleados(models.Model):
    _name = 'nominas.empleados'

    dni = fields.Integer('dni', required=True)
    foto = fields.Binary("Imagen", help="Insertar una foto")
    nombre = fields.Char('Nombre', required=True)
    apellidos = fields.Char('Apellidos', required=True)
    sexo = fields.Selection(selection=[('H', 'Hombre'),('M', 'Mujer')])
    cargo = fields.Many2one('nominas.cargo', 'Cargo')
    plus = fields.Many2one('nominas.plus', 'Plus')
    domicilio = fields.Char('Domicilio', required=True)
    totalnomina = fields.Float(string='Euros total Nómina', compute='_total')

    def name_get(self):
        res=[]
        for record in self:
            name = record.nombre
            res.append((record.id, name))
        return res

    @api.one
    @api.depends('cargo', 'plus')
    def _total(self):
        cursor = self.env.cr
        cargoselect = (self.cargo.nombrecargo)
        plusselect = (self.plus.nombreplus)
        if cargoselect is False:
            self.totalnomina = 0
        else:
            cargoselect: str = str(self.cargo.nombrecargo)
            cursor.execute("select salariobase from nominas_cargo where nombrecargo=%s", (cargoselect,))
            for x in cursor.fetchall():
                self.totalnomina= x[0]
        if plusselect is False:
            self.totalnomina = self.totalnomina
        else:
            plusselect: str = str(self.plus.nombreplus)
            cursor.execute("select comisionplus from nominas_plus where nombreplus=%s", (plusselect,))
            for x in cursor.fetchall():
                self.totalnomina = self.totalnomina + x[0]
