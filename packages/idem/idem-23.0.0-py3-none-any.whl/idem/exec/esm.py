from typing import Any
from typing import Dict


async def unlock(
    hub,
    provider: str,
    profile: str = "default",
    acct_data: Dict[str, Any] = None,
):
    """
    Remove the lock from the esm profile based on the provider and profile name.
    Generic example:

    .. code-block:: bash

        $ idem exec esm.unlock provider=[provider-name] <profile=[profile-name]>

    Specific example:

    .. code-block:: bash

        $ idem exec esm.unlock provider=aws profile=cloud-1
    """
    # Get the acct data from the kwargs and fallback to the acct_data in the current runtime
    if acct_data is None:
        acct_data = await hub.idem.acct.data(
            acct_key=hub.OPT.acct.get("acct_key"),
            acct_file=hub.OPT.acct.get("acct_file"),
            acct_blob=hub.OPT.acct.get("acct_blob"),
        )

    # Get the ESM ctx
    # copied from https://gitlab.com/vmware/idem/idem/-/blob/master/idem/idem/managed.py#L33
    ctx = await hub.idem.acct.ctx(
        f"esm.{provider}",
        profile=profile,
        acct_data=acct_data,
    )
    hub.log.info(f"Unlocking state run on provider {provider} using profile {profile}")
    try:
        await hub.esm[provider].exit_(ctx, None, None)
    except Exception as e:
        hub.log.error(f"{e.__class__.__name__}: {e}")
        return {
            "comment": [f"{e.__class__.__name__}: {e}"],
            "result": False,
            "ret": None,
        }
    hub.log.info("esm.unlock finished successfully")
    return {"result": True, "comment": "esm.unlock completed successfully", "ret": {}}


async def remove(
    hub,
    tag: str,
    provider: str = "local",
    profile: str = "default",
    acct_data: Dict[str, Any] = None,
    cache_dir: str = None,
    serial_plugin: str = "msgpack",
):
    """
    Removes the resource with the given 'tag' from the esm.
    Returns the removed element if found. Otherwise no-op. To find the exact tag use 'exec esm.show'.
    Default provider is local cache.
    Generic example:

    .. code-block:: bash

        $ idem exec esm.remove provider=[provider-name] tag=[tag-in-esm] <profile=[profile-name]>

    Specific example:

    .. code-block:: bash

        $ idem exec esm.remove tag="aws.iam.role_|-Create AWS IAM role ReadOnly01_|-ReadOnly01_|-"  provider=aws profile=cloud-1
    """
    # Get the acct data from the kwargs and fallback to the acct_data in the current runtime
    if acct_data is None:
        acct_data = await hub.idem.acct.data(
            acct_key=hub.OPT.acct.get("acct_key"),
            acct_file=hub.OPT.acct.get("acct_file"),
            acct_blob=hub.OPT.acct.get("acct_blob"),
        )

    # Get the ESM ctx
    # copied from https://gitlab.com/vmware/idem/idem/-/blob/master/idem/idem/managed.py#L33
    ctx = await hub.idem.acct.ctx(
        f"esm.{provider}",
        profile=profile,
        acct_data=acct_data,
    )

    # If no profile was specified then use the default profile
    if provider == "local" and not ctx.acct:
        hub.log.debug("Using the default local ESM profile")
        ctx = await hub.idem.acct.ctx(
            "esm.local",
            profile=None,
            acct_data={
                "profiles": {
                    "esm.local": {
                        None: {
                            "run_name": "cli",
                            "cache_dir": hub.OPT.idem.cache_dir
                            if cache_dir is None
                            else cache_dir,
                            "serial_plugin": serial_plugin,
                        }
                    }
                }
            },
        )

    # Enter the context of the Enforced State Manager
    # Do this outside of the try/except so that exceptions don't cause unintentional release of lock in exit
    try:
        handle = await hub.esm[provider].enter(ctx)
    except Exception as e:
        raise RuntimeError(
            f"Fail to enter enforced state management: {e.__class__.__name__}: {e}"
        )

    ret = {}
    try:
        state: Dict[str, Any] = await hub.esm[provider].get_state(ctx) or {}
        if tag in state:
            ret = state.pop(tag)
            comment = f"Removed resource with tag '{tag}' from ESM on provider '{provider}' using profile '{profile}'"
            hub.log.info(comment)
            print(comment)
            await hub.esm[provider].set_state(ctx, state)
        else:
            comment = f"Cannot find resource with tag '{tag}' in ESM on provider '{provider}' using profile '{profile}'"
            print(comment)
            hub.log.info(comment)
    finally:
        # Exit the context of the Enforced State Manager
        try:
            await hub.esm[provider].exit_(ctx, handle, None)
        except Exception as e:
            raise RuntimeError(
                f"Fail to exit enforced state management: {e.__class__.__name__}: {e}"
            )

    return {"result": True, "comment": f"{comment}", "ret": ret}


async def show(
    hub,
    provider: str = "local",
    profile: str = "default",
    acct_data: Dict[str, Any] = None,
    cache_dir: str = None,
    serial_plugin: str = "msgpack",
):
    """
    Displays the content of ESM. Default provider is local cache.
    Generic example:

    .. code-block:: bash

        $ idem exec esm.show provider=[provider-name] <profile=[profile-name]>

    Specific example:

    .. code-block:: bash

        $ idem exec esm.show provider=aws profile=cloud-1
    """
    # Get the ESM ctx
    ctx = await hub.idem.acct.ctx(
        f"esm.{provider}",
        profile=profile,
        acct_key=hub.OPT.acct.get("acct_key"),
        acct_file=hub.OPT.acct.get("acct_file"),
        acct_blob=hub.OPT.acct.get("acct_blob"),
        acct_data=acct_data,
    )

    # If no profile was specified then use the default profile
    if provider == "local" and not ctx.acct:
        hub.log.debug("Using the default local ESM profile")
        ctx = await hub.idem.acct.ctx(
            "esm.local",
            profile=None,
            acct_data={
                "profiles": {
                    "esm.local": {
                        None: {
                            "run_name": "cli",
                            "cache_dir": hub.OPT.idem.cache_dir
                            if cache_dir is None
                            else cache_dir,
                            "serial_plugin": serial_plugin,
                        }
                    }
                }
            },
        )

    # Enter the context of the Enforced State Manager
    # Do this outside of the try/except so that exceptions don't cause unintentional release of lock in exit
    try:
        handle = await hub.esm[provider].enter(ctx)
    except Exception as e:
        raise RuntimeError(
            f"Fail to enter enforced state management: {e.__class__.__name__}: {e}"
        )

    try:
        state: Dict[str, Any] = await hub.esm[provider].get_state(ctx) or {}
        for tag in state:
            print(f"{tag}: {state.get(tag)}")
    finally:
        # Exit the context of the Enforced State Manager
        try:
            await hub.esm[provider].exit_(ctx, handle, None)
        except Exception as e:
            raise RuntimeError(
                f"Fail to exit enforced state management: {e.__class__.__name__}: {e}"
            )

    return {"result": True, "comment": [], "ret": {}}


def version(hub):
    """
    Get the latest supported esm version from idem
    """
    return {
        "result": True,
        "comment": None,
        "ret": ".".join(str(x) for x in hub.esm.VERSION),
    }
