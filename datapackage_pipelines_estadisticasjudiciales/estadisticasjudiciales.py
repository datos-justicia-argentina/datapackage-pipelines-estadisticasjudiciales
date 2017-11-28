import os
import json

from datapackage_pipelines.generators import GeneratorBase, slugify, steps, SCHEDULE_MONTHLY

SCHEMA_FILE = os.path.join(os.path.dirname(__file__),'schema.json')

class Generator(GeneratorBase):
    @classmethod
    def get_schema(cls):
        return json.load(open(SCHEMA_FILE))

    @classmethod
    def generate_pipeline(cls, source):
        pipeline_id = dataset_name = "estadisticasjudiciales"

        pipeline_steps = steps(*[
            ("add_metadata", {
                "name": "testmetadata"
                }
            ),
            ("add_resource",
                {
                    "name": "testresource",
                    "url": "/mnt/datackan/provincias/ARG-14-CSJ/ARG-14-CSJ-listado5.csv",
                    "format": "csv",
                    "headers": 1
                }
            ),
            ("stream_remote_resources", {}),
            ("dump.to_path", {
                "out-path": "testpath"
            }),


        ])

        pipeline_details = {
            "pipeline": pipeline_steps,
            "schedule": {"crontab" : SCHEDULE_MONTHLY}
        }
        yield pipeline_id,pipeline_details


   # - run: set_types
   #   parameters:
   #     resources: test
   #     types:
   #       "tabla5.fila":
   #         description: " t}test"
   #         type: integer
   #       "tabla5.concodigo":
   #         type: string
   #       "tabla5.materia":
   #         type: string
   #       "tabla5.codof":
   #         type: integer
   #       "tabla5.fini":
   #         type: date
   #         format: "%Y%m%d"
   #       "tabla5.objetolit":
   #         type: string
   #       "tabla5.partes":
   #         type: string
