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


class RpmRpmRepositoryResponse(object):
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
        'versions_href': 'str',
        'pulp_labels': 'object',
        'latest_version_href': 'str',
        'name': 'str',
        'description': 'str',
        'retained_versions': 'int',
        'remote': 'str',
        'autopublish': 'bool',
        'metadata_signing_service': 'str',
        'retain_package_versions': 'int',
        'metadata_checksum_type': 'OneOfMetadataChecksumTypeEnumNullEnum',
        'package_checksum_type': 'OneOfPackageChecksumTypeEnumNullEnum',
        'gpgcheck': 'int',
        'repo_gpgcheck': 'int',
        'sqlite_metadata': 'bool'
    }

    attribute_map = {
        'pulp_href': 'pulp_href',
        'pulp_created': 'pulp_created',
        'versions_href': 'versions_href',
        'pulp_labels': 'pulp_labels',
        'latest_version_href': 'latest_version_href',
        'name': 'name',
        'description': 'description',
        'retained_versions': 'retained_versions',
        'remote': 'remote',
        'autopublish': 'autopublish',
        'metadata_signing_service': 'metadata_signing_service',
        'retain_package_versions': 'retain_package_versions',
        'metadata_checksum_type': 'metadata_checksum_type',
        'package_checksum_type': 'package_checksum_type',
        'gpgcheck': 'gpgcheck',
        'repo_gpgcheck': 'repo_gpgcheck',
        'sqlite_metadata': 'sqlite_metadata'
    }

    def __init__(self, pulp_href=None, pulp_created=None, versions_href=None, pulp_labels=None, latest_version_href=None, name=None, description=None, retained_versions=None, remote=None, autopublish=False, metadata_signing_service=None, retain_package_versions=None, metadata_checksum_type=None, package_checksum_type=None, gpgcheck=0, repo_gpgcheck=0, sqlite_metadata=False, local_vars_configuration=None):  # noqa: E501
        """RpmRpmRepositoryResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pulp_href = None
        self._pulp_created = None
        self._versions_href = None
        self._pulp_labels = None
        self._latest_version_href = None
        self._name = None
        self._description = None
        self._retained_versions = None
        self._remote = None
        self._autopublish = None
        self._metadata_signing_service = None
        self._retain_package_versions = None
        self._metadata_checksum_type = None
        self._package_checksum_type = None
        self._gpgcheck = None
        self._repo_gpgcheck = None
        self._sqlite_metadata = None
        self.discriminator = None

        if pulp_href is not None:
            self.pulp_href = pulp_href
        if pulp_created is not None:
            self.pulp_created = pulp_created
        if versions_href is not None:
            self.versions_href = versions_href
        if pulp_labels is not None:
            self.pulp_labels = pulp_labels
        if latest_version_href is not None:
            self.latest_version_href = latest_version_href
        self.name = name
        self.description = description
        self.retained_versions = retained_versions
        self.remote = remote
        if autopublish is not None:
            self.autopublish = autopublish
        self.metadata_signing_service = metadata_signing_service
        if retain_package_versions is not None:
            self.retain_package_versions = retain_package_versions
        self.metadata_checksum_type = metadata_checksum_type
        self.package_checksum_type = package_checksum_type
        if gpgcheck is not None:
            self.gpgcheck = gpgcheck
        if repo_gpgcheck is not None:
            self.repo_gpgcheck = repo_gpgcheck
        if sqlite_metadata is not None:
            self.sqlite_metadata = sqlite_metadata

    @property
    def pulp_href(self):
        """Gets the pulp_href of this RpmRpmRepositoryResponse.  # noqa: E501


        :return: The pulp_href of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp_href

    @pulp_href.setter
    def pulp_href(self, pulp_href):
        """Sets the pulp_href of this RpmRpmRepositoryResponse.


        :param pulp_href: The pulp_href of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: str
        """

        self._pulp_href = pulp_href

    @property
    def pulp_created(self):
        """Gets the pulp_created of this RpmRpmRepositoryResponse.  # noqa: E501

        Timestamp of creation.  # noqa: E501

        :return: The pulp_created of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._pulp_created

    @pulp_created.setter
    def pulp_created(self, pulp_created):
        """Sets the pulp_created of this RpmRpmRepositoryResponse.

        Timestamp of creation.  # noqa: E501

        :param pulp_created: The pulp_created of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: datetime
        """

        self._pulp_created = pulp_created

    @property
    def versions_href(self):
        """Gets the versions_href of this RpmRpmRepositoryResponse.  # noqa: E501


        :return: The versions_href of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._versions_href

    @versions_href.setter
    def versions_href(self, versions_href):
        """Sets the versions_href of this RpmRpmRepositoryResponse.


        :param versions_href: The versions_href of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: str
        """

        self._versions_href = versions_href

    @property
    def pulp_labels(self):
        """Gets the pulp_labels of this RpmRpmRepositoryResponse.  # noqa: E501


        :return: The pulp_labels of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: object
        """
        return self._pulp_labels

    @pulp_labels.setter
    def pulp_labels(self, pulp_labels):
        """Sets the pulp_labels of this RpmRpmRepositoryResponse.


        :param pulp_labels: The pulp_labels of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: object
        """

        self._pulp_labels = pulp_labels

    @property
    def latest_version_href(self):
        """Gets the latest_version_href of this RpmRpmRepositoryResponse.  # noqa: E501


        :return: The latest_version_href of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._latest_version_href

    @latest_version_href.setter
    def latest_version_href(self, latest_version_href):
        """Sets the latest_version_href of this RpmRpmRepositoryResponse.


        :param latest_version_href: The latest_version_href of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: str
        """

        self._latest_version_href = latest_version_href

    @property
    def name(self):
        """Gets the name of this RpmRpmRepositoryResponse.  # noqa: E501

        A unique name for this repository.  # noqa: E501

        :return: The name of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this RpmRpmRepositoryResponse.

        A unique name for this repository.  # noqa: E501

        :param name: The name of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this RpmRpmRepositoryResponse.  # noqa: E501

        An optional description.  # noqa: E501

        :return: The description of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this RpmRpmRepositoryResponse.

        An optional description.  # noqa: E501

        :param description: The description of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def retained_versions(self):
        """Gets the retained_versions of this RpmRpmRepositoryResponse.  # noqa: E501

        Retain X versions of the repository. Default is null which retains all versions. This is provided as a tech preview in Pulp 3 and may change in the future.  # noqa: E501

        :return: The retained_versions of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: int
        """
        return self._retained_versions

    @retained_versions.setter
    def retained_versions(self, retained_versions):
        """Sets the retained_versions of this RpmRpmRepositoryResponse.

        Retain X versions of the repository. Default is null which retains all versions. This is provided as a tech preview in Pulp 3 and may change in the future.  # noqa: E501

        :param retained_versions: The retained_versions of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                retained_versions is not None and retained_versions < 1):  # noqa: E501
            raise ValueError("Invalid value for `retained_versions`, must be a value greater than or equal to `1`")  # noqa: E501

        self._retained_versions = retained_versions

    @property
    def remote(self):
        """Gets the remote of this RpmRpmRepositoryResponse.  # noqa: E501


        :return: The remote of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._remote

    @remote.setter
    def remote(self, remote):
        """Sets the remote of this RpmRpmRepositoryResponse.


        :param remote: The remote of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: str
        """

        self._remote = remote

    @property
    def autopublish(self):
        """Gets the autopublish of this RpmRpmRepositoryResponse.  # noqa: E501

        Whether to automatically create publications for new repository versions, and update any distributions pointing to this repository.  # noqa: E501

        :return: The autopublish of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: bool
        """
        return self._autopublish

    @autopublish.setter
    def autopublish(self, autopublish):
        """Sets the autopublish of this RpmRpmRepositoryResponse.

        Whether to automatically create publications for new repository versions, and update any distributions pointing to this repository.  # noqa: E501

        :param autopublish: The autopublish of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: bool
        """

        self._autopublish = autopublish

    @property
    def metadata_signing_service(self):
        """Gets the metadata_signing_service of this RpmRpmRepositoryResponse.  # noqa: E501

        A reference to an associated signing service.  # noqa: E501

        :return: The metadata_signing_service of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._metadata_signing_service

    @metadata_signing_service.setter
    def metadata_signing_service(self, metadata_signing_service):
        """Sets the metadata_signing_service of this RpmRpmRepositoryResponse.

        A reference to an associated signing service.  # noqa: E501

        :param metadata_signing_service: The metadata_signing_service of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: str
        """

        self._metadata_signing_service = metadata_signing_service

    @property
    def retain_package_versions(self):
        """Gets the retain_package_versions of this RpmRpmRepositoryResponse.  # noqa: E501

        The number of versions of each package to keep in the repository; older versions will be purged. The default is '0', which will disable this feature and keep all versions of each package.  # noqa: E501

        :return: The retain_package_versions of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: int
        """
        return self._retain_package_versions

    @retain_package_versions.setter
    def retain_package_versions(self, retain_package_versions):
        """Sets the retain_package_versions of this RpmRpmRepositoryResponse.

        The number of versions of each package to keep in the repository; older versions will be purged. The default is '0', which will disable this feature and keep all versions of each package.  # noqa: E501

        :param retain_package_versions: The retain_package_versions of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                retain_package_versions is not None and retain_package_versions < 0):  # noqa: E501
            raise ValueError("Invalid value for `retain_package_versions`, must be a value greater than or equal to `0`")  # noqa: E501

        self._retain_package_versions = retain_package_versions

    @property
    def metadata_checksum_type(self):
        """Gets the metadata_checksum_type of this RpmRpmRepositoryResponse.  # noqa: E501

        The checksum type for metadata.  # noqa: E501

        :return: The metadata_checksum_type of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: OneOfMetadataChecksumTypeEnumNullEnum
        """
        return self._metadata_checksum_type

    @metadata_checksum_type.setter
    def metadata_checksum_type(self, metadata_checksum_type):
        """Sets the metadata_checksum_type of this RpmRpmRepositoryResponse.

        The checksum type for metadata.  # noqa: E501

        :param metadata_checksum_type: The metadata_checksum_type of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: OneOfMetadataChecksumTypeEnumNullEnum
        """

        self._metadata_checksum_type = metadata_checksum_type

    @property
    def package_checksum_type(self):
        """Gets the package_checksum_type of this RpmRpmRepositoryResponse.  # noqa: E501

        The checksum type for packages.  # noqa: E501

        :return: The package_checksum_type of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: OneOfPackageChecksumTypeEnumNullEnum
        """
        return self._package_checksum_type

    @package_checksum_type.setter
    def package_checksum_type(self, package_checksum_type):
        """Sets the package_checksum_type of this RpmRpmRepositoryResponse.

        The checksum type for packages.  # noqa: E501

        :param package_checksum_type: The package_checksum_type of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: OneOfPackageChecksumTypeEnumNullEnum
        """

        self._package_checksum_type = package_checksum_type

    @property
    def gpgcheck(self):
        """Gets the gpgcheck of this RpmRpmRepositoryResponse.  # noqa: E501

        An option specifying whether a client should perform a GPG signature check on packages.  # noqa: E501

        :return: The gpgcheck of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: int
        """
        return self._gpgcheck

    @gpgcheck.setter
    def gpgcheck(self, gpgcheck):
        """Sets the gpgcheck of this RpmRpmRepositoryResponse.

        An option specifying whether a client should perform a GPG signature check on packages.  # noqa: E501

        :param gpgcheck: The gpgcheck of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                gpgcheck is not None and gpgcheck > 1):  # noqa: E501
            raise ValueError("Invalid value for `gpgcheck`, must be a value less than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                gpgcheck is not None and gpgcheck < 0):  # noqa: E501
            raise ValueError("Invalid value for `gpgcheck`, must be a value greater than or equal to `0`")  # noqa: E501

        self._gpgcheck = gpgcheck

    @property
    def repo_gpgcheck(self):
        """Gets the repo_gpgcheck of this RpmRpmRepositoryResponse.  # noqa: E501

        An option specifying whether a client should perform a GPG signature check on the repodata.  # noqa: E501

        :return: The repo_gpgcheck of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: int
        """
        return self._repo_gpgcheck

    @repo_gpgcheck.setter
    def repo_gpgcheck(self, repo_gpgcheck):
        """Sets the repo_gpgcheck of this RpmRpmRepositoryResponse.

        An option specifying whether a client should perform a GPG signature check on the repodata.  # noqa: E501

        :param repo_gpgcheck: The repo_gpgcheck of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                repo_gpgcheck is not None and repo_gpgcheck > 1):  # noqa: E501
            raise ValueError("Invalid value for `repo_gpgcheck`, must be a value less than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                repo_gpgcheck is not None and repo_gpgcheck < 0):  # noqa: E501
            raise ValueError("Invalid value for `repo_gpgcheck`, must be a value greater than or equal to `0`")  # noqa: E501

        self._repo_gpgcheck = repo_gpgcheck

    @property
    def sqlite_metadata(self):
        """Gets the sqlite_metadata of this RpmRpmRepositoryResponse.  # noqa: E501

        An option specifying whether Pulp should generate SQLite metadata.  # noqa: E501

        :return: The sqlite_metadata of this RpmRpmRepositoryResponse.  # noqa: E501
        :rtype: bool
        """
        return self._sqlite_metadata

    @sqlite_metadata.setter
    def sqlite_metadata(self, sqlite_metadata):
        """Sets the sqlite_metadata of this RpmRpmRepositoryResponse.

        An option specifying whether Pulp should generate SQLite metadata.  # noqa: E501

        :param sqlite_metadata: The sqlite_metadata of this RpmRpmRepositoryResponse.  # noqa: E501
        :type: bool
        """

        self._sqlite_metadata = sqlite_metadata

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
        if not isinstance(other, RpmRpmRepositoryResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RpmRpmRepositoryResponse):
            return True

        return self.to_dict() != other.to_dict()
