# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_person_client.exceptions import PersonNotFoundException
from uw_person_client.clients.mock_client import MockedUWPersonClient


class MockedUWPersonClientTest(TestCase):

    def test_get_person_by_uwnetid(self):
        client = MockedUWPersonClient()
        person = client.get_person_by_uwnetid("javerage")
        self.assertEqual(person.uwnetid, "javerage")

        with self.assertRaises(PersonNotFoundException):
            client.get_person_by_uwnetid("foo")

    def test_get_person_by_uwregid(self):
        client = MockedUWPersonClient()
        person = client.get_person_by_uwregid(
            "FE36CCB8F66711D5BE060004AC494FCD")
        self.assertEqual(person.uwnetid, "jbothell")
        self.assertEqual(person.uwregid, "FE36CCB8F66711D5BE060004AC494FCD")

        with self.assertRaises(PersonNotFoundException):
            client.get_person_by_uwregid("foo")

    def test_get_person_by_student_number(self):
        client = MockedUWPersonClient()
        person = client.get_person_by_student_number("1033334")
        self.assertEqual(person.uwnetid, "javerage")
        self.assertEqual(person.uwregid, "9136CCB8F66711D5BE060004AC494FFE")
        self.assertEqual(person.student.student_number, "1033334")

        with self.assertRaises(PersonNotFoundException):
            client.get_person_by_student_number("foo")

    def test_get_person_by_system_key(self):
        client = MockedUWPersonClient()
        person = client.get_person_by_system_key("532353230")
        self.assertEqual(person.uwnetid, "javerage")
        self.assertEqual(person.uwregid, "9136CCB8F66711D5BE060004AC494FFE")
        self.assertEqual(person.student.student_number, "1033334")
        self.assertEqual(person.student.system_key, "532353230")
        with self.assertRaises(PersonNotFoundException):
            client.get_person_by_system_key("foo")

    def test_get_persons(self):
        client = MockedUWPersonClient()
        persons = client.get_persons()
        self.assertEqual(len(persons), 4)
        persons = client.get_persons(page=1, page_size=2)
        self.assertEqual(len(persons), 2)

    def test_get_registered_students(self):
        client = MockedUWPersonClient()
        persons = client.get_registered_students()
        self.assertEqual(len(persons), 2)
        persons = client.get_registered_students(page=1, page_size=1)
        self.assertEqual(len(persons), 1)

    def test_get_active_students(self):
        client = MockedUWPersonClient()
        persons = client.get_active_students()
        self.assertEqual(len(persons), 2)
        persons = client.get_active_students(page=1, page_size=1)
        self.assertEqual(len(persons), 1)

    def test_get_active_employees(self):
        client = MockedUWPersonClient()
        persons = client.get_active_employees()
        self.assertEqual(len(persons), 2)
        persons = client.get_active_employees(page=1, page_size=1)
        self.assertEqual(len(persons), 1)

    def test_get_advisers(self):
        client = MockedUWPersonClient()
        persons = client.get_advisers()
        self.assertEqual(len(persons), 1)

    def test_get_persons_by_adviser_netid(self):
        client = MockedUWPersonClient()
        persons = client.get_persons_by_adviser_netid("jadviser")
        self.assertEqual(len(persons), 2)
        persons = client.get_persons_by_adviser_netid("foo")
        self.assertEqual(len(persons), 0)

    def test_get_persons_by_adviser_regid(self):
        client = MockedUWPersonClient()
        persons = client.get_persons_by_adviser_regid(
            "5136CCB9F66711D5BE060004AC494FF0")
        self.assertEqual(len(persons), 2)
        persons = client.get_persons_by_adviser_regid("foo")
        self.assertEqual(len(persons), 0)

    def test_person_includes(self):
        client = MockedUWPersonClient()
        filters = {"include_student_transcripts": False,
                   "include_student_transfers": False,
                   "include_student_sports": False,
                   "include_student_advisers": False,
                   "include_student_majors": False,
                   "include_student_pending_majors": False,
                   "include_student_holds": False,
                   "include_student_degrees": False}
        person = client.get_person_by_student_number("1033334", **filters)
        self.assertFalse(hasattr(person.student, "transcripts"))
        self.assertFalse(hasattr(person.student, "transfers"))
        self.assertFalse(hasattr(person.student, "sports"))
        self.assertFalse(hasattr(person.student, "advisers"))
        self.assertFalse(hasattr(person.student, "majors"))
        self.assertFalse(hasattr(person.student, "pending_majors"))
        self.assertFalse(hasattr(person.student, "holds"))
        self.assertFalse(hasattr(person.student, "degrees"))

        person = client.get_person_by_student_number("1033334",
                                                     include_student=False)
        self.assertFalse(hasattr(person, "student"))

        person = client.get_person_by_uwnetid("bill",
                                              include_student=False,
                                              include_employee=False)
        self.assertFalse(hasattr(person, "employee"))
