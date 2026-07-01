import threading
import time
import tkinter as tk
from tkinter import ttk

from pydobot import Dobot
from serial.tools import list_ports as serial_list_ports

DEFAULT_BAUD = 115200
STEP_SLEEP = 0.25


def list_ports():
    ports = []
    for port in serial_list_ports.comports():
        if port.device:
            ports.append(port.device)
    return sorted(set(ports))


class AppState:
    def __init__(self, set_status, set_conn):
        self.set_status = set_status
        self.set_conn = set_conn
        self.dev = None
        self.port = None
        self.lock = threading.Lock()
        self.points = []
        self.loop_thread = None
        self.stop_evt = threading.Event()
        self.running = False

    def connected(self):
        return self.dev is not None

    def connect(self, port):
        self.disconnect()
        try:
            with self.lock:
                self.dev = Dobot(port)
                self.port = port
            self.set_conn(True)
            self.set_status(f"Ansluten: {port}")
            return True
        except Exception as e:
            with self.lock:
                self.dev = None
                self.port = None
            self.set_conn(False)
            self.set_status(f"Anslutning misslyckades: {type(e).__name__}")
            return False

    def disconnect(self):
        self.stop_loop()
        with self.lock:
            if self.dev:
                try:
                    self.dev.close()
                except Exception:
                    pass
            self.dev = None
            self.port = None
        self.set_conn(False)

    def test_pose(self):
        if not self.connected():
            self.set_status("Inte ansluten.")
            return
        try:
            with self.lock:
                p = self.dev.pose()
            pt = (float(p[0]), float(p[1]), float(p[2]), float(p[3]))
            self.set_status(f"Pose OK: {tuple(round(v, 1) for v in pt)}")
        except Exception as e:
            self.set_status(f"Pose fel: {type(e).__name__}")

    def add_point(self):
        if not self.connected():
            self.set_status("Inte ansluten. Tryck Connect först.")
            return
        try:
            with self.lock:
                p = self.dev.pose()
            pt = (float(p[0]), float(p[1]), float(p[2]), float(p[3]))
            self.points.append(pt)
            self.set_status(f"Punkt {len(self.points)} sparad: {tuple(round(v, 1) for v in pt)}")
        except Exception as e:
            self.set_status(f"Kunde inte spara punkt: {type(e).__name__}")

    def clear_points(self):
        self.stop_loop()
        self.points = []
        self.set_status("Punkter rensade.")

    def start_loop(self):
        if self.running:
            self.set_status("Loop kör redan.")
            return
        if not self.connected():
            self.set_status("Inte ansluten. Tryck Connect först.")
            return
        if len(self.points) < 2:
            self.set_status("Spara minst 2 punkter först.")
            return
        self.stop_evt.clear()
        self.running = True
        self.loop_thread = threading.Thread(target=self._loop, daemon=True)
        self.loop_thread.start()
        self.set_status("Loop startad.")

    def stop_loop(self):
        if not self.running:
            return
        self.stop_evt.set()
        if self.loop_thread:
            self.loop_thread.join(timeout=3.0)
        self.running = False
        self.set_status("Loop stoppad.")

    def _loop(self):
        idx = 0
        while not self.stop_evt.is_set():
            try:
                if not self.points:
                    break
                pt = self.points[idx % len(self.points)]
                with self.lock:
                    self.dev.move_to(*pt, wait=True)
                idx += 1
                time.sleep(STEP_SLEEP)
            except Exception as e:
                self.set_status(f"Rörelse stoppad: {type(e).__name__}")
                time.sleep(0.5)
        self.running = False


root = tk.Tk()
root.title("Dobot - Punktloop")

status_var = tk.StringVar(value="Redo. Välj port, tryck Connect, tryck Test Pose.")
conn_var = tk.StringVar(value="Ej ansluten")


def set_status(s):
    root.after(0, lambda: status_var.set(s))


def set_conn(is_on):
    root.after(0, lambda: conn_var.set("Ansluten" if is_on else "Ej ansluten"))


state = AppState(set_status, set_conn)

frm = ttk.Frame(root, padding=16)
frm.grid()

ttk.Label(frm, text="Dobot Magician", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky="w")
ttk.Label(frm, textvariable=conn_var).grid(row=0, column=3, sticky="e")

ttk.Label(frm, text="Port:").grid(row=1, column=0, sticky="w")
port_box = ttk.Combobox(frm, width=36, state="readonly")
port_box.grid(row=1, column=1, columnspan=2, padx=(6, 6), sticky="we")


def refresh_ports():
    ports = list_ports()
    port_box["values"] = ports
    if ports:
        port_box.current(0)
        set_status("Portar uppdaterade. Tryck Connect.")
    else:
        set_status("Inga portar hittades. Koppla USB och tryck Refresh.")


def on_connect():
    vals = port_box["values"]
    if not vals:
        set_status("Inga portar. Tryck Refresh.")
        return
    port = port_box.get()
    if not port:
        port = vals[0]
    state.connect(port)


def on_disconnect():
    state.disconnect()
    set_status("Frånkopplad.")


ttk.Button(frm, text="Refresh", command=refresh_ports, width=12).grid(row=1, column=3, padx=(6, 0))
ttk.Button(frm, text="Connect", command=on_connect, width=12).grid(row=2, column=1, pady=(8, 0), sticky="w")
ttk.Button(frm, text="Disconnect", command=on_disconnect, width=12).grid(row=2, column=2, pady=(8, 0), sticky="w")
ttk.Button(frm, text="Test Pose", command=state.test_pose, width=12).grid(row=2, column=3, pady=(8, 0), sticky="w")

ttk.Separator(frm, orient="horizontal").grid(row=3, column=0, columnspan=4, sticky="we", pady=12)

ttk.Button(frm, text="Spara punkt", command=state.add_point, width=16).grid(row=4, column=0, sticky="w")
ttk.Button(frm, text="Rensa punkter", command=state.clear_points, width=16).grid(row=4, column=1, sticky="w")

ttk.Button(frm, text="Start loop", command=state.start_loop, width=16).grid(row=5, column=0, pady=(10, 0), sticky="w")
ttk.Button(frm, text="Stop loop", command=state.stop_loop, width=16).grid(row=5, column=1, pady=(10, 0), sticky="w")

ttk.Label(frm, textvariable=status_var, wraplength=640).grid(row=6, column=0, columnspan=4, pady=(14, 0), sticky="w")


def on_close():
    try:
        state.disconnect()
    finally:
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)

refresh_ports()
root.mainloop()
