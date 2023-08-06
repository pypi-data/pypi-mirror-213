from odoo import api, fields, models, _
from datetime import datetime, timedelta
from pytz import timezone

class HrAttendanceMitxelena(models.Model):
    _inherit = 'hr.attendance'

    is_holiday = fields.Boolean(compute='_compute_is_holiday', store=True)
    shift_type = fields.Selection([
        ('', _('Unknown')),
        ('morning', _('Morning')),
        ('afternoon', _('Afternoon')),
        ('night', _('Night')),
    ], compute='_compute_shift_type', store=True)

    consecutive_days = fields.Integer(compute='_compute_consecutive_days', store=True)

    @api.depends('check_in')
    def _compute_is_holiday(self):
        holiday_model = self.env['hr.holidays.public']
        for record in self:
            if record.check_in:
                # Calcular si es festivo en función de la fecha de entrada
                record.is_holiday = holiday_model.is_public_holiday(record.check_in.date())
            else:
                # Si no hay fecha de entrada, no se puede calcular si es festivo
                record.is_holiday = False

    @api.depends('check_out')
    def _compute_shift_type(self):
        tz = timezone(self.env.user.company_id.tz or 'UTC')  # Get company timezone, or use UTC as default
        for record in self:
            if record.check_in and record.check_out:
                # Convert check_in and check_out to local time
                check_in = record.check_in.replace(tzinfo=timezone('UTC')).astimezone(tz)
                check_out = record.check_out.replace(tzinfo=timezone('UTC')).astimezone(tz)
                midpoint = check_in + (check_out - check_in) / 2
                hour = midpoint.hour
                if 5 <= hour < 13:
                    record.shift_type = 'morning'
                elif 13 <= hour < 21:
                    record.shift_type = 'afternoon'
                else:
                    record.shift_type = 'night'

    @api.depends('check_in')
    def _compute_consecutive_days(self):
        for record in self:
            if record.check_in:
                # Obtain attendance records of the last 6 days (including the current day and time)
                datetime_end = record.check_in
                datetime_start = datetime_end - timedelta(days=6)
                attendance_records = self.env['hr.attendance'].search([
                    ('employee_id', '=', record.employee_id.id),
                    ('check_in', '>=', datetime_start),
                    ('check_in', '<=', datetime_end),
                ])

                # Use a set to store unique check_in dates and times
                check_in_dates = set()
                for rec in attendance_records:
                    check_in_dates.add(rec.check_in)

                # Number of unique check_in dates and times is the count of consecutive days and hours
                record.consecutive_days = len(check_in_dates)
