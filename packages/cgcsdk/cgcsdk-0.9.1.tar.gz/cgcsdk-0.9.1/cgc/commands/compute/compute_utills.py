def list_get_mounted_volumes(volume_list: list) -> str:
    """Formats and returns list of PVC volumes mounted to an app.

    :param volume_list: list of all volumes mounted to an app
    :type volume_list: list
    :return: list of PVC volumes
    :rtype: str
    """
    volume_name_list = []
    for volume in volume_list:
        volume_type = volume.get("type")
        if volume_type == "PVC":
            volume_name = volume.get("name")
            volume_name_list.append(volume_name)
    volumes_mounted = (
        ", ".join(volume_name_list) if len(volume_name_list) != 0 else None
    )
    return volumes_mounted


def get_app_list(pod_list: list, detailed: bool) -> list:
    """Formats and returns list of apps to print.

    :param pod_list: list of pods
    :type pod_list: list
    :return: formatted list of apps
    :rtype: list
    """
    output_data = []

    for pod in pod_list:
        try:
            main_container_name = pod["labels"]["entity"]
            try:
                main_container = [
                    x for x in pod["containers"] if x["name"] == main_container_name
                ][0]
            except IndexError:
                raise Exception(
                    "Parser was unable to find main container in server output in container list"
                )
            volumes_mounted = list_get_mounted_volumes(main_container["mounts"])
            limits = main_container["resources"].get("limits")
            cpu = limits.get("cpu") if limits is not None else 0
            ram = limits.get("memory") if limits is not None else "0Gi"

            pod_data = {
                "name": pod["labels"]["app-name"],
                "type": pod["labels"]["entity"],
                "status": pod["status"],
                "volumes_mounted": volumes_mounted,
                "cpu": cpu,
                "ram": ram,
            }
            # getting rid of unwanted and used values
            if "pod-template-hash" in pod["labels"].keys():
                pod["labels"].pop("pod-template-hash")
            pod["labels"].pop("app-name")
            pod["labels"].pop("entity")
            if detailed:
                pod["labels"]["url"] = pod["labels"]["pod_url"]
                if pod_data["type"] != "filebrowser":
                    pod["labels"]["url"] += f"""/?token={pod["labels"]['app-token']}"""
            else:
                pod["labels"]["url"] = pod["labels"]["pod_url"]
                pod["labels"].pop("app-token")
            pod["labels"].pop("pod_url")

            # appending the rest of labels
            pod_data.update(pod["labels"])
            output_data.append(pod_data)
        except KeyError:
            pass

    return output_data


def compute_create_payload(
    name, entity, cpu, memory, volumes: list, gpu: int = 0, gpu_type: str = None
):
    """
    Create payload for app creation.
    """

    payload = {
        "name": name,
        "entity": entity,
        "cpu": cpu,
        "gpu": gpu,
        "memory": memory,
        "gpu_type": gpu_type,
    }
    try:
        if len(volumes) != 0:
            payload["pv_volume"] = volumes
    except TypeError:
        pass
    return payload


def compute_delete_payload(name):
    """
    Create payload for app creation.
    """
    payload = {
        "name": name,
    }
    return payload
