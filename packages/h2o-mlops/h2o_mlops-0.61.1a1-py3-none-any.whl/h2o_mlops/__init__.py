def _load_autogen() -> None:
    import importlib.util
    import pathlib
    import sys

    from h2o_mlops import __file__

    module_name = "h2o_mlops_autogen"
    if importlib.util.find_spec(module_name) is None:
        module_path = pathlib.Path(__file__).parent.joinpath(
            "_autogen/h2o_mlops_client/__init__.py"
        )
        spec = importlib.util.spec_from_file_location(
            name=module_name, location=module_path
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)


_load_autogen()


from h2o_mlops._core import MLOpsClient  # noqa: E402
from h2o_mlops._version import version as __version__  # noqa: F401


__all__ = ["MLOpsClient", "__version__"]
