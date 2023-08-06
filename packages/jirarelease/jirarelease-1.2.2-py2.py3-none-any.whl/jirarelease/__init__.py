"""
This is a example for jira release
"""
__version__ = "1.2.2"

import os
from datetime import datetime, timezone, timedelta
import pkg_resources
from jira import JIRA
import re
from loguru import logger


class DailyReleaseModel:
    
    date_format = '%Y.%m.%d'
    
    @staticmethod
    def match_version(version: str, label: str):    
        semver_pattern = "^\d+\.\d+\.\d+-##REPLACE_ME##\.\d{4}\.\d{2}\.\d{2}$".replace("##REPLACE_ME##", label)
        return True if re.match(semver_pattern, version) else False

    @staticmethod
    def to_date(versions: list) -> list:
        _versions = []
        for version in versions:
            pattern = re.compile(r"\d{4}\.\d{2}\.\d{2}$")
            match = pattern.search(version)
            if match:
                _versions.append(match.group())
        return _versions
    
    def __init__(self, vers: list, base_version: str, eod_hour: int, label: str)-> dict:
        version = {}
        today_date = datetime.now(timezone(offset=timedelta(hours=eod_hour))).strftime(self.date_format)
        matched_version = [v for v in vers if self.match_version(v, label)]

        logger.info("Getting matched versions:")
        logger.info(matched_version)
        if matched_version:
            for v in matched_version:
                arr = v.split('-')
                version.setdefault(arr[0], set())
                version[arr[0]].add(arr[1])
                
            latest_ver = max(version.keys(), key=pkg_resources.parse_version)
            latest_date = max(self.to_date(version[latest_ver]), key=lambda d: datetime.strptime(d, self.date_format))
        else:
            latest_ver = base_version
            latest_date = today_date
        
        self.today_ver = f"{latest_ver}-{label}.{today_date}"
        logger.info("today version: " + self.today_ver)

        self.latest_ver = f"{latest_ver}-{label}.{latest_date}"
        logger.info("latest version: " +self.latest_ver)
        
        self.today_date = today_date
        logger.info("today date: " +self.today_date)
    
    def daily_version(self)-> str:
        return self.today_ver
    
    def semantic_version(self):
        return self.daily_version().split('-')[0]
    
    def has_unreleased_version(self):
        return self.today_ver != self.latest_ver

        
class JiraTimeBasedDailyRelease:
    
    def __init__(self, base_version: str, eod_hour=11, domain: str=None, email: str=None, secret: str=None):
        self.base_version = base_version
        self.eod_hour = eod_hour
        
        jira_domain = domain or os.getenv("JIRA_DOMAIN")
        jira_email = email or os.getenv("JIRA_EMAIL")
        jira_secret = secret or os.getenv("JIRA_SECRET")
        
        self.jira = JIRA("https://" + jira_domain, basic_auth=(jira_email, jira_secret))
        
    def _create_versions(self, jira_project: str, model: DailyReleaseModel, versions: list):
        
        sem_versions = [v for v in versions if v.name == model.semantic_version()]
        daily_versions = [v for v in versions if v.name == model.daily_version()]
        
        s_version = self.jira.create_version(
            project=jira_project, 
            name=model.semantic_version()
        )if not sem_versions else sem_versions[0]
        
        d_version = self.jira.create_version(
            project=jira_project, 
            name=model.daily_version()
        )if not daily_versions else daily_versions[0]
        
        return s_version, d_version
        
    def include_issue(self, jira_issue: str, release_previous=True, label='rc'):
        issue = self.jira.issue(jira_issue)
        project = jira_issue.split('-')[0]
        
        versions = self.jira.project_versions(project)
        version_names = [v.name for v in versions]
        logger.info("all assigned version: ")
        logger.info(version_names)

        model = DailyReleaseModel(
            vers=version_names, 
            base_version=self.base_version, 
            eod_hour=self.eod_hour,
            label=label
        )
        
        assignable_versions = set(self._create_versions(project, model, versions))
        existing_versions = set(issue.get_field("fixVersions"))
        existing_versions = existing_versions - assignable_versions
        
        assignable_versions = list(assignable_versions)
        assignable_versions.extend(list(existing_versions))
        logger.info(assignable_versions)
        
        fix_vers = [{'id': v.id} for v in assignable_versions]
        logger.info("Updating issue: " + issue.key + " to versions: ")
        logger.info(fix_vers)
        
        issue.update(fields={'fixVersions': fix_vers})
            
        if release_previous and model.has_unreleased_version():
            latest_version = [v for v in versions if v.name == model.latest_ver][0]
            logger.info("Releasing previous version: " + latest_version.name)
            latest_version.update(released=True)
