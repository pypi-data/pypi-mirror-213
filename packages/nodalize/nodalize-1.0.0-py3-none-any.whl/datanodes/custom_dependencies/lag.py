"""Dependency loading data with a lag."""
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from nodalize.calculators.calculator import Calculator
from nodalize.constants import column_names
from nodalize.custom_dependencies.date import DateDependency
from nodalize.data_management.data_manager import DataManager


class LagDependency(DateDependency):
    """Dependency loading data with a lag."""

    def __init__(
        self,
        node_identifier: str,
        day_lag: int,
        *,
        filters: Optional[List[List[Tuple[str, str, Any]]]] = None,
        data_fields: Optional[Dict[str, str]] = None,
        lookback: Optional[int] = None
    ) -> None:
        """
        Initialize.

        Args:
            node_identifier: data node identifier
            day_lag: lag (in days) to apply when loading the data
            filters: optional list of filters to apply when loading the data for the node
            data_fields: dictionary where the keys are the fields to load from the data node and the values are the name
                to assign in the final data frame
            join_how: type of join (default is outer)
            join_on: optional list of columns to join on (will default on node keys)
            date_column: name of the column used as a date reference
            date_parameter: name of the parameter setting the date for the run
            lookback: lookback to apply when loading the data (default to node lookback)
        """
        DateDependency.__init__(
            self,
            node_identifier,
            filters=filters,
            data_fields=data_fields,
            lookback=lookback,
        )
        self._lag = day_lag

    def offset_days(self, dt: date, offset: int) -> date:
        """
        Offset days. To be overriden for calendar management.

        Args:
            dt: date to offset
            offset: number of days to offset hte date by

        Returns:
            date
        """
        return dt + timedelta(offset)

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
            dependency: dependency definition
            data_manager: data manager
            calculator: calculator
            parameters: parameters to use for the calculation - may or may not be related to parameters columns
            parent_batch_ids: batch ids of the parent data to load

        Returns:
            data frame
        """
        new_parameters = parameters.copy()
        new_parameters[self.date_column] = self.offset_days(
            parameters[self.date_column], -self._lag
        )

        df = DateDependency.load_data(
            self, data_manager, calculator, new_parameters, parent_batch_ids
        )
        df = calculator.add_column(
            df, self.date_column, parameters[self.date_column], literal=True
        )
        return df

    def generate_parameters(
        self,
        parameters: Dict[str, Any],
        parent_batch_ids: List[int],
        data_manager: DataManager,
        calculator: Calculator,
    ) -> List[Dict[str, Any]]:
        """
        Generate sets of parameters to run based on delta updates of dependency.

        Args:
            parameters: parameters used for parent runs
            parent_batch_ids: list of batch ids to narrow down data to load
            data_manager: DataManager,
            calculator: instance of calculator

        Returns:
            list of dictionary, where each dictionary is a set of parameters for the downsteam run
        """
        if len(parent_batch_ids) == 0:
            return []
        else:
            df = data_manager.load_data_frame(
                calculator,
                self.data_node.identifier,
                self.data_node.inserted_datetime_column,
                self.data_node.batch_id_column,
                self.data_node.get_enriched_schema(),
                [self.date_column],
                batch_ids=parent_batch_ids,
            )

            datadates = calculator.extract_unique_column_values(self.date_column, df)

            ret = []  # type: List[Dict[str, Any]]
            for datadate in datadates:
                if isinstance(datadate, np.datetime64):
                    datadate = datetime.utcfromtimestamp(
                        datadate.astype(int) * 1e-9
                    ).date()
                elif isinstance(datadate, datetime):
                    datadate = datadate.date()

                dt = self.offset_days(datadate, self._lag)
                new_parameters = parameters.copy()
                new_parameters[self.date_column] = datadate + timedelta(self._lag)
                ret.append(new_parameters)

            return ret


class WeekDayLagDependency(LagDependency):
    """Version of LagDependency that will avoid weekends."""

    def offset_days(self, dt: date, offset: int) -> date:
        """
        Offset days. To be overriden for calendar management.

        Args:
            dt: date to offset
            offset: number of days to offset hte date by

        Returns:
            date
        """
        if offset == 0:
            return dt

        new_date = dt + timedelta(offset)

        if new_date.weekday() == 5:
            if offset > 0:
                return new_date + timedelta(2)
            else:
                return new_date - timedelta(1)
        elif new_date.weekday() == 6:
            if offset > 0:
                return new_date + timedelta(1)
            else:
                return new_date - timedelta(2)
        else:
            return new_date
