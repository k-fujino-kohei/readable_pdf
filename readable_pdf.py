import sys
from os import listdir, mkdir, path

from pypdf import PageObject, PdfReader, PdfWriter


def concat_pdf(infile):
    if path.splitext(infile)[1] != ".pdf":
        return

    components = infile.split("/")
    file_name = components.pop(-1)
    components.append("out")
    outdir = "/".join(components)
    outfile = outdir + "/" + file_name

    if not path.exists(outdir):
        print("mkdir " + outdir)
        mkdir(outdir)

    reader = PdfReader(infile)
    writer = PdfWriter()
    page_len = len(reader.pages)

    print("start {} ({}p)".format(file_name, page_len))
    # 背表紙から始める
    start_page = -1 if use_cover else 0
    for i in range(start_page, page_len, 2):
        p1 = reader.pages[i]
        # ページ総数が奇数の場合に右ページを空白にする
        if i + 1 == page_len:
            p2 = PageObject.create_blank_page(
                width=p1.mediabox.right, height=p1.mediabox.top
            )
        else:
            p2 = reader.pages[i + 1]

        # 結合後の1ページ
        width_1_2 = p1.mediabox.right + p2.mediabox.right
        height_1_2 = max(p1.mediabox.top, p2.mediabox.top)
        p_1_2 = PageObject.create_blank_page(width=width_1_2, height=height_1_2)

        p_1_2.merge_page(p1)
        p_1_2.merge_translated_page(p2, p2.mediabox.right, 0)

        writer.add_page(p_1_2)

    with open(outfile, mode="wb") as f:
        writer.write(f)


input_file = sys.argv[1]
# 最初のページを表紙として別ページに切り出すかどうか
no_cover = sys.argv[2] == "no_cover" if len(sys.argv) > 2 else False
use_cover = not no_cover

if use_cover:
    print("use cover")

if path.isdir(input_file):
    for i in listdir(input_file):
        concat_pdf(path.join(input_file, i))
else:
    concat_pdf(input_file)
