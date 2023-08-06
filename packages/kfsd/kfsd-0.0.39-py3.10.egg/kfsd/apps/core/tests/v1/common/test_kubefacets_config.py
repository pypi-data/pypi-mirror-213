from unittest.mock import patch

from kfsd.apps.core.tests.base_api import BaseAPITestCases
from kfsd.apps.core.common.kubefacets_config import KubefacetsConfig

middleware_settings = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "kfsd.apps.core.middleware.token.KubefacetsTokenMiddleware",
]


class KubefacetsConfigTests(BaseAPITestCases):
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    def test_kubefacets_config_local(self, rawSettingsMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/core/tests/v1/data/requests/common/kubefacets/local_settings.json"
        )
        rawSettingsMocked.return_value = rawConfig
        obsConfig = KubefacetsConfig().getConfig()
        expConfig = self.readJSONData(
            "kfsd/apps/core/tests/v1/data/responses/common/kubefacets/test_kubefacets_config_local.json"
        )
        self.assertEquals(obsConfig, expConfig)

        localObsConfig = KubefacetsConfig().getLocalConfig()
        localExpConfig = self.readJSONData(
            "kfsd/apps/core/tests/v1/data/responses/common/kubefacets/test_kubefacets_config_local_localconfigobj.json"
        )
        self.assertEquals(localObsConfig, localExpConfig)

    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_kubefacets_config_remote(self, remoteConfigMocked, rawSettingsMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/core/tests/v1/data/requests/common/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/core/tests/v1/data/requests/common/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig
        obsConfig = KubefacetsConfig().getConfig()
        expConfig = self.readJSONData(
            "kfsd/apps/core/tests/v1/data/responses/common/kubefacets/test_kubefacets_config_remote.json"
        )
        self.assertEquals(obsConfig, expConfig)
