import tkinter as tk
from tkinter import ttk, messagebox
import math

class BPMConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("BPM to Milliseconds Converter")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="BPM to Milliseconds Converter", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # BPM Input
        ttk.Label(main_frame, text="BPM (Beats Per Minute):", 
                 font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.bpm_var = tk.StringVar()
        self.bpm_entry = ttk.Entry(main_frame, textvariable=self.bpm_var, 
                                  font=('Arial', 12), width=20)
        self.bpm_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Note value selection
        ttk.Label(main_frame, text="Note Value:", 
                 font=('Arial', 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.note_var = tk.StringVar(value="Quarter Note (1/4)")
        note_combo = ttk.Combobox(main_frame, textvariable=self.note_var, 
                                 font=('Arial', 10), width=18, state="readonly")
        note_combo['values'] = (
            "Whole Note (1/1)",
            "Half Note (1/2)", 
            "Quarter Note (1/4)",
            "Eighth Note (1/8)",
            "Sixteenth Note (1/16)",
            "Thirty-second Note (1/32)",
            "Sixty-fourth Note (1/64)",
            "One hundred twenty-eighth Note (1/128)"
        )
        note_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Convert button
        convert_btn = ttk.Button(main_frame, text="Convert", 
                               command=self.convert_bpm, style='Accent.TButton')
        convert_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Milliseconds result
        ttk.Label(results_frame, text="Milliseconds:", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.ms_result = ttk.Label(results_frame, text="0.00 ms", 
                                  font=('Arial', 12), foreground='blue')
        self.ms_result.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Seconds result
        ttk.Label(results_frame, text="Seconds:", 
                 font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.sec_result = ttk.Label(results_frame, text="0.00 s", 
                                   font=('Arial', 12), foreground='green')
        self.sec_result.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Formula explanation
        formula_frame = ttk.LabelFrame(main_frame, text="Formula", padding="10")
        formula_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        formula_text = "Milliseconds = (60,000 / BPM) × Note Value Multiplier"
        ttk.Label(formula_frame, text=formula_text, 
                 font=('Arial', 9), foreground='gray').grid(row=0, column=0, sticky=tk.W)
        
        # All subdivisions table (1/4 to 1/128)
        self.subdivisions = [
            ("Quarter Note (1/4)", 1.0),
            ("Eighth Note (1/8)", 0.5),
            ("Sixteenth Note (1/16)", 0.25),
            ("Thirty-second Note (1/32)", 0.125),
            ("Sixty-fourth Note (1/64)", 0.0625),
            ("One hundred twenty-eighth Note (1/128)", 0.03125),
        ]
        table_frame = ttk.LabelFrame(main_frame, text="All Subdivisions (1/4 to 1/128)", padding="10")
        table_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        columns = ("note", "ms", "sec")
        self.results_table = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        self.results_table.heading("note", text="Note")
        self.results_table.heading("ms", text="Milliseconds")
        self.results_table.heading("sec", text="Seconds")
        self.results_table.column("note", width=260, anchor=tk.W)
        self.results_table.column("ms", width=120, anchor=tk.E)
        self.results_table.column("sec", width=120, anchor=tk.E)
        self.results_table.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Add scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.results_table.yview)
        self.results_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Clear button
        clear_btn = ttk.Button(main_frame, text="Clear", command=self.clear_fields)
        clear_btn.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Bind Enter key to convert
        self.root.bind('<Return>', lambda event: self.convert_bpm())
        
        # Focus on BPM entry
        self.bpm_entry.focus()
        
    def get_note_multiplier(self, note_value):
        """Get the multiplier for different note values"""
        multipliers = {
            "Whole Note (1/1)": 4.0,
            "Half Note (1/2)": 2.0,
            "Quarter Note (1/4)": 1.0,
            "Eighth Note (1/8)": 0.5,
            "Sixteenth Note (1/16)": 0.25,
            "Thirty-second Note (1/32)": 0.125,
            "Sixty-fourth Note (1/64)": 0.0625,
            "One hundred twenty-eighth Note (1/128)": 0.03125,
        }
        return multipliers.get(note_value, 1.0)
        
    def convert_bpm(self):
        """Convert BPM to milliseconds"""
        try:
            bpm_text = self.bpm_var.get().strip()
            
            if not bpm_text:
                messagebox.showerror("Error", "Please enter a BPM value")
                return
                
            bpm = float(bpm_text)
            
            if bpm <= 0:
                messagebox.showerror("Error", "BPM must be greater than 0")
                return
                
            if bpm > 1000:
                messagebox.showwarning("Warning", "Very high BPM value. Are you sure this is correct?")
            
            # Get note multiplier
            note_multiplier = self.get_note_multiplier(self.note_var.get())
            
            # Calculate milliseconds per beat for quarter note, then adjust for selected note
            ms_per_quarter_note = 60000 / bpm
            milliseconds = ms_per_quarter_note * note_multiplier
            seconds = milliseconds / 1000
            
            # Update results
            self.ms_result.config(text=f"{milliseconds:.2f} ms")
            self.sec_result.config(text=f"{seconds:.3f} s")

            # Update all subdivisions table
            for row in self.results_table.get_children():
                self.results_table.delete(row)
            for note_name, mult in self.subdivisions:
                ms = ms_per_quarter_note * mult
                sec = ms / 1000
                self.results_table.insert('', tk.END, values=(note_name, f"{ms:.2f}", f"{sec:.3f}"))
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for BPM")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def clear_fields(self):
        """Clear all input fields and results"""
        self.bpm_var.set("")
        self.note_var.set("Quarter Note (1/4)")
        self.ms_result.config(text="0.00 ms")
        self.sec_result.config(text="0.00 s")
        self.bpm_entry.focus()

def main():
    root = tk.Tk()
    app = BPMConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
