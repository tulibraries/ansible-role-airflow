"""
Role tests default variables installation.
"""

import os
import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

TESTINFRA_HOSTS = AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    """
    Tests general host is available with root
    """
    hosts_file = host.file('/etc/hosts')
    assert hosts_file.exists
    assert hosts_file.user == 'root'
    assert hosts_file.group == 'root'


def test_airflow_user(host):
    """
    Tests about airflow user configuration
    """
    airflow_user = host.user('airflow')

    assert airflow_user.exists is True
    assert airflow_user.group == 'airflow'
    assert airflow_user.home == '/var/lib/airflow'
    assert airflow_user.shell == '/bin/bash'


def test_airflow_group(host):
    """
    Tests about airflow group configuration
    """
    assert host.group('airflow').exists is True


@pytest.mark.parametrize('name,codenames', [
    ('python3-dev', None),
    ('libpq-dev', None),
    ('libssl-dev', None),
    ('libffi-dev', None),
    ('build-essential', None),
    ('python-virtualenv', None),
    ('python-pip', None),
])
def test_debian_ubuntu_prerequisites_packages(host, name, codenames):
    """
    Tests about airflow prerequisites packages
    """

    if host.system_info.distribution not in ['debian', 'ubuntu']:
        pytest.skip('{} ({}) distribution not debian or ubuntu'.format(
            host.system_info.distribution, host.system_info.release))

    if codenames and host.system_info.codename.lower() not in codenames:
        pytest.skip('{} package not used with {} ({})'.format(
            name, host.system_info.distribution, host.system_info.codename))

    assert host.package(name).is_installed


@pytest.mark.parametrize('name,codenames', [
    ('python3-devel', None),
    ('openssl-devel', None),
    ('libffi-devel', None),
    ('libxml2', None),
    ('libxml2-devel', None),
    ('libxslt-devel', None),
    ('python2-pip', None),
    ('python-virtualenv', None),
    ('python-setuptools', None),
    ('gcc', None)
])
def test_centos_prerequisites_packages(host, name, codenames):
    """
    Tests about airflow prerequisites packages
    """

    if host.system_info.distribution != 'centos':
        pytest.skip('{} ({}) distribution not centos'.format(
            host.system_info.distribution, host.system_info.release))

    if codenames and host.system_info.codename.lower() not in codenames:
        pytest.skip('{} package not used with {} ({})'.format(
            name, host.system_info.distribution, host.system_info.codename))

    assert host.package(name).is_installed


def test_airflow_processes(host):
    """
    Test about airflow processes
    """

    assert len(host.process.filter(user='airflow', comm='airflow')) >= 2


@pytest.mark.parametrize('name', [
    ('airflow-webserver'),
    ('airflow-scheduler'),
])
def test_airflow_services(host, name):
    """
    Test about airflow services
    """

    if host.system_info.codename == 'jessie':
        output = host.check_output('service {} status'.format(name))
        assert '{} running'.format(name) in output
    else:
        service = host.service(name)
        assert service.is_running
        assert service.is_enabled


@pytest.mark.parametrize('library', [
    ('apache-airflow'),
    ('cryptography')
])
def test_pip_libraries(host, library):
    """
    Test pip libraries installed
    """

    pip_path = "/var/lib/airflow/venv/bin/pip3.6"
    libraries = host.pip_package.get_packages(pip_path=pip_path)
    assert libraries.get(library)


@pytest.mark.parametrize('path,path_type,user,group,mode', [
    ('/var/run/airflow', 'directory', 'airflow', 'airflow', 0o700),
    ('/var/lib/airflow/airflow', 'directory', 'airflow', 'airflow', 0o700),
    ('/var/lib/airflow/venv', 'directory', 'airflow', 'airflow', 0o755),
    ('/var/lib/airflow/airflow/airflow.cfg', 'file', 'airflow', 'airflow',
     0o400)
    ])
def test_airflow_paths(host, path, path_type, user, group, mode):
    """
    Tests Airflow paths
    """
    current_path = host.file(path)

    assert current_path.exists

    if path_type == 'directory':
        assert current_path.is_directory
    elif path_type == 'file':
        assert current_path.is_file
    assert current_path.user == user
    assert current_path.group == group
    assert current_path.mode == mode


@pytest.mark.parametrize('path', [
    ('/var/lib/airflow/airflow/dags/'),
    ('/var/lib/airflow/airflow/dags/cob_datapipeline/')
    ])
def test_airflow_dags_paths(host, path):
    """
    Tests Airflow DAGs paths
    """
    current_path = host.file(path)

    assert current_path.exists
    assert current_path.is_directory


@pytest.mark.parametrize('path', [
    ('/var/lib/airflow/airflow/dags/funcake_dags/'),
    ])
def test_undefined_branch_airflow_dags_paths(host, path):
    """
    Tests that a dag without a defined branch is not deployed
    """
    current_path = host.file(path)

    assert not current_path.exists


@pytest.mark.parametrize('path,path_type,user,group,mode', [
    ('/var/log/airflow', 'directory', 'airflow', 'airflow', 0o700),
    ('/var/run/airflow', 'directory', 'airflow', 'airflow', 0o700),
    ('/etc/logrotate.d/airflow', 'file', 'root', 'root', 0o644)
    ])
def test_logging_paths(host, path, path_type, user, group, mode):
    """
    Tests Airflow logging & pid paths
    """
    current_path = host.file(path)

    assert current_path.exists

    if path_type == 'directory':
        assert current_path.is_directory
    elif path_type == 'file':
        assert current_path.is_file
    assert current_path.user == user
    assert current_path.group == group
    assert current_path.mode == mode


@pytest.mark.parametrize('path,user,group', [
    ('/var/lib/airflow/airflow/dags/cob_datapipeline/requirements.txt',
     'airflow', 'airflow')
    ])
def test_pipfile_create(host, path, user, group):
    """
    Tests DAG in defaults converts Pipfile to requirements.txt
    """
    current_path = host.file(path)

    assert current_path.exists
    assert current_path.is_file
    assert current_path.user == user
    assert current_path.group == group


@pytest.mark.parametrize('library', [
    ('xmltodict'),
    ('pexpect')
])
def test_dags_pip_libraries(host, library):
    """
    Test DAGs' required pip libraries installed
    """

    pip_path = "/var/lib/airflow/venv/bin/pip3.6"
    libraries = host.pip_package.get_packages(pip_path=pip_path)
    print(libraries)
    assert libraries.get(library)


@pytest.mark.parametrize('name', [
    ('gettext'),
    ('automake'),
    ('sqlite-devel')
])
def test_dag_system_packages(host, name):
    """
    Tests about airflow DAGs system packages
    """
    assert host.package(name).is_installed
