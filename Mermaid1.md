classDiagram
    class Report{
        <<interface>>
        +set_data(data)
        +add_header(text)
        +add_footer(text)
        +render()
        + get_output()->string
    }

    class ReportService{
        +generate(data Data,format_type String) String
    }

    class PDFReport{

    }

    class ExcelReport{

    }

    class CSVReport{

    }

    PDFReport <|.. Report
    ExcelReport <|..Report
    CSVReport<|..Report

    ReportService "1" *-- "1" PDFReport
    ReportService "1" *-- "1" ExceltReport
    ReportService "1" *-- "1" CSVReport