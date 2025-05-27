#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gallery-DL GUI
A graphical user interface for the gallery-dl command-line tool.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import sys
import shlex
import platform


class GalleryDLGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gallery-DL GUI")
        self.root.geometry("700x750")
        self.root.minsize(600, 600)
        
        # Variables for GUI controls
        self.setup_variables()
        
        # Create the GUI layout
        self.create_widgets()
        
        # Track download process
        self.download_process = None
        self.download_thread = None
        self.is_downloading = False
        
    def setup_variables(self):
        """Initialize all tkinter variables for GUI controls"""
        # Input/Output variables
        self.url_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        
        # Common options
        self.overwrite_var = tk.BooleanVar(value=False)  # --no-skip
        self.verbose_var = tk.BooleanVar(value=True)     # -v
        self.filename_format_var = tk.StringVar()        # -f
        self.range_var = tk.StringVar()                  # --range
        self.filter_var = tk.StringVar()                 # --filter
        
        # Metadata and files
        self.write_metadata_var = tk.BooleanVar(value=False)    # --write-metadata
        self.write_info_json_var = tk.BooleanVar(value=False)   # --write-info-json
        self.write_tags_var = tk.BooleanVar(value=False)        # --write-tags
        self.zip_var = tk.BooleanVar(value=False)               # --zip
        
        # Advanced/Authentication
        self.username_var = tk.StringVar()               # -u
        self.password_var = tk.StringVar()               # -p
        self.limit_rate_var = tk.StringVar()             # -r
        self.download_archive_var = tk.StringVar()       # --download-archive
        self.additional_options_var = tk.StringVar()     # raw flags
        
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)  # Log area should expand
        
        # Input/Output section
        self.create_input_output_section(main_frame)
        
        # Options notebook (tabs)
        self.create_options_notebook(main_frame)
        
        # Download button
        self.create_download_button(main_frame)
        
        # Log area
        self.create_log_area(main_frame)
        
    def create_input_output_section(self, parent):
        """Create the input/output section"""
        io_frame = ttk.LabelFrame(parent, text="Entrada y Salida", padding="5")
        io_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        io_frame.columnconfigure(1, weight=1)
        
        # URL input
        ttk.Label(io_frame, text="URL(s):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        url_entry = ttk.Entry(io_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Output directory
        ttk.Label(io_frame, text="Directorio de Salida:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        
        dir_frame = ttk.Frame(io_frame)
        dir_frame.grid(row=1, column=1, sticky=(tk.W, tk.E))
        dir_frame.columnconfigure(0, weight=1)
        
        dir_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var)
        dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        browse_btn = ttk.Button(dir_frame, text="Buscar...", command=self.browse_directory)
        browse_btn.grid(row=0, column=1)
        
    def create_options_notebook(self, parent):
        """Create the options notebook with tabs"""
        notebook = ttk.Notebook(parent)
        notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Tab 1: Common Options
        self.create_common_options_tab(notebook)
        
        # Tab 2: Metadata and Files
        self.create_metadata_files_tab(notebook)
        
        # Tab 3: Advanced/Authentication
        self.create_advanced_tab(notebook)
        
    def create_common_options_tab(self, notebook):
        """Create the common options tab"""
        tab1 = ttk.Frame(notebook, padding="10")
        notebook.add(tab1, text="Opciones Comunes")
        
        # Overwrite files checkbox
        overwrite_cb = ttk.Checkbutton(
            tab1, 
            text="Sobrescribir archivos existentes", 
            variable=self.overwrite_var
        )
        overwrite_cb.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Verbose mode checkbox
        verbose_cb = ttk.Checkbutton(
            tab1, 
            text="Modo Detallado (Verbose)", 
            variable=self.verbose_var
        )
        verbose_cb.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Filename format
        ttk.Label(tab1, text="Formato de Nombre de Archivo:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        filename_entry = ttk.Entry(tab1, textvariable=self.filename_format_var, width=50)
        filename_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Range
        ttk.Label(tab1, text="Rango de descarga:").grid(row=4, column=0, sticky=tk.W, pady=(10, 0))
        range_entry = ttk.Entry(tab1, textvariable=self.range_var, width=50)
        range_entry.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Filter
        ttk.Label(tab1, text="Filtro de descarga:").grid(row=6, column=0, sticky=tk.W, pady=(10, 0))
        filter_entry = ttk.Entry(tab1, textvariable=self.filter_var, width=50)
        filter_entry.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=(0, 2))
        
        # Filter help text
        help_label = ttk.Label(
            tab1, 
            text="Ej: \"image_width >= 1000 and rating == 's'\"",
            font=("TkDefaultFont", 8),
            foreground="gray"
        )
        help_label.grid(row=8, column=0, sticky=tk.W)
        
        # Configure column weight for resizing
        tab1.columnconfigure(0, weight=1)
        
    def create_metadata_files_tab(self, notebook):
        """Create the metadata and files tab"""
        tab2 = ttk.Frame(notebook, padding="10")
        notebook.add(tab2, text="Metadatos y Archivos")
        
        # Write metadata checkbox
        metadata_cb = ttk.Checkbutton(
            tab2, 
            text="Escribir metadatos (.json por archivo)", 
            variable=self.write_metadata_var
        )
        metadata_cb.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Write info.json checkbox
        info_json_cb = ttk.Checkbutton(
            tab2, 
            text="Escribir info.json (galería/álbum)", 
            variable=self.write_info_json_var
        )
        info_json_cb.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Write tags checkbox
        tags_cb = ttk.Checkbutton(
            tab2, 
            text="Escribir tags (.txt por archivo)", 
            variable=self.write_tags_var
        )
        tags_cb.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        # ZIP compression checkbox
        zip_cb = ttk.Checkbutton(
            tab2, 
            text="Comprimir en ZIP", 
            variable=self.zip_var
        )
        zip_cb.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        # Configure column weight for resizing
        tab2.columnconfigure(0, weight=1)
        
    def create_advanced_tab(self, notebook):
        """Create the advanced/authentication tab"""
        tab3 = ttk.Frame(notebook, padding="10")
        notebook.add(tab3, text="Avanzado / Autenticación")
        tab3.columnconfigure(1, weight=1)
        
        # Username
        ttk.Label(tab3, text="Usuario:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        username_entry = ttk.Entry(tab3, textvariable=self.username_var, width=30)
        username_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Password
        ttk.Label(tab3, text="Contraseña:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        password_entry = ttk.Entry(tab3, textvariable=self.password_var, show="*", width=30)
        password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Limit rate
        ttk.Label(tab3, text="Límite de velocidad:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5))
        rate_entry = ttk.Entry(tab3, textvariable=self.limit_rate_var, width=30)
        rate_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Download archive
        ttk.Label(tab3, text="Archivo de historial:").grid(row=3, column=0, sticky=tk.W, padx=(0, 5))
        
        archive_frame = ttk.Frame(tab3)
        archive_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        archive_frame.columnconfigure(0, weight=1)
        
        archive_entry = ttk.Entry(archive_frame, textvariable=self.download_archive_var)
        archive_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        archive_btn = ttk.Button(archive_frame, text="Seleccionar archivo...", command=self.browse_archive_file)
        archive_btn.grid(row=0, column=1)
        
        # Additional options
        ttk.Label(tab3, text="Opciones Adicionales (raw flags):").grid(row=4, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        additional_entry = ttk.Entry(tab3, textvariable=self.additional_options_var, width=30)
        additional_entry.grid(row=5, column=1, sticky=(tk.W, tk.E))
        
    def create_download_button(self, parent):
        """Create the download and stop buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, pady=(0, 10))
        
        self.download_btn = ttk.Button(
            button_frame, 
            text="Descargar", 
            command=self.start_download,
            style="Accent.TButton"
        )
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(
            button_frame, 
            text="Detener", 
            command=self.stop_download,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT)
        
    def create_log_area(self, parent):
        """Create the log area"""
        log_frame = ttk.LabelFrame(parent, text="Log de Descarga", padding="5")
        log_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            height=15, 
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def browse_directory(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)
            
    def browse_archive_file(self):
        """Browse for download archive file"""
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de historial",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.download_archive_var.set(filename)
            
    def find_gallery_dl_executable(self):
        """
        Find the gallery-dl executable using multiple strategies.
        Returns a list of arguments for subprocess.
        """
        # Priority 1: Packaged environment (PyInstaller)
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            bundle_dir = os.path.dirname(sys.executable)
            if platform.system() == "Windows":
                gallery_dl_exe = os.path.join(bundle_dir, "gallery-dl.exe")
                if os.path.isfile(gallery_dl_exe):
                    return [gallery_dl_exe]
            else:
                gallery_dl_exe = os.path.join(bundle_dir, "gallery-dl")
                if os.path.isfile(gallery_dl_exe):
                    return [gallery_dl_exe]
        
        # Priority 2: Check if gallery-dl is in PATH
        try:
            result = subprocess.run(
                ["gallery-dl", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                return ["gallery-dl"]
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass
        
        # Priority 3: Python module
        try:
            result = subprocess.run(
                [sys.executable, "-m", "gallery_dl", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                return [sys.executable, "-m", "gallery_dl"]
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass
        
        # Priority 4: Local script (if GUI is in gallery-dl project root)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_py = os.path.join(script_dir, "gallery_dl", "__main__.py")
        if os.path.isfile(main_py):
            try:
                result = subprocess.run(
                    [sys.executable, main_py, "--version"], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                if result.returncode == 0:
                    return [sys.executable, main_py]
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
                pass
        
        # Fallback: assume gallery-dl is available
        return ["gallery-dl"]
        
    def build_command(self):
        """Build the gallery-dl command based on GUI selections"""
        # Get base command
        command = self.find_gallery_dl_executable()
        
        # Add output directory if specified
        output_dir = self.output_dir_var.get().strip()
        if output_dir:
            command.extend(["-d", output_dir])
        
        # Add common options
        if self.overwrite_var.get():
            command.append("--no-skip")
            
        if self.verbose_var.get():
            command.append("-v")
            
        filename_format = self.filename_format_var.get().strip()
        if filename_format:
            command.extend(["-f", filename_format])
            
        range_val = self.range_var.get().strip()
        if range_val:
            command.extend(["--range", range_val])
            
        filter_val = self.filter_var.get().strip()
        if filter_val:
            command.extend(["--filter", filter_val])
        
        # Add metadata and files options
        if self.write_metadata_var.get():
            command.append("--write-metadata")
            
        if self.write_info_json_var.get():
            command.append("--write-info-json")
            
        if self.write_tags_var.get():
            command.append("--write-tags")
            
        if self.zip_var.get():
            command.append("--zip")
        
        # Add advanced options
        username = self.username_var.get().strip()
        if username:
            command.extend(["-u", username])
            
        password = self.password_var.get().strip()
        if password:
            command.extend(["-p", password])
            
        limit_rate = self.limit_rate_var.get().strip()
        if limit_rate:
            command.extend(["-r", limit_rate])
            
        download_archive = self.download_archive_var.get().strip()
        if download_archive:
            command.extend(["--download-archive", download_archive])
        
        # Add additional options
        additional = self.additional_options_var.get().strip()
        if additional:
            # Split additional options properly
            try:
                additional_args = shlex.split(additional)
                command.extend(additional_args)
            except ValueError:
                # If shlex fails, split by spaces
                command.extend(additional.split())
        
        # Add URLs (required)
        urls = self.url_var.get().strip()
        if urls:
            # Split URLs by whitespace
            url_list = urls.split()
            command.extend(url_list)
        
        return command
        
    def start_download(self):
        """Start the download process"""
        # Validate input
        urls = self.url_var.get().strip()
        if not urls:
            messagebox.showerror("Error", "Por favor, ingrese al menos una URL.")
            return
        
        # Build command
        try:
            command = self.build_command()
        except Exception as e:
            messagebox.showerror("Error", f"Error al construir el comando: {str(e)}")
            return
        
        # Clear log
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Log the command being executed
        self.append_to_log(f"Ejecutando: {' '.join(command)}\n\n")
        
        # Disable download button and enable stop button
        self.download_btn.config(state=tk.DISABLED, text="Descargando...")
        self.stop_btn.config(state=tk.NORMAL)
        self.is_downloading = True
        
        # Start download in separate thread
        self.download_thread = threading.Thread(
            target=self.run_gallery_dl, 
            args=(command,),
            daemon=True
        )
        self.download_thread.start()
        
    def stop_download(self):
        """Stop the current download process"""
        if self.is_downloading and self.download_process:
            try:
                # Terminate the gallery-dl process
                self.download_process.terminate()
                
                # Give it a moment to terminate gracefully
                try:
                    self.download_process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    # If it doesn't terminate gracefully, force kill it
                    self.download_process.kill()
                    self.download_process.wait()
                
                # Log the cancellation
                self.append_to_log("\n⚠️ Descarga cancelada por el usuario.\n")
                
            except Exception as e:
                self.append_to_log(f"\n⚠️ Error al cancelar la descarga: {str(e)}\n")
            
            finally:
                # Reset the GUI state
                self.download_finished()
        
    def run_gallery_dl(self, command):
        """Run gallery-dl in a separate thread"""
        try:
            # Setup subprocess parameters
            startupinfo = None
            creationflags = 0
            
            # Hide console window on Windows
            if platform.system() == "Windows":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                creationflags = subprocess.CREATE_NO_WINDOW
            
            # Start process
            self.download_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            
            # Read output in real-time
            for line in iter(self.download_process.stdout.readline, ''):
                if line:
                    self.root.after(0, self.append_to_log, line)
                # Check if process was terminated
                if self.download_process.poll() is not None:
                    break
            
            # Wait for process to complete
            self.download_process.wait()
            
            # Check return code
            if self.download_process.returncode == 0:
                self.root.after(0, self.append_to_log, "\n✓ Descarga completada exitosamente.\n")
            elif self.download_process.returncode == -15 or self.download_process.returncode == 1:
                # Process was terminated (SIGTERM on Unix, or general error)
                # Don't show error message as it was likely user-initiated
                pass
            else:
                self.root.after(0, self.append_to_log, f"\n✗ Descarga terminó con código de error: {self.download_process.returncode}\n")
                
        except Exception as e:
            self.root.after(0, self.append_to_log, f"\n✗ Error durante la descarga: {str(e)}\n")
        
        finally:
            # Re-enable download button
            self.root.after(0, self.download_finished)
            
    def download_finished(self):
        """Called when download is finished"""
        self.download_btn.config(state=tk.NORMAL, text="Descargar")
        self.stop_btn.config(state=tk.DISABLED)
        self.is_downloading = False
        self.download_process = None
        
    def append_to_log(self, text):
        """Append text to the log area"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)  # Auto-scroll to bottom
        self.log_text.config(state=tk.DISABLED)
        
    def on_closing(self):
        """Handle window closing"""
        if self.is_downloading and self.download_process:
            if messagebox.askokcancel("Cerrar", "Hay una descarga en progreso. ¿Desea cancelarla y cerrar?"):
                # Use the stop_download method for proper cleanup
                self.stop_download()
                # Give a moment for cleanup
                self.root.after(100, self.root.destroy)
        else:
            self.root.destroy()


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    
    # Set up the GUI
    app = GalleryDLGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main() 