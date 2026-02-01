import sys
import subprocess
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QLineEdit,
    QDialog, QFormLayout, QComboBox, QMessageBox, QHeaderView,
    QAbstractItemView, QWizard, QWizardPage, QTextEdit, QSplitter
)
from PyQt6.QtCore import Qt, QProcess
from PyQt6.QtGui import QFont

try:
    from qt_material import apply_stylesheet
    THEME_AVAILABLE = True
except ImportError:
    THEME_AVAILABLE = False

from core.profile_store import ProfileStore

BACKEND_LINKED = False
try:
    from lucid_manager import LucidManager as ProductionManager
    BACKEND_LINKED = True
except Exception:
    ProductionManager = None

manager_cls = ProductionManager if BACKEND_LINKED else MockLucidManager

LAUNCH_SCRIPT_LINUX = Path("./start_lucid.sh")
LAUNCH_SCRIPT_WINDOWS = Path("./start_lucid.bat")
try:
    from core.bin_finder import find_sovereign_binary
    DEFAULT_FIREFOX_BIN = find_sovereign_binary() or Path("./bin/firefox/firefox")
except Exception:
    DEFAULT_FIREFOX_BIN = Path("./bin/firefox/firefox")


class MockLucidManager:
    def __init__(self):
        self.store = ProfileStore()

    def load_profiles(self):
        return self.store.get_all()

    def create_profile(self, payload):
        template = payload.get("template", "golden_template.json")
        data = {
            "name": payload["name"],
            "proxy": payload["proxy_host"],
            "template": template,
            "fullz": payload.get("fullz", {}),
            "financial": payload.get("cc", {}),
            "mission": {
                "target_site": payload["target"],
                "aging_days": int(payload.get("aging", 0))
            }
        }
        return self.store.create_profile(data)

    def delete_profile(self, profile_id):
        self.store.delete_profile(profile_id)


class IdentityWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lucid Genesis Protocol")
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setFixedSize(600, 520)

        self.addPage(PageIdentity())
        self.addPage(PageFinancial())
        self.addPage(PageNetwork())
        self.addPage(PageNarrative())

    def get_data(self):
        return {
            "name": self.field("profile_name"),
            "fullz": {
                "full_name": self.field("full_name"),
                "address": self.field("address"),
                "email": self.field("email"),
                "phone": self.field("phone")
            },
            "cc": {
                "pan": self.field("cc_pan"),
                "exp": self.field("cc_exp"),
                "cvv": self.field("cc_cvv")
            },
            "proxy_host": self.field("proxy_string"),
            "target": self.field("target_site"),
            "aging": self.field("aging_period")
        }


class PageIdentity(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Vector A: Identity Assets")
        self.setSubTitle("Fullz details for the persona.")
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.full_name = QLineEdit()
        self.address = QLineEdit()
        self.email = QLineEdit()
        self.phone = QLineEdit()

        layout.addRow("Profile Alias:", self.name_input)
        layout.addRow("Full Name:", self.full_name)
        layout.addRow("Billing Address:", self.address)
        layout.addRow("Email:", self.email)
        layout.addRow("Phone:", self.phone)

        self.registerField("profile_name*", self.name_input)
        self.registerField("full_name*", self.full_name)
        self.registerField("address", self.address)
        self.registerField("email", self.email)
        self.registerField("phone", self.phone)

        self.setLayout(layout)


class PageFinancial(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Vector B: Financial Injection")
        self.setSubTitle("Double-Tap CC data (stored locally).")
        layout = QFormLayout()

        self.cc_pan = QLineEdit()
        self.cc_exp = QLineEdit()
        self.cc_cvv = QLineEdit()
        self.cc_cvv.setEchoMode(QLineEdit.EchoMode.Password)

        self.cc_pan.setPlaceholderText("XXXX-XXXX-XXXX-XXXX")
        self.cc_exp.setPlaceholderText("MM/YY")

        layout.addRow("Card Number (PAN):", self.cc_pan)
        layout.addRow("Expiry:", self.cc_exp)
        layout.addRow("CVV:", self.cc_cvv)

        label = QLabel("Stored locally. Mirrors Double-Tap tokens.")
        label.setStyleSheet("color: #FF5555; font-size: 10px;")
        layout.addRow(label)

        self.registerField("cc_pan*", self.cc_pan)
        self.registerField("cc_exp*", self.cc_exp)
        self.registerField("cc_cvv", self.cc_cvv)

        self.setLayout(layout)


class PageNetwork(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Vector C: Network Sovereignty")
        layout = QFormLayout()
        self.proxy_input = QLineEdit()
        self.proxy_input.setPlaceholderText("user:pass@ip:port")
        layout.addRow("SOCKS5 Proxy:", self.proxy_input)
        self.registerField("proxy_string*", self.proxy_input)
        self.setLayout(layout)


class PageNarrative(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Vector D: Narrative & Aging")
        layout = QFormLayout()
        self.target = QComboBox()
        self.target.addItems([
            "Eneba (Gaming)", "Stripe (General)",
            "Adyen (High Risk)", "Shopify (Retail)"
        ])
        self.aging = QLineEdit()
        self.aging.setText("66")
        layout.addRow("Target Ecosystem:", self.target)
        layout.addRow("Aging Period (Days):", self.aging)
        self.registerField("target_site", self.target, "currentText")
        self.registerField("aging_period", self.aging)
        self.setLayout(layout)


class LucidCommander(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = manager_cls()
        self.process = None
        self.setWindowTitle("LUCID COMMANDER [OBLIVION ACCESS]")
        self.resize(1040, 720)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        self.setup_sidebar(main_layout)

        content_layout = QVBoxLayout()
        main_layout.addLayout(content_layout)

        header = QLabel("ACTIVE IDENTITIES")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        content_layout.addWidget(header)

        toolbar = QHBoxLayout()
        self.btn_create = QPushButton("+ CREATE IDENTITY")
        self.btn_create.setFixedWidth(170)
        self.btn_create.setStyleSheet(
            "background-color: #00AA77; color: white; font-weight: bold;"
        )
        self.btn_create.clicked.connect(self.launch_wizard)

        self.btn_refresh = QPushButton("REFRESH")
        self.btn_refresh.clicked.connect(self.refresh_table)

        toolbar.addWidget(self.btn_create)
        toolbar.addWidget(self.btn_refresh)
        toolbar.addStretch()
        content_layout.addLayout(toolbar)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "PROFILE NAME", "STATUS", "PROXY", "TRUST SCORE", "AGING", "ACTIONS"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.setStyleSheet("background-color: #0b0f12; color: #00ff9c; font-family: Consolas; font-size: 11px;")
        self.log_console.setMinimumHeight(180)

        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.table)
        splitter.addWidget(self.log_console)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        content_layout.addWidget(splitter)

        self.refresh_table()

        # Backend status indicator
        self.backend_label = QLabel("BACKEND: LINKED" if BACKEND_LINKED else "BACKEND: MOCK")
        self.backend_label.setStyleSheet("color: #00AA77; font-size: 10px;")
        self.backend_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        content_layout.addWidget(self.backend_label)

    def setup_sidebar(self, parent_layout):
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background-color: #1b1f24; border-right: 1px solid #444;")
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(12, 12, 12, 12)

        title = QLabel("LUCID\nEMPIRE")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Courier New", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #00AA77; margin-bottom: 20px;")
        layout.addWidget(title)

        buttons = ["Dashboard", "Proxies", "Templates", "Settings", "Logs"]
        for btn_text in buttons:
            btn = QPushButton(btn_text)
            btn.setStyleSheet(
                "QPushButton { text-align: left; padding: 8px; border: none; color: #ddd; }"
                "QPushButton:hover { background-color: #2f3338; }"
            )
            layout.addWidget(btn)

        layout.addStretch()
        footer = QLabel("v5.0.1 [OBLIVION]")
        footer.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(footer)

        parent_layout.addWidget(sidebar)

    def refresh_table(self):
        self.table.setRowCount(0)
        profiles = self.manager.load_profiles()
        for profile in profiles:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(profile['name']))

            status_text = "HIGH TRUST" if profile.get('genesis_complete') else "AGING"
            status_item = QTableWidgetItem(status_text)
            if "HIGH TRUST" in status_text:
                status_item.setForeground(Qt.GlobalColor.green)
            else:
                status_item.setForeground(Qt.GlobalColor.yellow)
            self.table.setItem(row, 1, status_item)

            self.table.setItem(row, 2, QTableWidgetItem(profile.get('proxy', 'N/A')))

            trust_score = profile.get('trust_score', profile.get('mission', {}).get('aging_days', 0))
            self.table.setItem(row, 3, QTableWidgetItem(f"{trust_score}/100"))

            aging_days = profile.get('mission', {}).get('aging_days', 0)
            self.table.setItem(row, 4, QTableWidgetItem(f"{aging_days} Days"))

            action_widget = QWidget()
            h_box = QHBoxLayout(action_widget)
            h_box.setContentsMargins(0, 0, 0, 0)

            btn_launch = QPushButton("▶")
            btn_launch.setFixedWidth(30)
            btn_launch.setStyleSheet("background-color: #00AA77; color: white;")
            btn_launch.clicked.connect(lambda _, pid=profile['id']: self.launch_profile(pid))

            btn_delete = QPushButton("X")
            btn_delete.setFixedWidth(30)
            btn_delete.setStyleSheet("background-color: #AA3333; color: white;")
            btn_delete.clicked.connect(lambda _, pid=profile['id']: self.delete_profile(pid))

            h_box.addWidget(btn_launch)
            h_box.addWidget(btn_delete)
            h_box.addStretch()

            self.table.setCellWidget(row, 5, action_widget)

    def launch_wizard(self):
        wizard = IdentityWizard(self)
        if wizard.exec():
            payload = wizard.get_data()
            self.manager.create_profile(payload)
            self.refresh_table()

    def launch_profile(self, profile_id):
        # Pre-flight: ensure browser binary exists
        if not DEFAULT_FIREFOX_BIN.exists():
            QMessageBox.critical(
                self,
                "Launch Failed",
                "Sovereign browser binary missing. Place the binary at ./bin/firefox/firefox or set LUCID_FIREFOX_BIN to an absolute path."
            )
            return

        # Select launcher based on platform
        if sys.platform.startswith("win"):
            script = LAUNCH_SCRIPT_WINDOWS
            cmd = ["cmd", "/c", str(script), profile_id]
            pending_msg = "Requesting UAC elevation via PowerShell..."
        else:
            script = LAUNCH_SCRIPT_LINUX
            cmd = [str(script), profile_id]
            pending_msg = None

        if not script.exists():
            QMessageBox.critical(
                self,
                "Launch Failed",
                f"Launcher missing: {script}"
            )
            return

        try:
            if pending_msg:
                QMessageBox.information(self, "Elevation", pending_msg)

            if self.process and self.process.state() != QProcess.ProcessState.NotRunning:
                self.process.kill()

            self.process = QProcess(self)
            self.process.setProgram(cmd[0])
            self.process.setArguments(cmd[1:])
            self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
            self.process.readyReadStandardOutput.connect(self._on_stdout)
            self.process.readyReadStandardError.connect(self._on_stderr)
            self.process.finished.connect(self._on_finished)
            self.log_console.append(f"[LAUNCH] {' '.join(cmd)}")
            self.process.start()
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Launch Failed",
                f"Launcher error: {exc}"
            )

    def delete_profile(self, profile_id):
        reply = QMessageBox.question(
            self,
            "Confirm Purge",
            "Are you sure you want to delete this identity?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.manager.delete_profile(profile_id)
            self.refresh_table()

    def _on_stdout(self):
        if not self.process:
            return
        data = self.process.readAllStandardOutput().data().decode(errors="ignore")
        if data:
            self.log_console.append(data.rstrip())

    def _on_stderr(self):
        if not self.process:
            return
        data = self.process.readAllStandardError().data().decode(errors="ignore")
        if data:
            self.log_console.append(data.rstrip())

    def _on_finished(self, code, status):
        self.log_console.append(f"[EXIT] Launcher exited with code {code}")
        if code != 0:
            QMessageBox.critical(
                self,
                "Launch Failed",
                f"Launcher exited with code {code}. See console for details."
            )


def main():
    app = QApplication(sys.argv)

    if THEME_AVAILABLE:
        apply_stylesheet(app, theme='dark_teal.xml')
    else:
        app.setStyle('Fusion')

    window = LucidCommander()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
