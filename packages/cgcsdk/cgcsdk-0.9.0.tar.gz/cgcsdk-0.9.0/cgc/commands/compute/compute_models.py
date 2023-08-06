from enum import Enum


class CGCEntityList(Enum):
    """Base class for other lists"""

    @classmethod
    def get_list(cls) -> list[str]:
        return [el.value for el in cls]


class EntityList(CGCEntityList):
    """List of templates in cgc-server

    :param Enum: name of template
    :type Enum: str
    """

    NVIDIA_TENSORFLOW = "nvidia-tensorflow"
    NVIDIA_RAPIDS = "nvidia-rapids"
    NVIDIA_PYTORCH = "nvidia-pytorch"
    NVIDIA_TRITON = "nvidia-triton"
    NGINX = "nginx"
    LABEL_STUDIO = "label-studio"


class DatabasesList(CGCEntityList):
    """List of templates in cgc-server

    :param Enum: name of template
    :type Enum: str
    """

    MONGODB = "mongodb"
    POSTGRESQL = "postgresql"
    REDIS = "redis"
    # MINIO = "minio"


class GPUsList(CGCEntityList):
    """List of templates in cgc-server

    :param Enum: name of template
    :type Enum: str
    """

    A100 = "A100"
    # V100 = "V100"
    A5000 = "A5000"
