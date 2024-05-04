import pypdfium2 as pdfium
from oemer.oemer import ete

def pdf_to_mxls(pdf_path, output_folder):
    pdf = pdfium.PdfDocument(pdf_path)
    n_pages = len(pdf)

    filepaths = []
    for page_number in range(n_pages):
        page = pdf.get_page(page_number)
        pil_image = page.render(scale = 5).to_pil()
        png_filepath = f"{output_folder}{pdf_path.split('/')[-1].split('.')[0]}_{page_number+1}.png"
        pil_image.save(png_filepath)
        mxl_filepath = ete.call_ete(png_filepath, output_folder)

        filepaths.append(mxl_filepath)

    return filepaths

if __name__ == '__main__':
    print(pdf_to_mxls('data/happy_birthday.pdf', 'intermediate_results/'))

