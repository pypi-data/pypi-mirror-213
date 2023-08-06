from typing import Optional
import attr
import numpy as np

from docstruct import (
    Word,
    Line,
    TableCell,
    TableColumn,
    Table,
    BoundingBox,
    Segment,
    VisLine,
    VisLineOrientation,
    TextBlock,
    TableType,
)
from ..graph import Node, Graph, BipartiteGraph
from .constants import (
    GRID_COVER_RATIO_THRESHOLD,
    IS_GRID_THRESHOLD,
    BORDERED_TABLE_MAX_NUMBER_OF_LINES,
)


@attr.s(auto_attribs=True)
class CellOfLines:
    left: VisLine
    right: VisLine
    top: VisLine
    bottom: VisLine


class BorderedTableExtractor:
    def __init__(
        self,
        words: list[Word],
        hor_lines: list[VisLine],
        ver_lines: list[VisLine],
        hor_threshold: float,
        ver_threshold: float,
    ):
        self.words = words
        # top to bottom
        self.hor_lines = sorted(hor_lines, key=lambda line: line.axis, reverse=True)
        # left to right
        self.ver_lines = sorted(ver_lines, key=lambda line: line.axis)

        self.hor_threshold = hor_threshold
        self.ver_threshold = ver_threshold
        self.table_words = self.get_table_words(words, self.hor_lines, self.ver_lines)

    def get_table_words(
        self, words: list[Word], hor_lines: list[VisLine], ver_lines: list[VisLine]
    ) -> list[Word]:
        if len(hor_lines) <= 1 or len(ver_lines) <= 1:
            return []
        top = hor_lines[0].axis
        bottom = hor_lines[-1].axis
        left = ver_lines[0].axis
        right = ver_lines[-1].axis
        table_bbox = BoundingBox(left=left, top=top, right=right, bottom=bottom)
        table_words = []
        for word in words:
            center = word.bounding_box.get_center()
            if table_bbox.contains_point(center):
                table_words.append(word)
        return table_words

    def group_lines_by_axis(
        self, lines: list[VisLine], length_threshold: float
    ) -> list[list[VisLine]]:
        """Assuming the lines are sorted by axis"""
        if not lines:
            return []
        grouped_lines = [[lines[0]]]

        for i in range(1, len(lines)):
            if abs(lines[i].axis - lines[i - 1].axis) > length_threshold:
                grouped_lines.append([lines[i]])
            else:
                grouped_lines[-1].append(lines[i])
        return grouped_lines

    def get_bipartite_graph(self):
        hor_nodes = []
        ver_nodes = []

        for hor_line in self.hor_lines:
            hor_nodes.append(Node(hor_line))

        for ver_line in self.ver_lines:
            ver_nodes.append(Node(ver_line))

        map_line_id_to_node = {}
        for node in hor_nodes:
            map_line_id_to_node[node.data.id] = node
        for node in ver_nodes:
            map_line_id_to_node[node.data.id] = node

        for hor_line in self.hor_lines:
            for ver_line in self.ver_lines:
                if self.are_adjacent_lines(hor_line, ver_line):
                    hor_node = map_line_id_to_node[hor_line.id]
                    ver_node = map_line_id_to_node[ver_line.id]
                    hor_node.add_neighbor(ver_node)
                    ver_node.add_neighbor(hor_node)

        bipartite_graph = BipartiteGraph(left_nodes=hor_nodes, right_nodes=ver_nodes)
        dummy_nodes = bipartite_graph.get_nodes_with_bounded_degree(
            min_degree=0, max_degree=1
        )
        for dummy_node in dummy_nodes:
            bipartite_graph.remove_node(dummy_node)
        return bipartite_graph

    def are_adjacent_lines(
        self,
        first_line: VisLine,
        second_line: VisLine,
    ):
        first_bb = first_line.convert_to_bb(
            length_threshold=0,
        )
        second_bb = second_line.convert_to_bb(
            length_threshold=0,
        )
        return first_bb.intersect(second_bb)

    def filter_lines_by_cycles(
        self, hor_nodes: list[Node], ver_nodes: list[Node]
    ) -> tuple[list[Node], list[Node]]:
        filtered_hor_nodes = set()
        filtered_ver_nodes = set()
        for top in hor_nodes:
            for j, left in enumerate(top.neighbors):
                for k in range(j + 1, len(top.neighbors)):
                    right = top.neighbors[k]
                    intersection_nodes = set(left.neighbors).intersection(
                        right.neighbors
                    )
                    if len(intersection_nodes) > 1:
                        filtered_hor_nodes.add(top)
                        filtered_ver_nodes.add(left)
                        filtered_ver_nodes.add(right)

        filtered_hor_nodes = list(filtered_hor_nodes)
        filtered_ver_nodes = list(filtered_ver_nodes)
        return filtered_hor_nodes, filtered_ver_nodes

    def detect_tables(self) -> list[Table]:
        bipartite_graph = self.get_bipartite_graph()
        connected_components = bipartite_graph.get_connected_components()
        tables = []
        for connected_component in connected_components:
            hor_nodes = [
                node
                for node in connected_component
                if node.data.orientation == VisLineOrientation.HORIZONTAL
            ]
            ver_nodes = [
                node
                for node in connected_component
                if node.data.orientation == VisLineOrientation.VERTICAL
            ]
            hor_nodes = sorted(hor_nodes, key=lambda node: node.data.axis, reverse=True)
            ver_nodes = sorted(ver_nodes, key=lambda node: node.data.axis)
            hor_cycle_nodes, ver_cycle_nodes = self.filter_lines_by_cycles(
                hor_nodes, ver_nodes
            )
            hor_cycle_nodes = [node.data for node in hor_nodes]
            ver_cycle_nodes = [node.data for node in ver_nodes]

            hor_cycle_lines = sorted(
                hor_cycle_nodes, key=lambda line: line.axis, reverse=True
            )
            ver_cycle_lines = sorted(ver_cycle_nodes, key=lambda line: line.axis)

            grouped_hor_lines = self.group_lines_by_axis(
                hor_cycle_lines, self.hor_threshold / 2
            )
            grouped_ver_lines = self.group_lines_by_axis(
                ver_cycle_lines, self.ver_threshold / 2
            )
            if len(grouped_hor_lines) < 2 or len(grouped_ver_lines) < 2:
                continue
            table_grid = TableGrid(
                grouped_hor_lines, grouped_ver_lines, self.table_words
            )

            table: Table = table_grid.detect_table(
                self.hor_lines, self.ver_lines, self.hor_threshold, self.ver_threshold
            )
            if table is None:
                continue
            tables.append(table)

        return tables


class TableGrid:
    def __init__(
        self,
        grouped_hor_lines: list[list[VisLine]],
        grouped_ver_lines: list[list[VisLine]],
        words: list[Word],
    ):
        self.grouped_hor_lines = grouped_hor_lines
        self.grouped_ver_lines = grouped_ver_lines
        self.words = words
        self.m = len(grouped_hor_lines) - 1
        self.n = len(grouped_ver_lines) - 1

        self.hor_lines_grid = np.zeros((self.m + 1, self.n), dtype=bool)
        self.ver_lines_grid = np.zeros((self.m, self.n + 1), dtype=bool)

        self.hor_axis_values = self.get_axis_values(self.grouped_hor_lines)
        self.ver_axis_values = self.get_axis_values(self.grouped_ver_lines)
        pass

    def filter_words_inside_cell(
        self, table_words: list[Word], cell_bbox: BoundingBox
    ) -> list[Word]:
        cell_words = []
        for word in table_words:
            center = word.bounding_box.get_center()
            if cell_bbox.contains_point(center):
                cell_words.append(word)
        return cell_words

    def get_axis_values(self, grouped_lines: list[list[VisLine]]) -> list[float]:
        axis_values = []
        for lines in grouped_lines:
            axis = VisLine.get_weighted_average_axis(lines)
            axis_values.append(axis)
        return axis_values

    def fill_lines_grid(
        self, axis_values, all_lines_grouped: list[list[VisLine]], is_hor: bool
    ):
        for k in range(len(all_lines_grouped)):
            segments = [
                Segment(left=line.start, right=line.end)
                for line in all_lines_grouped[k]
            ]
            for l in range(len(axis_values) - 1):
                grid_segment = Segment(
                    left=min(axis_values[l], axis_values[l + 1]),
                    right=max(axis_values[l], axis_values[l + 1]),
                )
                cover_ratio = grid_segment.proportion_covered_by_segments(segments)
                if cover_ratio > GRID_COVER_RATIO_THRESHOLD:
                    if is_hor:
                        self.hor_lines_grid[k][l] = True
                    else:
                        self.ver_lines_grid[l][k] = True

    def get_closest_index(self, value: float, values: list[float]) -> int:
        closest_index = -1
        min_diff = float("inf")
        for i, v in enumerate(values):
            diff = abs(value - v)
            if diff < min_diff:
                min_diff = diff
                closest_index = i
        return closest_index

    def group_lines_by_axis_values(
        self, axis_values: list[float], lines: list[VisLine], threshold: float
    ) -> list[list[VisLine]]:
        grouped_lines = [[] for _ in range(len(axis_values))]
        closest_axis_index = -1
        for line in lines:
            closest_axis_index = self.get_closest_index(line.axis, axis_values)
            distance = abs(line.axis - axis_values[closest_axis_index])
            if distance < threshold:
                grouped_lines[closest_axis_index].append(line)
        return grouped_lines

    def get_graph(self) -> Graph:
        """
        In this graph, each node represents a grid cell.
        Two nodes are connected if they are adjacent (plus)
        and there is no line between them.
        """
        nodes = []
        map_indexes_to_nodes = {}
        for i in range(self.m):
            for j in range(self.n):
                node = Node(data=(i, j))
                nodes.append(node)
                map_indexes_to_nodes[(i, j)] = node
        graph = Graph(nodes=nodes)
        for i in range(self.m):
            for j in range(self.n):
                current_node = map_indexes_to_nodes[(i, j)]
                for delta_y in (-1, 1):
                    if 0 <= i + delta_y < self.m:
                        neighbor_node = map_indexes_to_nodes[(i + delta_y, j)]
                        if not self.hor_lines_grid[i + delta_y][j]:
                            current_node.add_neighbor(neighbor_node)
                for delta_x in (-1, 1):
                    if 0 <= j + delta_x < self.n:
                        neighbor_node = map_indexes_to_nodes[(i, j + delta_x)]
                        if not self.ver_lines_grid[i][j + delta_x]:
                            current_node.add_neighbor(neighbor_node)
        return graph

    def compose_cell_words_to_lines(self, words: list[Word]) -> list[Line]:
        sorted_words = TextBlock.sort(words)
        lines_children = {}
        for word in sorted_words:
            parent = word.get_parent()
            if parent not in lines_children:
                lines_children[parent] = []
            lines_children[parent].append(word)
        lines = []
        for line_children in lines_children.values():
            line = Line(children=line_children)
            line.set_bounding_box()
            line.set_length()
            lines.append(line)
        return lines

    def validate_number_of_lines_in_cells(self, cells: list[TableCell]) -> bool:
        for cell in cells:
            number_of_lines_condition = (
                len(cell.children) > BORDERED_TABLE_MAX_NUMBER_OF_LINES
            )
            row_number_condition = cell.row_index > 0
            if number_of_lines_condition and row_number_condition:
                return False
        return True

    def get_cells(self, graph: Graph) -> list[TableCell]:
        connected_components = graph.get_connected_components()
        cells = []
        for component in connected_components:
            indexes = [node.data for node in component]
            min_i, max_i = (
                min(indexes, key=lambda x: x[0])[0],
                max(indexes, key=lambda x: x[0])[0],
            )
            min_j, max_j = (
                min(indexes, key=lambda x: x[1])[1],
                max(indexes, key=lambda x: x[1])[1],
            )
            if (max_i - min_i + 1) * (max_j - min_j + 1) == len(component):
                bounding_box = BoundingBox(
                    left=self.ver_axis_values[min_j],
                    right=self.ver_axis_values[max_j + 1],
                    top=self.hor_axis_values[min_i],
                    bottom=self.hor_axis_values[max_i + 1],
                )
                cell_words = self.filter_words_inside_cell(self.words, bounding_box)
                cell_lines = self.compose_cell_words_to_lines(cell_words)
                cell = TableCell(
                    bounding_box=bounding_box,
                    children=cell_lines,
                    row_index=min_i,
                    col_index=min_j,
                    row_span=max_i - min_i + 1,
                    col_span=max_j - min_j + 1,
                )
                cells.append(cell)
            else:
                for node in component:
                    i, j = node.data
                    bounding_box = BoundingBox(
                        left=self.ver_axis_values[j],
                        right=self.ver_axis_values[j + 1],
                        top=self.hor_axis_values[i],
                        bottom=self.hor_axis_values[i + 1],
                    )
                    cell_words = self.filter_words_inside_cell(self.words, bounding_box)
                    cell_lines = self.compose_cell_words_to_lines(cell_words)
                    cell = TableCell(
                        bounding_box=bounding_box,
                        children=cell_lines,
                        row_index=i,
                        col_index=j,
                        row_span=1,
                        col_span=1,
                    )
                    cells.append(cell)
        return cells

    def get_columns(self, cells: list[TableCell]) -> list[TableColumn]:
        num_columns = max(cell.col_index for cell in cells) + 1

        columns: list[list[TableCell]] = [None] * num_columns

        for cell in cells:
            if columns[cell.col_index] is None:
                columns[cell.col_index] = []
            columns[cell.col_index].append(cell)
        for column in columns:
            if column is None:
                continue
            column.sort(key=lambda cell: cell.row_index)
        return [
            TableColumn(children=column) for column in columns if column is not None
        ]

    @staticmethod
    def truth_ratio(matrix: np.ndarray) -> float:
        return np.count_nonzero(matrix) / matrix.size

    def is_grid(self):
        hor_cover = TableGrid.truth_ratio(self.hor_lines_grid)
        ver_cover = TableGrid.truth_ratio(self.ver_lines_grid)
        return hor_cover > IS_GRID_THRESHOLD and ver_cover > IS_GRID_THRESHOLD

    def non_trivial_table(self, cells: list[TableCell]) -> bool:
        if len(cells) <= 1:
            return False
        num_rows = max(cell.row_index + cell.row_span for cell in cells)
        num_cols = max(cell.col_index + cell.col_span for cell in cells)
        return num_rows > 1 and num_cols > 1

    def detect_table(
        self,
        all_hor_lines: list[VisLine],
        all_ver_lines: list[VisLine],
        hor_threshold: float,
        ver_threshold: float,
    ) -> Optional[Table]:
        all_hor_lines_grouped = self.group_lines_by_axis_values(
            self.hor_axis_values, all_hor_lines, hor_threshold
        )
        all_ver_lines_grouped = self.group_lines_by_axis_values(
            self.ver_axis_values, all_ver_lines, ver_threshold
        )

        self.fill_lines_grid(self.ver_axis_values, all_hor_lines_grouped, is_hor=True)
        self.fill_lines_grid(self.hor_axis_values, all_ver_lines_grouped, is_hor=False)
        if not self.is_grid():
            return None
        graph = self.get_graph()
        cells = self.get_cells(graph)
        if not self.validate_number_of_lines_in_cells(cells):
            return None
        if not self.non_trivial_table(cells):
            return None
        columns = self.get_columns(cells)

        table = Table(children=columns)
        return table
