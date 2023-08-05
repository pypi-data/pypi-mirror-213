from .my_table import MyTable

class MyLongTable(MyTable):
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
        nfields = len(self._header_fields)
        if self._centered:
            hlines.append("\\begin{center}")
        hlines.append("\\begin{longtable}")
        hlines.append("{" + self._header_field_formats + "}")
        hlines.append("\\caption{" + self._caption + "}\\label{tab:" + self._label + "} \\\\")
        hlines.append("\\hline")
        
        
        header = []
        for h in self._header_fields:
            header.append("\\multicolumn{1}{c}{\\textbf{" + h +"}}")
        hlines.append(" & ".join(header) + "\\\\ \\hline")
        hlines.append("\\endfirsthead")
        hlines.append("\\multicolumn{%d}{c}%%\n"  % nfields)
        hlines.append("{{\\bfseries \\tablename\\ \\thetable{} -- continued from previous page}} \\\\ \n")
        hlines.append("\\hline")
        hlines.append(" & ".join(header) + "\\\\ \\hline")
        hlines.append("\\endhead ")
        hlines.append("\\hline \multicolumn{%d}{|r|}{{Continued on next page}} \\\\ \\hline \n" % nfields)
        hlines.append("\\endfoot ")
        hlines.append("\\hline \\hline ")
        hlines.append("\\endlastfoot ")
        return hlines
    
    
   
    
    def _footer(self) -> None:
        flines = []
        flines.append("\\hline")
        flines.append("\\end{longtable}")
        if self._centered:
            flines.append("\\end{center}")
        return flines
