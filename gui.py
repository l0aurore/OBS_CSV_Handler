"""GUI interface for the OBS CSV Updater plugin."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from background_scripts.config import DEFAULT_CSV_PATH, OBS_HOST, OBS_PORT, BASE_DIR
from background_scripts.csv_handler import CSVHandler
from background_scripts.obs_controller import OBSController
from background_scripts.logger import logger

class ConfigureMappingDialog(tk.Toplevel):
    def __init__(self, parent, csv_handler):
        """Initialize the mapping configuration dialog."""
        super().__init__(parent)
        self.title("Configure CSV Mapping")
        self.geometry("600x500")
        self.csv_handler = csv_handler

        # Make dialog modal
        self.transient(parent)
        self.grab_set()

        # Create main frame with padding
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Instructions
        instruction_text = "Map CSV columns to OBS sources\n" + \
                           "Each column will create a separate text source in OBS"
        ttk.Label(main_frame, text=instruction_text, padding=5).pack(fill=tk.X)

        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Get and organize columns
        self.available_columns = self.organize_columns(self.csv_handler.get_available_columns())

        # Create mapping UI
        self.mapping_entries = []
        self.create_mapping_tabs()

        # Create buttons
        button_frame = ttk.Frame(main_frame, padding="5")
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(button_frame, text="Save", command=self.save_mapping).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def organize_columns(self, columns):
        """Organize columns into groups (e.g., player_1_*, player_2_*)."""
        organized = {}
        for col in columns:
            # Skip empty column names
            if not col:
                continue

            parts = col.split('_')
            if len(parts) > 1:
                # Use first two parts as group key (e.g., "player_1")
                group_key = '_'.join(parts[:2])
                if group_key not in organized:
                    organized[group_key] = []
                organized[group_key].append(col)
            else:
                # No grouping for simple columns
                if 'Other' not in organized:
                    organized['Other'] = []
                organized['Other'].append(col)

        logger.debug(f"Organized columns: {organized}")
        return organized

    def create_mapping_tabs(self):
        """Create tabs for each group of columns."""
        for group, columns in self.available_columns.items():
            # Skip empty groups
            if not columns:
                continue

            # Create a new tab for the group
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=group.replace('_', ' ').title())

            # Create scrollable frame for the tab
            canvas = tk.Canvas(tab)
            scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            # Configure scrolling
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Add header
            header_frame = ttk.Frame(scrollable_frame)
            header_frame.pack(fill=tk.X, pady=(0, 5))
            ttk.Label(header_frame, text="OBS Source Name", width=30).pack(side=tk.LEFT, padx=5)
            ttk.Label(header_frame, text="CSV Column", width=30).pack(side=tk.LEFT, padx=5)

            # Add mapping rows for each column
            for column in columns:
                self.add_mapping_row(scrollable_frame, column)

            # Pack the canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="both")

    def add_mapping_row(self, parent, column_name):
        """Add a new mapping row to the interface."""
        row_frame = ttk.Frame(parent)
        row_frame.pack(fill=tk.X, pady=2)

        # Source name entry with suggested name
        source_entry = ttk.Entry(row_frame, width=30)
        source_entry.pack(side=tk.LEFT, padx=5)

        # Suggest OBS source name based on column
        suggested_name = column_name.replace('_', ' ').title()
        source_entry.insert(0, suggested_name)

        # Column name (read-only)
        column_label = ttk.Label(row_frame, text=column_name, width=30)
        column_label.pack(side=tk.LEFT, padx=5)

        self.mapping_entries.append((source_entry, column_name))

    def save_mapping(self):
        """Save the current mapping configuration."""
        mapping = {}
        for source_entry, column_name in self.mapping_entries:
            source_name = source_entry.get().strip()
            if source_name:  # Only save non-empty source names
                mapping[source_name] = column_name

        if mapping:
            self.csv_handler.set_column_mapping(mapping)
            logger.info(f"Saved column mapping: {mapping}")
            messagebox.showinfo("Success", "Column mapping saved successfully")
            self.destroy()
        else:
            messagebox.showwarning("Warning", "Please configure at least one valid mapping")


class CreateSourceDialog(tk.Toplevel):
    def __init__(self, parent):
        """Initialize the create source dialog."""
        super().__init__(parent)
        self.title("Create New Source")
        self.geometry("300x150")
        self.resizable(False, False)

        # Center the dialog on parent
        self.transient(parent)
        self.grab_set()

        # Source name entry
        name_frame = ttk.Frame(self, padding="5")
        name_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(name_frame, text="Source Name:").pack(side=tk.LEFT)
        self.name_entry = ttk.Entry(name_frame)
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # Source value entry
        value_frame = ttk.Frame(self, padding="5")
        value_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(value_frame, text="Initial Value:").pack(side=tk.LEFT)
        self.value_entry = ttk.Entry(value_frame)
        self.value_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # Buttons
        button_frame = ttk.Frame(self, padding="5")
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(button_frame, text="Create", command=self.create).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT)

        self.result = None

    def create(self):
        """Validate and return the new source details."""
        name = self.name_entry.get().strip()
        value = self.value_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Source name is required")
            return

        self.result = (name, value)
        self.destroy()

    def cancel(self):
        """Cancel the dialog."""
        self.destroy()

class OBSUpdaterGUI:
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("OBS CSV Updater")
        self.root.geometry("600x400")

        # Initialize current CSV path
        self.current_csv_path = DEFAULT_CSV_PATH
        #self.ensure_csv_exists()

        # Initialize handlers
        self.csv_handler = CSVHandler(self.current_csv_path)
        self.obs_controller = OBSController(OBS_HOST, OBS_PORT)
        self.column_mapping = self.csv_handler.column_mapping

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # File selection frame
        self.create_file_selection_frame()

        # Status bar
        self.status_var = tk.StringVar(value="Status: Disconnected")
        self.status_label = ttk.Label(self.main_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, columnspan=2, sticky="w")

        # Create treeview for sources
        self.create_source_tree()

        # Buttons
        self.create_buttons()

        # Initial load
        self.connect_to_obs()

    def create_file_selection_frame(self):
        """Create the file selection frame with path display and browse button."""
        file_frame = ttk.Frame(self.main_frame)
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # CSV Path Label
        self.path_var = tk.StringVar(value=self.current_csv_path)
        path_label = ttk.Label(file_frame, textvariable=self.path_var, wraplength=450)
        path_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        # Browse Button
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_csv)
        browse_btn.pack(side=tk.RIGHT)

    def browse_csv(self):
        """Open file dialog to select a CSV file."""
        try:
            initial_dir = os.path.dirname(self.current_csv_path)
            filepath = filedialog.askopenfilename(
                title="Select CSV File",
                initialdir=initial_dir,
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if filepath:
                # Convert to absolute path
                filepath = os.path.abspath(filepath)
                logger.info(f"Selected CSV file path: {filepath}")

                # Create new CSV handler instance with the new file
                self.csv_handler = CSVHandler(filepath)

                # Update current path and display
                self.current_csv_path = filepath
                self.path_var.set(filepath)

                # Get available columns and log them
                columns = self.csv_handler.get_available_columns()
                logger.info(f"Found columns in CSV: {columns}")

                if columns:
                    # Clear existing tree items
                    for item in self.tree.get_children():
                        self.tree.delete(item)

                    # Open mapping dialog
                    logger.info("Opening mapping dialog...")
                    self.open_mapping_dialog()
                else:
                    logger.error("No columns found in CSV file")
                    messagebox.showerror("Error", "No columns found in the selected CSV file")

        except Exception as e:
            logger.error(f"Error loading CSV file: {str(e)}")
            messagebox.showerror("Error", f"Failed to load CSV file: {str(e)}")

    def create_source_tree(self):
        """Create the treeview for displaying sources."""
        columns = ("Source Name", "Value")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")

        # Set column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Grid layout
        self.tree.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=2, column=2, sticky=(tk.N, tk.S))

        # Bind double-click for editing
        self.tree.bind("<Double-1>", self.edit_item)

    def create_buttons(self):
        """Create control buttons."""
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add New Source", 
                  command=self.create_new_source).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Configure CSV Mapping",
                  command=self.open_mapping_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh",
                  command=self.load_sources).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Changes",
                  command=self.save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Connect to OBS",
                  command=self.connect_to_obs).pack(side=tk.LEFT, padx=5)

    def load_sources(self):
        """Load sources from CSV file."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load new data
        data = self.csv_handler.read_csv()
        if data:
            for source_name, value in data.items():
                self.tree.insert("", tk.END, values=(source_name, value))
            logger.info("Sources loaded successfully")
        else:
            messagebox.showerror("Error", f"Failed to load sources from {self.current_csv_path}")
    
    def edit_item(self, event):
        """Handle double-click to edit item in Treeview and update CSV."""
        item = self.tree.selection()[0]  # Get selected row
        column = self.tree.identify_column(event.x)

        if column in ("#1", "#2"):  # Allow editing Source Name (col #1) or Value (col #2)
            col_index = 0 if column == "#1" else 1  # 0 = source_name, 1 = value
            x, y, w, h = self.tree.bbox(item, column)

            # Get current value and create an Entry widget
            current_value = self.tree.item(item)['values'][col_index]
            entry = ttk.Entry(self.tree)
            entry.place(x=x, y=y, width=w, height=h)
            entry.insert(0, current_value)
            entry.select_range(0, tk.END)
            entry.focus()

            def save_edit(event):
                """Save edited value and update CSV."""
                new_value = entry.get().strip()  # Strip whitespace
                row_values = self.tree.item(item)['values'][:]  # Copy row data
                old_source_name = row_values[0]  # Store old source name before updating

                # Update the Treeview UI
                row_values[col_index] = new_value
                self.tree.item(item, values=row_values)
                entry.destroy()

                logger.info(f"Updating CSV: Old Row - {row_values}")

                # Find the corresponding column in the CSV using column_mapping
                column_name = self.csv_handler.column_mapping.get(old_source_name)

                if column_name:
                    try:
                        # Read CSV into a list
                        updated_data = []
                        with open(self.current_csv_path, 'r', newline='', encoding='utf-8') as f:
                            reader = csv.reader(f)
                            header = next(reader)  # Read header row
                            updated_data.append(header)  # Preserve header

                            # Read the row (since only one row in your CSV)
                            row = next(reader)
                            logger.info(f"Original row from CSV: {row}")

                            # Update the specific column in the CSV
                            if column_name in header:
                                column_index = header.index(column_name)
                                row[column_index] = new_value
                                logger.info(f"Updated column {column_name} with new value: {new_value}")
                            else:
                                logger.warning(f"Column '{column_name}' not found in CSV header!")

                            updated_data.append(row)

                        # Write the updated data back to the CSV
                        with open(self.current_csv_path, 'w', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerows(updated_data)  # Write all updated rows

                        logger.info(f"CSV successfully updated: {self.current_csv_path}")

                    except Exception as e:
                        logger.error(f"Error updating CSV: {str(e)}")
                else:
                    logger.warning(f"Source name '{old_source_name}' not found in column_mapping!")

            entry.bind('<Return>', save_edit)  # Save on Enter key
            entry.bind('<FocusOut>', lambda e: entry.destroy())  # Destroy on focus out


    def save_changes(self):
        """Save changes to CSV and update OBS."""
        try:
            # Get all items from treeview
            sources = {}
            for item in self.tree.get_children():
                source_name, value = self.tree.item(item)['values']
                sources[source_name] = value

            # Update OBS
            if self.obs_controller.bulk_update_sources(sources):
                messagebox.showinfo("Success", "Changes saved and sources updated")
                logger.info("Changes saved and sources updated successfully")
            else:
                messagebox.showwarning("Warning", "Changes saved but failed to update some sources")

            # Refresh the display
            self.load_sources()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {str(e)}")
            logger.error(f"Failed to save changes: {str(e)}")

    def connect_to_obs(self):
        """Connect to OBS."""
        if self.obs_controller.connect():
            self.status_var.set("Status: Connected to OBS")
            logger.info("Connected to OBS successfully")
        else:
            self.status_var.set("Status: Connection Failed")
            logger.error("Failed to connect to OBS")

    def create_new_source(self):
        """Open dialog to create a new source."""
        dialog = CreateSourceDialog(self.root)
        self.root.wait_window(dialog)

        if dialog.result:
            source_name, value = dialog.result

            try:
                # First create the source in OBS
                if self.obs_controller.create_text_source(source_name, str(value)):
                    # Add to tree
                    self.tree.insert("", tk.END, values=(source_name, value))

                    # Save changes immediately
                    self.save_changes()
                    logger.info(f"Created new source: {source_name} with value: {value}")
                else:
                    raise Exception("Failed to create source in OBS")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create source: {str(e)}")
                logger.error(f"Failed to create source: {str(e)}")

    def open_mapping_dialog(self):
        """Open the CSV mapping configuration dialog."""
        try:
            logger.info("Creating mapping dialog...")
            dialog = ConfigureMappingDialog(self.root, self.csv_handler)
            logger.info("Waiting for mapping dialog...")
            self.root.wait_window(dialog)
            logger.info("Mapping dialog closed, reloading sources...")
            # Reload sources after mapping is configured
            self.load_sources()
        except Exception as e:
            logger.error(f"Error in mapping dialog: {str(e)}")
            messagebox.showerror("Error", f"Failed to open mapping dialog: {str(e)}")


def main():
    root = tk.Tk()
    app = OBSUpdaterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()