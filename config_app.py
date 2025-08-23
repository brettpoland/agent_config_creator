import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QGroupBox,
    QCheckBox,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QScrollArea,
    QRadioButton,
    QButtonGroup,
    QMessageBox,
    QStackedWidget,
)
from PyQt5.QtCore import Qt


class ConfigApp(QWidget):
    def __init__(self, go_back=None):
        super().__init__()
        self.go_back = go_back or (lambda: None)
        self.setWindowTitle("Agent Coding Config Creator")
        self.setGeometry(100, 100, 700, 650)

        # mapping: canonical keys -> sections -> options
        self.section_options_by_lang = {
            "python": {
                "authentication": ["GitHub", "AWS IAM", "Personal Token", "SSH Key", "OAuth App"],
                "performance": ["CPython", "Async/Await", "Numba", "C extensions", "Profiling"],
                "code_quality": ["Black", "Flake8", "mypy", "Pre-commit", "isort"],
                "data_layer": ["S3", "Local FS", "SQLite", "Postgres", "Redis"],
                "testing": ["pytest", "unittest", "tox", "mock", "integration tests"],
                "web_kits_and_gui_libraries": ["Django", "Flask", "FastAPI", "Qt5 (PyQt5)", "Tkinter"],
                "miscellaneous": ["virtualenv", "packaging", "logging", "docs", "CI"],
            },
            "julia": {
                "authentication": ["OAuth2", "API Key", "SSH", "GPG", "Custom Token"],
                "performance": ["Multi-threading", "BLAS/OpenBLAS", "GPU (CUDA.jl)", "Profiling", "JIT tuning"],
                "code_quality": ["Lint.jl", "Formatter", "Documenter", "Revise", "Pkg.test"],
                "data_layer": ["HDF5", "JLD2", "CSV", "SQLite", "Arrays"],
                "testing": ["Pkg.test", "BenchmarkTools", "Coverage", "CI", "TestSets"],
                "web_kits_and_gui_libraries": ["Genie (web)", "HTTP.jl", "Blink.jl", "Gtk.jl", "Makie (visuals)"],
                "miscellaneous": ["REPL", "IJulia", "Plots", "Package manager", "Debugger"],
            },
            "r": {
                "authentication": ["OAuth2", "API Key", "GCP Service Account", "AWS IAM", "LDAP"],
                "performance": ["data.table", "parallel", "Rcpp", "byte-compile", "profiling"],
                "code_quality": ["lintr", "styler", "testthat", "roxygen2", "covr"],
                "data_layer": ["data.table", "SQLite", "RDS", "feather", "S3"],
                "testing": ["testthat", "RUnit", "covr", "httptest", "mockery"],
                "web_kits_and_gui_libraries": ["Shiny", "plumber", "R Markdown", "tcltk", "gWidgets2"],
                "miscellaneous": ["Shiny", "RMarkdown", "pkgdown", "renv", "CRAN checks"],
            },
            "go": {
                "authentication": ["OAuth2", "JWT", "mTLS", "API Key", "IAM"],
                "performance": ["Goroutines", "Memory profiling", "cgo", "race detector", "benchmarks"],
                "code_quality": ["gofmt", "golint", "govet", "staticcheck", "errcheck"],
                "data_layer": ["Postgres", "BoltDB", "Redis", "gRPC", "S3"],
                "testing": ["go test", "benchmarks", "mocking", "integration tests", "CI pipelines"],
                "web_kits_and_gui_libraries": ["Gin", "Echo", "Revel", "Fyne (GUI)", "webview"],
                "miscellaneous": ["Modules", "Docker", "Kubernetes", "Prometheus", "OpenTelemetry"],
            },
            # placeholders for other languages
            "typescript": {
                "authentication": ["OAuth2", "API Key", "JWT", "mTLS", "IAM"],
                "performance": ["V8 optimizations", "Bundling", "Minification", "Tree-shaking", "Profiling"],
                "code_quality": ["ESLint", "Prettier", "TypeScript types", "ts-node", "testing"],
                "data_layer": ["REST", "GraphQL", "IndexedDB", "LocalStorage", "Postgres"],
                "testing": ["Jest", "Mocha", "Playwright", "Cypress", "integration tests"],
                "web_kits_and_gui_libraries": ["React", "Vue", "Angular", "Electron", "Svelte"],
                "miscellaneous": ["npm scripts", "tsconfig", "lint-staged", "CI", "bundlers"],
            },
            "rust": {
                "authentication": ["OAuth2", "API Key", "mTLS", "SSH", "Custom Token"],
                "performance": ["Zero-cost abstractions", "Profiling", "SIMD", "Async (tokio)", "LTO"],
                "code_quality": ["cargo fmt", "clippy", "cargo test", "benchmarks", "documentation"],
                "data_layer": ["Postgres", "SQLite", "sled", "Redis", "gRPC"],
                "testing": ["cargo test", "mocking", "integration tests", "benchmarks", "CI"],
                "web_kits_and_gui_libraries": ["Actix-web", "Rocket", "Yew (WASM)", "Tauri", "Iced"],
                "miscellaneous": ["Cargo", "Modules", "FFI", "Error handling", "Telemetry"],
            },
            "terraform": {
                "authentication": ["Service Principal", "AWS IAM", "API Token", "SSH", "Cloud creds"],
                "performance": ["State backend", "Parallelism", "Modules", "Remote state", "Provisioners"],
                "code_quality": ["tflint", "formatting", "modules", "state management", "review"],
                "data_layer": ["S3 backend", "Terraform Cloud", "Consul", "Local state", "Secrets manager"],
                "testing": ["terragrunt", "kitchen-terraform", "unit tests", "integration tests", "policy checks"],
                "web_kits_and_gui_libraries": ["Terraform Cloud UI", "Terraform Enterprise", "Remote state dashboards", "Custom console", "Policy UI (Sentinel)"],
                "miscellaneous": ["modules", "workspaces", "remote state", "providers", "locking"],
            },
            "cloudformation_yaml": {
                "authentication": ["IAM Roles", "API Keys", "Service Role", "Cross-account", "STS"],
                "performance": ["Stack sets", "Nested stacks", "Resource optimization", "Custom resources", "Change sets"],
                "code_quality": ["cfn-lint", "SAM", "transform macros", "modularity", "templates"],
                "data_layer": ["S3", "DynamoDB", "RDS", "Parameter Store", "Secrets Manager"],
                "testing": ["cfn-nag", "taskcat", "integration tests", "stack policy tests", "CI/CD"],
                "web_kits_and_gui_libraries": ["CloudFormation Console UI", "SAM Local UI", "Custom resource dashboards", "Change set viewers", "Template visualizers"],
                "miscellaneous": ["SAM", "Custom resources", "Mappings", "Conditions", "Outputs"],
            },
        }

        # add common process time/token reduction section and misc option
        self.process_time_options = [
            "Minimize processing time",
            "Reduce token usage",
            "Enable response summarization",
        ]
        for opts in self.section_options_by_lang.values():
            opts["process_time_token_reduction"] = list(self.process_time_options)
            opts.setdefault("miscellaneous", []).append(
                "Automatically push code changes to a PR and main"
            )

        self.display_to_key = {
            "Python": "python",
            "Typescript": "typescript",
            "Rust": "rust",
            "Terraform": "terraform",
            "Cloudformation YAML": "cloudformation_yaml",
            "Julia": "julia",
            "R": "r",
            "Go": "go",
        }

        self.sections = {}
        # per-section enforcement button groups
        self.section_enforcement = {}

        # human-friendly section display names (override default title-casing)
        self.section_display_names = {
            "web_kits_and_gui_libraries": "Web / GUI Libraries",
            "process_time_token_reduction": "Process Time / Token Reduction",
        }

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        back_btn = QPushButton("\u2190 Back")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        # language selector
        h = QHBoxLayout()
        h.addWidget(QLabel("Select Programming Language:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(list(self.display_to_key.keys()))
        h.addWidget(self.lang_combo)
        layout.addLayout(h)

        # dynamic area (inside a scroll area)
        self.sections_widget = QWidget()
        self.sections_layout = QVBoxLayout()
        self.sections_widget.setLayout(self.sections_layout)

        # custom behavior (put inside scrollable content)
        cb_box = QGroupBox("Custom Behavior")
        cb_layout = QVBoxLayout()
        self.custom_text = QTextEdit()
        self.custom_text.setPlaceholderText("Enter custom instructions to include at the end of the generated file.")
        cb_layout.addWidget(self.custom_text)
        cb_box.setLayout(cb_layout)

        content_container = QWidget()
        content_layout = QVBoxLayout()
        content_layout.addWidget(self.sections_widget)
        content_layout.addWidget(cb_box)
        content_layout.addStretch()
        content_container.setLayout(content_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_container)
        layout.addWidget(scroll)

        # format radios
        fbox = QHBoxLayout()
        fbox.addWidget(QLabel("Save as:"))
        self.agent_radio = QRadioButton("agent.md format")
        self.copilot_radio = QRadioButton("Co-Pilot format")
        self.agent_radio.setChecked(True)
        fbox.addWidget(self.agent_radio)
        fbox.addWidget(self.copilot_radio)
        layout.addLayout(fbox)

        # save button
        self.save_btn = QPushButton("Save File")
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        # signals
        self.lang_combo.currentTextChanged.connect(self.update_sections)
        self.save_btn.clicked.connect(self.save_file)

        # init
        self.update_sections(self.lang_combo.currentText())

    def clear_sections(self):
        while self.sections_layout.count():
            item = self.sections_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        self.sections = {}

    def update_sections(self, lang_display):
        self.clear_sections()
        key = self.display_to_key.get(lang_display, lang_display.lower())
        opts_map = self.section_options_by_lang.get(key, {})

        order = [
            "process_time_token_reduction",
            "authentication",
            "performance",
            "code_quality",
            "data_layer",
            "testing",
            "web_kits_and_gui_libraries",
            "miscellaneous",
        ]

        for sec in order:
            opts = opts_map.get(sec)
            if not opts:
                continue

            title = self.section_display_names.get(sec, sec.replace("_", " ").title())
            gb = QGroupBox(title)
            v = QVBoxLayout()

            # enforcement radio buttons
            enforce_layout = QHBoxLayout()
            enforce_layout.addWidget(QLabel("Enforcement:"))
            rb_strict = QRadioButton("Strictly Enforced")
            rb_allow = QRadioButton("Allow AI to use better option if one applies")
            rb_strict.setChecked(True)
            bg = QButtonGroup(gb)
            bg.addButton(rb_strict, 1)
            bg.addButton(rb_allow, 2)
            enforce_layout.addWidget(rb_strict)
            enforce_layout.addWidget(rb_allow)
            enforce_layout.addStretch()
            v.addLayout(enforce_layout)

            for o in opts:
                cb = QCheckBox(o)
                v.addWidget(cb)

            gb.setLayout(v)
            self.sections_layout.addWidget(gb)
            self.sections[sec] = gb
            self.section_enforcement[sec] = bg

        if not self.sections:
            lbl = QLabel("(no options available)")
            lbl.setAlignment(Qt.AlignCenter)
            self.sections_layout.addWidget(lbl)

    def save_file(self):
        root = os.path.dirname(os.path.abspath(__file__))
        copilot_dir = os.path.join(root, ".github")

        if self.agent_radio.isChecked():
            default = os.path.join(root, "AGENTS.md")
            exp_dir = root
            exp_file = "AGENTS.md"
        else:
            if not os.path.exists(copilot_dir):
                os.makedirs(copilot_dir)
            default = os.path.join(copilot_dir, "copilot-instructions.md")
            exp_dir = copilot_dir
            exp_file = "copilot-instructions.md"

        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", default, "Markdown Files (*.md);;All Files (*)")
        if not file_path:
            return

        save_dir = os.path.dirname(os.path.abspath(file_path))
        save_base = os.path.basename(file_path)
        if save_dir != exp_dir or save_base != exp_file:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            if self.agent_radio.isChecked():
                msg.setText(f"Warning: AGENTS.md is expected in the project root: {exp_dir}\n\nSave anyway?")
            else:
                msg.setText(f"Warning: copilot-instructions.md is expected in .github: {exp_dir}\n\nSave anyway?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            ret = msg.exec_()
            if ret != QMessageBox.Yes:
                return

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.generate_markdown())

    def generate_markdown(self):
        lang = self.lang_combo.currentText()
        fmt = "agent.md" if self.agent_radio.isChecked() else "Co-Pilot"
        lines = ["# Agent Configuration", "", f"Language: **{lang}**", f"Format: **{fmt}**", ""]

        order = [
            "process_time_token_reduction",
            "authentication",
            "performance",
            "code_quality",
            "data_layer",
            "testing",
            "web_kits_and_gui_libraries",
            "miscellaneous",
        ]

        for sec in order:
            header = self.section_display_names.get(sec, sec.replace("_", " ").title())
            lines.append(f"## {header}")
            gb = self.sections.get(sec)
            if not gb:
                lines.append("- (no options)")
                lines.append("")
                continue

            selected = [cb.text() for cb in gb.findChildren(QCheckBox) if cb.isChecked()]

            # enforcement: default to Strictly Enforced unless the 'Allow AI...' option (id 2) is selected
            bg = self.section_enforcement.get(sec)
            if bg is not None:
                checked = bg.checkedId()
                if checked == 2:
                    enforcement_text = "Allow AI to use better option if one applies"
                else:
                    enforcement_text = "Strictly Enforced"
            else:
                enforcement_text = "Strictly Enforced"

            lines.append(f"- Enforcement: {enforcement_text}")
            if not selected:
                lines.append("- (none selected)")
            else:
                for s in selected:
                    lines.append(f"- {s}")
            lines.append("")

        # append custom behavior
        custom = self.custom_text.toPlainText().strip() if hasattr(self, 'custom_text') else ''
        if custom:
            lines.append("## Custom Behavior")
            for l in custom.splitlines():
                lines.append(l)
            lines.append("")

        return "\n".join(lines)


class MainMenu(QWidget):
    def __init__(self, open_config, open_optimizer):
        super().__init__()
        layout = QVBoxLayout()

        header = QWidget()
        header_layout = QHBoxLayout()
        header_label = QLabel("Agent Coding Config Creator")
        header_label.setStyleSheet("color: white; font-weight: bold; font-size: 14pt;")
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header.setLayout(header_layout)
        header.setStyleSheet("background-color: #0078d4; padding: 8px;")
        layout.addWidget(header)

        btn_config = QPushButton("Agent Guide Creator")
        btn_optimizer = QPushButton("Agent Optimizer")
        btn_config.clicked.connect(open_config)
        btn_optimizer.clicked.connect(open_optimizer)
        layout.addWidget(btn_config)
        layout.addWidget(btn_optimizer)
        layout.addStretch()
        self.setLayout(layout)


class AgentOptimizerMenu(QWidget):
    def __init__(self, go_back, open_agent):
        super().__init__()
        layout = QVBoxLayout()
        back = QPushButton("\u2190 Back")
        back.clicked.connect(go_back)
        layout.addWidget(back, alignment=Qt.AlignLeft)
        for name in ["Co-Pilot", "Cline", "Codex"]:
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, n=name: open_agent(n))
            layout.addWidget(btn)
        layout.addStretch()
        self.setLayout(layout)


class AgentDetail(QWidget):
    def __init__(self, go_back):
        super().__init__()
        layout = QVBoxLayout()
        back = QPushButton("\u2190 Back")
        back.clicked.connect(go_back)
        layout.addWidget(back, alignment=Qt.AlignLeft)

        self.title = QLabel("")
        layout.addWidget(self.title, alignment=Qt.AlignCenter)

        layout.addWidget(QLabel("Model reasoning effort"))
        self.combo = QComboBox()
        self.combo.addItems(["low", "medium", "high"])
        layout.addWidget(self.combo)

        layout.addStretch()
        apply_btn = QPushButton("Apply")
        layout.addWidget(apply_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def set_agent(self, name):
        self.title.setText(name)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agent Tools")
        self.setGeometry(100, 100, 700, 650)
        self.stack = QStackedWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.config_app = ConfigApp(self.show_main)
        self.main_menu = MainMenu(self.show_config, self.show_optimizer)
        self.optimizer_menu = AgentOptimizerMenu(self.show_main, self.show_agent)
        self.agent_detail = AgentDetail(self.show_optimizer)

        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.config_app)
        self.stack.addWidget(self.optimizer_menu)
        self.stack.addWidget(self.agent_detail)

    def show_main(self):
        self.stack.setCurrentWidget(self.main_menu)

    def show_config(self):
        self.stack.setCurrentWidget(self.config_app)

    def show_optimizer(self):
        self.stack.setCurrentWidget(self.optimizer_menu)

    def show_agent(self, name):
        self.agent_detail.set_agent(name)
        self.stack.setCurrentWidget(self.agent_detail)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
