import logging
import os

import h5py
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix

from implicit.datasets import _download

log = logging.getLogger("implicit")

"""
TODO:

 * host the file somewhere - probably will be too big to fit in github release storage
        *just put on GH releases? seems like will *just* fit

 * filter out '0' values from items/repos

"""

URL = "https://github.com/benfred/recommender_data/releases/download/v2.0/github_stars.hdf5"


def get_github_stars():
    """Returns the ghstars-dataset, downloading locally if necessary.
    Returns a tuple of (reponames, usernames, stars) where stars is a CSR matrix
    of reponame/userid"""

    filename = os.path.join(_download.LOCAL_CACHE_DIR, "github_stars.hdf5")
    if not os.path.isfile(filename):
        log.info("Downloading dataset to '%s'", filename)
        _download.download_file(URL, filename)
    else:
        log.info("Using cached dataset at '%s'", filename)

    with h5py.File(filename, "r") as f:
        m = f.get("stars")
        indices = m.get("indices")
        data = np.ones(indices.shape, dtype="float32")
        stars = csr_matrix((data, indices, m.get("indptr")))
        return (
            np.array(f["repo"].asstr(encoding="utf8")[:]),
            np.array(f["user"].asstr(encoding="utf8")[:]),
            stars,
        )


def _generate_dataset(input_path, output_filename):
    repos, users, stars = _convert_dataset(input_path)
    _write_hdf5(repos, users, stars, output_filename)


def _write_hdf5(repos, users, stars, output_filename):
    with h5py.File(output_filename, "w") as f:
        g = f.create_group("stars")
        g.create_dataset("indptr", data=stars.indptr)
        g.create_dataset("indices", data=stars.indices)

        dt = h5py.string_dtype(encoding="utf-8")
        dset = f.create_dataset("repo", (len(repos),), dtype=dt)
        dset[:] = [r or "" for r in repos]

        dset = f.create_dataset("user", (len(users),), dtype=dt)
        dset[:] = [u or "" for u in users]


def _convert_dataset(input_path):
    # you shouldn't have to run this yourself
    import cudf
    import nvtabular

    # TODO: host these parquet files publicly so others can use them
    stars = cudf.read_parquet(os.path.join(input_path, "stars.parquet"))

    # lets remap from github ids to low valued ids, and frequency cap too
    workflow = nvtabular.Workflow(
        ["repoid", "userid"]
        >> nvtabular.ops.Categorify(freq_threshold=2)
        >> nvtabular.ops.Filter(lambda df: df[(df.userid != 0) & (df.repoid != 0)])
    )
    transformed = workflow.fit_transform(nvtabular.Dataset(stars)).to_ddf().compute()
    items = transformed.repoid.values_host.astype("int32")
    users = transformed.userid.values_host.astype("int32")
    user_stars = coo_matrix((np.ones(users.shape[0], dtype="float32"), (users, items))).tocsr()

    repos = cudf.read_parquet(os.path.join(input_path, "repos.parquet"))
    repoids = cudf.read_parquet(".//categories/unique.repoid.parquet")
    repoids["embedding"] = repoids.index
    repos = cudf.merge(repoids, repos, on="repoid", how="left")
    repoids = None
    repo_names = np.empty(user_stars.shape[1], dtype="object")
    repo_names[repos.embedding.values_host] = repos.reponame.values_host
    repos = None

    users = cudf.read_parquet(os.path.join(input_path, "users.parquet"))
    userids = cudf.read_parquet(".//categories/unique.userid.parquet")
    userids["embedding"] = userids.index
    users = cudf.merge(userids, users, on="userid", how="left")
    userids = None
    user_logins = np.empty(user_stars.shape[0], dtype="object")
    user_logins[users.embedding.values_host] = users.userlogin.values_host
    users = None

    return repo_names, user_logins, user_stars


if __name__ == "__main__":
    _generate_dataset("/mnt/md0/data/ghstars/output", "github_stars.hdf5")
