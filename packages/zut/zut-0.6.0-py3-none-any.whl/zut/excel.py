from __future__ import annotations
import logging
from pathlib import Path
from typing import Any
from .tabular import Row
from .misc import Literal
from . import filesh
from openpyxl import load_workbook, Workbook, DEFUSEDXML
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.worksheet.table import Table, TableColumn, TableFormula, TableStyleInfo
from openpyxl.worksheet.formula import DataTableFormula, ArrayFormula
from openpyxl.worksheet.filters import AutoFilter
from openpyxl.cell.cell import Cell
from openpyxl.styles.differential import DifferentialStyle, DifferentialStyleList
from openpyxl.styles.fills import PatternFill
from openpyxl.utils import range_boundaries, get_column_letter

logger = logging.getLogger(__name__)


class ExcelWorkbook:
    _workbook_cache: dict[str,ExcelWorkbook] = {}
    """ Workbooks per canonical path """
    
    _defusedxml_alert_emitted = False

    def __init__(self, path: str|Path):        
        if not DEFUSEDXML and not self.__class__._defusedxml_alert_emitted:
            logger.warning("By default openpyxl does not guard against quadratic blowup or billion laughs xml attacks. To guard against these attacks install defusedxml.")
            self.__class__._defusedxml_alert_emitted = True

        self.path = Path(path) if not isinstance(path, Path) else path
        
        if filesh.exists(self.path):
            logger.debug("load workbook %s", self.path)
            with filesh.open_file(self.path, 'rb') as fp:
                self._pyxl_workbook: Workbook = load_workbook(fp)
            self._create_next_table_in_active_sheet = False
        else:
            logger.debug("create workbook for %s", self.path)
            self._pyxl_workbook = Workbook()
            self._create_next_table_in_active_sheet = True

        self._tables: dict[str,ExcelTable] = {}
        self._needs_save = False


    @classmethod
    def get_or_create_cached(cls, path: str|Path) -> ExcelWorkbook:
        path = Path(path) if not isinstance(path, Path) else path
        canonical_path = str(path.resolve())
        if not canonical_path in cls._workbook_cache:
            cls._workbook_cache[canonical_path] = ExcelWorkbook(path)
        return cls._workbook_cache[canonical_path]


    def close(self):
        if not self._needs_save:
            return
        
        for table in self._tables.values():
            table.redefine()
        
        logger.debug("save workbook %s", self.path)
        with filesh.open_file(self.path, 'wb') as fp:
            self._pyxl_workbook.save(fp)

        self._needs_save = False
        

    def get_table(self, name: str, default: Any|Literal['__raise__'] = '__raise__') -> ExcelTable:
        if name in self._tables:
            return self._tables[name]
        
        for sheet_name in self._pyxl_workbook.sheetnames:
            pyxl_worksheet: Worksheet = self._pyxl_workbook[sheet_name]
            if name in pyxl_worksheet.tables:
                pyxl_table = pyxl_worksheet.tables[name]
                self._tables[name] = ExcelTable(pyxl_table, pyxl_worksheet, self)
                return self._tables[name]
            
        if default == '__raise__':
            raise KeyError(f"no table found with name \"{name}\" in workbook \"{self.path}\"")
        else:
            return default
        

    def create_table(self, name: str, no_headers: bool = False) -> ExcelTable:
        for sheet_name in self._pyxl_workbook.sheetnames:
            pyxl_worksheet: Worksheet = self._pyxl_workbook[sheet_name]
            if name in pyxl_worksheet.tables:
                raise ValueError(f"table {name} already exist")
    
        self._needs_save = True
        
        if self._create_next_table_in_active_sheet:
            pyxl_worksheet: Worksheet = self._pyxl_workbook.active
            pyxl_worksheet.title = name
            self._create_next_table_in_active_sheet = False
        else:
            pyxl_worksheet: Worksheet = self._pyxl_workbook.create_sheet(title=name)

        self._tables[name] = ExcelTable(name, pyxl_worksheet, self)
        return self._tables[name]


class ExcelTable:
    def __init__(self, pyxl_table: Table|str, pyxl_worksheet: Worksheet, workbook: ExcelWorkbook, no_headers: bool = None):
        self.workbook = workbook
        self._pyxl_worksheet = pyxl_worksheet        
        self._column_formats: dict[int,dict[str,Any]] = {}

        if isinstance(pyxl_table, str):
            self._pyxl_table: Table = None
            self.name: str = pyxl_table
            if no_headers:
                self.has_headers = False
                self._min_row = 1
            else:
                self.has_headers = True
                self._min_row = 2
            self._min_col = 1
            self._row_count = 0
            self._column_names: list[str] = []

        elif isinstance(pyxl_table, Table):
            self._pyxl_table: Table = pyxl_table
            self.name: str = pyxl_table.name
            
            self._min_col, min_row, max_col, max_row = range_boundaries(pyxl_table.ref)

            if pyxl_table.headerRowCount == 0:
                self.has_headers = False
                self._min_row = min_row
            elif pyxl_table.headerRowCount == 1:
                self.has_headers = True
                self._min_row = min_row + 1
            else:
                raise ValueError(f'invalid headerRowCount: {pyxl_table.headerRowCount}')
            
            self._row_count = max_row - self._min_row + 1
            col_count = max_col - self._min_col + 1
        
            self._column_names: list[str] = list(self._pyxl_table.column_names)
            # NOTE: if no headers, default names are returned, example in French: ['Colonne1', 'Colonne2']
            if len(self._column_names) != col_count:
                raise ValueError(f'invalid column_names length ({len(self._column_names)}, expected {col_count}): {self._column_names}')
        else:
            raise ValueError(f"invalid type for pyxl_table: {type(pyxl_table).__name__}")


    @property
    def column_names(self) -> list[str]:
        return self._column_names

    @property
    def min_row(self) -> int:
        return self._min_row
    
    @property
    def min_col(self) -> int:
        return self._min_col
    
    @property
    def row_count(self) -> int:
        return self._row_count
    
    @property
    def col_count(self) -> int:
        return len(self._column_names)
    
    @property
    def ref(self) -> str:
        if self.col_count == 0:
            raise ValueError(f"cannot get table ref: table does not contain any column")
        if self.row_count == 0 and not self.has_headers:
            raise ValueError(f"cannot get table ref: table does not contain any line")
        
        min_row = self._min_row
        if self.has_headers:
            min_row -= 1
        
        return f"{get_column_letter(self._min_col)}{min_row}:{get_column_letter(self._min_col + self.col_count - 1)}{self._min_row + self._row_count - 1}"


    def get_row(self, index: int) -> Row:
        if index == -1:
            if self.row_count == 0:
                raise ValueError(f"cannot get last row: table does not contain any row")
            index = self.row_count - 1
        elif index < 0:
            raise ValueError(f"invalid row index: {index}")
        
        if index >= self.row_count:
            raise ValueError(f"cannot get row at index {index}: table contains {self.row_count} rows")

        return Row(
            get=lambda col_index: self.get_value(index, col_index),
            set=lambda col_index, value: self.set_value(index, col_index, value),
            headers=self.column_names
        )
    

    def insert_row(self) -> Row:
        self.workbook._needs_save = True
        row_index = self._row_count

        # ensure empty values
        for col_index in range(0, self.col_count):
            cell = self._pyxl_worksheet.cell(self._min_row + row_index, self._min_col + col_index)
            if cell.value is not None:
                raise ValueError(f'cannot insert row: row {row_index} is not empty')

        self._row_count += 1

        # erase old styles and apply column format
        for col_index in range(0, self.col_count):
            self._erase_cell(row_index, col_index)
            
        return self.get_row(row_index)
    

    def insert_col(self, name: str):
        self.workbook._needs_save = True
        if not name:
            raise ValueError(f'name cannot be empty')
        if name in self.column_names:
            raise ValueError(f'column name already used: {name}')
            
        col_index = self.col_count

        # ensure empty values
        for row_index in range(0, self._row_count):
            cell = self._pyxl_worksheet.cell(self._min_row + row_index, self._min_col + col_index)
            if cell.value is not None:
                raise ValueError(f'cannot insert column: column {col_index} is not empty')

        self.column_names.append(name) # implies self.col_count += 1

        if self.has_headers:
            cell = self._pyxl_worksheet.cell(self._min_row - 1, self._min_col + col_index)
            cell.value = name

        # erase old styles and apply column format
        for row_index in range(0, self._row_count):
            self._erase_cell(row_index, col_index)
            

    def truncate(self):
        self.workbook._needs_save = True
        prev_row_count = self._row_count
        self._row_count = 0

        for row_index in range(0, prev_row_count):
            for col_index in range(0, self.col_count):
                self._erase_cell(row_index, col_index, allow_outside=True)


    def redefine(self):
        self.workbook._needs_save = True
        new_ref = self.ref
        if self._pyxl_table is not None and new_ref == self._pyxl_table.ref:
            return
        
        logger.debug("define table %s: %s => %s", self.name, self._pyxl_table.ref if self._pyxl_table is not None else None, new_ref)

        newcolumns = []

        for i in range(0, self.col_count):
            if self.has_headers:
                name = self._pyxl_worksheet.cell(self._min_row - 1, self._min_col + i).value
            else:
                name = self.column_names[i] if i < len(self.column_names) else None
            newcolumn = TableColumn(id=i+1, name=name)
            newcolumns.append(newcolumn)

            if self._pyxl_table is not None and i < len(self._pyxl_table.tableColumns):
                prevcolumn: TableColumn = self._pyxl_table.tableColumns[i]
                newcolumn.dataCellStyle = prevcolumn.dataCellStyle
                newcolumn.dataDxfId = prevcolumn.dataDxfId # refers to workbook._differential_styles
                newcolumn.calculatedColumnFormula = prevcolumn.calculatedColumnFormula


        newtable_kwargs = {
            'name': self.name,
            'displayName': self.name,
            'ref': new_ref,
            'tableColumns': newcolumns,
            'headerRowCount': 1 if self.has_headers else 0,
        }

        if self._pyxl_table is not None:
            newtable_kwargs['autoFilter'] = self._pyxl_table.autoFilter
            newtable_kwargs['sortState'] = self._pyxl_table.sortState
            newtable_kwargs['tableStyleInfo'] = self._pyxl_table.tableStyleInfo
        else:
            newtable_kwargs['autoFilter'] = AutoFilter()
            newtable_kwargs['tableStyleInfo'] = TableStyleInfo(name="TableStyleMedium2", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)

        newtable = Table(**newtable_kwargs)

        self._pyxl_table = newtable
        
        if self.name in self._pyxl_worksheet.tables:
            del self._pyxl_worksheet.tables[self.name]
        self._pyxl_worksheet.add_table(newtable)


    def get_value(self, row_index: int, col_index: int) -> Any:
        self._check_indexes(row_index, col_index)
        cell = self._pyxl_worksheet.cell(self._min_row + row_index, self._min_col + col_index)
        value = cell.value
        # TODO: formatting
        return value
    

    def set_value(self, row_index: int, col_index: int, value: Any):
        self._check_indexes(row_index, col_index)
        self.workbook._needs_save = True
        cell = self._pyxl_worksheet.cell(self._min_row + row_index, self._min_col + col_index)

        self._apply_column_format(cell)

        try:
            cell.value = value
        except ValueError as err:
            if str(err).startswith('Cannot convert'):
                cell.value = str(value)
            else:
                raise
        

    def _check_indexes(self, row_index: int, col_index: int):
        if row_index == -1:
            row_index = self.row_count - 1
        if col_index == -1:
            col_index = self.col_count - 1

        if row_index < 0 or row_index >= self.row_count:
            raise ValueError(f"invalid row index: {row_index} (row count: {self.row_count})")
        if col_index < 0 or col_index >= self.col_count:
            raise ValueError(f"invalid row index: {col_index} (row count: {self.col_count})")


    def _erase_cell(self, row_index: int, col_index: int, allow_outside: bool = False) -> Cell:
        cell = self._pyxl_worksheet.cell(self._min_row + row_index, self._min_col + col_index)
        cell.style = 'Normal'
        cell.value = None

        if not allow_outside or (row_index < self._row_count and col_index < self.col_count):
            self._apply_column_format(cell)
        
        return cell


    def _apply_column_format(self, cell: Cell):
        index = cell.col_idx - self.min_col
        if index in self._column_formats:
            fmt = self._column_formats[index]
        else:
            fmt = self._build_column_format(index)
            self._column_formats[index] = fmt

        if 'formula' in fmt:
            formula = fmt['formula']
            if isinstance(formula, ArrayFormula):
                pass # TODO: not supported yet
            else:
                cell.value = formula

        if 'style' in fmt:
            cell.style = fmt['style']

        for fmt_key, fmt_value in fmt.items():
            if fmt_key in ['formula', 'style']:
                continue
            setattr(cell, fmt_key, fmt_value)


    def _build_column_format(self, index: int):
        fmt: dict[str,Any] = {}

        if self._pyxl_table is None or index >= len(self._pyxl_table.tableColumns):
            return fmt
        
        column: TableColumn = self._pyxl_table.tableColumns[index]

        # Read dataCellStyle
        if column.dataCellStyle:
            fmt['style'] = column.dataCellStyle
        
        # Read dxf
        if column.dataDxfId is not None:
            dxf: DifferentialStyle = self.workbook._pyxl_workbook._differential_styles[column.dataDxfId]

            if dxf.numFmt:
                fmt['number_format'] = dxf.numFmt.formatCode
            else:
                if not 'style' in fmt:
                    fmt['number_format'] = self._DEFAULT_NUMBER_FORMAT

            fmt['alignment'] = dxf.alignment if dxf.alignment else self._DEFAULT_ALIGNMENT
            fmt['border'] = dxf.border if dxf.border else self._DEFAULT_BORDER
            fmt['font'] = dxf.font if dxf.font else self._DEFAULT_FONT
            fmt['protection'] = dxf.protection if dxf.protection else self._DEFAULT_PROTECTION
            fmt['fill'] = PatternFill(fill_type=dxf.fill.fill_type, bgColor=dxf.fill.fgColor, fgColor=dxf.fill.bgColor) if dxf.fill else self._DEFAULT_FILL # NOTE: fgcolor and bgcolor are inversed in DifferentialStyle

        # Read formula
        if column.calculatedColumnFormula:
            formula = column.calculatedColumnFormula
            if formula.array:
                fmt['formula'] = ArrayFormula(formula.attr_text)
            else:
                fmt['formula'] = '=' + formula.attr_text
        
        # Return built format
        return fmt
    

    _DEFAULT_NUMBER_FORMAT = 'General'
    _DEFAULT_FILL = PatternFill(fill_type=None)
    _DEFAULT_ALIGNMENT = None # openpyxl.styles.alignment.Alignment
    _DEFAULT_BORDER = None # openpyxl.styles.alignment.Border
    _DEFAULT_FONT = None # openpyxl.styles.fonts.Font
    _DEFAULT_PROTECTION = None # openpyxl.styles.protection.Protection


    def __len__(self):
        return self._row_count

    def __iter__(self):
        return self.Iterator(self)

    class Iterator:
        def __init__(self, table: ExcelTable):
            self.next_index = 0
            self.table = table

        def __next__(self):
            if self.next_index >= self.table.row_count:
                raise StopIteration()
            
            row = self.table.get_row(self.next_index)
            self.next_index += 1
            return row
