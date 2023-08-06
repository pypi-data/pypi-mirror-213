# Copyright 2023 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""This module represents resources.

Most of the resources support all CRUD methods.
"""
import collections
import contextlib
import http
import json
import time
import typing

import inflection
import pydantic.utils
import semver

import igz_mgmt.client
import igz_mgmt.common.helpers
import igz_mgmt.constants
import igz_mgmt.cruds
import igz_mgmt.exceptions
import igz_mgmt.schemas.app_services


class BaseResource(pydantic.BaseModel):
    """Base resource contains common attributes and methods for resources in the system."""

    type: str
    id: typing.Optional[typing.Union[int, str]]
    relationships: typing.Optional[dict]

    class Config:
        class _BaseGetter(pydantic.utils.GetterDict):
            def get(self, key: typing.Any, default: typing.Any = None) -> typing.Any:
                if key in ["id", "type"]:
                    return self._obj["data"][key]
                elif key == "relationships":
                    return self._obj["data"].get("relationships", {})
                elif key in self._obj["data"]["attributes"]:
                    return self._obj["data"]["attributes"][key]
                return default

        orm_mode = True
        use_enum_values = True
        underscore_attrs_are_private = True
        getter_dict = _BaseGetter

        # be forward compatible
        extra = "allow"

    @classmethod
    def get(
        cls,
        http_client: igz_mgmt.client.APIClient,
        resource_id: typing.Union[int, str],
        include: typing.Optional[typing.List[str]] = None,
    ) -> "BaseResource":
        """Gets the resource record.

        Args:
            http_client (APIClient): The client to use.
            resource_id (int or str): Record id.
            include (typing.List[str], optional): Include related resources. None by default.

        Returns:
            BaseResource: The resource record.
        """
        params = {}
        if include:
            params["include"] = ",".join(include)
        resource = cls._get_crud().get(http_client, resource_id, params=params)
        return cls.from_orm(resource)

    @classmethod
    def list(
        cls,
        http_client: igz_mgmt.client.APIClient,
        filter_by: typing.Optional[typing.Mapping[str, str]] = None,
        sort_by: typing.Optional[typing.List[str]] = None,
        paging: typing.Optional[igz_mgmt.cruds.ResourceListPagingQueryParams] = None,
        include: typing.Optional[typing.List[str]] = None,
    ) -> typing.List["BaseResource"]:
        """Lists resource records.

        Args:
            http_client (APIClient): The client to use.
            filter_by (typing.Mapping[str, str], optional): Filter by field values. None by default.
            sort_by (typing.List[str], optional): Sort by field names. None by default.
            paging (ResourceListPagingQueryParams, optional): Allow to paginate resource by given records size.
            None by default.
            include (typing.List[str], optional): Include related resources. None by default.

        Returns:
            typing.List[BaseResource]: List of records for the specific resource.
        """
        list_resource = cls._get_crud().list(
            http_client, filter_by, sort_by, paging, include
        )
        return [
            cls.from_orm({"data": item, "included": item.get("included", [])})
            for item in list_resource["data"]
        ]

    def update(
        self, http_client: igz_mgmt.client.APIClient, relationships=None, **kwargs
    ) -> "BaseResource":
        """Updates resource record.

        Args:
            http_client (APIClient): The client to use.
            relationships (optional): The resource relationships. None by default.
            **kwargs: additional arguments to pass to the request.

        Returns:
            BaseResource: The updated record.
        """
        self._get_crud().update(
            http_client,
            self.id,
            attributes=self._fields_to_attributes(),
            relationships=relationships,
            **kwargs,
        )

        # TODO: build cls from response when BE will return the updated resource within the response body
        updated_resource = self.get(http_client, self.id)
        self.__dict__.update(updated_resource)
        return self

    def delete(
        self,
        http_client: igz_mgmt.client.APIClient,
        ignore_missing: bool = False,
        wait_for_job_deletion: bool = True,
    ) -> typing.Optional["Job"]:
        """Deletes resource record.

        Args:
            http_client (APIClient): The client to use.
            ignore_missing (bool, optional): When True, don't raise an exception in case the record does not exist.
            False by default.
            wait_for_job_deletion (bool, optional): Whether to wait for the job to complete. True by default.

        Returns:
            Job, optional: the job that was created or None.
        """
        job_id = self._get_crud().delete(http_client, self.id, ignore_missing)
        if job_id:
            if wait_for_job_deletion:
                Job.wait_for_completion(
                    http_client, job_id, job_completion_retry_interval=10
                )
            return Job.get(http_client, job_id)

    @classmethod
    def _get_crud(cls) -> igz_mgmt.cruds._BaseCrud:
        return igz_mgmt.cruds._CrudFactory.create(
            inflection.underscore(cls.__fields__["type"].default)
        )

    @classmethod
    def _get_resource_by_name(
        cls, http_client: igz_mgmt.client.APIClient, filter_key, name, include=None
    ) -> "BaseResource":
        """Gets a resource by name, by listing all resource instances and filtering by name.

        If resource is not found, ResourceNotFoundException is raised
        """
        resources = cls.list(http_client, filter_by={filter_key: name})
        if not resources:
            raise igz_mgmt.exceptions.ResourceNotFoundException(
                cls.__fields__["type"].default, name
            )
        resource_id = resources[0].id

        # although we already have the resource, we need to get it again to get the relationships
        # passed in the include parameter
        return cls.get(http_client, resource_id, include=include)

    def _fields_to_attributes(self, exclude_unset=True):
        return self.dict(
            exclude={"type", "relationships", "id"},
            exclude_none=True,
            exclude_unset=exclude_unset,
            by_alias=True,
        )


class User(BaseResource):
    """User resource represents user in the system."""

    type: str = "user"
    username: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    uid: int = 0
    created_at: str = ""
    data_access_mode: str = ""
    authentication_scheme: str = ""
    send_password_on_creation: bool = False
    assigned_policies: typing.List[igz_mgmt.constants.TenantManagementRoles] = []
    operational_status: str = igz_mgmt.constants.UserOperationalStatuses.up
    admin_status: str = igz_mgmt.constants.UserAdminStatuses.up
    password: pydantic.SecretStr = None
    phone_number: str = ""
    job_title: str = ""
    department: str = ""
    last_activity: str = ""

    @classmethod
    def create(
        cls,
        http_client: igz_mgmt.client.APIClient,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        password: str = None,
        uid: int = None,
        assigned_policies: typing.List[igz_mgmt.constants.TenantManagementRoles] = None,
        primary_group: typing.Union[str, "Group", None] = None,
        groups: typing.Union[typing.List[str], typing.List["Group"], None] = None,
        timeout: int = 30,
        wait_for_completion=True,
        phone_number: str = "",
        job_title: str = "",
        department: str = "",
    ) -> "User":
        """Creates a new User.

        Args:
            http_client (APIClient): The client to use.
            username (str): The user username.
            password (str, optional): The user password. None by default. (if not provided, an email is automatically
            sent to the user to set his password)
            assigned_policies (typing.List[TenantManagementRoles], optional): The assigned policies of the group.
            None by default.
            primary_group (str or Group or None): None by default.
            groups (typing.Union[typing.List[str], typing.List["Group"], None], optional): A list of group objects
            or group ids to add user to the groups. None by default.
            timeout (int, optional): The default is 30.
            wait_for_completion (bool): Whether to wait for the job to complete
            phone_number (str, optional): The user phone number.
            job_title (str, optional): The user job title.
            department (str, optional): The user department.

        Returns:
            User
        """
        assigned_policies = assigned_policies or [
            igz_mgmt.constants.TenantManagementRoles.developer.value,
            igz_mgmt.constants.TenantManagementRoles.application_read_only.value,
        ]
        attributes = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "assigned_policies": assigned_policies,
            "phone_number": phone_number,
            "job_title": job_title,
            "department": department,
        }
        if uid is not None:
            attributes["uid"] = uid
        if password is not None:
            attributes["password"] = password

        relationships = collections.defaultdict(dict)
        if primary_group:
            primary_group_id = (
                primary_group.id if isinstance(primary_group, Group) else primary_group
            )
            relationships["primary_group"] = {
                "data": {
                    "type": "user_group",
                    "id": primary_group_id,
                },
            }

            # ensure primary group is in groups list
            if groups:
                primary_group_in_groups = False
                for group in groups:
                    group_id = group.id if isinstance(group, Group) else group
                    if primary_group_id == group_id:
                        primary_group_in_groups = True
                        break
                if not primary_group_in_groups:
                    groups += primary_group_id
            else:
                groups = [primary_group_id]

        if groups:
            for group in groups:
                relationships["user_groups"].setdefault("data", []).append(
                    {
                        "type": "user_group",
                        "id": group.id if isinstance(group, Group) else group,
                    }
                )

        created_resource = cls._get_crud().create(
            http_client,
            attributes=attributes,
            relationships=relationships,
        )

        # there might be jobs handling the creating
        jobs_data = (
            created_resource.get("data", {})
            .get("relationships", {})
            .get("jobs", {})
            .get("data", [])
        )
        if jobs_data and wait_for_completion:
            job_id = jobs_data[0].get("id", None)
            Job.wait_for_completion(
                http_client, job_id, job_completion_retry_interval=10
            )

        def _verify_user_is_operational(user_id):
            user_obj = User.get(http_client, user_id, include=["user_groups"])
            if not user_obj.is_operational(http_client):
                http_client._logger.warn_with("User is not yet operational, retrying")

                raise igz_mgmt.common.helpers.RetryUntilSuccessfulInProgressErrorMessage(
                    "Waiting for the user to be operational",
                )
            return user_obj

        user = cls.from_orm(created_resource)

        user = igz_mgmt.common.helpers.retry_until_successful(
            1,
            timeout,
            http_client._logger,
            True,
            _verify_user_is_operational,
            user_id=user.id,
        )
        return user

    def is_operational(self, http_client: igz_mgmt.client.APIClient):
        """Verify user is operational.

        Verifying that the user operational status is up and that the all_users group
        exists in the user_groups relationships.

        Args:
            http_client (APIClient): The client to use.

        Returns:
            bool: True if user is operational, False otherwise.
        """
        if self.operational_status == igz_mgmt.constants.UserOperationalStatuses.up:
            # check that all_users group exists in the user_groups relationships
            if "user_groups" in self.relationships:
                all_users_group = Group.get_by_name(http_client, "all_users")
                for relationship_group in self.relationships["user_groups"]["data"]:
                    if relationship_group["id"] == all_users_group.id:
                        return True
        return False

    @classmethod
    def get_by_username(
        cls, http_client: igz_mgmt.client.APIClient, username: str, include=None
    ) -> "User":
        """A convenience method to get a user by username.

        Args:
            http_client (APIClient): The client to use.
            username (str): The user username.
            include (optional): Include related resources. None by default.

        Returns:
            User: The user instance by username.

        Raises:
            ResourceNotFoundException: If user is not found
        """
        return cls._get_resource_by_name(
            http_client, "username", username, include=include
        )

    @classmethod
    def self(cls, http_client: igz_mgmt.client.APIClient) -> "User":
        """Gets the current user.

        Args:
            http_client (APIClient): The client to use.

        Returns:
            User: The current user instance.
        """
        user = cls._get_crud().get_custom(http_client, "self")
        return cls.from_orm(user)

    def add_to_group(
        self, http_client: igz_mgmt.client.APIClient, group: typing.Union[str, "Group"]
    ):
        """Adds a user to a group.

        1. get the user
        2. add the group to the user
        3. update the user

        Args:
            http_client (APIClient): The client to use.
            group (str or Group): The group id or group instance to add user into it.
        """
        user = self.get(http_client, self.id, include=["user_groups"])
        if "user_groups" not in user.relationships:
            user.relationships["user_groups"] = {"data": []}

        group_id = group.id if isinstance(group, Group) else group
        if User._ensure_user_in_group(user, group_id):
            user.update(http_client, relationships=user.relationships)

    def remove_from_group(
        self, http_client: igz_mgmt.client.APIClient, group: typing.Union[str, "Group"]
    ):
        """Removes a user from a group.

        Args:
            http_client (APIClient): The client to use.
            group (str or Group): The group id or group instance to remove user from it.
        """
        user = self.get(http_client, self.id, include=["user_groups"])
        group_id = group.id if isinstance(group, Group) else group
        if "user_groups" in user.relationships:
            user.relationships["user_groups"]["data"] = [
                group
                for group in user.relationships["user_groups"]["data"]
                if group["id"] != group_id
            ]
            user.update(http_client, relationships=user.relationships)

    def set_primary_group(
        self, http_client: igz_mgmt.client.APIClient, group: typing.Union[str, "Group"]
    ):
        """Sets the primary group of a user.

        Args:
            http_client (APIClient): The client to use.
            group (str or Group): The primary group id or group instance.
        """
        group_id = group.id if isinstance(group, Group) else group

        # we need primary group
        user = self.get(http_client, self.id, include=["user_groups"])
        if "primary_group" not in user.relationships:
            user.relationships["primary_group"] = {"data": None}
        if "user_groups" not in user.relationships:
            user.relationships["user_groups"] = {"data": []}

        User._ensure_user_in_group(user, group_id)
        user.relationships["primary_group"]["data"] = {
            "id": group_id,
            "type": "user_group",
        }
        user.update(http_client, relationships=user.relationships)

    def disable(self, http_client: igz_mgmt.client.APIClient):
        """Disables the user instance.

        Args:
            http_client (APIClient): The client to use.
        """
        self.admin_status = igz_mgmt.constants.UserAdminStatuses.down
        return self.update(http_client)

    @classmethod
    def disable_by_username(cls, http_client: igz_mgmt.client.APIClient, username: str):
        """Disables the user by username.

        Args:
            http_client (APIClient): The client to use.
            username (str): The user username.
        """
        user = cls.get_by_username(http_client, username)
        return user.disable(http_client)

    @classmethod
    def disable_by_id(cls, http_client: igz_mgmt.client.APIClient, user_id: str):
        """Disables the user by user id.

        Args:
            http_client (APIClient): The client to use.
            user_id (str): The user id.
        """
        user = cls.get(http_client, user_id)
        return user.disable(http_client)

    def enable(self, http_client: igz_mgmt.client.APIClient):
        """Enables the user instance.

        Args:
            http_client (APIClient): The client to use.
        """
        self.admin_status = igz_mgmt.constants.UserAdminStatuses.up
        return self.update(http_client)

    @classmethod
    def enable_by_username(cls, http_client: igz_mgmt.client.APIClient, username: str):
        """Enables the user by username.

        Args:
            http_client (APIClient): The client to use.
            username (str): The user username.
        """
        user = cls.get_by_username(http_client, username)
        return user.enable(http_client)

    @classmethod
    def enable_by_id(cls, http_client: igz_mgmt.client.APIClient, user_id: str):
        """Enables the user by user id.

        Args:
            http_client (APIClient): The client to use.
            user_id (str): The user id.
        """
        user = cls.get(http_client, user_id)
        return user.enable(http_client)

    @staticmethod
    def _ensure_user_in_group(user, group_id: str) -> bool:
        """Ensures that a user has a group in its relationships.

        e.g.:
        If group is not in user relationships, add it and return True
        Alternatively, if group is in user relationships, return False

        Returns:
            bool: True if the group was added to the user relationship, False otherwise.
        """
        if group_id not in [
            group["id"] for group in user.relationships["user_groups"]["data"]
        ]:
            user.relationships["user_groups"]["data"].append(
                {"id": group_id, "type": "user_group"}
            )
            return True

        return False


class Group(BaseResource):
    """Group resource represents user group in the system."""

    type: str = "user_group"
    name: str = ""
    description: str = None
    data_access_mode: str = "enabled"
    gid: int = 0
    kind: str = "local"
    assigned_policies: typing.List[igz_mgmt.constants.TenantManagementRoles] = []
    system_provided: bool = False

    @classmethod
    def create(
        cls,
        http_client: igz_mgmt.client.APIClient,
        name: typing.Optional[str],
        assigned_policies: typing.Optional[
            typing.List[igz_mgmt.constants.TenantManagementRoles]
        ] = None,
        description: typing.Optional[str] = None,
        gid: typing.Optional[int] = None,
        users: typing.Optional[typing.List[typing.Union[int, str, User]]] = None,
    ) -> "Group":
        """Creates a new group.

        Args:
            http_client (APIClient): The client to use.
            name (str, optional): Group name.
            assigned_policies (typing.List[TenantManagementRoles], optional): The assigned policies of the group.
            None by default.
            description (str, optional): The description of the group. None by default.
            gid (int, optional): The gid of the group (leave empty for auto-assign). None by default.
            users (typing.List[typing.Union[int, str, User]], optional): A list of User objects or user ids
            to add to the group. None by default.

        Returns:
            Group
        """
        if not assigned_policies:
            assigned_policies = [
                igz_mgmt.constants.TenantManagementRoles.data.value,
                igz_mgmt.constants.TenantManagementRoles.application_admin.value,
            ]
        relationships = {}
        if users:
            relationships["users"] = {
                "data": [
                    {"id": user.id if isinstance(user, User) else user, "type": "user"}
                    for user in users
                ]
            }
        created_resource = cls._get_crud().create(
            http_client,
            attributes={
                "name": name,
                "description": description,
                "gid": gid,
                "assigned_policies": assigned_policies,
            },
            relationships=relationships,
        )
        return cls.from_orm(created_resource)

    @classmethod
    def get_by_name(
        cls, http_client: igz_mgmt.client.APIClient, name: str, include=None
    ) -> "Group":
        """A convenience method to get a group by name.

        Args:
            http_client (APIClient): The client to use.
            name (str): Group name.
            include (optional): Include related resources. None by default.

        Returns:
            Group: The group instance by group name.

        Raises:
            ResourceNotFoundException: If group is not found
        """
        return cls._get_resource_by_name(http_client, "name", name, include=include)

    def add_user(
        self,
        http_client: igz_mgmt.client.APIClient,
        user: typing.Union[str, int, "User"],
    ):
        """Adds a user to group.

        1. get the user
        2. add the group to the user
        3. update the group

        Args:
            http_client (APIClient): The client to use.
            user (str or int or User): The user id or user instance to add.
        """
        if not isinstance(user, User):
            user = User.get(http_client, user)
        user.add_to_group(http_client, self)
        self.__dict__.update(Group.get(http_client, self.id))

    def remove_user(
        self,
        http_client: igz_mgmt.client.APIClient,
        user: typing.Union[str, int, "User"],
    ):
        """Removes a user from group.

        Args:
            http_client (APIClient): The client to use.
            user (str ot int or User): The user id or user instance to remove.
        """
        if not isinstance(user, User):
            user = User.get(http_client, user)
        user.remove_from_group(http_client, self)
        self.__dict__.update(Group.get(http_client, self.id))


class AccessKey(BaseResource):
    """AccessKey resource represents access key in the system."""

    type: str = "access_key"
    tenant_id: str = ""
    ttl: int = 315360000  # 10 years
    created_at: str = ""
    updated_at: str = ""
    group_ids: typing.List[str] = []
    uid: int = 0
    gids: typing.List[int] = []
    expires_at: int = 0  # EPOCH
    interface_kind: str = "web"
    label: str = ""
    kind: str = "accessKey"
    planes: typing.List[
        igz_mgmt.constants.SessionPlanes
    ] = igz_mgmt.constants.SessionPlanes.all()

    @classmethod
    def create(
        cls,
        http_client: igz_mgmt.client.APIClient,
        planes: typing.List[
            igz_mgmt.constants.SessionPlanes
        ] = igz_mgmt.constants.SessionPlanes.all(),
        label: str = None,
    ):
        """Creates a new access key.

        Args:
            http_client (APIClient): The client to use.
            planes (typing.List[SessionPlanes], optional): The planes of the access key.
            label (str, optional): The label of the access key.
        """
        created_resource = cls._get_crud().create(
            http_client,
            attributes={
                "planes": planes,
                "label": label,
            },
        )
        return cls.from_orm(created_resource)


class Job(BaseResource):
    """Job is an abstraction for long-running operations in the API.

    Some operations, cannot be finished within a reasonable amount of time for a normal HTTP request.
    Job has a state, id and can be awaited on asynchronously.
    """

    type: str = "job"
    kind: str = ""
    params: str = ""
    max_total_execution_time: int = 3 * 60 * 60  # in seconds
    max_worker_execution_time: typing.Optional[int] = None  # in seconds
    delay: float = 0  # in seconds
    state: igz_mgmt.constants.JobStates = igz_mgmt.constants.JobStates.created
    result: str = ""
    created_at: str = ""
    on_success: typing.List[dict] = None
    on_failure: typing.List[dict] = None
    updated_at: str = ""
    handler: str = ""
    ctx_id: str = ""

    def delete(
        self, http_client: igz_mgmt.client.APIClient, **kwargs
    ) -> typing.Optional["Job"]:
        """This method is forbidden."""
        raise igz_mgmt.exceptions.ResourceDeleteException

    def update(self, http_client: igz_mgmt.client.APIClient, **kwargs):
        """This method is forbidden."""
        raise igz_mgmt.exceptions.ResourceUpdateException

    @staticmethod
    def wait_for_completion(
        http_client: igz_mgmt.client.APIClient,
        job_id: str,
        job_completion_retry_interval: float = 30,
        timeout: int = 3600,
    ):
        """Wait for a job to be finished.

        Args:
            http_client (APIClient): The client to use.
            job_id (str): The job id.
            job_completion_retry_interval (float, optional): The default is 30.
            timeout (int, optional): The default is 3600.
        """

        def _verify_job_in_terminal_state():
            try:
                job_obj = Job.get(http_client, job_id)
            except igz_mgmt.exceptions.ResourceNotFoundException as exc:
                http_client._logger.warn_with(
                    "Job not found, bail out",
                    job_id=job_id,
                )
                raise igz_mgmt.common.helpers.RetryUntilSuccessfulFatalError(
                    "Resource was not found", caused_by_exc=exc
                )
            if job_obj.state not in igz_mgmt.constants.JobStates.terminal_states():
                http_client._logger.info_with(
                    "Job is not in a terminal state yet, retrying",
                    current_state=job_obj.state,
                    job_id=job_id,
                )
                raise igz_mgmt.common.helpers.RetryUntilSuccessfulInProgressErrorMessage(
                    "Waiting for job completion",
                    variables={
                        "job_id": job_id,
                        "job_state": job_obj.state,
                    },
                )
            return job_obj

        http_client._logger.info_with("Waiting for job completion", job_id=job_id)
        job = igz_mgmt.common.helpers.retry_until_successful(
            job_completion_retry_interval,
            timeout,
            http_client._logger,
            True,
            _verify_job_in_terminal_state,
        )
        if job.state != igz_mgmt.constants.JobStates.completed:
            error_message = f"Job {job_id} failed with state: {job.state}"
            try:
                parsed_result = json.loads(job.result)
                error_message += f", message: {parsed_result['message']}"
                # status is optional
                if "status" in parsed_result:
                    status_code = int(parsed_result["status"])
                    error_message = f", status: {status_code}"

            except Exception:
                error_message += f", message: {job.result}"

            raise RuntimeError(error_message)
        http_client._logger.info_with("Job completed successfully", job_id=job_id)


class AppServicesManifest(BaseResource):
    """AppServicesManifest resource."""

    type: str = "app_services_manifest"
    cluster_name: str = ""
    tenant_name: str = ""
    tenant_id: str = ""
    app_services: typing.List[igz_mgmt.schemas.app_services.AppServiceBase] = []
    state: typing.Optional[igz_mgmt.constants.AppServicesManifestStates]
    last_error: typing.Optional[str]
    last_modification_job: str = ""
    apply_services_mode: typing.Optional[igz_mgmt.constants.ApplyServicesMode]
    running_modification_job: str = ""
    force_apply_all_mode: typing.Optional[igz_mgmt.constants.ForceApplyAllMode]

    _skip_apply: bool = False

    @staticmethod
    @contextlib.contextmanager
    def apply_services(
        http_client: igz_mgmt.client.APIClient,
        force_apply_all_mode: igz_mgmt.constants.ForceApplyAllMode = igz_mgmt.constants.ForceApplyAllMode.disabled,
    ):
        """A context manager to apply services with multiple changes at once.

        Args:
            http_client (APIClient): The client to use.
            force_apply_all_mode (ForceApplyAllMode, optional): Disabled by default.

        Returns:
            AppServicesManifest: The app service manifest instance.
        """
        app_services_manifest = AppServicesManifest.get(http_client)
        app_services_manifest._skip_apply = True
        try:
            yield app_services_manifest
        finally:
            app_services_manifest._apply(
                http_client,
                # writing it down here for explicitness
                wait_for_completion=True,
                force_apply_all_mode=force_apply_all_mode,
            )
            app_services_manifest._skip_apply = False

    def delete(
        self, http_client: igz_mgmt.client.APIClient, **kwargs
    ) -> typing.Optional[Job]:
        """This method is forbidden."""
        raise igz_mgmt.exceptions.ResourceDeleteException

    def update(self, http_client: igz_mgmt.client.APIClient, **kwargs):
        """This method is forbidden."""
        raise igz_mgmt.exceptions.ResourceUpdateException

    def list(self, http_client: igz_mgmt.client.APIClient, **kwargs):
        """This method is forbidden."""
        raise igz_mgmt.exceptions.ResourceListException

    @classmethod
    def get(
        cls, http_client: igz_mgmt.client.APIClient, **kwargs
    ) -> "AppServicesManifest":
        """Gets the app services manifest from the API.

        Args:
            http_client (APIClient): The client to use.
            **kwargs: Arbitrary keyword arguments (not in used).

        Returns:
            AppServicesManifest: The app service manifest instance.
        """
        resource = cls._get_crud().list(http_client)
        return [cls.from_orm({"data": item}) for item in resource["data"]][0]

    def set_apply_mode(self, apply_mode: igz_mgmt.constants.ApplyServicesMode):
        """Sets the apply mode of the app services manifest.

        Args:
            apply_mode (ApplyServicesMode): apply services mode value.
        """
        self.apply_services_mode = apply_mode

    def resolve_service(
        self,
        app_service_spec_name: str,
    ) -> typing.Optional[igz_mgmt.schemas.app_services.AppServiceBase]:
        """Gets the app service that matches the given spec name.

        Args:
            app_service_spec_name (str): The name of the app service spec.

        Returns:
            AppServiceBase, optional: The app service instance that matches the given spec name.
        """
        for app_service in self.app_services:
            if app_service.spec.name == app_service_spec_name:
                return app_service
        return None

    def create_or_update(
        self,
        http_client: igz_mgmt.client.APIClient,
        app_service: typing.Union[
            igz_mgmt.schemas.app_services.AppServiceSpec,
            igz_mgmt.schemas.app_services.AppServiceBase,
        ],
        wait_for_completion=True,
    ) -> typing.Optional[Job]:
        """Creates or updates an app service.

        Args:
            http_client (APIClient): The client to use.
            app_service (AppServiceSpec or AppServiceBase): The app service to create or update
            wait_for_completion (bool): Whether to wait for the job to complete

        Returns:
            Job, optional: the job that was created or None if wait_for_completion is False.
        """
        app_service_spec = (
            app_service.spec
            if isinstance(app_service, igz_mgmt.schemas.app_services.AppServiceBase)
            else app_service
        )
        app_service_spec.mark_as_changed = True
        app_service_spec_obj = self.resolve_service(app_service_spec.name)
        if app_service_spec_obj:
            for position, service in enumerate(self.app_services):
                if service.spec.name == app_service_spec_obj.spec.name:
                    self.app_services[position].spec = app_service_spec
                    break
        else:
            self.app_services.append(
                igz_mgmt.schemas.app_services.AppServiceBase(spec=app_service_spec)
            )
        if not self._skip_apply:
            return self._apply(http_client, wait_for_completion)

    def restart(
        self,
        http_client: igz_mgmt.client.APIClient,
        app_service_spec_name: str,
        wait_for_completion=True,
    ) -> typing.Optional[Job]:
        """Restarts an app service.

        Args:
            http_client (APIClient): The client to use.
            app_service_spec_name (str): Name of the app service to restart
            wait_for_completion (bool): Whether to wait for the job to complete

        Returns:
            Job, optional: the job that was created or None if wait_for_completion is False.
        """
        app_service_obj = self.resolve_service(app_service_spec_name)
        if not app_service_obj:
            raise igz_mgmt.exceptions.AppServiceNotExistsException(
                name=app_service_spec_name
            )
        for position, app_service in enumerate(self.app_services):
            if app_service.spec.name == app_service_obj.spec.name:
                self.app_services[position].spec.mark_for_restart = True
                break
        if not self._skip_apply:
            return self._apply(http_client, wait_for_completion)

    def remove_service(
        self,
        http_client: igz_mgmt.client.APIClient,
        app_service_spec_name: str,
        wait_for_completion=True,
    ) -> typing.Optional[Job]:
        """Removes an app service.

        Args:
            http_client (APIClient): The client to use.
            app_service_spec_name (str): Name of the app service to remove
            wait_for_completion (bool): Whether to wait for the job to complete

        Returns:
            Job, optional: the job that was created or None if wait_for_completion is False.
        """
        app_service_obj = self.resolve_service(app_service_spec_name)
        if not app_service_obj:
            raise igz_mgmt.exceptions.AppServiceNotExistsException(
                name=app_service_spec_name
            )
        for position, app_service in enumerate(self.app_services):
            if app_service.spec.name == app_service_obj.spec.name:
                del self.app_services[position]
                break
        if not self._skip_apply:
            return self._apply(http_client, wait_for_completion)

    def scale_from_zero(
        self,
        http_client: igz_mgmt.client.APIClient,
        app_service_spec_name: str,
        wait_for_completion=True,
    ) -> typing.Optional[Job]:
        """Scales an app service from zero.

        Args:
            http_client (APIClient): The client to use.
            app_service_spec_name (str): Name of the app service to scale from zero
            wait_for_completion (bool): Whether to wait for the job to complete

        Returns:
            Job, optional: the job that was created or None if wait_for_completion is False.
        """
        app_service_obj = self.resolve_service(app_service_spec_name)
        if not app_service_obj:
            raise igz_mgmt.exceptions.AppServiceNotExistsException(
                name=app_service_spec_name
            )
        app_service_obj.spec.mark_as_changed = True
        app_service_obj.spec.desired_state = (
            igz_mgmt.constants.AppServiceDesiredStates.ready
        )
        for position, app_service in enumerate(self.app_services):
            if app_service.spec.name == app_service_obj.spec.name:
                self.app_services[position].spec = app_service_obj.spec
                break
        if not self._skip_apply:
            current_apply_mode = self.apply_services_mode

            # In 3.5.3, the ApplyServicesMode.scale_from_zero_only mode is deprecated.
            # because we can scale services from zero by using the mark_as_changed and desired_state fields
            if http_client.version >= semver.VersionInfo.parse("3.5.3"):
                self.set_apply_mode(
                    igz_mgmt.constants.ApplyServicesMode.service_owner_edit
                )
            else:
                self.set_apply_mode(
                    igz_mgmt.constants.ApplyServicesMode.scale_from_zero_only
                )
            apply_result = self._apply(http_client, wait_for_completion)

            # set to the previous apply mode
            self.set_apply_mode(current_apply_mode)
            return apply_result

    def _apply(
        self,
        http_client: igz_mgmt.client.APIClient,
        wait_for_completion=True,
        force_apply_all_mode=igz_mgmt.constants.ForceApplyAllMode.disabled,
    ) -> Job:
        """Apply the current state of the manifest to the API.

        Args:
            http_client (APIClient): The client to use.
            wait_for_completion (bool, optional): Whether to wait for the job to complete. True by default.
            force_apply_all_mode (ForceApplyAllMode, optional): Disabled by default.

        Returns:
            Job: the job that was created.
        """
        # TODO: handle errors
        self.force_apply_all_mode = force_apply_all_mode
        response = self._get_crud().update(
            http_client,
            None,
            # don't ignore unset fields
            attributes=self._fields_to_attributes(exclude_unset=False),
            relationships=self.relationships,
        )

        job_id = response.json().get("data", {}).get("id")
        if not wait_for_completion:
            return Job.get(http_client, job_id)

        # wait few seconds before checking job status
        time.sleep(5)
        apply_exc = None
        try:
            Job.wait_for_completion(
                http_client, job_id, job_completion_retry_interval=10
            )
        except Exception as exc:
            apply_exc = exc

        updated_resource = self.get(http_client)
        self.__dict__.update(updated_resource)
        if apply_exc:
            errors = []
            for service in updated_resource.app_services:
                if service.status.error_info and service.status.error_info.description:
                    errors.append(
                        f"Service {service.spec.name} failed due to {service.status.error_info.description}"
                    )
            if errors:
                raise RuntimeError(", ".join(errors)) from apply_exc
            else:
                raise apply_exc
        return Job.get(http_client, job_id)


class Project(BaseResource):
    """Project resource represents project in the system."""

    type: str = "project"
    name: str = ""
    description: str = ""
    created_at: str = ""
    updated_at: str = ""
    admin_status: str = igz_mgmt.constants.ProjectAdminStatuses.online
    operational_status: str = igz_mgmt.constants.ProjectOperationalStatuses.creating

    # e.g.: [{"name":"", "value":""}, ...]
    labels: typing.List[typing.Dict[str, str]] = []
    annotations: typing.List[typing.Dict[str, str]] = []

    mlrun_project: str = ""
    nuclio_project: str = ""

    @classmethod
    def create(
        cls,
        http_client: igz_mgmt.client.APIClient,
        name: str,
        description: str = "",
        labels: typing.List[typing.Dict[str, str]] = None,
        annotations: typing.List[typing.Dict[str, str]] = None,
        owner: typing.Union[str, "User", None] = None,
        wait_for_completion=True,
    ) -> "Project":
        """Creates a new project.

        Args:
            http_client (APIClient): The client to use.
            name (str): The project name.
            description (str, optional): The project description.
            labels (typing.List[typing.Dict[str, str]], optional): The project labels.
            annotations (typing.List[typing.Dict[str, str]], optional): The project annotations.
            owner (str or User or None): The project owner. None by default
            wait_for_completion (bool): Whether to wait for the job to complete

        Returns:
            Project: The project instance.
        """
        attributes = {
            "name": name,
            "description": description,
            "labels": labels,
            "annotations": annotations,
        }

        relationships = cls._fill_relationships(owner=owner)

        created_resource = cls._get_crud().create(
            http_client,
            attributes=attributes,
            relationships=relationships,
            headers=cls._resolve_project_header(),
        )

        # there might be jobs handling the creating
        job_id = (
            created_resource.get("data", {})
            .get("relationships", {})
            .get("last_job", {})
            .get("data", {})
            .get("id", None)
        )
        if job_id and wait_for_completion:
            Job.wait_for_completion(
                http_client, job_id, job_completion_retry_interval=10
            )
        return cls.from_orm(created_resource)

    def update(
        self, http_client: igz_mgmt.client.APIClient, relationships=None, **kwargs
    ) -> "BaseResource":
        """Updates project.

        Args:
            http_client (APIClient): The client to use.
            relationships (optional): The project relationships. None by default.
            **kwargs: additional arguments to pass to the request.

        Returns:
            BaseResource: The updated record.
        """
        return super().update(
            http_client,
            relationships=relationships,
            headers=self._resolve_project_header(),
            **kwargs,
        )

    def delete(
        self,
        http_client: igz_mgmt.client.APIClient,
        ignore_missing: bool = False,
        wait_for_job_deletion: bool = True,
        deletion_strategy: igz_mgmt.constants.ProjectDeletionStrategies = None,
    ) -> typing.Optional[Job]:
        """Deletes resource record.

        Args:
            http_client (APIClient): The client to use.
            ignore_missing (bool, optional): When True, don't raise an exception in case the record does not exist.
            False by default.
            wait_for_job_deletion (bool, optional): Whether to wait for the job to complete. True by default.
            deletion_strategy (ProjectDeletionStrategies, optional): The project deletion type. None by default

        Returns:
            Job, optional: the job that was created or None.
        """
        response = http_client.delete_by_attribute(
            self.type,
            "name",
            self.name,
            ignore_missing=ignore_missing,
            headers=self._resolve_project_header(deletion_strategy),
        )

        if response.status_code == http.HTTPStatus.ACCEPTED:
            response_body = response.json()
            job_id = response_body.get("data", {}).get("id", None)
            if job_id:
                if wait_for_job_deletion:
                    Job.wait_for_completion(
                        http_client, job_id, job_completion_retry_interval=10
                    )
                return Job.get(http_client, job_id)

    @classmethod
    def get_by_name(
        cls,
        http_client: igz_mgmt.client.APIClient,
        name: str,
        include: typing.Optional[typing.List[str]] = None,
    ) -> "Project":
        """A convenience method to get a project by name.

        Args:
            http_client (APIClient): The client to use.
            name (str): The project name.
            include (typing.List[str], optional): Include related resources (e.g. include=["tenant", "owner"]).
                None by default.

        Returns:
            Project: The project instance by name.

        Raises:
            ResourceNotFoundException: If project is not found
        """
        return cls._get_resource_by_name(http_client, "name", name, include=include)

    def set_owner(
        self, http_client: igz_mgmt.client.APIClient, owner: typing.Union[str, "User"]
    ):
        """Sets the owner of the project.

        Args:
            http_client (APIClient): The client to use.
            owner (str or User): The user id or user instance.

        Returns:
            Project: The project instance.
        """
        relationships = self._fill_relationships(owner=owner)
        return self.update(http_client, relationships=relationships)

    @staticmethod
    def _resolve_project_header(
        deletion_strategy: igz_mgmt.constants.ProjectDeletionStrategies = None,
    ):
        headers = {
            igz_mgmt.constants._RequestHeaders.projects_role_header: "igz-mgmt-sdk"
        }
        if deletion_strategy:
            headers[
                igz_mgmt.constants._RequestHeaders.deletion_strategy_header
            ] = deletion_strategy
        return headers

    @staticmethod
    def _fill_relationships(owner: typing.Union[str, "User", None]):
        relationships = collections.defaultdict(dict)
        if owner:
            user_id = owner.id if isinstance(owner, User) else owner
            relationships["owner"] = {
                "data": {
                    "type": "user",
                    "id": user_id,
                },
            }
        return relationships
