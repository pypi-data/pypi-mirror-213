import json

import numpy as np
import pytest
from astropy.io import fits

from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.graphql import RecipeRunResponse
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.debug_frame import DebugFrameMixin
from dkist_processing_common.tasks.mixin.fits import FitsDataMixin


class DebugTask(WorkflowTaskBase, FitsDataMixin, DebugFrameMixin):
    def run(self) -> None:
        pass


@pytest.fixture
def debug_task(tmp_path, recipe_run_id):
    with DebugTask(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        yield task
    task.scratch.purge()
    task.constants._purge()


@pytest.fixture
def random_data() -> np.ndarray:
    return np.random.random(10)


@pytest.fixture
def dummy_header() -> fits.Header:
    return fits.Header({"FOO": "BAR"})


def debug_switch(write_debug_frames):
    class GQLClientWithDebugSwitch:
        def __init__(self, *args, **kwargs):
            pass

        def execute_gql_query(self, **kwargs):
            query_base = kwargs["query_base"]
            if query_base == "recipeRuns":
                return [
                    RecipeRunResponse(
                        recipeInstanceId=1,
                        recipeInstance=None,
                        configuration=json.dumps({"write_debug_frames": write_debug_frames}),
                    ),
                ]

        @staticmethod
        def execute_gql_mutation(**kwargs):
            ...

    return GQLClientWithDebugSwitch


@pytest.mark.parametrize(
    "name",
    [
        pytest.param("custom", id="Custom name"),
        pytest.param("raw", id="Raw name"),
        pytest.param("default", id="Default name"),
    ],
)
def test_debug_frame_write_array(debug_task, random_data, dummy_header, name, mocker):
    """
    Given: A task with the DebugFrameMixin
    When: Writing an array as a debug frame
    Then: The array is written correctly and has the proper name
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=debug_switch(True),
    )
    if name == "custom":
        filename = "my great array.ext"
        raw_name = None
        expected_name = "DEBUG_DebugTask_my_great_array.ext.dat"
    elif name == "raw":
        raw_name = "a_raw_filename.ext"
        filename = None
        expected_name = raw_name
    elif name == "default":
        filename = None
        raw_name = None
        expected_name = "DEBUG_DebugTask_MODSTATE-6_MOVIE_TASK-SOUP.dat"
    else:
        raise ValueError("`name` needs to be either `custom`, `raw`, or `default`")

    extra_tags = [Tag.movie(), Tag.modstate(6), Tag.task("SOUP")]
    debug_task.debug_frame_write_array(
        array=random_data, header=dummy_header, name=filename, tags=extra_tags, raw_name=raw_name
    )

    path_list = list(debug_task.read(tags=[Tag.debug()]))
    assert len(path_list) == 1
    debug_path = path_list[0]
    assert debug_path.name == expected_name
    assert sorted(debug_task.tags(debug_path)) == sorted([Tag.debug(), Tag.frame()] + extra_tags)
    hdul = fits.open(debug_path)
    assert len(hdul) == 1
    assert isinstance(hdul[0], fits.PrimaryHDU)
    assert np.array_equal(hdul[0].data, random_data)
    assert hdul[0].header["FOO"] == dummy_header["FOO"]


def test_error_on_raw_name_and_name(debug_task, mocker):
    """
    Given: A task with the DebugFrameMixin
    When: Trying to write debug array by specifying both name and raw_name
    Then: An error is raised
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=debug_switch(True),
    )
    with pytest.raises(ValueError):
        debug_task.debug_frame_write_array(array=np.array([1]), name="foo", raw_name="bar")
