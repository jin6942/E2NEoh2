"""Verify the integrated plus five DOCX files and internal Word/PDF evidence.

PDFs remain internal evidence, never members of delivery_files. This entry point
requires delivery_mode=integrated_plus_five_docx and performs no rendering,
review, receipt creation or approval on the caller's behalf.
"""
from verify_release import main, verify as _verify


def verify(record, base='.'):
    return _verify(record, base, delivery_mode='integrated_plus_five_docx')


if __name__ == '__main__':
    raise SystemExit(main(delivery_mode='integrated_plus_five_docx'))
