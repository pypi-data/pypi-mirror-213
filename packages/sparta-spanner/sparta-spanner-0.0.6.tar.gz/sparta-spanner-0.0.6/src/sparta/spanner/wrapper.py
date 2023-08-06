from google.cloud.spanner_v1.snapshot import Snapshot
from google.cloud.spanner_v1.streamed import StreamedResultSet
from google.cloud.spanner_v1.transaction import Transaction

from sparta.spanner import DBService


class DBServiceAsyncWrapper:
    def __init__(
        self,
        db: DBService,
    ):
        self.db = db

    async def execute_sql_async(self, *arg, **kwarg) -> StreamedResultSet:
        def func(snapshot: Snapshot):
            return snapshot.execute_sql(*arg, **kwarg)

        return await self.db.run_in_snapshot(func)

    async def read_async(self, *arg, **kwarg) -> StreamedResultSet:
        def func(snapshot: Snapshot):
            return snapshot.read(*arg, **kwarg)

        return await self.db.run_in_snapshot(func)

    async def update_async(self, *arg, **kwarg) -> StreamedResultSet:
        def func(transition: Transaction):
            return transition.update(*arg, **kwarg)

        return await self.db.run_in_transaction(func)

    async def insert_async(self, *arg, **kwarg) -> StreamedResultSet:
        def func(transition: Transaction):
            return transition.insert(*arg, **kwarg)

        return await self.db.run_in_transaction(func)

    async def insert_or_update_async(self, *arg, **kwarg) -> StreamedResultSet:
        def func(transition: Transaction):
            return transition.insert_or_update(*arg, **kwarg)

        return await self.db.run_in_transaction(func)

    async def delete_async(self, *arg, **kwarg) -> StreamedResultSet:
        def func(transition: Transaction):
            return transition.delete(*arg, **kwarg)

        return await self.db.run_in_transaction(func)
