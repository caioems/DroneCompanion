import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk
import os
from run import Main
from tqdm import tqdm
import sys
import io

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Collection GUI")

        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack()

        self.output_text = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, height=20, width=80)
        self.output_text.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.run_button = ttk.Button(self.main_frame, text="RUN", command=self.run_script)
        self.run_button.grid(row=1, column=0, pady=10)

    def update_output_text(self, message):
        self.output_text.insert(tk.END, message)
        self.output_text.see(tk.END)  # Auto-scroll to the end of the text

    def run_script(self):
        original_stdout = sys.stdout
        sys.stdout = io.StringIO()  # Redirecting stdout to a string buffer

        try:
            flights = Main()
            kml_file = f"{flights._root.root_folder}/flights.kml"

            with tqdm(total=len(flights._log_list), desc="Analyzing Logs", file=sys.stdout) as pbar:
                for log in flights._log_list:
                    flights.run(log)
                    pbar.update(1)  # Update tqdm progress bar

                    # Redirect tqdm output to the GUI text widget
                    sys.stdout = io.StringIO()
                    pbar.write(sys.stdout.getvalue())
                    self.update_output_text(sys.stdout.getvalue())

            sys.stdout = original_stdout

            flights._kml.save(kml_file)
            print("Done.")
            os.startfile(kml_file)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()