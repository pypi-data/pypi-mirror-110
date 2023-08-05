# HEA Server Data Adapters Microservice
[Research Informatics Shared Resource](https://risr.hci.utah.edu), [Huntsman Cancer Institute](https://hci.utah.edu), 
Salt Lake City, UT

The HEA Data Adapters Microservice provides access to data files and databases.

## Version 1
Initial release.

## Runtime requirements
* Python 3.8

## Build requirements
* Python 3.8 and the following packages (install using pip)
    * pytest 3.5.3 or greater
    * twine 3.1.1 or greater
    * wheel 0.34.2 or greater
* Any development environment is fine.
* On Windows, you also will need:
    * Build Tools for Visual Studio 2019, found at https://visualstudio.microsoft.com/downloads/. Select the C++ tools.
    * git, found at https://git-scm.com/download/win.
* On Mac, Xcode or the command line developer tools is required, found in the Apple Store app.

## Development notes

### Creating your development environment
From the project's root directory, run `pip install -e .`. Do NOT run `python setup.py develop`. It will break your
environment. You alternatively can run `pip install .`, but you will need to rerun this command after any code changes
before you run unit tests.

### Running unit tests
Run tests with the `pytest` command.

### Versioning
Use semantic versioning as described in 
https://packaging.python.org/guides/distributing-packages-using-setuptools/#choosing-a-versioning-scheme. In addition,
while development is underway, the version should be the next version number suffixed by -SNAPSHOT.

### Version tags in git
Version tags should follow the format `heaserver-data-adapters-<version>`, for example, `heaserver-data-adapters-1.0.0`.

### Uploading to an index server
You will need a custom index server such as devpi to upload HEA component releases so that HEA
components can depend on each other. You will need to configure pip to use the custom index server
instead of the usual Pypi.

The following instructions assume separate stable and staging indexes. Numbered releases, including alphas and betas, go 
into the stable index. Snapshots of works in progress go into the staging index. Artifacts uploaded to the
staging index can be overwritten. Artifacts uploaded to stable cannot. Thus, also use staging to upload numbered
releases, verify the uploaded packages, and then upload to stable.

From the project's root directory:
1. For numbered releases, remove .dev from the version number in setup.py, tag it in git to indicate a release, 
and commit to version control. Skip this step for dev releases.
2. Run `python setup.py clean --all sdist bdist_wheel` to create the artifacts.
3. Run `twine upload -r <repository> dist/*` to upload to the repository. The repository name has to be defined in a
twine configuration file such as `$HOME/.pypirc`.
4. For numbered releases, increment the version number in setup.py, append .dev to it, and commit to version 
control. Skip this step for dev releases.
