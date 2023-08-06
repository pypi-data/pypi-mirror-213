{
    'name': 'HR Attendance Mitxelena',
    'version': '14.0.1.0.2',
    'category': 'Human Resources',
    'sequence': 20,
    'summary': 'Employee Attendances Customizations for Mitxelena',
    'description': """
Customizations of Employee Attendances for Mitxelena
====================================================
This module includes customizations for handling employee attendances at Mitxelena, 
including custom rules for shifts, public holidays and calculation of extra hours.
""",
    'website': 'https://www.coopdevs.org',
    'author': 'Coopdevs',
    'depends': [
        'base',
        'hr',
        'hr_attendance',
        'hr_holidays_public',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_attendance_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
