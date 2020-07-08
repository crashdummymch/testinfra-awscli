"""
module for testing awscli
"""

import site
import shutil

import logging
import pytest
import testinfra

logger = logging.getLogger()

@pytest.mark.awscli
class TestAwscli:
    """
    Test class for awscli install
    """

    @pytest.mark.awscli_package
    def test_package(self, host, load_defaults, load_overrides):
        """
        test if package is installed
        """
        module_vars = {**load_defaults, **load_overrides}

        package = host.package(module_vars['awscli_ospackage_name'])
        if module_vars['awscli_ospackage_state']:
            pytest.assume(package.is_installed)
            pytest.assume(package.version == module_vars['awscli_ospackage_version'])
        else:
            pytest.assume(not package.is_installed)

        if module_vars['awscli_pippackage_path'] is None:
            os_site_packages = site.getsitepackages()
        else:
            os_site_packages = module_vars['awscli_pippackage_path']
        if not isinstance(os_site_packages, list):
            os_site_packages = [os_site_packages]
        logger.debug("os_site_packages={}".format(os_site_packages))

        package = {}
        for path in os_site_packages:
            package.update(host.pip_package.get_packages(pip_path="pip list --path {}".format(path)))
        logger.debug("package={}".format(package))
        if module_vars['awscli_pippackage_state']:
            try:
                pytest.assume(package.get(module_vars['awscli_pippackage_name']))
            except AttributeError as error:
                raise Exception("Package not found error={}".format(error))
            try:
                if module_vars['awscli_pippackage_version'] is not None:
                    pytest.assume(package.get(module_vars['awscli_pippackage_name']).get('version') == module_vars['awscli_pippackage_version'])
            except AttributeError as error:
                raise Exception("Package version not found error={}".format(error))
        else:
            pytest.assume(package.get(module_vars['awscli_pippackage_name']) is None)


    @pytest.mark.awscli_process
    def test_process(self, host, load_defaults, load_overrides):
        """
        test process is running correctly
        """
        module_vars = {**load_defaults, **load_overrides}
        logger.debug("module_vars['awscli_process_path']={}".format(module_vars['awscli_process_path']))
        awscli = shutil.which(module_vars['awscli_process_path'])
        cmd = host.run("{} --version".format(awscli))
        logger.debug("cmd={}".format(cmd))

        pytest.assume(cmd.succeeded)
