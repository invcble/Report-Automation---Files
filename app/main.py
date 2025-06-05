import customtkinter as ctk
import os
from tkinter import messagebox
import dataclean
import dataprocess


class MerckTalentApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Merck Talent Incubator Report Generator")
        self.geometry("600x520")

        # Title box
        self.title_label = ctk.CTkLabel(self, text="Merck Talent Incubator", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=20)

        # Self Data file path input
        self.self_dat_label = ctk.CTkLabel(self, text="Self Assessment Data File (.csv):")
        self.self_dat_label.pack(pady=10)
        self.self_dat_entry = ctk.CTkEntry(self, width=500)
        self.self_dat_entry.pack()

        # Peer Data file path input
        self.peer_dat_label = ctk.CTkLabel(self, text="Peer Assessment Data File (.csv):")
        self.peer_dat_label.pack(pady=10)
        self.peer_dat_entry = ctk.CTkEntry(self, width=500)
        self.peer_dat_entry.pack()

        # Logo file path input
        self.logo_label = ctk.CTkLabel(self, text="Custom Logo File (2560×720 px .png):")
        self.logo_label.pack(pady=10)
        self.logo_entry = ctk.CTkEntry(self, width=500)
        self.logo_entry.pack()

        # Template file path input
        self.template_label = ctk.CTkLabel(self, text="Template File (.pdf):")
        self.template_label.pack(pady=10)
        self.template_entry = ctk.CTkEntry(self, width=500)
        self.template_entry.pack()

        # Generate Report button
        self.generate_button = ctk.CTkButton(self, text="Generate Reports", command=self.generate_reports)
        self.generate_button.pack(pady=30)

        # Status label
        self.status_label = ctk.CTkLabel(self, text="Ready to generate reports", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=10)

    def generate_reports(self):
        # Get input values and remove quotes
        self_dat_path = self.self_dat_entry.get().replace('"', '')
        peer_dat_path = self.peer_dat_entry.get().replace('"', '')
        logo_path = self.logo_entry.get().replace('"', '')
        template_path = self.template_entry.get().replace('"', '')

        # Validate inputs
        if not all([self_dat_path, peer_dat_path, logo_path, template_path]):
            messagebox.showerror("Input Error", "All fields must be filled in.")
            return

        # Check if input paths are valid
        if not os.path.exists(self_dat_path):
            messagebox.showerror("Error", "Self Assessment Data file not found.")
            return
        
        if not os.path.exists(peer_dat_path):
            messagebox.showerror("Error", "Peer Assessment Data file not found.")
            return
        
        if not os.path.exists(logo_path):
            messagebox.showerror("Error", "Logo file not found.")
            return
        
        if not os.path.exists(template_path):
            messagebox.showerror("Error", "Template file not found.")
            return

        # Validate file formats
        if not self_dat_path.endswith('.csv'):
            messagebox.showerror("Format Error", "Self Assessment Data file must be in .csv format.")
            return
        
        if not peer_dat_path.endswith('.csv'):
            messagebox.showerror("Format Error", "Peer Assessment Data file must be in .csv format.")
            return
        
        if not logo_path.endswith('.png'):
            messagebox.showerror("Format Error", "Logo file must be in .png format.")
            return
        
        if not template_path.endswith('.pdf'):
            messagebox.showerror("Format Error", "Template file must be in .pdf format.")
            return

        try:
            # Update status
            self.status_label.configure(text="Processing data...")
            self.update()

            # Constant path for combined CSV
            combined_csv_path = "CombinedDataNational_py.csv"

            # Run data cleaning
            self.status_label.configure(text="Cleaning data...")
            self.update()
            dataclean.clean(self_path=self_dat_path, peer_path=peer_dat_path)

            # Run data processing
            self.status_label.configure(text="Generating reports...")
            self.update()
            dataprocess.process(
                combined_path=combined_csv_path, 
                feedback_path=peer_dat_path, 
                logo_path=logo_path, 
                template_path=template_path
            )

            # Success message
            self.status_label.configure(text="Reports generated successfully!")
            messagebox.showinfo("Success", "Reports have been generated successfully!")

        except Exception as e:
            # Error handling
            self.status_label.configure(text="Error occurred during processing")
            messagebox.showerror("Processing Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Set the appearance mode and color theme
    ctk.set_appearance_mode("system")  # or "dark" or "light"
    ctk.set_default_color_theme("blue")  # or "green" or "dark-blue"
    
    app = MerckTalentApp()
    app.mainloop()