import PyPDF2
import os

def modifer(path,frames):
    left_margin = 30
    right_margin = 30
    top_margin = 80
    bottom_margin = 50

    input_file_path = []
    output_file_path = []
    name='2016-'
    out_path='.\\lib\\examples'
    if not os.path.exists(out_path):
        os.makedirs(out_path+'\\'+name)  # 新建文件夹

    input_file_path.append(out_path+'\\{}.pdf'.format(name))
    output_file_path.append(out_path+'\\{}\\{}.pdf'.format(name,name))


    def split(page):
        page.mediaBox.lowerLeft = (left_margin, bottom_margin)
        page.mediaBox.lowerRight = (width - right_margin, bottom_margin)
        page.mediaBox.upperLeft = (left_margin, height - top_margin)
        page.mediaBox.upperRight = (width - right_margin, height - top_margin)


    for m in range(len(input_file_path)):
        input_file = PyPDF2.PdfFileReader(open(input_file_path[m], 'rb'))
        output_file = PyPDF2.PdfFileWriter()

        page_info = input_file.getPage(0)
        width = float(page_info.mediaBox.getWidth())
        height = float(page_info.mediaBox.getHeight())
        page_count = input_file.getNumPages()

        for page_num in range(page_count):
            this_page = input_file.getPage(page_num)
            split(this_page)
            output_file.addPage(this_page)

        output_file.write(open(output_file_path[m], 'wb'))