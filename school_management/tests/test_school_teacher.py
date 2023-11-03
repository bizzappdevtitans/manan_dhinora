from datetime import date

from odoo.tests.common import TransactionCase


class TestSchoolTeacher(TransactionCase):
    def setUp(self):
        super(TestSchoolTeacher, self).setUp()
        self.teacher_record = self.teacher_record_1 = self.env["school.teacher"].create(
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
        self.teacher_record.wiz_teacher_leave()
        self.env["school.student"].create(
            {
                "student_name": "Manan",
                "student_date_of_birth": date.today(),
                "class_teacher_id": self.teacher_record.id,
            }
        )
        self.assertEqual(
            self.teacher_record.student_count,
            1,
            "incorrect student count based on linked records(one2many)",
        )
        self.teacher_record.action_student_count()

    def test_03_day_joined_cron(self):
        self.assertEqual(
            self.teacher_record.cron_day_counter(),
            0,
            "the numberdays joined calculation is true",
        )

    def test_04_server_action(self):
        self.assertEqual(
            self.teacher_record.state, "draft", "serveaction doesn't work as intended"
        )
        # TODO winf a way to test for both the validation errors
        self.teacher_record.action_validate()

    def test_05_unlinked_archive(self):
        record_sequence = self.teacher_record.employee_number
        self.teacher_record.unlink()
        self.assertEqual(
            self.env["former.teachers"].search_count(
                [("former_employee_number", "=", record_sequence)]
            ),
            1,
            "former record not created",
        )
