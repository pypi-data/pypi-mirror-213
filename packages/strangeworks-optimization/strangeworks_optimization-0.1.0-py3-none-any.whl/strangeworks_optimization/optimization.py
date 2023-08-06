from ast import Dict
import strangeworks as sw
from dimod import SampleSet
import json
from typing import Optional

from dimod import BinaryQuadraticModel

import tempfile

path = "qubo"


class OptimizationJob:
    def __init__(
        self,
        bqm: BinaryQuadraticModel | Dict,
        var_type: str,
        lagrange_multiplier: float,
        solver: dict,
    ) -> None:
        self.var_type = var_type
        self.lagrange_multiplier = lagrange_multiplier
        self.solver = solver
        self.model = json.dumps(bqm.to_serializable())


class StrangeworksOptimization:
    """Strangeworks client object."""

    def __init__(self, resource_slug: Optional[str] = " ") -> None:
        if resource_slug != " " and resource_slug != "":
            self.rsc = sw.resources(slug=resource_slug)[0]
        else:
            rsc_list = sw.resources()
            for rr in range(len(rsc_list)):
                if rsc_list[rr].product.slug == "optimization":
                    self.rsc = rsc_list[rr]

        # self.backend_list = " "

    def run(self, qubo_job: OptimizationJob) -> str:
        job = sw.execute(self.rsc, payload=qubo_job.__dict__, endpoint=path)
        slug = job["job_slug"]
        # Get Strangeworks Job from slug
        return slug

    def get_results(self, slug: str):
        result = sw.download_job_files(slug)[1]
        return SampleSet.from_serializable(result)

    def upload_model(self, bqm: BinaryQuadraticModel) -> str:
        with tempfile.NamedTemporaryFile(mode="w+") as t:
            json.dump(bqm.to_serializable(), t)
            t.flush()

            return sw.upload_file(t.name)

    # def get_status(self, slug: str):
    # todo: implement this
    # def get_backends(self):
    # todo: implement this
