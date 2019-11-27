import requests

"""
https://www.terraform.io/docs/cloud/api/modules.html
"""
class Modules():
    def list_modules(self, organization, **kwargs):
        is_verified = (kwargs.get("verified", False) == True)
        provider = kwargs.get("provider", "")
        limit = kwargs.get("limit", 0)
        offset = kwargs.get("offset", 0)

        #TODO Possibly use urllib.urlencode if Python 3 above will be the minimum support
        query = "verified=" + str(is_verified).lower() + "&"  + "provider=" + str(provider) + "&" + "offset=" + str(offset)
        if limit > 0:
            query = query + "&" + "limit=" + str(limit)

        url = self.url_module_standard_registry + '{}'.format(organization) + "?" + query
        return self._get_handler(url)

    def register_module(self, register_params):
        """
        Register a module in TFE
        Note that if the module already exist in the organisation, this will result in an 422 Response error
        https://www.terraform.io/docs/cloud/api/modules.html#publish-a-module-from-a-vcs
        :param register_params: Parameters to register the modules
        {
            "identifier":"SKI/terraform-aws-instance",
            "oauth-token-id":"ot-hmAyP66qk2AMVdbJ"
        }
        """
        url = self.url + 'registry-modules'
        register_params["display_identifier"] = register_params["identifier"]
        payload = {
            "data": {
                "attributes": {
                    "vcs-repo": register_params
                },
                "type":"registry-modules"
            }
        }
        return self._post_handler(url=url, json=payload)