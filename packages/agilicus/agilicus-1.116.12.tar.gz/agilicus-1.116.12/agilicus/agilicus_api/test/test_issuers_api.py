"""
    Agilicus API

    Agilicus is API-first. Modern software is controlled by other software, is open, is available for you to use the way you want, securely, simply.  A rendered, online viewable and usable version of this specification is available at [api](https://www.agilicus.com/api). You may try the API inline directly in the web page. To do so, first obtain an Authentication Token (the simplest way is to install the Python SDK, and then run `agilicus-cli --issuer https://MYISSUER get-token`). You will need an org-id for most calls (and can obtain from `agilicus-cli --issuer https://MYISSUER list-orgs`). The `MYISSUER` will typically be `auth.MYDOMAIN`, and you will see it as you sign-in to the administrative UI.  This API releases on Bearer-Token authentication. To obtain a valid bearer token you will need to Authenticate to an Issuer with OpenID Connect (a superset of OAUTH2).  Your \"issuer\" will look like https://auth.MYDOMAIN. For example, when you signed-up, if you said \"use my own domain name\" and assigned a CNAME of cloud.example.com, then your issuer would be https://auth.cloud.example.com.  If you selected \"use an Agilicus supplied domain name\", your issuer would look like https://auth.myorg.agilicus.cloud.  For test purposes you can use our [Python SDK](https://pypi.org/project/agilicus/) and run `agilicus-cli --issuer https://auth.MYDOMAIN get-token`.  This API may be used in any language runtime that supports OpenAPI 3.0, or, you may use our [Python SDK](https://pypi.org/project/agilicus/), our [Typescript SDK](https://www.npmjs.com/package/@agilicus/angular), or our [Golang SDK](https://git.agilicus.com/pub/sdk-go).  100% of the activities in our system our API-driven, from our web-admin, through our progressive web applications, to all internals: there is nothing that is not accessible.  For more information, see [developer resources](https://www.agilicus.com/developer).   # noqa: E501

    The version of the OpenAPI document: 2021.06.17
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


import unittest

import agilicus_api
from agilicus_api.api.issuers_api import IssuersApi  # noqa: E501


class TestIssuersApi(unittest.TestCase):
    """IssuersApi unit test stubs"""

    def setUp(self):
        self.api = IssuersApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_client(self):
        """Test case for create_client

        Create a client  # noqa: E501
        """
        pass

    def test_create_issuer(self):
        """Test case for create_issuer

        Create an issuer  # noqa: E501
        """
        pass

    def test_create_policy(self):
        """Test case for create_policy

        Create a policy  # noqa: E501
        """
        pass

    def test_create_policy_rule(self):
        """Test case for create_policy_rule

        Create a policy rule  # noqa: E501
        """
        pass

    def test_create_upstream_group_mapping(self):
        """Test case for create_upstream_group_mapping

        Create an upstream group mapping  # noqa: E501
        """
        pass

    def test_delete_client(self):
        """Test case for delete_client

        Delete a client  # noqa: E501
        """
        pass

    def test_delete_policy(self):
        """Test case for delete_policy

        Delete a Policy  # noqa: E501
        """
        pass

    def test_delete_policy_rule(self):
        """Test case for delete_policy_rule

        Delete a Policy Rule  # noqa: E501
        """
        pass

    def test_delete_root(self):
        """Test case for delete_root

        Delete an Issuer  # noqa: E501
        """
        pass

    def test_delete_upstream_group_mapping(self):
        """Test case for delete_upstream_group_mapping

        Delete an upstream group mapping  # noqa: E501
        """
        pass

    def test_get_client(self):
        """Test case for get_client

        Get a client  # noqa: E501
        """
        pass

    def test_get_issuer(self):
        """Test case for get_issuer

        Get an issuer  # noqa: E501
        """
        pass

    def test_get_policy(self):
        """Test case for get_policy

        Get a policy  # noqa: E501
        """
        pass

    def test_get_policy_rule(self):
        """Test case for get_policy_rule

        Get a policy rule  # noqa: E501
        """
        pass

    def test_get_root(self):
        """Test case for get_root

        Get an issuer  # noqa: E501
        """
        pass

    def test_get_upstream_group_mapping(self):
        """Test case for get_upstream_group_mapping

        Get an upstream group mapping  # noqa: E501
        """
        pass

    def test_get_upstreams(self):
        """Test case for get_upstreams

        Get provisioned upstreams for the issuer  # noqa: E501
        """
        pass

    def test_get_wellknown_issuer_info(self):
        """Test case for get_wellknown_issuer_info

        Get well-known issuer information  # noqa: E501
        """
        pass

    def test_list_clients(self):
        """Test case for list_clients

        Query Clients  # noqa: E501
        """
        pass

    def test_list_issuer_roots(self):
        """Test case for list_issuer_roots

        Query Issuers  # noqa: E501
        """
        pass

    def test_list_issuer_upstreams(self):
        """Test case for list_issuer_upstreams

        list issuer upstream information  # noqa: E501
        """
        pass

    def test_list_issuers(self):
        """Test case for list_issuers

        Query Issuers  # noqa: E501
        """
        pass

    def test_list_policies(self):
        """Test case for list_policies

        Query Policies  # noqa: E501
        """
        pass

    def test_list_policy_rules(self):
        """Test case for list_policy_rules

        Query Policy rules  # noqa: E501
        """
        pass

    def test_list_upstream_group_mappings(self):
        """Test case for list_upstream_group_mappings

        Query upstream group mappings for an issuer  # noqa: E501
        """
        pass

    def test_list_wellknown_issuer_info(self):
        """Test case for list_wellknown_issuer_info

        list well-known issuer information  # noqa: E501
        """
        pass

    def test_replace_client(self):
        """Test case for replace_client

        Update a client  # noqa: E501
        """
        pass

    def test_replace_issuer(self):
        """Test case for replace_issuer

        Update an issuer  # noqa: E501
        """
        pass

    def test_replace_policy(self):
        """Test case for replace_policy

        Update a policy  # noqa: E501
        """
        pass

    def test_replace_policy_rule(self):
        """Test case for replace_policy_rule

        Update a policy rule  # noqa: E501
        """
        pass

    def test_replace_root(self):
        """Test case for replace_root

        Update an issuer  # noqa: E501
        """
        pass

    def test_replace_upstream_group_mapping(self):
        """Test case for replace_upstream_group_mapping

        Update an upstream group mapping  # noqa: E501
        """
        pass

    def test_reset_service_account(self):
        """Test case for reset_service_account

        Reset the service account for the specified issuer  # noqa: E501
        """
        pass

    def test_reset_to_default_policy(self):
        """Test case for reset_to_default_policy

        Reset the current policy to the default policy  # noqa: E501
        """
        pass

    def test_set_policy(self):
        """Test case for set_policy

        Set the current policy to the policy sent  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
