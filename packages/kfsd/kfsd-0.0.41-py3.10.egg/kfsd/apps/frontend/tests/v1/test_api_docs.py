from kfsd.apps.core.tests.base_api import BaseAPITestCases
from django.urls import reverse
from unittest.mock import patch


class APIDocsViewTests(BaseAPITestCases):
    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_get(self, remoteConfigMocked, rawSettingsMocked, tokenUserInfoMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/core/tests/v1/data/requests/common/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/core/tests/v1/data/requests/common/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig
        staffUserInfoResp = {
            "status": True,
            "data": {
                "user": {
                    "identifier": "123",
                    "is_staff": True,
                    "is_active": True,
                    "is_email_verified": True,
                }
            },
        }
        tokenUserInfoMocked.return_value = staffUserInfoResp
        url = reverse("api_doc")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
