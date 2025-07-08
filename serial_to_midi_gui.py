import tkinter as tk
import serial
import serial.tools.list_ports
import mido
from mido import Message
import threading

class SerialMIDIBridge:
    def __init__(self, master):
        self.master = master
        self.master.title("Arduino Serial → MIDI Bridge")

        self.port_var = tk.StringVar()
        self.log_text = tk.StringVar()

        self.serial_conn = None
        self.running = False

        self.create_widgets()
        self.refresh_ports()

    def create_widgets(self):
        tk.Label(self.master, text="Serial Port:").pack()

        self.port_menu = tk.OptionMenu(self.master, self.port_var, "")
        self.port_menu.pack()

        tk.Button(self.master, text="Refresh Ports", command=self.refresh_ports).pack()
        self.connect_btn = tk.Button(self.master, text="Connect", command=self.connect)
        self.connect_btn.pack()

        self.log_box = tk.Label(self.master, textvariable=self.log_text, justify="left", anchor="w")
        self.log_box.pack(fill="both", expand=True)

    def log(self, text):
        current = self.log_text.get()
        self.log_text.set(current + "\n" + text)

    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        menu = self.port_menu["menu"]
        menu.delete(0, "end")
        for p in ports:
            menu.add_command(label=p, command=lambda val=p: self.port_var.set(val))
        if ports:
            self.port_var.set(ports[0])

    def connect(self):
        port = self.port_var.get()
        try:
            self.serial_conn = serial.Serial(port, 31250)
            available_ports = mido.get_output_names()
            target_port = next((p for p in available_ports if "ArduinoMIDI" in p), None)
            if not target_port:
                self.log("❌ Could not find IAC port with name 'ArduinoMIDI'")
                return
            self.midi_out = mido.open_output(target_port)
            self.running = True
            self.log("✅ MIDI connected to " + target_port)
            self.log("✅ Connected to " + port)
            threading.Thread(target=self.read_serial_loop, daemon=True).start()
            self.connect_btn.config(text="Disconnect", command=self.disconnect)
        except Exception as e:
            import traceback
            self.log(f"❌ Failed to connect: {e}")
            self.log(traceback.format_exc())

    def disconnect(self):
        self.running = False
        if self.serial_conn:
            self.serial_conn.close()
        self.log("🔌 Disconnected")
        self.connect_btn.config(text="Connect", command=self.connect)

    def read_serial_loop(self):
        while self.running:
            try:
                raw = self.serial_conn.readline().strip()
                self.handle_serial_message(raw)
            except Exception as e:
                self.log(f"⚠️ Serial error: {e}")

    def handle_serial_message(self, raw_line):
        try:
            line = raw_line.decode(errors="ignore")
            parts = line.strip().split()
            if len(parts) < 3:
                return
            cc_type, cc_num, cc_val = parts
            if cc_type == "CC":
                msg = Message("control_change", control=int(cc_num), value=int(cc_val), channel=0)
                self.midi_out.send(msg)
                self.log(f"🎛️ CC {cc_num} {cc_val}")
        except Exception as e:
            self.log(f"⚠️ MIDI conversion error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialMIDIBridge(root)
    root.mainloop()
