#!/home/catalin/repos/CommandClassifier/venv/bin/python
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gdk
import sys
from predict import predict_command

class CommandClassifierApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = Gtk.ApplicationWindow(application=app)
        self.win.set_title("Command Classifier")
        self.win.set_default_size(400, 200)

        # Create a CSS provider
        css_provider = Gtk.CssProvider()
        css_provider.load_from_string("""
            entry {
                font-size: 18px;
            }
            label.result {
                font-size: 20px;
                font-weight: bold;
                margin-top: 10px;
            }
        """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.box.set_halign(Gtk.Align.CENTER)
        self.box.set_valign(Gtk.Align.CENTER)
        self.box.set_margin_top(2)
        self.box.set_margin_bottom(2)
        self.box.set_margin_start(2)
        self.box.set_margin_end(2)
        self.win.set_child(self.box)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Enter a command")
        self.box.append(self.entry)
        self.entry.connect("activate", self.on_button_clicked)

        self.button = Gtk.Button(label="Predict")
        self.button.connect("clicked", self.on_button_clicked)
        self.box.append(self.button)

        self.label = Gtk.Label(label="")
        self.label.add_css_class("result") # Add the CSS class to the label
        self.box.append(self.label)

        self.win.present()

    def on_button_clicked(self, widget):
        command = self.entry.get_text()
        if command:
            prediction = predict_command(command)
            self.label.set_text(prediction)
        else:
            self.label.set_text("Please enter a command.")

if __name__ == "__main__":
    app = CommandClassifierApp(application_id="com.example.CommandClassifier")
    app.run(sys.argv)
