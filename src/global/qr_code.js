import pdfMake from "pdfmake/build/pdfmake";
import pdfFonts from "pdfmake/build/vfs_fonts";
pdfMake.vfs = pdfFonts.pdfMake.vfs;

export function generatePDF(qrText, headerText, titleText)
{

  let docDefinition = {
    pageSize: 'A6',
    info: {
      title: titleText
    },
    header: {
      text: headerText, alignment: 'center',  margin: [0, 20, 0, 0]
    },
    content: [
      {width: "auto", alignment: "center", qr: qrText, ecoLevel: "H"}

    ],
    styles: {
      header: {
        fontSize: 40,
      }
    }
  };

  const pdf = pdfMake.createPdf(docDefinition)
  pdf.download(titleText)
  pdf.getBase64((data) => {
    let pdfData = {title: titleText, b64: data}
    console.log(JSON.stringify(pdfData));
  })
}