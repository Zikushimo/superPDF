import tkinter as tk
from tkinter import filedialog, messagebox
import os
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm

def extend_pdf_with_lines(input_pdf, output_pdf, line_spacing):
    # Open the input PDF
    doc = fitz.open(input_pdf)
    
    # Create a new PDF for output
    out_doc = fitz.open()

    for page in doc:
        # Get the size of the original page
        original_width, original_height = page.rect.width, page.rect.height

        # Determine if the page is vertical (portrait) or horizontal (landscape)
        is_vertical = original_height > original_width

        # Set the output page size based on orientation
        if is_vertical:
            output_width, output_height = landscape(A4)
        else:
            output_width, output_height = A4

        # Calculate scaling factor to fit within output dimensions while maintaining aspect ratio
        scale_factor = min(output_height / original_height, output_width / original_width)

        # Calculate new dimensions
        new_width = original_width * scale_factor
        new_height = original_height * scale_factor

        # Create a new page with appropriate size
        new_page = out_doc.new_page(width=output_width, height=output_height)

        if is_vertical:
            # For vertical pages, place content on the left side
            content_rect = fitz.Rect(0, 0, new_width, output_height)
            # Calculate the width of the added area
            added_width = output_width - new_width
        else:
            # For horizontal pages, place content at the top
            content_rect = fitz.Rect(0, 0, output_width, new_height)
            # Calculate the height of the added area
            added_height = output_height - new_height

        # Add the original content to the new page, scaled to fit
        new_page.show_pdf_page(
            content_rect,
            doc,
            page.number,
            rotate=0,
            clip=page.rect
        )

        # Draw horizontal lines in the added area
        line_spacing_cm = float(line_spacing) * cm
        if is_vertical:
            # Draw horizontal lines on the right side for vertical pages
            for y in range(int(cm), int(output_height - cm), int(line_spacing_cm)):
                new_page.draw_line(
                    fitz.Point(new_width, y),
                    fitz.Point(output_width - cm, y),
                    color=(0.7, 0.7, 0.7),
                    width=0.5
                )
        else:
            # Draw lines at the bottom for horizontal pages
            for y in range(int(output_height - added_height), int(output_height), int(line_spacing_cm)):
                new_page.draw_line(
                    fitz.Point(cm, y),
                    fitz.Point(output_width - cm, y),
                    color=(0.7, 0.7, 0.7),
                    width=0.5
                )

    # Save the output PDF
    out_doc.save(output_pdf)
    out_doc.close()
    doc.close()

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def process_pdf():
    input_file = input_entry.get()
    output_file = output_entry.get()
    line_spacing = spacing_entry.get()

    if not input_file:
        messagebox.showerror("Error", "Please select an input PDF file.")
        return

    if not output_file:
        # Use the same name as input and add " - notes"
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name} - notes.pdf"

    try:
        extend_pdf_with_lines(input_file, output_file, line_spacing)
        messagebox.showinfo("Success", f"PDF processed successfully.\nOutput saved as: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("superPDF")
root.geometry("350x125")

# Input file selection
tk.Label(root, text="Input PDF:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
input_entry = tk.Entry(root, width=25)
input_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_input_file).grid(row=0, column=2, padx=5, pady=5)

# Output file name
tk.Label(root, text="Output PDF:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
output_entry = tk.Entry(root, width=25)
output_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Label(root, text="(Optional)").grid(row=1, column=2, padx=5, pady=5)

# Line spacing and Process button (inline)
tk.Label(root, text="Line Spacing:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
spacing_entry = tk.Entry(root, width=5)
spacing_entry.insert(0, "0.7")  # Default value
spacing_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
tk.Label(root, text="cm").grid(row=2, column=1, padx=(40, 5), pady=5, sticky="w")
tk.Button(root, text="Process PDF", command=process_pdf).grid(row=2, column=2, padx=5, pady=5)

root.mainloop()

# Process button
tk.Button(root, text="Process PDF", command=process_pdf).grid(row=3, column=1, pady=20)

root.mainloop()