
from .my_table import MyTable

class MyLatexTable(MyTable):
    def __init__(self, header_fields, 
                 header_field_formats = None, 
                 label="to_do",
                 caption="to do",
                 centered=True, 
                 use_booktabs=False) -> None:
        super().__init__(header_fields=header_fields, 
                 header_field_formats=header_field_formats, 
                 label=label,
                 caption=caption,
                 centered=centered, 
                 use_booktabs=use_booktabs)
        self._hlines = self._header()
        self._flines = self._footer()
        
        
    def _header(self) -> None:
        hlines = []
        hlines.append("\\begin{table}")
        hlines.append("\\begin{tabular}" + "{" + self._header_field_formats + "}")
        if self._use_booktabs:
            hlines.append("\\toprule")
        else:
            hlines.append("\\hline")
        header = []
        for h in self._header_fields:
            header.append("\\textbf{" + h +"}")
        hlines.append(" & ".join(header) + "\\\\")
        return hlines
    
    def _footer(self) -> None:
        flines = []
        if self._use_booktabs:
            flines.append("\\bottomrule")
        else:
            flines.append("\\hline")
        flines.append("\\end{tabular}")
        flines.append("\\caption{" + self._caption + "}")
        flines.append("\\label{tab:" + self._label + "}")
        flines.append("\\end{table}")
        return flines

   
        
    
    
    
    
    



