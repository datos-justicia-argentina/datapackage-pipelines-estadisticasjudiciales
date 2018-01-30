import os
import json
import logging

from datapackage_pipelines.generators import GeneratorBase, slugify, steps, SCHEDULE_MONTHLY

SCHEMA_FILE = os.path.join(os.path.dirname(__file__),'schema.json')

class Generator(GeneratorBase):
    @classmethod
    def get_schema(cls):
        return json.load(open(SCHEMA_FILE))

    @classmethod
    def generate_pipeline(cls, source):
        pipeline_id = dataset_name = "estadisticasjudiciales"

        resources = []

        # //find CSV files
        files = get_files("/mnt/datackan/provincias/","csv")
        for f in files:
            obj = {
                "name": f["table"],
                "url": f["filename"],
                "format": "csv",
                "headers": 1
            }
            #
            # logging.info("len(resources)")
            # logging.info(len(resources))

            if len(resources) < 1:
                objlist = obj,True
            else:
                objlist = [obj]

            r = ["add_resource"]
            r += objlist
            resources += [r]


        logging.info("resources")
        logging.info(tuple(resources))

        pipeline_steps = steps(*[
            ("add_metadata", {
                "processed_by": "datapackage_pipelines_estadisticasjudiciales"
                }
            ),

            tuple(resources),
            #
            # ['add_resource',{'name': 'table', 'url': '/mnt/datackan/provincias/ARG-03-MPF/Dependencias.csv', 'format': 'csv', 'headers': 1}, True],
            # ['add_resource', {'name': 'table', 'url': '/mnt/datackan/provincias/ARG-03-MPF/Listado1(2016).csv', 'format': 'csv', 'headers': 1}],
            # ['add_resource', {'name': 'table', 'url': '/mnt/datackan/provincias/ARG-03-MPF/Listado1.csv', 'format': 'csv', 'headers': 1}],
            # ['add_resource', {'name': 'table', 'url': '/mnt/datackan/provincias/ARG-03-MPF/Listado2(2016).csv', 'format': 'csv', 'headers': 1}],
            # ['add_resource', {'name': 'table', 'url': '/mnt/datackan/provincias/ARG-03-MPF/Listado2.csv', 'format': 'csv', 'headers': 1}],
            # ['add_resource', {'name': 'table', 'url': '/mnt/datackan/provincias/ARG-03-MPF/TiposRoles.csv', 'format': 'csv', 'headers': 1}],
            # ['add_resource', {'name': 'table', 'url': '/mnt/datackan/provincias/ARG-09-MPF/prueba unificacion/ARG-09-MPF-listado1.csv', 'format': 'csv', 'headers': 1}],
            # ['add_resource', {'name': 'table', 'url': '/mnt/datackan/provincias/ARG-09-MPF/prueba unificacion/ARG-09-MPF-Listado1_1.csv', 'format': 'csv', 'headers': 1}],
            # ['add_resource', {'name': 'table', 'url': '/mnt/datackan/provincias/ARG-09-MPF/prueba unificacion/ARG-09-MPF-Listado1_2.csv', 'format': 'csv', 'headers': 1}],
            # ['add_resource', {'name': 'table', 'url': '/mnt/datackan/provincias/ARG-09-MPF/prueba unificacion/ARG-09-MPF-listado1_p1.csv', 'format': 'csv', 'headers': 1}],
            # ['add_resource', {'name': 'table', 'url': '/mnt/datackan/provincias/ARG-09-MPF/prueba unificacion/ARG-09-MPF-listado1_p2.csv', 'format': 'csv', 'headers': 1}]
            # ,
            ("stream_remote_resources", {"cache": True}),
            # dump to mysql
            # run tests

            ("dump.to_path", {
                "out-path": "testpath"
            }),
            # ("dump.to_mysql", {
            #     "out-path": "testpath"
            # }),


        ])

        pipeline_details = {
            "pipeline": pipeline_steps,
            "schedule": {"crontab" : SCHEDULE_MONTHLY}
        }
        logging.info("pipeline_steps")
        logging.info(pipeline_steps)
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




# Inspirado en http://www.bogotobogo.com/python/python_traversing_directory_tree_recursively_os_walk.php
def get_files(base,ext=False):
    topdir = base
    files_array = []
    if ext:
        ext = ext.lower()
    for dirpath, dirnames, files in os.walk(topdir):
        for name in files:
            # print (name,dirpath)
            if not ext or ext and name.lower().endswith(ext):
                # print(dirpath,name);
                files_array.append({
                    "table": "table", #TODO: detectar aca el numero de tabla
                    "filename":os.path.join(dirpath, name)
                })
            # else:
    return files_array
