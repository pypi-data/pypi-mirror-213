#!../venv/bin/pytest -s

from confattr import HelpWriter, SectionLevel

import io


# ------- heading -------

def test__help_writer__dont_discard_on_subsection() -> None:
	f = io.StringIO()
	w = HelpWriter(f)
	w.write_heading(SectionLevel.SECTION, 'Section')
	w.write_heading(SectionLevel.SUB_SECTION, 'Subsection')
	w.write_line('hello world')

	expected = '''\
Section
=======

Subsection
----------
hello world
'''
	assert f.getvalue() == expected

def test__help_writer__no_discard() -> None:
	f = io.StringIO()
	w = HelpWriter(f)
	w.write_heading(SectionLevel.SECTION, 'Empty section')
	w.write_heading(SectionLevel.SECTION, 'Nonempty section')
	w.write_line('hello world')

	expected = '''\
Empty section
=============

Nonempty section
================
hello world
'''
	assert f.getvalue() == expected


# ------- empty line -------

def test__help_writer__empty_line_before_section() -> None:
	f = io.StringIO()
	w = HelpWriter(f)
	w.write_line('intro')
	w.write_heading(SectionLevel.SECTION, 'Section 1')
	w.write_line('This is the first section.')

	expected = '''\
intro

Section 1
=========
This is the first section.
'''
	assert f.getvalue() == expected
