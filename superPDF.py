import fitz  # PyMuPDF
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm

def extend_pdf_with_lines(input_pdf, output_pdf):
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
        line_spacing = 0.7 * cm
        if is_vertical:
            # Draw horizontal lines on the right side for vertical pages
            for y in range(int(cm), int(output_height - cm), int(line_spacing)):
                new_page.draw_line(
                    fitz.Point(new_width, y),
                    fitz.Point(output_width - cm, y),
                    color=(0.7, 0.7, 0.7),
                    width=0.5
                )
        else:
            # Draw lines at the bottom for horizontal pages
            for y in range(int(output_height - added_height), int(output_height), int(line_spacing)):
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

# Usage
input_pdf = "input2.pdf"
output_pdf = "output.pdf"
extend_pdf_with_lines(input_pdf, output_pdf)