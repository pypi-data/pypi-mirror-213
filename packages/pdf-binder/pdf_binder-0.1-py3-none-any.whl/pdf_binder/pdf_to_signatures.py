import sys
import math
import PyPDF2
from PIL import Image, ImageDraw
from io import BytesIO
from pdf2image import convert_from_path
from tqdm import tqdm


def pdf_to_signatures(input_pdf_path, papers_per_signature=4, output_pdf_path="bound_book.pdf", num_stitches = 7):
    # Convert PDF to list of images
    print("Reading in PDF...")
    images = convert_from_path(input_pdf_path)
    total_pages = len(images)

    # Add blank pages to make total pages a multiple of 4
    while total_pages % 4 != 0:
        blank_page = Image.new('RGB', (images[0].width, images[0].height), 'white')
        images.append(blank_page)
        total_pages += 1

    pages_per_signature = papers_per_signature * 4
    total_signatures = math.ceil(total_pages / pages_per_signature)

    output_pdf = PyPDF2.PdfWriter()

    # Progress bar for signatures
    for sig_index in tqdm(range(total_signatures), desc="Processing signatures", unit="signature"):
        start_page = sig_index * pages_per_signature
        end_page = min(start_page + pages_per_signature, total_pages)

        pages_in_signature = end_page - start_page
        papers_in_signature = math.ceil(pages_in_signature / 4)
        offset = sig_index * pages_per_signature

        # Process pages within a signature
        for i in range(papers_in_signature):
            # Calculate the page indices for front side of the paper
            left_page_front = offset + pages_in_signature - 1 - 2 * i
            right_page_front = offset + 2 * i

            # Calculate the page indices for back side of the paper
            left_page_back = offset + 1 + 2 * i
            right_page_back = offset + pages_in_signature - 2 - 2 * i

            # Create new image with double width for front side
            new_image_front = Image.new('RGB', (2 * images[0].width, images[0].height), 'white')

            # Paste the pages for front side
            if left_page_front < total_pages:
                new_image_front.paste(images[left_page_front], (0, 0))
            if right_page_front < total_pages:
                new_image_front.paste(images[right_page_front], (images[0].width, 0))

            # Create new image with double width for back side
            new_image_back = Image.new('RGB', (2 * images[0].width, images[0].height), 'white')

            # Paste the pages for back side
            if left_page_back < total_pages:
                new_image_back.paste(images[left_page_back], (0, 0))
            if right_page_back < total_pages:
                new_image_back.paste(images[right_page_back], (images[0].width, 0))

            # Draw stitch marks on the first front page of the signature
            if i == 0:
                draw = ImageDraw.Draw(new_image_front)
                for s in range(num_stitches):
                    y_position = (s + 1) * (images[0].height / (num_stitches + 1))
                    draw.ellipse([(images[0].width - 5, y_position - 2), (images[0].width + 5, y_position + 2)], fill="black")

            # Draw stitch marks on the last back page of the signature
            if i == papers_in_signature - 1:
                draw = ImageDraw.Draw(new_image_back)
                for s in range(num_stitches):
                    y_position = (s + 1) * (images[0].height / (num_stitches + 1))
                    draw.ellipse([(images[0].width - 5, y_position - 2), (images[0].width + 5, y_position + 2)], fill="black")

            # Save the new combined images to bytes buffers
            buffer_front = BytesIO()
            new_image_front.save(buffer_front, format="PDF", resolution=100.0, quality=95, optimize=True)

            buffer_back = BytesIO()
            new_image_back.save(buffer_back, format="PDF", resolution=100.0, quality=95, optimize=True)

            # Move buffer positions to beginning
            buffer_front.seek(0)
            buffer_back.seek(0)

            # Create new PDF pages from the bytes buffers and add them to the output PDF
            page_front = PyPDF2.PdfReader(buffer_front)
            output_pdf.add_page(page_front.pages[0])

            page_back = PyPDF2.PdfReader(buffer_back)
            output_pdf.add_page(page_back.pages[0])

    # Save the output PDF
    with open(output_pdf_path, 'wb') as output_file:
        output_pdf.write(output_file)


def main():
    if len(sys.argv) != 4:
        print('Usage: python pdf_to_signatures.py <input_pdf> <papers_per_signature> <output_pdf>')
        sys.exit(1)

    input_pdf_path = sys.argv[1]
    papers_per_signature = int(sys.argv[2])
    output_pdf_path = sys.argv[3]

    pdf_to_signatures(input_pdf_path, papers_per_signature, output_pdf_path)


if __name__ == '__main__':
    main()
