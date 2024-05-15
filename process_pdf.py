import pypdfium2 as pdfium
from oemer.oemer import ete
import midi_vec

def pdf_to_mxls(pdf_path, output_folder):
    """
    Convert a PDF to a list of MusicXML files.

    pdf_path: path to PDF
    output_folder: folder to save intermediate results

    Returns: list of paths to the MusicXML files
    """
    pdf = pdfium.PdfDocument(pdf_path)
    n_pages = len(pdf)

    filepaths = []
    for page_number in range(n_pages):
        page = pdf.get_page(page_number)
        pil_image = page.render(scale = 5).to_pil()
        png_filepath = f"{output_folder}{pdf_path.split('/')[-1].split('.')[0]}_{page_number+1}.png"
        pil_image.save(png_filepath)
        mxl_filepath, staff_uppers = ete.call_ete(png_filepath, output_folder)

        filepaths.append({"filepath": mxl_filepath,
                          "y_pos": staff_uppers})
        

    midi_vec.set_mxls(filepaths)
    return filepaths

if __name__ == '__main__':
    print(pdf_to_mxls('data/concatenated_002.pdf', 'intermediate_results/'))

