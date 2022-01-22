#!/usr/bin/env python3
from setuptools import setup

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'skill-WTvFDigitalGrindhouseDriveIn.jarbasai=skill_WTvFDigitalGrindhouseDriveIn:WTvFDigitalGrindhouseDriveInSkill'

setup(
    # this is the package name that goes on pip
    name='ovos-skill-WTvFDigitalGrindhouseDriveIn',
    version='0.0.1',
    description='ovos WTvFDigitalGrindhouseDriveIn skill plugin',
    url='https://github.com/JarbasSkills/skill-WTvFDigitalGrindhouseDriveIn',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    package_dir={"skill_WTvFDigitalGrindhouseDriveIn": ""},
    package_data={'skill_WTvFDigitalGrindhouseDriveIn': ['locale/*', 'ui/*']},
    packages=['skill_WTvFDigitalGrindhouseDriveIn'],
    include_package_data=True,
    install_requires=["ovos_workshop~=0.0.5a1"],
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
