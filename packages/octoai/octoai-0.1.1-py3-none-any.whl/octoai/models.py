"""OctoAI models."""

from abc import ABC, abstractproperty
from typing import Any, Mapping

from octoai.client import Client


class Model(ABC):
    """Base class representing an endpoint serving inferences.

    :param ABC: Abstract class
    :type ABC: :class:`ABC`
    """

    def __init__(self, client: Client):
        self._client = client

    @property
    def endpoint_url(self) -> str:
        """Return the url of an endpoint.

        :return: endpoint url with /predict at the end
        :rtype: str
        """
        if not self._client.public_endpoints:
            self._client._initialize_public_endpoints()
        return self._client.public_endpoints[self.name]

    @abstractproperty
    def name(self) -> str:
        """Return the name of the model.

        :return: name
        :rtype: str
        """
        ...

    def infer(self, inputs: Mapping[str, Any]) -> Mapping[str, Any]:
        """Infers from an endpoint with inputs as request body.

        :param inputs: necessary inputs plus customization to run an inference
        :type inputs: Mapping[str, Any]
        :return: outputs from the model, may include text, base64 image or audio, etc.
        :rtype: Mapping[str, Any]
        """
        return self._client.infer(self.endpoint_url, inputs=inputs)


class StableDiffusion(Model):
    """Class that point to pre-optimized text2image generation model.

    :param Model: Model base class.
    :type Model: :class:`Model`
    :return: StableDiffusion wrapper for :class:`Model`
    :rtype: :class:`StableDiffusion`
    """

    # TODO COV-564 finalize names of models with Clownfish team
    @property
    def name(self) -> str:
        """Return the Stable Diffusion name.

        :return: name on API.
        :rtype: str
        """
        return "stable-diffusion-demo"


class Dolly(Model):
    """Class that points to a pre-optimized text2text generation model.

    :param Model: Model base class.
    :type Model: :class:`Model`
    :return: Dolly wrapper for :class:`Model`
    :rtype: :class:`Dolly`
    """

    # TODO COV-564 finalize names of models with Clownfish team
    @property
    def name(self) -> str:
        """Return the Dolly name.

        :return: name on API.
        :rtype: str
        """
        return "dolly-demo"


class Whisper(Model):
    """Class that points to pre-optimized speech recognition model.

    :param Model: Model base class.
    :type Model: :class:`Model`
    :return: Whisper wrapper for :class:`Model`
    :rtype: :class:`Whisper`
    """

    # TODO COV-564 finalize names of models with Clownfish team
    @property
    def name(self) -> str:
        """Return the Whisper name.

        :return: name on API.
        :rtype: str
        """
        return "whisper-demo"
