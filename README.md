# TU Libraries Ansible Role for Building Airflow

[![Build Status](https://img.shields.io/travis/tulibraries/ansible-role-airflow/master.svg?label=travis_master)](https://travis-ci.org/tulibraries/ansible-role-airflow)
[![Ansible Role](https://img.shields.io/ansible/role/39140.svg)](https://galaxy.ansible.com/tulibraries/ansible_role_airflow)

Ansible role to manage Airflow installation and configuration with limited support for DAG retrieval and Operators (worker) environment setup.

## Breaking changes

To be filled in. This is originally a fork from https://github.com/infOpen/ansible-role-airflow, but separated into own repository given breaking changes setting up Airflow 1.10.x features and DAGs support.

## Requirements

This role requires Ansible 2.4 or higher, and platform requirements are listed in the metadata file.

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Local and Travis tests run tests on Docker by default. See molecule documentation to use other backend.

Currently, tests are done on:
- Centos 7
- Debian Stretch
- Ubuntu Xenial
- Ubuntu Bionic

and use:
- Ansible 2.4.x
- Ansible 2.5.x

### Running tests

#### Using Docker driver

```
$ pip install pipenv
$ pipenv install
$ pipenv run molecule test
```

Note: currently testing skips the idempotency checks, given work required to have Airflow database upgrades pass the Ansible requirements for idempotency.

## Role Variables

> **Warning**
> No Fernet key defined on configuration, so set your own before store passwords !

### Default role variables

This needs to be rewritten. Currently, see the `defaults/main.yml` for the variables expected for Airflow and Airflow Worker configurations.

## Dependencies

None

## Example Playbook

``` yaml
- hosts: airflow
  become: yes
  roles:
  - role: tulibraries.airflow
```

## License

MIT
