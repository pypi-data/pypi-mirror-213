from docstruct.bounding_box import BoundingBox
from docstruct.text_block import Line, TableCell, TableColumn, Table, TableType
from docbuild.graph import Node, Graph, GraphGenerator

from docstruct.spatial_grid_indexing import SpatialGrid
from ..visual_detection.constants import SPATIAL_GRID_SIZE
from typing import Optional

import numpy as np
import string


class BorderLessTableExtractor:
    def __init__(self):
        pass


class Column:
    def __init__(self, lines: list[Line]):
        self.lines = lines
        self.bounding_box = BoundingBox.compose_bounding_boxes(
            [line.bounding_box for line in lines]
        )


class ColumnLineFilter:
    def __init__(self, lines: list[Line]):
        self.lines = lines

    def are_adjacent_lines(self, line1: Line, line2: Line) -> bool:
        bbox1 = line1.bounding_box.scale(width_scale=1.2, height_scale=1.5)
        bbox2 = line2.bounding_box.scale(width_scale=1.2, height_scale=1.5)
        return bbox1.intersect(bbox2)

    def get_graph(self) -> Graph:
        graph_generator = GraphGenerator(
            items=self.lines, are_adjacent=self.are_adjacent_lines
        )
        return graph_generator.generate_undirected_graph()

    def filter_lines(self) -> list[Line]:
        filtered_lines = []
        graph = self.get_graph()
        ccs = graph.get_connected_components()
        for cc in ccs:
            bbox = BoundingBox.compose_bounding_boxes(
                [self.lines[node.data].bounding_box for node in cc]
            )
            if bbox.get_width() < 0.4:
                for node in cc:
                    filtered_lines.append(self.lines[node.data])

        return filtered_lines


def get_bounding_box_interior(
    grid,
    bbox: BoundingBox,
) -> set:
    start_x, start_y = grid.convert_to_grid_coordinates(bbox.get_bottom_left())
    end_x, end_y = grid.convert_to_grid_coordinates(bbox.get_top_right())

    data = set()
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            current_set = grid.get_by_grid_coordinates(x, y)
            if current_set is None:
                continue
            data.update(current_set)
    return data




class ColumnExtractor:
    def __init__(self, lines: list[Line]):
        self.lines = lines
        self.spatial_grid = self.get_spatial_grid(lines=lines)

    def get_spatial_grid(self, lines: list[Line]) -> SpatialGrid:
        spatial_grid = SpatialGrid(
            num_rows=SPATIAL_GRID_SIZE, num_cols=SPATIAL_GRID_SIZE
        )
        for line in lines:
            spatial_grid.add_bounding_box_interior(
                bbox=line.bounding_box.scale(width_scale=1, height_scale=1), data=line
            )
        return spatial_grid

    def get_next_under_line(self, line: Line) -> Optional[Line]:
        top = line.bounding_box.bottom
        height = line.bounding_box.get_height()
        bottom = top - 2 * height
        left = line.bounding_box.left
        right = line.bounding_box.right
        bounding_box = BoundingBox(top=top, bottom=bottom, left=left, right=right)
        potential_under_lines = get_bounding_box_interior(self.spatial_grid, bbox=bounding_box)

        close_under_lines = [
            l
            for l in potential_under_lines
            if l.bounding_box.get_top() < line.bounding_box.get_bottom()
        ]

        if not close_under_lines:
            return
        close_under_lines = [
            l
            for l in close_under_lines
            if l.bounding_box.get_horizontal_segment().intersect(
                line.bounding_box.get_horizontal_segment()
            )
        ]
        if not close_under_lines:
            return

        under_line = None
        max_height = 0
        for line in close_under_lines:
            current_height = line.bounding_box.get_top()
            if current_height > max_height:
                max_height = current_height
                under_line = line
        return under_line

    def are_adjacent_lines(self, line1: Line, line2: Line) -> bool:
        left_condition = self.left_is_similar(line1=line1, line2=line2)
        right_condition = self.right_is_similar(line1=line1, line2=line2)
        center_condition = self.center_is_similar(line1=line1, line2=line2)
        height_condition = self.vertically_close(line1=line1, line2=line2)
        return (
            left_condition or right_condition or center_condition
        ) and height_condition

    def vertically_close(self, line1: Line, line2: Line) -> bool:
        """
        I want to bound the space to 1.15 + epsilon error for epsilon = 0.1 -> 1.25
        Assuming the scale_y is c and the height of the first line is h1
        -> The scaled height is c*h1 -> the delta is (c-1)*h1 -> the one sided delta is (c-1)*h1/2
        -> Combining the two sides we get (c-1)*h1/2 + (c-1)*h2/2 = (c-1)*(h1+h2)/2 = (c-1) * avg(h1,h2)
        for c = 2.25 we get an epsilon of 0.1
        """

        bbox1 = line1.bounding_box.scale(height_scale=2.25)
        bbox2 = line2.bounding_box.scale(height_scale=2.25)
        return bbox1.get_vertical_segment().intersect(bbox2.get_vertical_segment())

    def left_is_similar(self, line1: Line, line2: Line) -> bool:
        left_dist = abs(line1.bounding_box.left - line2.bounding_box.left)
        return left_dist < 0.01

    def right_is_similar(self, line1: Line, line2: Line) -> bool:
        right_dist = abs(line1.bounding_box.right - line2.bounding_box.right)
        return right_dist < 0.01

    def center_is_similar(self, line1: Line, line2: Line) -> bool:
        center_dist = abs(
            line1.bounding_box.get_center().x - line2.bounding_box.get_center().x
        )
        return center_dist < 0.01

    def get_map_line_to_line_index(self, lines: list[Line]) -> dict[Line, int]:
        map_line_to_line_index = {}
        for i, line in enumerate(lines):
            map_line_to_line_index[line] = i
        return map_line_to_line_index

    def get_graph(self, lines: list[Line]) -> Graph:
        nodes = []
        map_line_to_line_index = self.get_map_line_to_line_index(lines)
        for line in lines:
            nodes.append(Node(data=line))
        for line in lines:
            line_index = map_line_to_line_index[line]
            under_line = self.get_next_under_line(line=line)
            # print(line)
            # print(under_line)
            if under_line is None:
                continue
            if under_line not in map_line_to_line_index:
                continue
            if self.are_adjacent_lines(line1=line, line2=under_line):
                close_under_line_index = map_line_to_line_index[under_line]
                nodes[line_index].add_neighbor(nodes[close_under_line_index])
                nodes[close_under_line_index].add_neighbor(nodes[line_index])

        graph = Graph(nodes=nodes)
        return graph

    def convert_cc_to_column(self, cc: list[Node]) -> Column:
        lines = [node.data for node in cc]
        column = Column(lines=lines)
        return column

    def filter_connected_components(self, ccs: list[list[Node]]) -> list[list[Node]]:
        filtered_ccs = []
        for cc in ccs:
            if len(cc) >= 3:
                filtered_ccs.append(cc)
        return filtered_ccs

    def extract_columns(self):
        lines = ColumnLineFilter(lines=self.lines).filter_lines()
        graph = self.get_graph(lines)
        connected_components = graph.get_connected_components()
        connected_components = self.filter_connected_components(connected_components)
        columns = [self.convert_cc_to_column(cc) for cc in connected_components]
        return columns



class BoundingBoxExpander (object):
    def __init__(self):
        self.bounding_box = None

    def expand(self, bbox : BoundingBox) -> None:
        if self.bounding_box is None:
            self.bounding_box = BoundingBox(bbox.left, bbox.top, bbox.right, bbox.bottom)
        self._expand(bbox)
        self.bounding_box.width = self.bounding_box.right - self.bounding_box.left
        self.bounding_box.height = self.bounding_box.top - self.bounding_box.bottom

    def _expand(self, bbox : BoundingBox):
        raise NotImplementedError()

    def get_bounding_box(self) -> BoundingBox:
        return self.bounding_box
    
class MinimalBoundingBoxExpander (BoundingBoxExpander):
    def __init__(self):
        super().__init__()
        self.bounding_box = None

    def _expand(self, bbox : BoundingBox):
        self.bounding_box.left = min(self.bounding_box.left, bbox.left)
        self.bounding_box.right = max(self.bounding_box.right, bbox.right)
        self.bounding_box.top = min(self.bounding_box.top, bbox.top)
        self.bounding_box.bottom = max(self.bounding_box.bottom, bbox.bottom)

class MaximalBoundingBoxExpander (BoundingBoxExpander):
    def __init__(self):
        super().__init__()
        self.bounding_box = None

    def _expand(self, bbox : BoundingBox):
        self.bounding_box.left = min(self.bounding_box.left, bbox.left)
        self.bounding_box.right = max(self.bounding_box.right, bbox.right)
        self.bounding_box.top = max(self.bounding_box.top, bbox.top)
        self.bounding_box.bottom = min(self.bounding_box.bottom, bbox.bottom)


class BoundingBoxAggregator (object):
    def __init__(self) -> None:
        self.elements = []
        self.all_boxes = []
        self.optional_boxes = {
            "minimal": MinimalBoundingBoxExpander(),
            "maximal": MaximalBoundingBoxExpander()
        }

    def get_bounding_box(self) -> BoundingBox:
        return self.optional_boxes["maximal"].get_bounding_box()
    
    def is_row_colliding(self, other_box : BoundingBox) -> bool:
        bounding_box = self.get_bounding_box()
        if bounding_box is None:
            return True
        return bounding_box.vertical_intersect(other_box)

    def get_intersection_percentage(self, other_box : BoundingBox) -> float:
        bounding_box = self.get_bounding_box()
        if bounding_box is None:
            return 0
        intersection_area = max(0,(min(bounding_box.right, other_box.right) - max(bounding_box.left, other_box.left))) * \
                            max(0,(min(bounding_box.top, other_box.top) - max(bounding_box.bottom, other_box.bottom)))
        return intersection_area / (other_box.width * other_box.height)
    
    def add_element(self, element_box : BoundingBox, element : object = None):
        self.elements.append(element)
        self.all_boxes.append(element_box)

        for box in self.optional_boxes.values():
            box.expand(element_box)


class BoundingBoxTable(object):
    EMPTY_CELL = 0

    def __init__(self):
        self.columns = []
        self.rows = []
        self.cells = np.zeros((0,0), dtype=object)
        self.header_lines = 0

    def add_element(self, element_box : BoundingBox, element=None):
        col_ind = 0
        add_new_col = True
        if len(self.columns) > 0:
            while col_ind < len(self.columns) and self.columns[col_ind].bounding_box.right < element_box.left:
                col_ind += 1
            if col_ind < len(self.columns) and self.columns[col_ind].bounding_box.horizontal_intersect(element_box):
                add_new_col = False
        
        # add new col if needed
        if add_new_col:
            self.columns = self.columns[:col_ind] + [MaximalBoundingBoxExpander()] + self.columns[col_ind:]
            self.cells = np.c_[self.cells[:,:col_ind], np.zeros((self.cells.shape[0],1), dtype=object) + self.EMPTY_CELL, self.cells[:,col_ind:]]
        
        self.columns[col_ind].expand(element_box)

        row_ind = 0
        add_new_row = True
        if len(self.rows) > 0:
            while row_ind < len(self.rows) and self.rows[row_ind].bounding_box.bottom > element_box.top:
                row_ind += 1
            if row_ind < len(self.rows) and self.rows[row_ind].bounding_box.vertical_intersect(element_box):
                add_new_row = False

        # add new row if needed
        if add_new_row:
            self.rows = self.rows[:row_ind] + [MaximalBoundingBoxExpander()] + self.rows[row_ind:]
            self.cells = np.r_[self.cells[:row_ind,:], np.zeros((1,self.cells.shape[1]), dtype=object) + self.EMPTY_CELL, self.cells[row_ind:,:]]

        self.rows[row_ind].expand(element_box)

        if self.cells[row_ind, col_ind] != BoundingBoxTable.EMPTY_CELL:
            self.cells[row_ind, col_ind].append(element)
        else:
            self.cells[row_ind, col_ind] = [element]

    def get_columns_distances(self) -> list[float]:
        return [self.columns[i].bounding_box.left - self.columns[i-1].bounding_box.left for i in range(1,len(self.columns))]
    
    def get_rows_distances(self) -> list[float]:
        return [self.rows[i-1].bounding_box.top - self.rows[i].bounding_box.top for i in range(1,len(self.rows))]
    
    def remove_top_rows(self, n=1):
        "Remove the top n rows from the table"
        self.rows = self.rows[n:]
        self.cells = self.cells[n:,:]

    def remove_bottom_rows(self, n=1):
        "Remove the bottom n rows from the table"
        self.rows = self.rows[:-n]
        self.cells = self.cells[:-n,:]

    def is_colliding_from_bellow(self, other) -> bool:
        return self.rows[-1].bounding_box.bottom < other.rows[0].bounding_box.top and \
            self.rows[0].bounding_box.top > other.rows[-1].bounding_box.bottom
    
    def is_colliding(self, other) -> bool:
        return self.is_colliding_from_bellow(other) or other.is_colliding_from_bellow(self)

    def add_table_at_bottom(self, other_table):
        table_lowest_row = self.rows[-1].bounding_box.bottom
        first_index_below_table = [i for i,row in enumerate(other_table.rows) if row.bounding_box.top < table_lowest_row][0]
        self.rows = self.rows + other_table.rows[first_index_below_table:]
        self.cells = np.r_[self.cells, other_table.cells[first_index_below_table:,:]]
        for this_col, other_col in zip(self.columns, other_table.columns):
            this_col.expand(other_col.bounding_box)


class BorderlessTableExtractor:
    NO_LIMIT_FOR_FORCED_LINES = -1

    def __init__(self, lines : list[Line],
                 line_overlap_percentage : float = 0.2,
                 max_forced_lines = NO_LIMIT_FOR_FORCED_LINES,
                 suspect_header_over_std_factor : float = 3,
                 remove_singles_at_bottom_rows : bool = True,
                 row_distance_variation_sensitivity : float = 3) -> None:
        self.lines = lines
        
        self._line_overlap_percentage = line_overlap_percentage
        self._max_forced_lines = max_forced_lines
        self._suspect_header_over_std_factor = suspect_header_over_std_factor
        self._remove_singles_at_bottom_rows = remove_singles_at_bottom_rows
        self._row_distance_variation_sensitivity = row_distance_variation_sensitivity
        self._ascii_letters = string.ascii_letters + ' '

    def aggregate_aligned_columns(self, columns) -> list[BoundingBoxAggregator]:
        aggregate_columns = []
        for col in columns:
            found = False
            for agg in aggregate_columns:
                if agg.is_row_colliding(col.bounding_box):
                    agg.add_element(col.bounding_box, col)
                    found = True
                    break
            if not found:
                aggregate_columns.append(BoundingBoxAggregator())
                aggregate_columns[-1].add_element(col.bounding_box, col)

        # Remove aggragators with only one element
        aggregate_columns = [agg for agg in aggregate_columns if len(agg.elements) > 1]
        return aggregate_columns
    
    def cluster_lines_to_tables(self, aggregate_columns : list[BoundingBoxAggregator]) -> list[BoundingBoxTable]:
        # Look for missing lines
        tables = []
        for agg in aggregate_columns:
            bb_table = BoundingBoxTable()
            for line in self.lines:
                if agg.get_intersection_percentage(line.bounding_box) > self._line_overlap_percentage:
                    bb_table.add_element(line.bounding_box, line)
            tables.append(bb_table)
        return tables
    
    def force_headers(self, table : BoundingBoxTable) -> list[list[Line]]:
        " Assumes that self.lines is sorted by top coordinate"
        potential_headers = [[] for i in range(len(table.columns))]
        
        # Find the lowest line that is above the table
        lowest_ind = [i for i,line in enumerate(self.lines) if line.bounding_box.bottom > table.rows[0].bounding_box.top]
        lowest_ind = lowest_ind[-1] if len(lowest_ind) > 0 else -1
        
        for curr_ind in range(lowest_ind, -1, -1):
            curr_line = self.lines[curr_ind]
            # check if line is aligned with a column
            columns = [i for i,col in enumerate(table.columns) if col.bounding_box.horizontal_intersect(curr_line.bounding_box)]

            # If line collides with more than one column, end loop
            if len(columns) > 1:
                break

            # add if collides with one column
            if len(columns) == 1:
                if self._max_forced_lines == -1 or len(potential_headers[columns[0]]) < self._max_forced_lines:
                    potential_headers[columns[0]].append(curr_line)
        return potential_headers

    def is_first_row_header_heuristics(self, table : BoundingBoxTable) -> bool:
        non_letters_ratio_per_row = []
        for row in range(len(table.rows)):
            count_non_letters = 0
            count_total_chars = 0
            for cell in table.cells[row, :]:
                if cell != BoundingBoxTable.EMPTY_CELL:
                    count_non_letters += sum([len([c for c in elm.get_text() if c not in self._ascii_letters]) for elm in cell])
                    count_total_chars += sum([len(elm.get_text()) for elm in cell])
            non_letters_ratio_per_row.append(count_non_letters / count_total_chars)
        
        mean_non_letters = np.mean(non_letters_ratio_per_row[1:])
        std_non_letters = np.std(non_letters_ratio_per_row[1:]) + 1e-3 # Add 0.1 to handle with zero std
        return non_letters_ratio_per_row[0] < mean_non_letters - self._suspect_header_over_std_factor * std_non_letters
    

    def decide_which_headers(self, table, forced_headers : list[list[Line]]) -> None:
        if self.is_first_row_header_heuristics(table):
            table.header_lines = 1
            return

        original_table_height = len(table.rows)
        avg_row_distance = np.mean(table.get_rows_distances())

        for col in forced_headers:
            for element in col:
                table.add_element(element.bounding_box, element)

        rows_of_header = len(table.rows) - original_table_height
        
        # Remove rows with only one element
        elements_per_row = (table.cells[:rows_of_header,:] != BoundingBoxTable.EMPTY_CELL).sum(axis=1)
        last_index_to_remove = 0
        for i in range(len(elements_per_row)):
            if elements_per_row[i] == 1:
                last_index_to_remove = i+1
        table.remove_top_rows(last_index_to_remove)

        if self._remove_singles_at_bottom_rows:
            elements_per_row = (table.cells != BoundingBoxTable.EMPTY_CELL).sum(axis=1)
            last_non_single_row = np.argmax(elements_per_row[::-1] > 1)
            if last_non_single_row > 0:
                table.remove_bottom_rows(last_non_single_row)
                original_table_height -= last_non_single_row

        # Remove rows that are too far away from the average row distance
        rows_of_header = table.cells.shape[0] - original_table_height
        for i in range(rows_of_header, 0, -1):
            if table.get_rows_distances()[i-1] > avg_row_distance * self._row_distance_variation_sensitivity:
                break
        if rows_of_header > 0:
            table.remove_top_rows(i-1)

        # update number of rows of header
        table.header_lines = table.cells.shape[0] - original_table_height


    def unite_tables(self, tables : list[BoundingBoxTable]) -> list[BoundingBoxTable]:
        new_tables = []
        for table in tables:
            found = False
            for ind, ntable in enumerate(new_tables):
                if ntable.is_colliding_from_bellow(table):
                    if len(table.columns) != len(ntable.columns):
                        table.remove_top_rows(table.header_lines)
                        table.header_lines = 0
                    else:
                        ntable.add_table_at_bottom(table)
                        found = True
                        break
                if table.is_colliding_from_bellow(ntable):
                    if len(table.columns) != len(ntable.columns):
                        ntable.remove_top_rows(ntable.header_lines)
                        ntable.header_lines = 0
                    else:
                        table.add_table_at_bottom(ntable)
                        new_tables[ind] = table
                        found = True
                        break
            if not found:
                new_tables.append(table)
        return new_tables
    

    
    def convert_bounding_box_table_to_table(self, bb_table : BoundingBoxTable) -> Table:
        docstruct_cols = []
        for col_ind, col in enumerate(bb_table.columns):
            docstruct_cells = []
            for row_ind, row in enumerate(bb_table.rows):
                cell = bb_table.cells[row_ind, col_ind]
                if cell == BoundingBoxTable.EMPTY_CELL:
                    cell = []

                bounding_box = BoundingBox(
                    left=col.get_bounding_box().left,
                    top=row.get_bounding_box().top,
                    right=col.get_bounding_box().right,
                    bottom=row.get_bounding_box().bottom
                )
                docstruct_cells.append(TableCell(
                    bounding_box=bounding_box,
                    children=cell,
                    row_index=row_ind,
                    col_index=col_ind,
                    row_span=1,
                    col_span=1,
                ))
            docstruct_cols.append(TableColumn(
                children=docstruct_cells
            ))
        docstruct_table = Table(children=docstruct_cols, table_type=TableType.BORDERLESS_TABLE)
        return docstruct_table

    def extract_tables(self) -> list[Table]:
        # Look for columns
        column_extractor = ColumnExtractor(self.lines)
        columns = column_extractor.extract_columns()
        # Aggregate columns
        aggregate_columns = self.aggregate_aligned_columns(columns)
        # Look for missing lines
        bb_tables = self.cluster_lines_to_tables(aggregate_columns)
        # Look for potential headers
        forced_headers = [self.force_headers(table) for table in bb_tables]
        for t,f in zip(bb_tables, forced_headers):
            self.decide_which_headers(t, f)
        bb_tables = self.unite_tables(bb_tables)
        tables = [self.convert_bounding_box_table_to_table(table) for table in bb_tables]
        return tables