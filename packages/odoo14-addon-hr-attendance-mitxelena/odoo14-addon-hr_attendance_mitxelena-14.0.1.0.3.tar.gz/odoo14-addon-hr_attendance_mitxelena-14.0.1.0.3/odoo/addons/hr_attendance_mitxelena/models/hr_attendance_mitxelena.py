from odoo import api, fields, models, _
from datetime import timedelta
from pytz import timezone
from collections import defaultdict
from logging import getLogger
_logger = getLogger(__name__)


class HrAttendanceMitxelena(models.Model):
    _inherit = 'hr.attendance'

    is_holiday = fields.Boolean(compute='_compute_is_holiday', store=True)
    shift_type = fields.Selection([
        ('', _('Unknown')),
        ('morning', _('Morning')),
        ('afternoon', _('Afternoon')),
        ('night', _('Night')),
    ], compute='_compute_shift_type', store=True)

    consecutive_days = fields.Integer(
        compute='_compute_consecutive_days', store=True)

    @api.depends('check_in')
    def _compute_is_holiday(self):
        holiday_model = self.env['hr.holidays.public']
        for record in self:
            if record.check_in:
                # Calcular si es festivo en función de la fecha de entrada
                record.is_holiday = holiday_model.is_public_holiday(
                    record.check_in.date())
            else:
                # Si no hay fecha de entrada, no se puede calcular si es festivo
                record.is_holiday = False

    @api.depends('check_out')
    def _compute_shift_type(self):
        # Get user timezone, or use Europe/Madrid as default
        tz = timezone(self.env.user.tz or 'Europe/Madrid')
        for record in self:
            if record.check_in and record.check_out:
                # Convert check_in and check_out to local time
                check_in = record.check_in.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
                check_out = record.check_out.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
                midpoint = check_in + (check_out - check_in) / 2
                hour = midpoint.hour
                if 5 <= hour < 13:
                    record.shift_type = 'morning'
                elif 13 <= hour < 21:
                    record.shift_type = 'afternoon'
                else:
                    record.shift_type = 'night'

    @api.depends('check_in', 'shift_type', 'worked_hours')
    def _compute_consecutive_days(self):
        for record in self:
            if record.check_in:
                # Get the last 7 days range
                datetime_end = record.check_in
                datetime_start = datetime_end - timedelta(days=6)

                # Only select attendances where worked_hours > 0.5 hours to avoid erroneous short attendances
                attendance_records = self.env['hr.attendance'].search([
                    ('employee_id', '=', record.employee_id.id),
                    ('check_in', '>=', datetime_start),
                    ('check_in', '<=', datetime_end),
                    ('worked_hours', '>', 0.5)
                ], order='check_in desc')

                previous_record = None
                consecutive_days = 0
                for rec in attendance_records:
                    date = rec.check_in.date()

                    # If there is a previous record and it's on the same day
                    if previous_record and previous_record.check_in.date() == date:
                        # Check if the start time of the last shift of the day is at least 4 hours after the end of the previous record
                        time_difference = rec.check_in - previous_record.check_out
                        if time_difference >= timedelta(hours=6):
                            consecutive_days += 1

                    # If the day is not consecutive with the previous one, break the loop
                    elif previous_record and previous_record.check_in.date() - date > timedelta(days=1):
                        break

                    else:
                        consecutive_days += 1

                    previous_record = rec

                record.consecutive_days = consecutive_days


    def recompute_all(self):
        # Get all records  from hr.attendance and iterate over them
        attendance_records = self.env['hr.attendance'].search([])
        _logger.debug('Attendance records: %s', attendance_records)
        for record in attendance_records:
            _logger.debug('Updating is_holiday for')
            record.is_holiday = record._compute_is_holiday()
            _logger.debug('Updating shift_type for', record)
            record.shift_type = record._compute_shift_type()
            _logger.debug('Shift type: %s', record.shift_type)
