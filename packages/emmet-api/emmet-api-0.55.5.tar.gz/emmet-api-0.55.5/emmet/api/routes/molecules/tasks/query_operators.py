from maggma.api.query_operator import QueryOperator
from maggma.api.utils import STORE_PARAMS
from fastapi import Query
from typing import Optional


# TODO: might need these utils once pmg changes are in place (see below)
# from emmet.api.routes.tasks.utils import calcs_reversed_to_trajectory, task_to_entry


class MultipleTaskIDsQuery(QueryOperator):
    """
    Method to generate a query on search docs using multiple task_id values
    """

    def query(
        self,
        task_ids: Optional[str] = Query(
            None, description="Comma-separated list of task_ids to query on"
        ),
    ) -> STORE_PARAMS:
        crit = {}

        if task_ids:
            # TODO: not sure if this should be string or int?
            crit.update(
                {
                    "task_id": {
                        "$in": [task_id.strip() for task_id in task_ids.split(",")]
                    }
                }
            )

        return {"criteria": crit}

    def post_process(self, docs, query):
        """
        Post processing to remove unwanted fields from all task queries
        """

        for doc in docs:
            doc.pop("tags", None)
            doc.pop("custodian", None)
            doc.pop("dir_name", None)

        return docs


class DeprecationQuery(QueryOperator):
    """
    Method to generate a query on deprecated task documents
    """

    def query(
        self,
        task_ids: str = Query(
            ..., description="Comma-separated list of task_ids to query on"
        ),
    ) -> STORE_PARAMS:
        self.task_ids = [task_id.strip() for task_id in task_ids.split(",")]

        crit = {}

        if task_ids:
            crit.update({"deprecated_tasks": {"$in": self.task_ids}})

        return {"criteria": crit}

    def post_process(self, docs, query):
        """
        Post processing to generate deprecation data
        """

        d = []

        for task_id in self.task_ids:
            deprecation = {
                "task_id": task_id,
                "deprecated": False,
                "deprecation_reason": None,
            }
            for doc in docs:
                if task_id in doc["deprecated_tasks"]:
                    deprecation = {
                        "task_id": task_id,
                        "deprecated": True,
                        "deprecation_reason": None,
                    }
                    break

            d.append(deprecation)

        return d


# TODO: class TrajectoryQuery(QueryOperator):
# Need to write Trajectory class in pmg for Molecules

# TODO: class EntryQuery(QueryOperator):
# Need to write MoleculeEntry class in pmg
