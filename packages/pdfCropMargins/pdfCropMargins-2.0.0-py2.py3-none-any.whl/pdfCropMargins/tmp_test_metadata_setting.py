
import fitz
from pprint import pprint

DOC = "/home/alb/programming/python/pdfCropMargins/pdf_test_files/pdf_files/regular_arxiv_nonlocalMeasurementsInTheTime-SymmetricQuantumMechanics_VaidmanNevo05.pdf"
doc = fitz.open(DOC)

# ---------------------
# standard metadata
# ---------------------
doc.metadata = {'author': 'PRINCE',
 'creationDate': "D:2010102417034406'-30'",
 'creator': 'PrimoPDF http://www.primopdf.com/',
 'encryption': None,
 'format': 'PDF 1.4',
 'keywords': '',
 'modDate': "D:20200725062431-04'00'",
 'producer': 'macOS Version 10.15.6 (Build 19G71a) Quartz PDFContext, '
             'AppendMode 1.1',
 'subject': '',
 'title': 'Full page fax print',
 'trapped': ''}

#
# Use the following code to see all items stored in the metadata object:
#

# ----------------------------------
# metadata including private items
# ----------------------------------

def get_all_metadata():
    metadata = {}  # Make a local metadata dict.
    data_type, value = doc.xref_get_key(-1, "Info")  # /Info key in the trailer
    if data_type != "xref":
        pass  # PDF has no metadata.
    else:
        xref = int(value.replace("0 R", ""))  # Extract the metadata xref.
        for key in doc.xref_get_keys(xref):
            metadata[key] = doc.xref_get_key(xref, key)[1]
    print("\nShowing all metadata gotten from paper:")
    pprint(metadata)
    return metadata

metadata = get_all_metadata()

#
# Vice versa, you can also store private metadata items in a PDF. It is your
# responsibility to make sure that these items conform to PDF specifications -
# especially they must be (unicode) strings. Consult section 14.3 (p. 548) of
# the Adobe PDF References for details and caveats:
#

#{'Author': 'PRINCE',
# 'CreationDate': "D:2010102417034406'-30'",
# 'Creator': 'PrimoPDF http://www.primopdf.com/',
# 'ModDate': "D:20200725062431-04'00'",
# 'PXCViewerInfo': 'PDF-XChange Viewer;2.5.312.1;Feb  9 '
#                 "2015;12:00:06;D:20200725062431-04'00'",
# 'Producer': 'macOS Version 10.15.6 (Build 19G71a) Quartz PDFContext, '
#             'AppendMode 1.1',
# 'Title': 'Full page fax print'}
# ---------------------------------------------------------------
# note the additional 'PXCViewerInfo' key - ignored in standard!
# ---------------------------------------------------------------

def set_new_nonstandard_metadata_item():
    data_type, value = doc.xref_get_key(-1, "Info")  # /Info key in the trailer
    if data_type != "xref":
        raise ValueError("PDF has no metadata")
    xref = int(value.replace("0 R", ""))  # extract the metadata xref
    # add some private information
    doc.xref_set_key(xref, "mykey", fitz.get_pdf_str("北京 is Beijing"))
    #
    # after executing the previous code snippet, we will see this:
    print("\nFull metadata after adding new key:")
    pprint(metadata)
    #{'Author': 'PRINCE',
    # 'CreationDate': "D:2010102417034406'-30'",
    # 'Creator': 'PrimoPDF http://www.primopdf.com/',
    # 'ModDate': "D:20200725062431-04'00'",
    # 'PXCViewerInfo': 'PDF-XChange Viewer;2.5.312.1;Feb  9 '
    #                  "2015;12:00:06;D:20200725062431-04'00'",
    # 'Producer': 'macOS Version 10.15.6 (Build 19G71a) Quartz PDFContext, '
    #             'AppendMode 1.1',
    # 'Title': 'Full page fax print',
    # 'mykey': '北京 is Beijing'}

set_new_nonstandard_metadata_item()
get_all_metadata()

#
# To delete selected keys, use doc.xref_set_key(xref, "mykey", "null"). As
# explained in the next section, string “null” is the PDF equivalent to
# Python’s None. A key with that value will be treated as not being specified –
# and physically removed in garbage collections.
#
