import abc



class MyTable(metaclass=abc.ABCMeta):
    
    def __init__(self, header_fields, 
                 header_field_formats = None, 
                 label="to_do",
                 caption="to do",
                 centered=True, 
                 use_booktabs=False) -> None:
        if not isinstance(header_fields, list):
            raise ValueError(f"Argument 'header_fields' must be a list of strings")
        self._header_fields = header_fields
        self._centered = centered
        if header_field_formats is None:
            n = len(self._header_fields)
            self._header_field_formats = n * "l"
        elif not isinstance(header_field_formats, str):
            raise ValueError(f"If passed, argument 'header_field_formats' must be a string such as 'llr'")
        else:
            self._header_field_formats = header_field_formats
        self._use_booktabs = use_booktabs
        self._label = label
        self._caption = caption
        self._hlines = []
        self._flines = []
        self._lines = []
        
    
    @abc.abstractmethod
    def _header(self):
        pass
    
    def add_row(self, row, normalize=False) -> None:
        if len(row) != len(self._header_fields):
            raise ValueError(f"Malformed row with {len(row)} fields, but we were expecting {len(self._header_fields)} fields: {row}")
        if normalize:
            row = [r.replace("_", "\\_") for r in row]
        self._lines.append(" & ".join(row))
    
    @abc.abstractmethod
    def _footer(self):
        pass
    
    
    def _combine_lines_and_add_line_endings(self):
        lines = self._hlines + [line + "\\\\" for line in self._lines]  + self._flines
        return lines
    
    def get_latex(self):
        lines = self._combine_lines_and_add_line_endings()
        return "\n".join(lines)
                    
    def write_to_handle(self, fh):
        lines = self._combine_lines_and_add_line_endings()
        for line in lines:
            fh.write(line + "\n")
            
    def write_to_file(self, fname):
        fh = open(fname, "wt")
        self.write_to_handle(fh)
        fh.close()
 
    