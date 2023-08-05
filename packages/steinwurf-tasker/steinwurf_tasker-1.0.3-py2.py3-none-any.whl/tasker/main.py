# ! /usr/bin/env python
# encoding: utf-8
from invoke import Collection, Program
from invoke import Config

from . import project_tasks


class SteinwurfTaskerConfig(Config):
    prefix = "steinwurf-tasker"
    env_prefix = "SW"


VERSION = "1.0.3"

collection = Collection()

collection.add_collection(Collection.from_module(project_tasks, name="project"))

program = Program(
    config_class=SteinwurfTaskerConfig, namespace=collection, version=VERSION
)
