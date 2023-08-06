"""
A Python library for logging data to BrainTrust.

### Quickstart

Install the library with pip.

```bash
pip install braintrust
```

Then, run a simple experiment with the following code:

```python
import braintrust

experiment = braintrust.init(project="PyTest")
experiment.log(
    inputs={"test": 1},
    output="foo",
    expected="bar",
    scores={
        "n": 0.5,
    },
    metadata={
        "id": 1,
    },
)
print(experiment.summarize())
```

### API Reference
"""
import atexit
import datetime
import json
import logging
import os
import queue
import threading
import traceback
import urllib.parse
import uuid
from functools import cache as _cache
from getpass import getpass
from typing import Any

import git
import openai
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .cache import API_INFO_PATH, CACHE_PATH
from .oai import run_cached_request


class BrainTrustState:
    def __init__(self):
        self.current_project = None
        self.current_experiment = None


_state = BrainTrustState()
_logger = logging.getLogger("braintrust")

API_URL = None
ORG_ID = None
LOG_URL = None


class HTTPConnection:
    def __init__(self, base_url=API_URL):
        self.session = requests.Session()
        self.base_url = base_url

        # Following a suggestion in https://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url-in-requests
        retry = Retry(connect=10, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def set_token(self, token):
        token = token.rstrip("\n")
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get(self, path, *args, **kwargs):
        return self.session.get(_urljoin(self.base_url, path), *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self.session.post(_urljoin(self.base_url, path), *args, **kwargs)


@_cache
def api_conn():
    return HTTPConnection(LOG_URL)  # TODO: Fix to use global install


def api_get(object_type, args=None):
    resp = api_conn().get(f"/{object_type}", params=args)
    assert resp.ok, resp.text
    return resp.json()


def api_insert(object_type, args):
    resp = api_conn().post(
        f"/{object_type}",
        json=args,
    )
    assert resp.ok, resp.text
    return resp.json()


class ModelWrapper:
    _ENDPOINT = None

    def __getattr__(self, name: str) -> Any:
        return self.data[name]


@_cache
def _user_info():
    return api_get("ping")


class Project(ModelWrapper):
    _ENDPOINT = "projects"

    def __init__(self, name):
        unique_key, insert_args = {"name": name}, {"org_id": _user_info()["organizations"][0]["id"]}

        # Can we have an upsert (or insert if not exists) method instead?
        existing = []
        if unique_key:
            existing = api_get(self._ENDPOINT, unique_key)

        if not existing:
            insert_args.update(unique_key)
            existing = api_insert(self._ENDPOINT, insert_args)

        if existing:
            self.data = existing[0]
        else:
            assert False, "Unable to find record in " + self._ENDPOINT


def guess_notebook_block_name():
    try:
        import IPython

        ipython = IPython.get_ipython()

        cell_text = "\n".join(reversed([ipython.history_manager.get_tail(i + 1)[0][2] for i in range(3)]))
    except Exception:
        return None

    return [
        {
            "role": "system",
            "content": """\
You can generate two word summaries for machine learning experiment names, based
on the last 3 blocks of code in your notebook.
The experiment name should be exactly two words, concatenated with a hyphen, all lowercase.
The input format is recently executed python code. For example, "foo-bar" is valid but
"foo-bar-baz" is not.""",
        },
        {
            "role": "user",
            "content": f"{cell_text[:4096]}",
        },
    ]


def guess_git_experiment_name():
    try:
        repo = git.Repo(search_parent_directories=True)
    except git.InvalidGitRepositoryError:
        return None

    branch = repo.active_branch.name
    diff = repo.git.diff(repo.head.commit.tree)
    if not diff and len(repo.head.commit.parents) > 0:
        diff = repo.head.commit.message + "\n" + repo.git.diff(repo.head.commit.tree, repo.head.commit.parents[0].tree)

    return [
        {
            "role": "system",
            "content": """\
You can generate two word summaries for machine learning experiment names, based
on the branch name and an optional "diff" of the experiment's code on top of the branch.
The experiment name should be exactly two words, concatenated with a hyphen, all lowercase.
The input format is the output of "git diff". For example, "foo-bar" is valid but
"foo-bar-baz" is not.""",
        },
        {
            "role": "user",
            "content": f"Branch: {branch}" + (f"\n\nDiff:\n{diff[:4096]}" if diff else ""),
        },
    ]


def guess_experiment_name():
    if openai.api_key is None:
        return None

    messages = guess_notebook_block_name()
    if not messages:
        messages = guess_git_experiment_name()

    if not messages:
        return None

    resp = run_cached_request(
        Completion=openai.ChatCompletion,
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=128,
        temperature=0.7,
    )

    name = None
    if len(resp["choices"]) > 0:
        name = "-".join(resp["choices"][0]["message"]["content"].split("-")[:2])
        # Strip punctuation and whitespace from the prefix and suffix
        name = name.strip(" .,;:!?-")
    return name


class _LogThread:
    def __init__(self, name=None):
        self.thread = threading.Thread(target=self._publisher, daemon=True)
        self.started = False

        log_namespace = "braintrust"
        if name:
            log_namespace += f" [{name}]"

        self.logger = logging.getLogger(log_namespace)

        try:
            queue_size = int(os.environ.get("BRAINTRUST_QUEUE_SIZE"))
        except Exception:
            queue_size = 1000
        self.queue = queue.Queue(maxsize=queue_size)

        atexit.register(self._finalize)

    def log(self, *args):
        self._start()
        for event in args:
            self.queue.put(event)

    def _start(self):
        if not self.started:
            self.thread.start()
            self.started = True

    def _finalize(self):
        self.logger.info("Flushing final log events...")
        self._flush()

    def _publisher(self, batch_size=None):
        kwargs = {}
        if batch_size is not None:
            kwargs["batch_size"] = batch_size

        while True:
            try:
                item = self.queue.get()
            except queue.Empty:
                continue

            try:
                self._flush(initial_items=[item], **kwargs)
            except Exception:
                traceback.print_exc()

    def _flush(self, initial_items=None, batch_size=100):
        items = initial_items or []
        while True:
            while len(items) < batch_size:
                try:
                    items.append(self.queue.get_nowait())
                except queue.Empty:
                    break

            api_insert("logs", items)

            if len(items) < batch_size:
                break

            items.clear()


class Experiment(ModelWrapper):
    """
    An experiment is a collection of logged events, such as model inputs and outputs, which represent
    a snapshot of your application at a particular point in time. An experiment is meant to capture more
    than just the model you use, and includes the data you use to test, pre- and post- processing code,
    comparison metrics (scores), and any other metadata you want to include.

    Experiments are associated with a project, and two experiments are meant to be easily comparable via
    their `inputs`. You can change the attributes of the experiments in a project (e.g. scoring functions)
    over time, simply by changing what you log.

    You should not create `Experiment` objects directly. Instead, use the `braintrust.init()` method.
    """

    def __init__(self, project: Project, name: str = None, description: str = None):
        self.project = project
        args = {"project_id": project.id}

        if not name:
            name = guess_experiment_name()

        if name:
            args["name"] = name

        if description:
            args["description"] = description

        self.data = api_insert("register-experiment", args)[0]
        self.logger = _LogThread(name=name)

    def log(self, inputs, output, expected, scores, metadata=None):
        user_id = _user_info()["id"]
        args = {
            "id": str(uuid.uuid4()),
            "inputs": inputs,
            "output": output,
            "expected": expected,
            "scores": scores,
            "project_id": self.project.id,
            "experiment_id": self.id,
            "user_id": user_id,
            "created": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }

        if metadata:
            args["metadata"] = metadata

        self.logger.log(args)
        return args["id"]

    def summarize(self):
        # TODO: Show results so far here as well
        org_name = _user_info()["organizations"][0]["name"]

        project_url = f"{API_URL}/app/{urllib.parse.quote(org_name)}/p/{urllib.parse.quote(self.project.name)}"
        experiment_url = f"{project_url}/{urllib.parse.quote(self.name)}"

        print(f"See results for all experiments in {self.project.name} at {project_url}")
        print(f"See results for {self.name} at {experiment_url}")


def init(project, experiment=None, description=None, api_url=None):
    """
    Initialize a new experiment in a specified project. If the project does not exist, it will be created.

    :param project: The name of the project to create the experiment in.
    :param experiment: The name of the experiment to create. If not specified, a name will be generated automatically.
    :param description: An optional description of the experiment.
    :param api_url: The URL of the BrainTrust API to use. If not specified, the default will be used.
    :returns: The experiment object.
    """
    kwargs = {}
    if api_url:
        kwargs["api_url"] = api_url
    login(**kwargs)

    _state.current_project = Project(project)
    _state.current_experiment = Experiment(_state.current_project, name=experiment, description=description)
    return _state.current_experiment


def log(inputs, output, expected, scores, metadata=None):
    """
    Log a single event to the current experiment. The event will be batched and uploaded behind the scenes.

    :param inputs: The arguments that uniquely define a test case (an arbitrary, JSON serializable object). Later on,
    BrainTrust will use the `inputs` to know whether two test casess are the same between experiments, so they should
    not contain experiment-specific state. A simple rule of thumb is that if you run the same experiment twice, the
    `inputs` should be identical.
    :param output: The output of your application, including post-processing (an arbitrary, JSON serializable object),
    that allows you to determine whether the result is correct or not. For example, in an app that generates SQL queries,
    the `output` should be the _result_ of the SQL query generated by the model, not the query itself, because there may
    be multiple valid queries that answer a single question.
    :param expected: The ground truth value (an arbitrary, JSON serializable object) that you'd compare to `output` to
    determine if your `output` value is correct or not. BrainTrust currently does not compare `output` to `expected` for
    you, since there are so many different ways to do that correctly. Instead, these values are just used to help you
    navigate your experiments while digging into analyses. However, we may later use these values to re-score outputs or
    fine-tune your models.
    :param scores: A dictionary of numeric values (between 0 and 1) to log. The scores should give you a variety of signals
    that help you determine how accurate the outputs are compared to what you expect and diagnose failures. For example, a
    summarization app might have one score that tells you how accurate the summary is, and another that measures the word similarity
    between the generated and grouth truth summary. The word similarity score could help you determine whether the summarization was
    covering similar concepts or not. You can use these scores to help you sort, filter, and compare experiments.
    :param metadata: (Optional) a JSON-serializable object with additional data about the test example, model outputs, or just
    about anything else that's relevant, that you can use to help find and analyze examples later. For example, you could log the
    `prompt`, example's `id`, or anything else that would be useful to slice/dice later.
    :returns: The `id` of the logged event.
    """

    if not _state.current_experiment:
        raise Exception("Not initialized. Please call init() or login() first")

    return _state.current_experiment.log(
        inputs=inputs, output=output, expected=expected, scores=scores, metadata=metadata
    )


def login(api_url=os.environ.get("BRAINTRUST_API_URL", "https://www.braintrustdata.com")):
    """
    Login to BrainTrust. This will prompt you for your API token, which you can find at
    https://www.braintrustdata.com/app/token. This method is called automatically by `init()`.

    :param api_url: The URL of the BrainTrust API. Defaults to https://www.braintrustdata.com.
    """

    global API_URL, ORG_ID, LOG_URL

    API_URL = api_url

    os.makedirs(CACHE_PATH, exist_ok=True)

    api_info = None
    ping_ok = False
    if os.path.exists(API_INFO_PATH):
        with open(API_INFO_PATH) as f:
            api_info = json.load(f)

        LOG_URL = api_info.get("log_url")
        ORG_ID = api_info.get("org_id")
        conn = api_conn()

        token = api_info.get("token")
        if token is not None:
            conn.set_token(token)

        ping_resp = conn.get("ping")
        ping_ok = ping_resp.ok

    if not ping_ok and api_info and api_info.get("refresh_token"):
        resp = requests.post(
            _urljoin(API_URL, "/api/token/refresh"), json={"refresh_token": api_info.get("refresh_token")}
        )
        if resp.ok:
            resp_data = resp.json()
            token = resp_data["id_token"]
            refresh_token = resp_data.get("refresh_token")
            _save_api_info({**api_info, "token": token, "refresh_token": refresh_token})

            conn.set_token(token)
            ping_resp = conn.get("ping")
            ping_ok = ping_resp.ok
        else:
            _logger.warning(f"Failed to refresh token: [{resp.status_code}] {resp.text}")

    if not ping_ok:
        print(f"Please copy your API token from {API_URL}/app/token")
        temp_token = getpass("Token: ")

        resp = requests.post(_urljoin(API_URL, "/api/id-token"), json={"token": temp_token})
        assert resp.ok, f"Failed to acquire token: {resp.text}"
        info = resp.json()
        token, ORG_ID, LOG_URL = info["token"], info["org_info"][0]["id"], info["org_info"][0]["api_url"]

        _save_api_info(
            {"token": token, "org_id": ORG_ID, "log_url": LOG_URL, "refresh_token": info.get("refresh_token")}
        )

        conn = api_conn()
        conn.set_token(token)

    assert conn, "Conn should be set at this point (a bug)"
    resp = conn.get("ping")
    assert resp.ok, "Invalid token: " + resp.text


def _save_api_info(api_info):
    with open(API_INFO_PATH, "w") as f:
        json.dump(api_info, f)


def _urljoin(*parts):
    return "/".join([x.lstrip("/") for x in parts])


__all__ = ["init", "log", "login"]
