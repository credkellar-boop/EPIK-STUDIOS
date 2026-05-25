import tkinter as tk
from tkinter import ttk, messagebox
import threading
from brain.engine import run_epic_engine

class EpicStudiosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EPIC-STUDIO'S // AI Control Center")
        self.root.geometry("650x550")
        self.root.configure(bg="#121212")
        
        # Apply dark mode style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background="#121212", foreground="#FFFFFF")
        self.style.configure("TLabel", background="#121212", foreground="#8E8E93", font=("Helvetica", 10))
        self.style.configure("TButton", background="#1D1D1F", foreground="#007AFF", borderwidth=0, font=("Helvetica", 10, "bold"))
        self.style.map("TButton", background=[("active", "#2C2C2E")])

        self.create_widgets()

    def create_widgets(self):
        # Header Title
        title_label = tk.Label(self.root, text="EPIC-STUDIO'S", font=("Helvetica", 18, "bold"), bg="#121212", fg="#007AFF")
        title_label.pack(pady=15)
        
        subtitle_label = ttk.Label(self.root, text="Gemini-Powered GitHub Automation Layer for FL Studio")
        subtitle_label.pack(pady=2)

        # Input Prompt Field
        input_label = ttk.Label(self.root, text="What script or macro do you want to generate?")
        input_label.pack(anchor="w", padx=25, pady=(15, 5))
        
        self.prompt_entry = tk.Text(self.root, height=4, bg="#1D1D1F", fg="#FFFFFF", insertbackground="white", relief="flat", font=("Helvetica", 11))
        self.prompt_entry.pack(fill="x", padx=25, pady=5)
        self.prompt_entry.insert("1.0", "Create a piano roll script that automates velocity dynamics and applies an auto-tone key filter.")

        # Action Button
        self.gen_button = ttk.Button(self.root, text="COMPILE VIA GEMINI & GITHUB", command=self.start_generation_thread)
        self.gen_button.pack(fill="x", padx=25, pady=15)

        # Output/Status Logs console
        output_label = ttk.Label(self.root, text="Generated Extension Console Output:")
        output_label.pack(anchor="w", padx=25, pady=(10, 5))
        
        self.output_text = tk.Text(self.root, bg="#000000", fg="#34C759", insertbackground="white", relief="flat", font=("Courier New", 10))
        self.output_text.pack(fill="both", expand=True, padx=25, pady=(5, 20))

    def start_generation_thread(self):
        """Prevents the UI window from freezing up while Gemini computes the response."""
        user_prompt = self.prompt_entry.get("1.0", "end-1c").strip()
        if not user_prompt:
            messagebox.showwarning("Empty Prompt", "Please enter a script objective before compiling.")
            return
        
        self.gen_button.config(state="disabled")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", "[SYSTEM] Contacting GitHub and spinning up Gemini Engine...\n")
        
        thread = threading.Thread(target=self.generate_script, args=(user_prompt,))
        thread.start()

    def generate_script(self, user_prompt):
        try:
            # Execute pipeline
            compiled_output = run_epic_engine(user_prompt)
            
            # Update the application screen safely on the main loop
            self.root.after(0, self.display_output, compiled_output)
        except Exception as e:
            self.root.after(0, self.display_output, f"[ERROR] Execution pipeline failed:\n{str(e)}")

    def display_output(self, content):
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", content)
        self.gen_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = EpicStudiosApp(root)
    root.mainloop()
