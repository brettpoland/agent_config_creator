import pytest
from PyQt5.QtWidgets import QCheckBox
from config_app import ConfigApp


def test_default_enforcement(qtbot):
    win = ConfigApp()
    qtbot.addWidget(win)
    win.update_sections('Python')
    auth_gb = win.sections.get('authentication')
    first_label = None
    if auth_gb:
        cb = auth_gb.findChildren(QCheckBox)[0]
        first_label = cb.text()
        cb.setChecked(True)
    md = win.generate_markdown()
    assert '## Authentication' in md
    assert '- Enforcement: Strictly Enforced' in md
    assert f'- {first_label}' in md

def test_allow_ai_enforcement(qtbot):
    win = ConfigApp()
    qtbot.addWidget(win)
    win.update_sections('Python')
    auth_gb = win.sections.get('authentication')
    if auth_gb:
        auth_gb.findChildren(QCheckBox)[0].setChecked(True)
    bg = win.section_enforcement.get('authentication')
    # set to id 2 (Allow AI)
    if bg and bg.button(2):
        bg.button(2).setChecked(True)
    md = win.generate_markdown()
    assert '## Authentication' in md
    assert 'Enforcement: Allow AI to use better option if one applies' in md

def test_custom_behavior_included(qtbot):
    win = ConfigApp()
    qtbot.addWidget(win)
    win.update_sections('Python')
    win.custom_text.setPlainText('Do this and that')
    md = win.generate_markdown()
    assert '## Custom Behavior' in md
    assert 'Do this and that' in md


def test_sections_without_selection_skipped(qtbot):
    win = ConfigApp()
    qtbot.addWidget(win)
    win.update_sections('Python')
    md = win.generate_markdown()
    assert '## Authentication' not in md


def test_process_time_section_selected_included(qtbot):
    win = ConfigApp()
    qtbot.addWidget(win)
    win.update_sections('Python')
    pt_gb = win.sections.get('process_time_token_reduction')
    if pt_gb:
        pt_gb.findChildren(QCheckBox)[0].setChecked(True)
    md = win.generate_markdown()
    assert '## Process Time / Token Reduction' in md


def test_auto_push_option_in_misc(qtbot):
    win = ConfigApp()
    qtbot.addWidget(win)
    win.update_sections('Python')
    misc_gb = win.sections.get('miscellaneous')
    if misc_gb:
        for cb in misc_gb.findChildren(QCheckBox):
            if cb.text() == 'Automatically push and merge any code updates to main':
                cb.setChecked(True)
    md = win.generate_markdown()
    assert '## Miscellaneous' in md
    assert 'Automatically push and merge any code updates to main' in md
