"""Dependency loading data over a window of dates."""
from datetime import date, timedelta
from typing import Any, Dict, List, Optional, Tuple

from nodalize.calculators.calculator import Calculator
from nodalize.constants.column_category import ColumnCategory
from nodalize.data_management.data_manager import DataManager
from nodalize.dependency import DependencyDefinition


class WindowDependency(DependencyDefinition):
    """
    Dependency loading data over a window of dates.

    Note: generate_parameters is not overridden. Cascading to all dates could generate a lot of calculations based on
        the size of the window,
    """

    def __init__(
        self,
        node_identifier: str,
        start_day_offset: int = 0,
        end_day_offset: int = 0,
        *,
        filters: Optional[List[List[Tuple[str, str, Any]]]] = None,
        data_fields: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Initialize.

        Args:
            node_identifier: data node identifier
            start_day_offset: offset (in days) to apply in order to compute the start date of the window
            end_day_offset: offset (in days) to apply in order to compute the start date of the window
            filters: optional list of filters to apply when loading the data for the node
            data_fields: dictionary where the keys are the fields to load from the data node and the values are the name
                to assign in the final data frame
        """
        DependencyDefinition.__init__(
            self,
            node_identifier,
            filters=filters,
            data_fields=data_fields,
        )
        self._start_offset = start_day_offset
        self._end_offset = end_day_offset

    def assign_data_node(self, node: Any) -> None:
        """
        Assign data node.

        Args:
            node: data node
        """
        DependencyDefinition.assign_data_node(self, node)
        self._date_column = node.date_column

    @property
    def date_column(self) -> str:
        """
        Get header of the date column.

        Returns:
            column header
        """
        if self._date_column is None:
            raise AssertionError("Dependency not initialized with node")
        else:
            return self._date_column

    def compute_start_date(self, dt: date) -> date:
        """
        Compute start date of the window.

        Args:
            dt: reference date of the run

        Returns:
            start date
        """
        return dt + timedelta(self._start_offset)

    def compute_end_date(self, dt: date) -> date:
        """
        Compute end date of the window.

        Args:
            dt: reference date of the run

        Returns:
            end date
        """
        return dt + timedelta(self._end_offset)

    def load_data(
        self,
        data_manager: DataManager,
        calculator: Calculator,
        parameters: Dict[str, Any],
        parent_batch_ids: Optional[List[int]] = None,
    ) -> Any:
        """
        Load dependency data.

        Args:
            data_manager: data manager
            calculator: calculator
            parameters: parameters to use for the calculation - may or may not be related to parameters columns
            parent_batch_ids: batch ids of the parent data to load

        Returns:
            data frame
        """
        if self.filters is None or len(self.filters) == 0:
            filters = [[]]  # type: List[List[Tuple[str, str, Any]]]
        else:
            filters = self.filters.copy()

        if len(filters) == 1:
            parameter_columns = set(
                self.data_node.get_column_names([ColumnCategory.PARAMETER])
            )
            extra_filters = [
                (k, "=", v)
                for k, v in parameters.items()
                if k in parameter_columns and k != self.date_column
            ]
            filters[0].extend(extra_filters)

            start_date = self.compute_start_date(parameters[self.date_column])
            end_date = self.compute_end_date(parameters[self.date_column])
            filters[0].append((self.date_column, "<=", end_date))
            filters[0].append((self.date_column, ">=", start_date))

        parent_df = data_manager.load_data_frame(
            calculator,
            self.data_node.identifier,
            self.data_node.inserted_datetime_column,
            self.data_node.batch_id_column,
            self.data_node.get_enriched_schema(),
            self.populate_fields_to_load(),
            filters,
        )

        if parent_df is None:
            raise ValueError(f"No data found for data node {self.data_node.identifier}")

        parent_df = calculator.rename_columns(parent_df, self.fields)
        return parent_df
