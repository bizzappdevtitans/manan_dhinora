from datetime import date

from odoo.tests.common import TransactionCase


class TestSchoolTeacher(TransactionCase):
    def setUp(self):
        super(TestSchoolTeacher, self).setUp()
        self.teacher_record = self.env["school.teacher"].create(
            {
                "teacher_name": "Michael Scott",
                "employee_email": "michael.scott@dundermifflin.co.us",
                "work_exprience": 12,
            }
        )

        self.student_record = self.env["school.student"].create(
            {
                "student_name": "Manan",
                "student_date_of_birth": date.today(),
                "class_teacher_id": self.teacher_record.id,
            }
        )

    def test_01_salary_compute(self):
        """validating that weather the calulatd salary is the expected value #T00476"""
        exprience = [2, 4, 6, 8]
        salary = [15000, 20000, 40000, 80000]
        for element in zip(exprience, salary):
            exprience, salary = element
            self.teacher_record.write({"work_exprience": exprience})
            self.assertEqual(
                self.teacher_record.teacher_salary,
                salary,
                "the salary logic is incorrect",
            )

    def test_02_buttons(self):
        """validating that weather the buttonswork as intended #T00476"""
        self.teacher_record.wiz_teacher_leave()
        self.assertEqual(
            self.teacher_record.student_count,
            1,
            "incorrect student count based on linked records(one2many)",
        )
        self.teacher_record.action_student_count()

    def test_03_day_joined_cron(self):
        """validating that cron is working and is giving
        is the expected value #T00476"""
        self.assertEqual(
            self.teacher_record.cron_day_counter(),
            self.teacher_record.days_from_joining,
            "the numberdays joined calculation is true",
        )

    def test_04_unlinked_archive(self):
        """testing for weather the unlinked records are indeed stored in
        former.teacher object $T00476"""
        record_sequence = self.teacher_record.employee_number
        self.teacher_record.unlink()
        self.assertEqual(
            self.env["former.teachers"].search_count(
                [("former_employee_number", "=", record_sequence)]
            ),
            1,
            "former record not created",
        )

    def test_05_leave_application_wizard(self):
        """calling the wizard to check if the wizard action is running by
        checking coverage #T00476"""
        self.teacher_record.wiz_teacher_leave()

    def test_06_name_get(self):
        """testing that the name found after running name_get is as expected #T00476"""
        self.assertFalse(
            "Michael Scott - michael.scott@dundermifflin.co.us"
            in self.teacher_record.name_get(),
            "created name_get name is incorrect",
        )
