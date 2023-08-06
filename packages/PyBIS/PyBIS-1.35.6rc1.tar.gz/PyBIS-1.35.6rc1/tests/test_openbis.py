#   Copyright ETH 2018 - 2023 Zürich, Scientific IT Services
# 
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
#   
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
import re
import time

import pytest

from pybis import Openbis


def test_token(openbis_instance):
    assert openbis_instance.token is not None
    assert openbis_instance.is_token_valid(openbis_instance.token) is True
    assert openbis_instance.is_session_active() is True


def test_http_only(openbis_instance):
    with pytest.raises(Exception):
        new_instance = Openbis("http://localhost")
        assert new_instance is None

    new_instance = Openbis(
        url="http://localhost",
        allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True,
    )
    assert new_instance is not None


def test_cached_token(other_openbis_instance):
    assert other_openbis_instance.is_token_valid() is True

    other_openbis_instance.logout()
    assert other_openbis_instance.is_token_valid() is False


def test_create_perm_id(openbis_instance):
    permId = openbis_instance.create_permId()
    assert permId is not None
    m = re.search("([0-9]){17}-([0-9]*)", permId)
    ts = m.group(0)
    assert ts is not None
    count = m.group(1)
    assert count is not None


def test_get_samples_update_in_transaction(openbis_instance):
    """
        Update samples in transaction without overriding parents/children
    """
    name_suffix = str(time.time())
    # Create new space
    space = openbis_instance.new_space(code='space_name' + name_suffix, description='')
    space.save()

    # Create new project
    project = space.new_project(code='project_code' + name_suffix)
    project.save()

    # Create new experiment
    experiment = openbis_instance.new_experiment(
        code='MY_NEW_EXPERIMENT',
        type='DEFAULT_EXPERIMENT',
        project=project.code
    )
    experiment.save()

    # Create parent sample
    sample1 = openbis_instance.new_sample(
        type='YEAST',
        space=space.code,
        experiment=experiment.identifier,
        parents=[],
        children=[],
        props={"$name": "sample1"}
    )
    sample1.save()

    # Create child sample
    sample2 = openbis_instance.new_sample(
        type='YEAST',
        space=space.code,
        experiment=experiment.identifier,
        parents=[sample1],
        children=[],
        props={"$name": "sample2"}
    )
    sample2.save()

    # Verify samples parent/child relationship
    sample1 = openbis_instance.get_sample(
        sample_ident=sample1.identifier,
        space=space.code,
        props="*"
    )
    sample2 = openbis_instance.get_sample(
        sample_ident=sample2.identifier,
        space=space.code,
        props="*"
    )
    assert sample1.children == [sample2.identifier]
    assert sample2.parents == [sample1.identifier]

    trans = openbis_instance.new_transaction()
    # get samples that have parents and update name
    samples = openbis_instance.get_samples(space=space.code, props="*", withParents="*")
    for sample in samples:
        sample.props["$name"] = 'new name for sample2'
        trans.add(sample)
    # get samples that have children and update name
    samples = openbis_instance.get_samples(space=space.code, props="*", withChildren="*")
    for sample in samples:
        sample.props["$name"] = 'new name for sample1'
        trans.add(sample)
    trans.commit()

    # Verify that name has been changed and parent/child relationship remains
    sample1 = openbis_instance.get_sample(
        sample_ident=sample1.identifier,
        space=space.code,
        props="*"
    )
    sample2 = openbis_instance.get_sample(
        sample_ident=sample2.identifier,
        space=space.code,
        props="*"
    )
    assert sample1.props["$name"] == 'new name for sample1'
    assert sample1.children == [sample2.identifier]
    assert sample2.props["$name"] == 'new name for sample2'
    assert sample2.parents == [sample1.identifier]

    trans = openbis_instance.new_transaction()
    # get samples with attributes and change name
    samples = openbis_instance.get_samples(space=space.code, attrs=["parents", "children"])
    for sample in samples:
        sample.props["$name"] = "default name"
        trans.add(sample)
    trans.commit()

    # Verify that name has been changed and parent/child relationship remains
    sample1 = openbis_instance.get_sample(
        sample_ident=sample1.identifier,
        space=space.code,
        props="*"
    )
    sample2 = openbis_instance.get_sample(
        sample_ident=sample2.identifier,
        space=space.code,
        props="*"
    )
    assert sample1.props["$name"] == 'default name'
    assert sample1.children == [sample2.identifier]
    assert sample2.props["$name"] == 'default name'
    assert sample2.parents == [sample1.identifier]

    sample3 = openbis_instance.new_sample(
        type='YEAST',
        space=space.code,
        experiment=experiment.identifier,
        parents=[],
        children=[],
        props={"$name": "sample3"}
    )
    sample3.save()

    trans = openbis_instance.new_transaction()
    # get sample1 without attributes and add sample3 as a parent
    samples = openbis_instance.get_samples(space=space.code, identifier=sample1.identifier)
    for sample in samples:
        sample.add_parents([sample3.identifier])
        trans.add(sample)
    # get sample2 without attributes and remove sample1 as a parent
    samples = openbis_instance.get_samples(space=space.code, identifier=sample2.identifier)
    for sample in samples:
        sample.del_parents([sample1.identifier])
        trans.add(sample)
    trans.commit()

    # Verify changes
    sample1 = openbis_instance.get_sample(
        sample_ident=sample1.identifier,
        space=space.code,
        props="*"
    )
    sample2 = openbis_instance.get_sample(
        sample_ident=sample2.identifier,
        space=space.code,
        props="*"
    )
    sample3 = openbis_instance.get_sample(
        sample_ident=sample3.identifier,
        space=space.code,
        props="*"
    )
    assert sample1.children == []
    assert sample1.parents == [sample3.identifier]
    assert sample2.parents == []
    assert sample3.children == [sample1.identifier]


def test_failed_second_login_raises_exception(openbis_instance):
    """
        Logins to openBIS using wrong username/password, PyBIS should raise exception
    """
    assert openbis_instance.is_session_active() is True

    try:
        openbis_instance.login('non_existing_username_for_test', 'abcdef')
        # Login should fail at this point
        assert False
    except ValueError as e:
        assert str(e) == "login to openBIS failed"


def test_set_token_accepts_personal_access_token_object(openbis_instance):
    """
        Verifies that set_token method accepts both permId and PersonalAccessToken object
    """
    assert openbis_instance.is_session_active() is True

    pat = openbis_instance.get_or_create_personal_access_token(sessionName="Project A")

    openbis_instance.set_token(pat, save_token=True)
    openbis_instance.set_token(pat.permId, save_token=True)

def test_pat():
    """
        Verifies that set_token method accepts both permId and PersonalAccessToken object
    """
    from pybis import Openbis
    # base_url = "https://alaskowski:8443/"
    base_url = "http://127.0.0.1:8888/"
    base_url = "https://openbis-sis-ci-sprint.ethz.ch/"
    # base_url = "https://openbis-empa-lab000.ethz.ch"
    openbis_instance = Openbis(
        url=base_url,
        verify_certificates=False,
        allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True
    )

    token = openbis_instance.login('admin', 'changeit')
    # pat = openbis_instance.get_or_create_personal_access_token(sessionName="Project A")
    print(token)

    samples = openbis_instance.get_samples(space='DEFAULT')
    print(samples)
    print("AAA")
    # # pluggy = openbis_instance.get_plugin('AA.NEW_PLUGIN')
    # # pluggy2 = openbis_instance.get_plugin('14')
    #
    # plugin_name = 'AA.NEW_PLUGIN'
    # # pl = openbis_instance.new_plugin(
    # #     name=plugin_name,
    # #     pluginType='DYNAMIC_PROPERTY',  # or 'DYNAMIC_PROPERTY' or 'MANAGED_PROPERTY',
    # #     entityKind='SAMPLE',  # or 'SAMPLE', 'MATERIAL', 'EXPERIMENT', 'DATA_SET'
    # #     script='def validate(x, True):\n\treturn True'  # a JYTHON script
    # # )
    # # pl.save()
    # #
    # # pt = openbis_instance.new_property_type(
    # #     code='SOME_FANCY_PROPERTY',
    # #     label='otrs ticket test',
    # #     description='otrs ticket test',
    # #     dataType='VARCHAR',
    # # )
    # # pt.save()
    #
    # code = 'aaa_my_own_sample_type_1'
    # # sample_type = openbis_instance.new_sample_type(
    # #     code=code,  # mandatory
    # #     generatedCodePrefix='S-',  # mandatory
    # #     autoGeneratedCode=True
    # # )
    # # sample_type.save()
    # i = 0
    # while i < 1000:
    #     i = i+1
    #     sample_type = openbis_instance.get_sample_type(code)
    #     # ass = sample_type.get_property_assignments()[['propertyType', 'plugin']]
    #     # print(ass)
    #
    #     property_code = 'SOME_FANCY_PROPERTY'
    #     # property_code = '$BARCODE'
    #     # barcode = openbis_instance.get_property_type('$BARCODE')
    #     prop_type = openbis_instance.get_property_type(property_code)
    #
    #     assignments = sample_type.get_property_assignments()
    #     print("BEFORE")
    #     print(assignments)
    #
    #     # sample_type.assign_property('$NAME', section='General info', ordinal=2,
    #     #                             initialValueForExistingEntities='')
    #
    #     # plug = openbis_instance.get_plugin(plugin_name).name
    #     sample_type.assign_property(prop_type, section='General info', ordinal=2,
    #                                 initialValueForExistingEntities='')
    #
    #     assignments = sample_type.get_property_assignments()
    #     print("DURING")
    #     print(assignments)
    #
    #
    #     # sample = openbis_instance.new_sample(
    #     #     type=sample_type.code,
    #     #     space='DEFAULT',
    #     #     experiment='/DEFAULT/DEFAULT/DEFAULT'
    #     #     # props={"$name": "some name"}
    #     # )
    #     # sample.save()
    #
    #     try:
    #         sample = openbis_instance.get_samples(type=sample_type.code)[0]
    #         sample.props[property_code.lower()] = '123'
    #     # sample.save()
    #     except Exception as e:
    #         print(e)
    #
    #
    #     # ass = sample_type.get_property_assignments().df[['propertyType', 'plugin']]
    #     # print(ass)
    #     sample_type = openbis_instance.get_sample_type(code)
    #     # ass = sample_type.get_property_assignments().df[['propertyType', 'plugin']]
    #     # print(ass)
    #
    #     sample_type.revoke_property(property_code, force=True)
    #
    #     assignments_after = sample_type.get_property_assignments()
    #     print("AFTER")
    #     print(assignments_after)
    #     ass = sample_type.get_property_assignments().df[['propertyType', 'plugin']]
    #     print(ass)
    #
    # # sample = openbis_instance.new_sample(
    # #     type=sample_type.code,
    # #     space='DEFAULT',
    # #     experiment='/DEFAULT/DEFAULT/DEFAULT'
    # #     # props={"$name": "some name"}
    # # )
    # # sample.save()
    # #
    # #
    # #
    # # # sample = openbis_instance.get_samples(type=sample_type.code)[0]
    # # sample.props['$barcode'] = 'FEDCBA'
    # # sample.save()
    # #
    # # sample2 = openbis_instance.get_samples(type=sample_type.code)[0]
    # # print(sample2.props)
    #
    # # ps = sample_type.get_property_assignments() # [['propertyType', 'plugin']]
    # # print(ps.df)
    # #
    # # # pl = openbis_instance.new_plugin(
    # # #     name='my_new_entry_validation_plugin_2',
    # # #     pluginType='ENTITY_VALIDATION',  # or 'DYNAMIC_PROPERTY' or 'MANAGED_PROPERTY',
    # # #     entityKind=None,  # or 'SAMPLE', 'MATERIAL', 'EXPERIMENT', 'DATA_SET'
    # # #     script='def calculate(): pass'  # a JYTHON script
    # # # )
    # # # pl.save()
    # # pl = openbis_instance.get_plugin('my_new_entry_validation_plugin_2')
    # # # print(pl.name)
    # # # print(pl.permId)
    # #
    # # sample_type.assign_property(barcode, section='General info', ordinal=2,
    # #                             initialValueForExistingEntities='', plugin='my_new_entry_validation_plugin_2')
    # #
    # # sample_type = openbis_instance.get_sample_type('aaa_my_own_sample_type')
    # # print(sample_type.df)

    print("END")

def test_new_sample_user_rights():
    from pybis import Openbis
    # base_url = "https://alaskowski:8443/"
    base_url = "http://127.0.0.1:8888/"
    # base_url = "https://openbis-sis-ci-sprint.ethz.ch/"
    # base_url = "https://openbis-empa-lab000.ethz.ch"
    openbis_instance = Openbis(
        url=base_url,
        verify_certificates=False,
        allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True
    )

    token = openbis_instance.login('admin', 'changeit')
    # pat = openbis_instance.get_or_create_personal_access_token(sessionName="Project A")
    print(token)

    exp = openbis_instance.get_experiment("20230607102400512-23")

    # samples = openbis_instance.get_samples(space='TEST_SPACE')
    # print(samples)
    #
    # sample = openbis_instance.new_sample(
    #     type='ENTRY',
    #     space='TEST_SPACE',
    #     # project='/TEST_SPACE/PROJECT_101',
    #     experiment='/TEST_SPACE/PROJECT_101/PROJECT_101_EXP_1',
    #     props={"$name": "some name"}
    # )
    # sample.save()


    print("END")
