# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import json
import glob
import os
from uw_person_client.clients import AbstractUWPersonClient
from uw_person_client.components import Person
from uw_person_client.exceptions import PersonNotFoundException


class MockedUWPersonClient(AbstractUWPersonClient):
    paths = []

    @classmethod
    def register_mock_path(self, path):
        if path not in MockedUWPersonClient.paths:
            MockedUWPersonClient.paths.append(path)

    def get_registered_paths(self):
        return MockedUWPersonClient.paths

    def _get_mock_paths(self):
        default_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../fixtures/'))
        return self.get_registered_paths() + [default_path]

    def _read_person_file(self, search_value,  **kwargs):
        """Return first matching mocked person record
        """
        for path in self._get_mock_paths():
            files = glob.glob(os.path.join(path, search_value), recursive=True)
            try:
                return self._load_person_from_file(files[0],  **kwargs)
            except IndexError:
                pass

        raise PersonNotFoundException()

    def _read_person_files(self, search_value,  **kwargs):
        """Return all matching mocked person records
        First matched uwnetid in record wins
        """
        persons = {}
        for path in self._get_mock_paths():
            for file_name in glob.glob(
                    os.path.join(path, search_value), recursive=True):
                person = self._load_person_from_file(file_name,  **kwargs)
                if person.uwnetid not in persons:
                    persons[person.uwnetid] = person

        return list(persons.values())

    def _load_person_from_file(self, filename,  **kwargs):
        person = Person().from_dict(json.load(open(filename)))
        if not kwargs.get('include_employee', True):
            self._delete_attr(person, "employee")
        if not kwargs.get('include_student', True):
            self._delete_attr(person, "student")
        else:
            if not kwargs.get('include_student_transcripts', True):
                self._delete_attr(person.student, "transcripts")
            if not kwargs.get('include_student_transfers', True):
                self._delete_attr(person.student, "transfers")
            if not kwargs.get('include_student_sports', True):
                self._delete_attr(person.student, "sports")
            if not kwargs.get('include_student_advisers', True):
                self._delete_attr(person.student, "advisers")
            if not kwargs.get('include_student_majors', True):
                self._delete_attr(person.student, "majors")
            if not kwargs.get('include_student_pending_majors', True):
                self._delete_attr(person.student, "pending_majors")
            if not kwargs.get('include_student_holds', True):
                self._delete_attr(person.student, "holds")
            if not kwargs.get('include_student_degrees', True):
                self._delete_attr(person.student, "degrees")
        return person

    def _delete_attr(self, obj, attr):
        try:
            delattr(obj, attr)
        except AttributeError:
            pass

    def _paginate(self, values, page=None, page_size=None):
        if page is not None and page_size is not None:
            offset = (page - 1) * page_size
            values = values[offset:offset+page_size]
        return values

    def get_person_by_uwnetid(self, uwnetid, **kwargs):
        return self._read_person_file(f'**/*{uwnetid}*.json',  **kwargs)

    def get_person_by_uwregid(self, uwregid, **kwargs):
        return self._read_person_file(f'**/*{uwregid}*.json',  **kwargs)

    def get_person_by_student_number(self, student_number, **kwargs):
        return self._read_person_file(f'**/*{student_number}*.json',  **kwargs)

    def get_person_by_system_key(self, system_key, **kwargs):
        return self._read_person_file(f'**/*{system_key}*.json',  **kwargs)

    def get_persons(self, page=None, page_size=None, **kwargs):
        return self._paginate(
            self._read_person_files('**/**.json',  **kwargs),
            page=page,
            page_size=page_size)

    def get_registered_students(self, page=None, page_size=None, **kwargs):
        persons = self._read_person_files('**/students/**.json',  **kwargs)
        registered_persons = [person for person in persons if
                              person.student.enroll_status_code == '12']
        return self._paginate(
            registered_persons,
            page=page,
            page_size=page_size)

    def get_active_students(self, page=None, page_size=None, **kwargs):
        return self._paginate(
            self._read_person_files('**/students/**.json',  **kwargs),
            page=page,
            page_size=page_size)

    def get_active_employees(self, page=None, page_size=None, **kwargs):
        return self._paginate(
            self._read_person_files('**/employees/**/*.json',  **kwargs),
            page=page,
            page_size=page_size)

    def get_advisers(self, advising_program=None, **kwargs):
        advisers = self._read_person_files('**/employees/advisers/*.json',
                                           **kwargs)
        if advising_program:
            filtered_advisers = []
            for person in advisers:
                if (person.employee.adviser.advising_program ==
                        advising_program):
                    filtered_advisers.append(person)
            return filtered_advisers
        else:
            return advisers

    def get_persons_by_adviser_netid(self, uwnetid, **kwargs):
        students = self.get_active_students(**kwargs)
        persons = []
        for person in students:
            for adviser in person.student.advisers:
                if adviser.uwnetid == uwnetid:
                    persons.append(person)
                    break
        return persons

    def get_persons_by_adviser_regid(self, uwregid, **kwargs):
        students = self.get_active_students(**kwargs)
        persons = []
        for person in students:
            for adviser in person.student.advisers:
                if adviser.uwregid == uwregid:
                    persons.append(person)
                    break
        return persons
