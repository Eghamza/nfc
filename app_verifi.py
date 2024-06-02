import tkinter as tk
from tkinter import messagebox
import nfc
import threading
import requests

class NFCReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NFC Reader Verification")

        self.label = tk.Label(root, text="NFC Reader")
        self.label.pack(pady=10)

        self.read_button = tk.Button(root, text="Read NFC UID", command=self.read_nfc_uid)
        self.read_button.pack(pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10)

    def read_nfc_uid(self):
        threading.Thread(target=self.read_nfc).start()

    def read_nfc(self):
        def on_connect(tag):
            return tag.identifier.hex().upper()
        
        try:
            clf = nfc.ContactlessFrontend('usb')
            nfc_uid = clf.connect(rdwr={'on-connect': on_connect})
            self.verify_nfc_uid(nfc_uid)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def verify_nfc_uid(self, nfc_uid):
        url = 'http://your-django-server/employees/verify/'
        data = {'nfc_uid': nfc_uid}
        try:
            response = requests.post(url, data=data)
            result = response.json()
            if result['status'] == 'success':
                self.result_label.config(text=f"Employee verified: {result['employee']['name']} ({result['employee']['email']})", fg="green")
            else:
                self.result_label.config(text="Verification failed: Employee not found", fg="red")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = NFCReaderApp(root)
    root.mainloop()
