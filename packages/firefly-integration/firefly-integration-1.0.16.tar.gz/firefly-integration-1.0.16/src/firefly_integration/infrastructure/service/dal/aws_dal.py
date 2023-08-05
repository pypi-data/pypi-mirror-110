from __future__ import annotations

from datetime import datetime
from hashlib import md5
from typing import List

import awswrangler as wr
import firefly as ff
import pandas as pd
from botocore.exceptions import ClientError

import firefly_integration.domain as domain
from firefly_integration.domain.service.dal import Dal

MAX_FILE_SIZE = 250000000  # ~250MB
PARTITION_LOCK = 'partition-lock-{}'


class AwsDal(Dal):
    _batch_process: ff.BatchProcess = None
    _remove_duplicates: domain.RemoveDuplicates = None
    _sanitize_input_data: domain.SanitizeInputData = None
    _s3_client = None
    _mutex: ff.Mutex = None
    _db_created: dict = {}
    _context: str = None
    _bucket: str = None
    _max_compact_records: str = None

    def __init__(self):
        super().__init__()
        if self._max_compact_records is None:
            self._max_compact_records = '1000'

    def store(self, df: pd.DataFrame, table: domain.Table):
        self._ensure_db_created(table)

        df = df[list(map(lambda c: c.name, table.columns))]

        if 'created_on' in table.type_dict:
            df['created_on'].fillna(datetime.utcnow(), inplace=True)
        if 'updated_on' in table.type_dict:
            df['updated_on'] = datetime.utcnow()

        params = {
            'df': df,
            'path': table.full_path(),
            'dataset': True,
            'database': table.database.name,
            'table': table.name,
            'partition_cols': table.partition_columns,
            'compression': 'snappy',
            'dtype': table.type_dict,
            'schema_evolution': True,
        }

        if table.time_partitioning is not None:
            params['partition_cols'] = ['dt']
            # params['projection_enabled'] = True
            params['regular_partitions'] = True
            fmt = '%Y'
            if table.time_partitioning == 'month':
                fmt += '-%m'
            if table.time_partitioning == 'day':
                fmt += '-%m-%d'

            df['dt'] = pd.to_datetime(df[table.time_partitioning_column]).dt.strftime(fmt)

            # params['projection_types'] = {'dt': 'enum'}
            # params['projection_values'] = {'dt': self._date_partition_range(df, table.time_partitioning)}

        if not df.empty:
            wr.s3.to_parquet(**params)

    def _date_partition_range(self, df: pd.DataFrame, timeframe: str):
        start = df['dt'].min()
        end = df['dt'].max()
        fmt = '%Y'
        if timeframe == 'month':
            fmt += '-%m'
        if timeframe == 'day':
            fmt += '-%m-%d'

        return ','.join(pd.date_range(start, end, freq='MS').strftime(fmt).to_list())

    def load(self, table: domain.Table, criteria: ff.BinaryOp = None) -> pd.DataFrame:
        pass

    def delete(self, criteria: ff.BinaryOp, table: domain.Table):
        pass

    def get_partitions(self, table: domain.Table, criteria: ff.BinaryOp = None) -> List[str]:
        args = {'database': table.database.name, 'table': table.name}
        if criteria is not None:
            args['expression'] = str(criteria)

        try:
            partitions = wr.catalog.get_parquet_partitions(**args)
        except ClientError:
            return []

        return list(map(lambda p: p.replace('s3://', ''), partitions.keys()))

    def wait_for_tmp_files(self, files: list):
        wr.s3.wait_objects_exist(
            list(map(lambda f: f's3://{self._bucket}/{f}', files)),
            delay=1,
            max_attempts=60,
            use_threads=True
        )

    def read_tmp_files(self, files: list) -> pd.DataFrame:
        return wr.s3.read_parquet(list(map(lambda f: f's3://{self._bucket}/{f}', files)), use_threads=True)

    def write_tmp_file(self, file: str, data: pd.DataFrame):
        wr.s3.to_parquet(data, path=f's3://{self._bucket}/{file}')

    def compact(self, table: domain.Table, path: str):
        while True:
            if self._do_compact(table, path) is True:
                break

    def _do_compact(self, table: domain.Table, path: str) -> bool:
        path = path.rstrip('/')
        if not path.startswith('s3://'):
            path = f's3://{path}'
        bucket = path.split('/')[2]

        ret = True
        to_delete = []
        key = None
        n = 0
        try:
            for k, size in wr.s3.size_objects(path=f'{path}/', use_threads=True).items():
                if k.endswith('.tmp'):
                    continue
                if k.endswith('.dat.snappy.parquet'):
                    if size < MAX_FILE_SIZE:
                        key = k
                    n += 1
                else:
                    to_delete.append(k)
        except ClientError:
            return True  # Another process must be compacting, so stop running

        if len(to_delete) == 0:
            return True  # Nothing new to compact

        if len(to_delete) > int(self._max_compact_records):
            ret = False
            to_delete = to_delete[:int(self._max_compact_records)]
        to_read = to_delete.copy()
        if key is not None:
            to_read.append(key)

        try:
            with self._mutex(PARTITION_LOCK.format(md5(path.encode('utf-8')).hexdigest()), timeout=0):
                if key is None:
                    key = f'{path}/{n + 1}.dat.snappy.parquet'

                try:
                    df = self._sanitize_input_data(wr.s3.read_parquet(path=to_read, use_threads=True), table)
                except ClientError:
                    return True  # Another process must be compacting, so stop running

                self._remove_duplicates(df, table)
                try:
                    df.reset_index(inplace=True)
                except ValueError:
                    pass
                wr.s3.to_parquet(
                    df=df, path=f'{key}.tmp', compression='snappy', dtype=table.type_dict, use_threads=True
                )
                k = '/'.join(key.split('/')[3:])
                self._s3_client.copy_object(Bucket=bucket, CopySource=f'{bucket}/{k}.tmp', Key=k)
                self._s3_client.delete_object(Bucket=bucket, Key=f'{k}.tmp')
                wr.s3.delete_objects(to_delete, use_threads=True)
        except TimeoutError:
            pass

        return ret

    def _ensure_db_created(self, table: domain.Table):
        if table.database.name not in self._db_created:
            wr.catalog.create_database(name=table.database.name, exist_ok=True,
                                       description=table.database.description or '')
            self._db_created[table.database.name] = True
