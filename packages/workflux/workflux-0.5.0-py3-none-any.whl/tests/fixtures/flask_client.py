import os, shutil
import tempfile
import pytest
import workflux
from . import test_workflows_dir

@pytest.fixture
def client():
    temp_base_dir = os.path.join(
        os.path.dirname(__file__),
        "temp"
    )

    if os.path.isdir(temp_base_dir):
        shutil.rmtree(temp_base_dir)

    os.mkdir(temp_base_dir)

    # temp_base_dir = tempfile.TemporaryDirectory()
    # os.environ['WORKFLUX_BASE_DIR'] = temp_base_dir.name

    os.environ['WORKFLUX_BASE_DIR'] = temp_base_dir
    os.environ['WORKFLUX_CONFIG'] = os.path.join(
        os.path.dirname(__file__),
        "test_config.yaml"
    )
    os.environ['WORKFLUX_DEFAULT_INPUT_DIR'] = test_workflows_dir

    test_app = workflux.create_app(webapp=False)
    test_app.config['TESTING'] = True

    with test_app.test_client() as client:
        with test_app.app_context():
            yield client

    # temp_base_dir.cleanup()