
def make_exe():
    dist = default_python_distribution()

    policy = dist.make_python_packaging_policy()
    # policy.allow_files = True
    # policy.bytecode_optimize_level_two = True
    # policy.file_scanner_classify_files = True
    # policy.resources_location_fallback = "filesystem-relative:lib"
    policy.resources_location_fallback = "filesystem-relative:prefix"

    python_config = dist.make_python_interpreter_config()
    python_config.filesystem_importer = True
    # python_config.sys_frozen = True
    python_config.run_module = "pfd"

    exe = dist.to_python_executable(
        name="pfd",
        packaging_policy=policy,
        config=python_config,
    )

    exe.add_python_resources(exe.pip_install(["-e", "."]))


    exe.add_python_resources(
        exe.read_package_root(
            path="./src",
            packages=["pfd"],
        )
    )

    return exe


def make_embedded_resources(exe):
    return exe.to_embedded_resources()


def make_install(exe):
    files = FileManifest()
    files.add_python_resource(".", exe)

    return files


def make_msi(exe):
    return exe.to_wix_msi_builder(
        "pfd",
        "pfd",
        "0.0",
        "PF Devs",
    )


def register_code_signers():
    if not VARS.get("ENABLE_CODE_SIGNING"):
        return

register_code_signers()

register_target("exe", make_exe)
register_target("resources", make_embedded_resources, depends=["exe"], default_build_script=True)
register_target("install", make_install, depends=["exe"], default=True)
register_target("msi_installer", make_msi, depends=["exe"])

resolve_targets()
