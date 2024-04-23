import pypdfium2 as pdfium

def pdf_to_pngs(pdf_path, output_folder):
    pdf = pdfium.PdfDocument(pdf_path)
    n_pages = len(pdf)

    filepaths = []
    for page_number in range(n_pages):
        page = pdf.get_page(page_number)
        pil_image = page.render(scale = 5).to_pil()
        filepath = f"{output_folder}{pdf_path.split('/')[-1].split('.')[0]}_{page_number+1}.png"
        pil_image.save(filepath)
        filepaths.append(filepath)

    return filepaths