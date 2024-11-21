import csv
import io
import xlsxwriter

from datetime import datetime
from django.http import HttpResponse, StreamingHttpResponse
import logging

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("DB Query")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)


# output helper class
class Echo:
    def write(self, value):
        return value


def csv_output(queryset, col_names):
    # combine column header with rows
    rows = [col_names] + [list(x.values()) for x in queryset]

    echo_buffer = Echo()
    csv_writer = csv.writer(echo_buffer)
    rows = (csv_writer.writerow(row) for row in rows)

    # setup HTTP response
    response = StreamingHttpResponse(rows, content_type="text/csv")
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    response["Content-Disposition"] = f'attachment; filename="db_query_output_{current_datetime}.csv"'

    return response


def xslx_output(queryset, col_names):
    # code adapted from: https://github.com/jmcnamara/XlsxWriter
    # BSD 2-Clause License: https://github.com/jmcnamara/XlsxWriter/blob/main/LICENSE.txt

    # Create an in-memory output file for the new workbook.
    output = io.BytesIO()

    # Even though the final file will be in memory the module uses temp
    # files during assembly for efficiency. To avoid this on servers that
    # don't allow temp files, for example the Google APP Engine, set the
    # 'in_memory' Workbook() constructor option as shown in the docs.
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Get data to write to the spreadsheet
    data = [col_names] + [list(x.values()) for x in queryset]

    # Write data
    for row_num, columns in enumerate(data):
        for col_num, cell_data in enumerate(columns):
            worksheet.write(row_num, col_num, cell_data)

    # Close the workbook before sending the data
    workbook.close()

    # Rewind the buffer
    output.seek(0)

    # Set up the Http response
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'db_query_output_{current_datetime}.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
