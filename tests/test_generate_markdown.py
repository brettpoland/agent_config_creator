import pytest
from config_app import ConfigApp


def test_default_enforcement(qtbot):
    win = ConfigApp()
    qtbot.addWidget(win)
    win.update_sections('Python')
    md = win.generate_markdown()
    assert '## Authentication' in md
    assert 'Enforcement: Strictly Enforced' in md

def test_allow_ai_enforcement(qtbot):
    win = ConfigApp()
    qtbot.addWidget(win)
    win.update_sections('Python')
    bg = win.section_enforcement.get('authentication')
    # set to id 2 (Allow AI)
    if bg and bg.button(2):
        bg.button(2).setChecked(True)
    md = win.generate_markdown()
    assert 'Enforcement: Allow AI to use better option if one applies' in md

def test_custom_behavior_included(qtbot):
    win = ConfigApp()
    qtbot.addWidget(win)
    win.update_sections('Python')
    win.custom_text.setPlainText('Do this and that')
    md = win.generate_markdown()
    assert '## Custom Behavior' in md
    assert 'Do this and that' in md
