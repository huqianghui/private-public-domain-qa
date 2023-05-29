import { renderToStaticMarkup } from "react-dom/server";

function JsonDataDisplay(answer: Array<string>){

  if(answer.length ==0){
    return <table></table>;
  }

  const headers = Object.keys(answer[0]);
  let records  = new Array();
  answer.map((item) => {records.push(Object.values(item))});

  const data = records;
  const tableHeaders = headers.map((header, index) => (
    <th key={index}>{header}</th>
  ));

  const tableRows = data.map((row, rowIndex) => (
    <tr key={rowIndex}>
      {row.map((cell: Array<string>, cellIndex: string) => (
        <td key={cellIndex}>{cell}</td>
      ))}
    </tr>
  ));

  return (
    <table>
      <thead>
        <tr>{tableHeaders}</tr>
      </thead>
      <tbody>{tableRows}</tbody>
    </table>
  );

}


export function parseArrayAnswerToHtml(answer: Array<string>): string {
    return renderToStaticMarkup(JsonDataDisplay(answer));
}
