# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_rpm.configuration import Configuration


class RpmModulemdResponse(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'pulp_href': 'str',
        'pulp_created': 'datetime',
        'md5': 'str',
        'sha1': 'str',
        'sha224': 'str',
        'sha256': 'str',
        'sha384': 'str',
        'sha512': 'str',
        'artifact': 'str',
        'name': 'str',
        'stream': 'str',
        'version': 'str',
        'static_context': 'bool',
        'context': 'str',
        'arch': 'str',
        'artifacts': 'object',
        'dependencies': 'object',
        'packages': 'list[str]'
    }

    attribute_map = {
        'pulp_href': 'pulp_href',
        'pulp_created': 'pulp_created',
        'md5': 'md5',
        'sha1': 'sha1',
        'sha224': 'sha224',
        'sha256': 'sha256',
        'sha384': 'sha384',
        'sha512': 'sha512',
        'artifact': 'artifact',
        'name': 'name',
        'stream': 'stream',
        'version': 'version',
        'static_context': 'static_context',
        'context': 'context',
        'arch': 'arch',
        'artifacts': 'artifacts',
        'dependencies': 'dependencies',
        'packages': 'packages'
    }

    def __init__(self, pulp_href=None, pulp_created=None, md5=None, sha1=None, sha224=None, sha256=None, sha384=None, sha512=None, artifact=None, name=None, stream=None, version=None, static_context=None, context=None, arch=None, artifacts=None, dependencies=None, packages=None, local_vars_configuration=None):  # noqa: E501
        """RpmModulemdResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pulp_href = None
        self._pulp_created = None
        self._md5 = None
        self._sha1 = None
        self._sha224 = None
        self._sha256 = None
        self._sha384 = None
        self._sha512 = None
        self._artifact = None
        self._name = None
        self._stream = None
        self._version = None
        self._static_context = None
        self._context = None
        self._arch = None
        self._artifacts = None
        self._dependencies = None
        self._packages = None
        self.discriminator = None

        if pulp_href is not None:
            self.pulp_href = pulp_href
        if pulp_created is not None:
            self.pulp_created = pulp_created
        if md5 is not None:
            self.md5 = md5
        if sha1 is not None:
            self.sha1 = sha1
        if sha224 is not None:
            self.sha224 = sha224
        if sha256 is not None:
            self.sha256 = sha256
        if sha384 is not None:
            self.sha384 = sha384
        if sha512 is not None:
            self.sha512 = sha512
        if artifact is not None:
            self.artifact = artifact
        self.name = name
        self.stream = stream
        self.version = version
        if static_context is not None:
            self.static_context = static_context
        self.context = context
        self.arch = arch
        self.artifacts = artifacts
        self.dependencies = dependencies
        if packages is not None:
            self.packages = packages

    @property
    def pulp_href(self):
        """Gets the pulp_href of this RpmModulemdResponse.  # noqa: E501


        :return: The pulp_href of this RpmModulemdResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp_href

    @pulp_href.setter
    def pulp_href(self, pulp_href):
        """Sets the pulp_href of this RpmModulemdResponse.


        :param pulp_href: The pulp_href of this RpmModulemdResponse.  # noqa: E501
        :type: str
        """

        self._pulp_href = pulp_href

    @property
    def pulp_created(self):
        """Gets the pulp_created of this RpmModulemdResponse.  # noqa: E501

        Timestamp of creation.  # noqa: E501

        :return: The pulp_created of this RpmModulemdResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._pulp_created

    @pulp_created.setter
    def pulp_created(self, pulp_created):
        """Sets the pulp_created of this RpmModulemdResponse.

        Timestamp of creation.  # noqa: E501

        :param pulp_created: The pulp_created of this RpmModulemdResponse.  # noqa: E501
        :type: datetime
        """

        self._pulp_created = pulp_created

    @property
    def md5(self):
        """Gets the md5 of this RpmModulemdResponse.  # noqa: E501

        The MD5 checksum if available.  # noqa: E501

        :return: The md5 of this RpmModulemdResponse.  # noqa: E501
        :rtype: str
        """
        return self._md5

    @md5.setter
    def md5(self, md5):
        """Sets the md5 of this RpmModulemdResponse.

        The MD5 checksum if available.  # noqa: E501

        :param md5: The md5 of this RpmModulemdResponse.  # noqa: E501
        :type: str
        """

        self._md5 = md5

    @property
    def sha1(self):
        """Gets the sha1 of this RpmModulemdResponse.  # noqa: E501

        The SHA-1 checksum if available.  # noqa: E501

        :return: The sha1 of this RpmModulemdResponse.  # noqa: E501
        :rtype: str
        """
        return self._sha1

    @sha1.setter
    def sha1(self, sha1):
        """Sets the sha1 of this RpmModulemdResponse.

        The SHA-1 checksum if available.  # noqa: E501

        :param sha1: The sha1 of this RpmModulemdResponse.  # noqa: E501
        :type: str
        """

        self._sha1 = sha1

    @property
    def sha224(self):
        """Gets the sha224 of this RpmModulemdResponse.  # noqa: E501

        The SHA-224 checksum if available.  # noqa: E501

        :return: The sha224 of this RpmModulemdResponse.  # noqa: E501
        :rtype: str
        """
        return self._sha224

    @sha224.setter
    def sha224(self, sha224):
        """Sets the sha224 of this RpmModulemdResponse.

        The SHA-224 checksum if available.  # noqa: E501

        :param sha224: The sha224 of this RpmModulemdResponse.  # noqa: E501
        :type: str
        """

        self._sha224 = sha224

    @property
    def sha256(self):
        """Gets the sha256 of this RpmModulemdResponse.  # noqa: E501

        The SHA-256 checksum if available.  # noqa: E501

        :return: The sha256 of this RpmModulemdResponse.  # noqa: E501
        :rtype: str
        """
        return self._sha256

    @sha256.setter
    def sha256(self, sha256):
        """Sets the sha256 of this RpmModulemdResponse.

        The SHA-256 checksum if available.  # noqa: E501

        :param sha256: The sha256 of this RpmModulemdResponse.  # noqa: E501
        :type: str
        """

        self._sha256 = sha256

    @property
    def sha384(self):
        """Gets the sha384 of this RpmModulemdResponse.  # noqa: E501

        The SHA-384 checksum if available.  # noqa: E501

        :return: The sha384 of this RpmModulemdResponse.  # noqa: E501
        :rtype: str
        """
        return self._sha384

    @sha384.setter
    def sha384(self, sha384):
        """Sets the sha384 of this RpmModulemdResponse.

        The SHA-384 checksum if available.  # noqa: E501

        :param sha384: The sha384 of this RpmModulemdResponse.  # noqa: E501
        :type: str
        """

        self._sha384 = sha384

    @property
    def sha512(self):
        """Gets the sha512 of this RpmModulemdResponse.  # noqa: E501

        The SHA-512 checksum if available.  # noqa: E501

        :return: The sha512 of this RpmModulemdResponse.  # noqa: E501
        :rtype: str
        """
        return self._sha512

    @sha512.setter
    def sha512(self, sha512):
        """Sets the sha512 of this RpmModulemdResponse.

        The SHA-512 checksum if available.  # noqa: E501

        :param sha512: The sha512 of this RpmModulemdResponse.  # noqa: E501
        :type: str
        """

        self._sha512 = sha512

    @property
    def artifact(self):
        """Gets the artifact of this RpmModulemdResponse.  # noqa: E501

        Artifact file representing the physical content  # noqa: E501

        :return: The artifact of this RpmModulemdResponse.  # noqa: E501
        :rtype: str
        """
        return self._artifact

    @artifact.setter
    def artifact(self, artifact):
        """Sets the artifact of this RpmModulemdResponse.

        Artifact file representing the physical content  # noqa: E501

        :param artifact: The artifact of this RpmModulemdResponse.  # noqa: E501
        :type: str
        """

        self._artifact = artifact

    @property
    def name(self):
        """Gets the name of this RpmModulemdResponse.  # noqa: E501

        Modulemd name.  # noqa: E501

        :return: The name of this RpmModulemdResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this RpmModulemdResponse.

        Modulemd name.  # noqa: E501

        :param name: The name of this RpmModulemdResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def stream(self):
        """Gets the stream of this RpmModulemdResponse.  # noqa: E501

        Stream name.  # noqa: E501

        :return: The stream of this RpmModulemdResponse.  # noqa: E501
        :rtype: str
        """
        return self._stream

    @stream.setter
    def stream(self, stream):
        """Sets the stream of this RpmModulemdResponse.

        Stream name.  # noqa: E501

        :param stream: The stream of this RpmModulemdResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and stream is None:  # noqa: E501
            raise ValueError("Invalid value for `stream`, must not be `None`")  # noqa: E501

        self._stream = stream

    @property
    def version(self):
        """Gets the version of this RpmModulemdResponse.  # noqa: E501

        Modulemd version.  # noqa: E501

        :return: The version of this RpmModulemdResponse.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this RpmModulemdResponse.

        Modulemd version.  # noqa: E501

        :param version: The version of this RpmModulemdResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and version is None:  # noqa: E501
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def static_context(self):
        """Gets the static_context of this RpmModulemdResponse.  # noqa: E501

        Modulemd static-context flag.  # noqa: E501

        :return: The static_context of this RpmModulemdResponse.  # noqa: E501
        :rtype: bool
        """
        return self._static_context

    @static_context.setter
    def static_context(self, static_context):
        """Sets the static_context of this RpmModulemdResponse.

        Modulemd static-context flag.  # noqa: E501

        :param static_context: The static_context of this RpmModulemdResponse.  # noqa: E501
        :type: bool
        """

        self._static_context = static_context

    @property
    def context(self):
        """Gets the context of this RpmModulemdResponse.  # noqa: E501

        Modulemd context.  # noqa: E501

        :return: The context of this RpmModulemdResponse.  # noqa: E501
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context):
        """Sets the context of this RpmModulemdResponse.

        Modulemd context.  # noqa: E501

        :param context: The context of this RpmModulemdResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and context is None:  # noqa: E501
            raise ValueError("Invalid value for `context`, must not be `None`")  # noqa: E501

        self._context = context

    @property
    def arch(self):
        """Gets the arch of this RpmModulemdResponse.  # noqa: E501

        Modulemd architecture.  # noqa: E501

        :return: The arch of this RpmModulemdResponse.  # noqa: E501
        :rtype: str
        """
        return self._arch

    @arch.setter
    def arch(self, arch):
        """Sets the arch of this RpmModulemdResponse.

        Modulemd architecture.  # noqa: E501

        :param arch: The arch of this RpmModulemdResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and arch is None:  # noqa: E501
            raise ValueError("Invalid value for `arch`, must not be `None`")  # noqa: E501

        self._arch = arch

    @property
    def artifacts(self):
        """Gets the artifacts of this RpmModulemdResponse.  # noqa: E501

        Modulemd artifacts.  # noqa: E501

        :return: The artifacts of this RpmModulemdResponse.  # noqa: E501
        :rtype: object
        """
        return self._artifacts

    @artifacts.setter
    def artifacts(self, artifacts):
        """Sets the artifacts of this RpmModulemdResponse.

        Modulemd artifacts.  # noqa: E501

        :param artifacts: The artifacts of this RpmModulemdResponse.  # noqa: E501
        :type: object
        """

        self._artifacts = artifacts

    @property
    def dependencies(self):
        """Gets the dependencies of this RpmModulemdResponse.  # noqa: E501

        Modulemd dependencies.  # noqa: E501

        :return: The dependencies of this RpmModulemdResponse.  # noqa: E501
        :rtype: object
        """
        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies):
        """Sets the dependencies of this RpmModulemdResponse.

        Modulemd dependencies.  # noqa: E501

        :param dependencies: The dependencies of this RpmModulemdResponse.  # noqa: E501
        :type: object
        """

        self._dependencies = dependencies

    @property
    def packages(self):
        """Gets the packages of this RpmModulemdResponse.  # noqa: E501

        Modulemd artifacts' packages.  # noqa: E501

        :return: The packages of this RpmModulemdResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._packages

    @packages.setter
    def packages(self, packages):
        """Sets the packages of this RpmModulemdResponse.

        Modulemd artifacts' packages.  # noqa: E501

        :param packages: The packages of this RpmModulemdResponse.  # noqa: E501
        :type: list[str]
        """

        self._packages = packages

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RpmModulemdResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RpmModulemdResponse):
            return True

        return self.to_dict() != other.to_dict()
