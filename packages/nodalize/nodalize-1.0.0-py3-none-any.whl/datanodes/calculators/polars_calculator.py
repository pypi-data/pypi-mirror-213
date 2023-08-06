"""Pandas calculator."""
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, cast

import pandas as pd
import polars as pl

from nodalize.calculators.calculator import Calculator
from nodalize.tools.static_func_tools import generate_possible_name


class PolarsCalculator(Calculator[pl.DataFrame]):
    """Pandas calculator."""

    calculator_type = "polars"

    def __init__(self, app_name: str) -> None:
        """
        Initialize calculator.

        Args:
            app_name: application name
        """
        Calculator.__init__(self, app_name)

    def from_pandas(self, dataframe: pd.DataFrame, **kwargs) -> pl.DataFrame:
        """
        Convert from pandas data frame to polars data frame.

        Args:
            dataframe: pandas data frame

        Returns:
            polars data frame
        """
        return pl.DataFrame(dataframe)

    def to_pandas(self, dataframe: pl.DataFrame) -> pd.DataFrame:
        """
        Convert to pandas data frame.

        Args:
            dataframe: polars data frame

        Returns:
            pandas data frame
        """
        return dataframe.to_pandas()

    def create_data_frame(
        self,
        values: Dict[str, List[Any]],
        types: Dict[str, type],
    ) -> pl.DataFrame:
        """
        Create data frame from column values.

        Args:
            values: column values
            types: column types

        Returns:
            data frame
        """
        return pl.DataFrame(values)

    def column_exists(self, dataframe: pl.DataFrame, column_name: str) -> bool:
        """
        Tell if a column exists in the data frame.

        Args:
            dataframe: data frame
            column_name: name of the column to find

        Returns:
            bool
        """
        return column_name in dataframe.columns

    def get_column(self, dataframe: pl.DataFrame, column_name: str) -> Any:
        """
        Get column object, to make basic calculations and reinsert using add_column.

        Args:
            dataframe: data frame
            column_name: column name to get

        Returns:
            column object
        """
        return pl.col(column_name)

    def add_column(
        self,
        dataframe: pl.DataFrame,
        column_name: str,
        value: Any,
        literal: bool = False,
        override: bool = True,
    ) -> pl.DataFrame:
        """
        Add column to data frame, with same default value on each rows.

        Args:
            dataframe: data frame
            column_name: new column name
            value: value to assign to the new column
            literal: if True then will set the same value for the entire column, otherwise will consider it as a column
            override: if False, then will not try to replace an existing column

        Returns:
            polars data frame
        """
        if override or not self.column_exists(dataframe, column_name):
            if literal:
                dataframe = dataframe.with_column(pl.lit(value).alias(column_name))
            else:
                dataframe = dataframe.with_column(value.alias(column_name))

        return dataframe

    def filter_in_max_values(
        self, dataframe: pl.DataFrame, value_columns: List[str], key_columns: List[str]
    ) -> pl.DataFrame:
        """
        Filter on max values from the data frame.

        Value columns are typically date columns (InsertedDateTime).

        Args:
            dataframe: data frame
            value_columns: list of columns for which we look for the maximum values
            key_columns: columns to group by on, before searching for the maximum values

        Returns:
            polars  data frame
        """
        key_columns = key_columns.copy()
        for c in key_columns:
            if c not in dataframe.columns:
                raise ValueError(f"Column not found in data frame: {c}")

        aggregation = dataframe
        for vc in value_columns:
            max_series = aggregation.groupby(key_columns).agg(pl.max(vc))
            aggregation = max_series.join(aggregation, how="left", on=key_columns + [vc])  # type: ignore
            key_columns.append(vc)
        return aggregation

    def drop_columns(
        self, dataframe: pl.DataFrame, columns: Iterable[str]
    ) -> pl.DataFrame:
        """
        Drop columns from data frame.

        Args:
            dataframe: data frame
            columns: list of columns to remove

        Returns:
            polars data frame
        """
        for c in columns:
            dataframe = dataframe.drop(c)
        return dataframe

    def select_columns(
        self, dataframe: pl.DataFrame, columns: Iterable[str]
    ) -> pl.DataFrame:
        """
        Select columns in data frame.

        Args:
            dataframe: data frame
            columns: list of columns to keep

        Returns:
            polars data frame
        """
        return dataframe.select(list(columns))

    def drop_duplicates(self, dataframe: pl.DataFrame) -> pl.DataFrame:
        """
        Drop duplicates.

        Args:
            dataframe: polars data frame

        Returns:
            polars data frame
        """
        return dataframe.unique()

    def concat(self, dataframes: List[pl.DataFrame]) -> pl.DataFrame:
        """
        Concatenate data frames.

        Args:
            dataframes: list of data frames to concatenate

        Returns:
            data frame
        """
        if len(dataframes) > 1:
            columns = dataframes[0].columns
            dataframes = [df.select(columns) for df in dataframes]
        return pl.concat(dataframes)

    @staticmethod
    def apply_filter(
        df: pl.DataFrame, filter: Tuple[str, str, Any], schema: Dict[str, type]
    ) -> pl.DataFrame:
        """
        Apply filter to data frame and return new instance.

        Args:
            df: data frame
            filter: filter
            schema: schema

        Returns:
            new data frame
        """
        left_op = df[filter[0]]
        operator = filter[1].lower()
        right_op = filter[2]

        if operator == "=":
            if isinstance(right_op, bool):
                if right_op:
                    return df.filter(left_op)
                else:
                    return df.filter(~left_op)
            else:
                return df.filter(left_op == right_op)
        elif operator == "!=":
            if isinstance(right_op, bool):
                if right_op:
                    return df.filter(~left_op)
                else:
                    return df.filter(left_op)
            else:
                return df.filter(left_op != right_op)
        elif operator == "<=":
            return df.filter(left_op <= right_op)
        elif operator == "<":
            return df.filter(left_op < right_op)
        elif operator == ">=":
            return df.filter(left_op >= right_op)
        elif operator == ">":
            return df.filter(left_op > right_op)
        elif operator == "in":
            return df.filter(left_op.is_in(right_op))
        elif operator == "not in":
            return df.filter(~left_op.is_in(right_op))
        else:
            raise NotImplementedError(f"Unknown filter operator: {operator}")

    def _apply_and_filters(
        self,
        df: pl.DataFrame,
        filters: List[Tuple[str, str, Any]],
        schema: Dict[str, type],
    ) -> pl.DataFrame:
        """
        Apply ABD filters to data frame and return new instance.

        Args:
            df: data frame
            filters: filters
            schema: schema

        Returns:
            new data frame
        """
        for filter in filters:
            df = self.apply_filter(df, filter, schema)
        return df

    def apply_filters(
        self,
        df: pl.DataFrame,
        filters: List[List[Tuple[str, str, Any]]],
        schema: Dict[str, type],
    ) -> pl.DataFrame:
        """
        Apply filters to data frame and return new instance.

        Args:
            df: data frame
            filters: filters
            schema: schema

        Returns:
            new data frame
        """
        if len(filters) == 0:
            raise AssertionError("No filter provided")
        elif len(filters) == 1:
            return self._apply_and_filters(df, filters[0], schema)
        else:
            row_num_column = self.generate_temporary_column_name(df)
            df = df.with_row_count(offset=1, name=row_num_column)
            dfs = [self._apply_and_filters(df, filter, schema) for filter in filters]
            df = pl.concat(dfs)
            df = df.unique()
            df = df.drop(row_num_column)
            return df

    @staticmethod
    def _empty_table(dataframe: pl.DataFrame) -> pl.DataFrame:
        """
        Make data frame empty.

        Args:
            dataframe: data frame

        Return:
            empty data frame with same column types
        """
        first_col = dataframe.columns[0]
        return dataframe.filter(pl.col(first_col) != pl.col(first_col))

    @staticmethod
    def _add_columns(
        dataframe: pl.DataFrame, columns: Dict[str, pl.DataType]
    ) -> pl.DataFrame:
        """
        Add empty columns to data frame.

        Args:
            dataframe: data frame

        Return:
            same data frame with new columns, remaining empty
        """
        for n, t in columns.items():
            if n not in dataframe.columns:
                dataframe = dataframe.with_column(pl.lit(None, t).alias(n))  # type: ignore

        return dataframe

    @staticmethod
    def _get_column_types(dataframe: pl.DataFrame) -> Dict[str, pl.DataType]:
        """
        Get column types from data frame.

        Args:
            dataframe: data frame

        Return:
            dictionary name/type
        """
        ret = {}  # type: Dict[str, pl.DataType]
        for i in range(len(dataframe.columns)):
            ret[dataframe.columns[i]] = cast(pl.DataType, dataframe.dtypes[i])
        return ret

    def _join_non_empty_tables(
        self,
        left: pl.DataFrame,
        right: pl.DataFrame,
        how: str,
        on: List[Tuple[str, str]],
    ) -> pl.DataFrame:
        """
        Join 2 non-empty data frames.

        Args:
            left: left data frame
            right: right data frame
            how: type of join (inner, outer, left, right)
            on: columns to join on

        Returns:
            joined data frame
        """
        left_on = [p[0] for p in on]
        right_on = [p[1] for p in on]

        # Note: there is no "right" join in polars, but we can just swap
        if how == "right":
            tmp = left
            left = right
            right = tmp

            how = "left"

            tmp2 = left_on
            left_on = right_on
            right_on = tmp2

        # Polars does not offer something similar to pd.merge.
        # Joining with left or outer will merge the "on" columns.
        # The code below will duplicate them in order to keep them in the output.
        name_changes = {}  # type: Dict[str, str]

        for i in range(len(left_on)):
            if left_on[i] != right_on[i]:
                col_left = generate_possible_name(
                    lambda n: n not in left_on and n not in right_on
                )
                left = left.with_column(pl.col(left_on[i]).alias(col_left))
                name_changes[col_left] = left_on[i]

                col_right = generate_possible_name(
                    lambda n: n not in left_on and n not in right_on and n != col_left
                )
                right = right.with_column(pl.col(right_on[i]).alias(col_right))
                name_changes[col_right] = right_on[i]

        # Handle cases where 2 columns to merge have the same type but one is flagged as object in Pandas
        for i, cleft in enumerate(left_on):
            cright = right_on[i]
            if left[cleft].dtype != right[cright].dtype:
                left = self.add_column(
                    left, cleft, pl.col(cleft).cast(right[cright].dtype)
                )

        df = left.join(
            right,
            how=how,  # type: ignore
            left_on=left_on,  # type: ignore
            right_on=right_on,  # type: ignore
        )

        if len(name_changes) > 0:
            for c in name_changes.values():
                if c in df.columns:
                    df = df.drop(c)
            df = df.rename(name_changes)

        return df

    def join_data_frames(
        self,
        left: pl.DataFrame,
        right: pl.DataFrame,
        how: str,
        on: List[Tuple[str, str]],
    ) -> pl.DataFrame:
        """
        Join 2 data frames.

        Args:
            left: left data frame
            right: right data frame
            how: type of join (inner, outer, left, right)
            on: columns to join on

        Returns:
            joined data frame
        """
        # Note: polars does not support joining with empty tables.
        # Let's work around it.
        how = how.lower()
        if left.height == 0:
            if right.height == 0:
                return self._add_columns(left, self._get_column_types(right))
            else:
                if how == "inner":
                    right = self._empty_table(right)
                    return self._add_columns(right, self._get_column_types(left))
                elif how in ["right", "outer"]:
                    return self._add_columns(right, self._get_column_types(left))
                elif how == "left":
                    return self._add_columns(left, self._get_column_types(right))
                else:
                    raise NotImplementedError(f"Join method not supported: {how}")
        else:
            if right.height == 0:
                if how == "inner":
                    left = self._empty_table(left)
                    return self._add_columns(left, self._get_column_types(right))
                elif how in ["left", "outer"]:
                    return self._add_columns(left, self._get_column_types(right))
                elif how == "right":
                    return self._add_columns(right, self._get_column_types(left))
                else:
                    raise NotImplementedError(f"Join method not supported: {how}")
            else:
                return self._join_non_empty_tables(left, right, how, on)

    def rename_columns(
        self, dataframe: pl.DataFrame, names: Dict[str, str]
    ) -> pl.DataFrame:
        """
        Rename columns in data frame.

        Args:
            dataframe: data frame
            names: dictionary of column names - before: after

        Returns:
            polars data frame
        """
        return dataframe.rename(names)

    def has_duplicates(self, key_columns: List[str], dataframe: pl.DataFrame) -> bool:
        """
        Find duplicates for a set of key columns into a given data frame.

        Args:
            key_columns: primary key columns
            dataframe: data frame

        Returns:
            bool
        """
        df = dataframe.select(key_columns)

        temp_col_name = generate_possible_name(lambda n: n not in key_columns)
        count_col_name = generate_possible_name(
            lambda n: n not in key_columns and n != temp_col_name
        )

        df = df.with_column(pl.lit(1).alias(temp_col_name))
        df = df.groupby(key_columns).agg(pl.count(temp_col_name).alias(count_col_name))
        df = df.filter(pl.col(count_col_name) > 1)

        return len(df) > 0

    def extract_unique_column_values(
        self, column_name: str, dataframe: pl.DataFrame
    ) -> Set[Any]:
        """
        Get existing values from a given column in the data frame.

        Args:
            column_name: name of the column
            dataframe: dataframe

        Returns:
            set of values
        """
        return set([r[0] for r in dataframe.select(column_name).unique().rows()])

    def load_parquet(
        self,
        file_paths: List[str],
        schema: Dict[str, type],
        columns: Optional[List[str]] = None,
        filters: Optional[List[List[Tuple[str, str, Any]]]] = None,
    ) -> Optional[pl.DataFrame]:
        """
        Load data frame from parquet files.

        Args:
            file_paths: paths to the files
            schema: schema (dictionary of [column name: str, type; type])
            columns: optional list of columns to load, if None then load all
            filters: optional list of filters to apply when loading

        Returns:
            polars data frame
        """
        with pl.StringCache():

            def read_parquet(file_path: str) -> pl.DataFrame:
                return pl.read_parquet(
                    file_path,
                    columns=columns,
                    use_pyarrow=True,
                    pyarrow_options={"filters": filters},
                )

            dfs = [read_parquet(f) for f in file_paths]

        if len(dfs) > 0:
            column_headers = dfs[0].columns
            dfs = [df.select(column_headers) for df in dfs]

        df = pl.concat(dfs)
        return df

    def save_parquet(
        self,
        file_path: str,
        dataframe: pl.DataFrame,
        schema: Dict[str, type],
        partitions: Optional[List[str]],
    ) -> None:
        """
        Save data frame as parquet file.

        Args:
            file_path: path to the file
            dataframe: pandas data frame
            schema: schema (dictionary of [column name: str, type; type])
            partitions: optional list of partition columns
        """
        pyarrow_options = {}  # type: Dict[str, Any]

        if partitions is not None:
            # todo: Polars does not supprot Hive partioning at the time of writing
            self.to_pandas(dataframe).to_parquet(file_path, partition_cols=partitions)
        else:
            pl.DataFrame.write_parquet(
                dataframe,
                file_path,
                use_pyarrow=True,
                pyarrow_options=pyarrow_options,
                compression="snappy",
            )

    def has_nulls(self, column_names: List[str], dataframe: pl.DataFrame) -> bool:
        """
        Check if data frame contains null values for a given set of columns.

        Args:
            column_names: name of the columns
            dataframe: data frame

        Returns:
            True if at least one null was found
        """
        dataframe = dataframe[column_names]
        nulls = dataframe.null_count()
        total = sum(nulls[c].sum() for c in column_names)
        return total > 0

    def row_count(self, dataframe: pl.DataFrame) -> int:
        """
        Compute row count.

        Args:
            dataframe: data frame

        Returns:
            row count
        """
        return len(dataframe)

    def compute_correlations(
        self,
        key_columns: List[str],
        value_columns: List[str],
        dataframe1: pl.DataFrame,
        dataframe2: pl.DataFrame,
    ) -> Dict[str, float]:
        """
        Compute correlations between columns in 2 different data frames. Key columns must match.

        Args:
            key_columns: list of key columns
            value_columns: list of columns to check
            dataframe1: data frame
            dataframe2: data frame

        Returns:
            dictionary column/correlation
        """
        all_columns = key_columns + value_columns
        dataframe1 = dataframe1[all_columns]
        dataframe2 = dataframe2[all_columns]
        merged_data = self.join_data_frames(
            dataframe1, dataframe2, "outer", [(c, c) for c in key_columns]
        )

        correlations = {}
        for col in value_columns:
            col_left = col
            col_right = f"{col}_right"

            if merged_data.schema[col] in [pl.Utf8, pl.Categorical]:
                match = merged_data[col_left] == merged_data[col_right]
                correl = match.sum() / len(merged_data)
                correlations[col] = correl
            else:
                if merged_data.schema[col] in [pl.Int8, pl.Int16, pl.Int32, pl.Int64]:
                    merged_data = merged_data.with_column(
                        pl.col(col).cast(pl.Float64).alias(col)
                    )
                    merged_data = merged_data.with_column(
                        pl.col(col_right).cast(pl.Float64).alias(col_right)
                    )

                correl_matrix = merged_data.select(pl.pearson_corr(col_left, col_right))
                correlations[col] = correl_matrix.rows()[0][0]

        return correlations
