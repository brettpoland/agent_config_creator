from PyQt5.QtWidgets import QApplication, QCheckBox
from config_app import ConfigApp


def run():
    app = QApplication([])
    win = ConfigApp()
    # Ensure sections are built for Python
    win.update_sections('Python')
    # Select first option in authentication
    gb = win.sections.get('authentication')
    if gb:
        cbs = gb.findChildren(QCheckBox)
        if cbs:
            cbs[0].setChecked(True)
    # Set enforcement for authentication to 'Allow AI...' (id 2)
    bg = win.section_enforcement.get('authentication')
    if bg and bg.button(2):
        bg.button(2).setChecked(True)

    print(win.generate_markdown())


if __name__ == "__main__":
    run()
