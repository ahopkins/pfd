import setuptools


def tag_version_scheme(version):
    return str(version.tag)


if __name__ == "__main__":
    setuptools.setup(
        use_scm_version={
            "version_scheme": tag_version_scheme,
            "local_scheme": "no-local-version",
        },
        setup_requires=["setuptools_scm"],
    )
