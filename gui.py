import tkinter as tk
from tkinter import ttk
from arabic_to_ipa import transliterate_arabic_to_ipa

class ArabicToIPAApp:
    def __init__(self, master):
        self.master = master
        master.title("Arabic to IPA Transliterator")
        master.geometry("400x300")

        self.label = ttk.Label(master, text="Enter Arabic text:")
        self.label.pack(pady=10)

        self.input_text = tk.Text(master, height=5, width=40)
        self.input_text.pack(pady=10)

        self.translate_button = ttk.Button(master, text="Transliterate", command=self.transliterate)
        self.translate_button.pack(pady=10)

        self.output_label = ttk.Label(master, text="IPA Result:")
        self.output_label.pack(pady=5)

        self.output_text = tk.Text(master, height=5, width=40, state="disabled")
        self.output_text.pack(pady=10)

    def transliterate(self):
        arabic_text = self.input_text.get("1.0", tk.END).strip()
        ipa_text = transliterate_arabic_to_ipa(arabic_text)
        
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, ipa_text)
        self.output_text.config(state="disabled")

def main():
    root = tk.Tk()
    app = ArabicToIPAApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
