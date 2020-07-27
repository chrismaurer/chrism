#!/usr/bin/env python2.7
# -*- mode: python -*-
###########################################################################
#
#                  Unpublished Work Copyright (c) 2018
#                  Trading Technologies International, Inc.
#                       All Rights Reserved Worldwide
#
#          * * *   S T R I C T L Y   P R O P R I E T A R Y   * * *
#
# WARNING:  This program (or document) is unpublished, proprietary property
# of Trading Technologies International, Inc. and is to be maintained in
# strict confidence. Unauthorized reproduction, distribution or disclosure
# of this program (or document), or any program (or document) derived from
# it is prohibited by State and Federal law, and by local law outside of
# the U.S.
#
############################################################################
import os
import re
import sys
import time
import uuid
import itertools
from distutils.version import StrictVersion
from ttjenkins import TTJenkins
from bcolors import bcolors
from sh import git, ErrorReturnCode
from subprocess import check_output, call
from debesys_chef_api import DebesysChefAPI
from debesys_logging import DebesysLogging
from add_environment_version_constraints import ChefEnvironmentCookbookVersions
from argparse import RawTextHelpFormatter, ArgumentParser
from bump_cookbook import CookbookTargets
from distutils.version import StrictVersion
from spinner import Spinner
from itertools import izip_longest
import multiprocessing
from multiprocessing import Pool


def upload_environment(chef_organization, repo_root, environment):
    result = True
    log_prefix = "pid {0}".format(os.getpid())
    logger = multiprocessing.get_logger()
    logger.info("{0} | Uploading environment '{1}' to Chef Org '{2}'.".format(log_prefix, environment, chef_organization))
    try:
        capi = DebesysChefAPI(chef_organization, repo_root, logger, 20, 3)
        capi.environment_upload(environment + ".rb")
    except Exception as ex:
        logger.error("{0} | Failed to upload environment {1}.".format(log_prefix, environment), exc_info=True)
        result = False

    logger.info("{} | Result of uploading environment '{}' to '{}' was '{}'.".format(
        log_prefix, environment, chef_organization, result))
    return result


class UpdateEnvironment(object):
    def __init__(self,
                 branch,
                 cookbook,
                 target,
                 reason,
                 environment,
                 skip_confirm,
                 support_locks,
                 version,
                 sync_release,
                 log_dir,
                 no_upload,
                 rollback,
                 jenkins_user,
                 token,
                 only_add_missing,
                 query=None,
                 stdout=False,
                 verbose=False
                 ):
        self.branch = branch
        self.cookbook = cookbook
        self.target = target
        self.reason = reason
        self.environment = environment
        self.skip_confirm = skip_confirm
        self.support_locks = support_locks
        self.version = version
        self.stdout = stdout
        self.verbose = verbose
        self.sync_release = sync_release
        self.env = os.environ
        self.log_dir = log_dir
        self.no_upload = no_upload
        self.rollback = rollback
        self.jenkins_user = jenkins_user
        self.token = token
        self.query = query
        self.only_add_missing = only_add_missing
        self.log = DebesysLogging("update_environment.log", stdout, not verbose, log_dir=log_dir,
                                     use_multiprocess_logger=True)
        self.repo_root = self.run("git rev-parse --show-toplevel")
        self.spinner = Spinner()
        ext_targeted = False
        self.ext_write_access = False
        self.int_capi = DebesysChefAPI('int', self.repo_root, self.log)
        for env in self.environment:
            if env.startswith("ext"):
                ext_targeted = True
        if ext_targeted:
            if os.path.isfile("{0}/.chef/knife.external-read.rb".format(os.path.expanduser("~"))) or os.path.isfile("{0}/.chef/knife.external.rb".format(os.path.expanduser("~"))):
                self.ext_capi = DebesysChefAPI('ext', self.repo_root, self.log)
                self.ext_write_access = self.ext_capi.write_test()
            else:
                print(bcolors.get("red") + "It looks like you are trying to update external environments without external chef access!\n"
                      "Please open a hotfix at go/hotfix and the deployment team will take care of this update for you."+ bcolors.get("endc"))
                sys.exit(1)

        # Set api object fot ttsdk chef org if it is present
        self.ttsdk_capi = None
        if os.path.isfile("{0}/.chef/knife.ttsdk.rb".format(os.path.expanduser("~"))):
            self.ttsdk_capi = DebesysChefAPI('ttsdk', self.repo_root, self.log)

        if "PRE_RUN_PATH" in self.env:
            self.env['PATH'] = self.env['PRE_RUN_PATH']

        envs = ["LD_LIBRARY_PATH", "PYTHONPATH", "PYTHONHOME"]
        for env in envs:
            if env in self.env:
                del self.env[env]

        worker_count = multiprocessing.cpu_count() * 4
        self.pool = Pool(processes=worker_count)

        if self.sync_release:
            self.perform_sync()
        else:
            self.perform_updates()


    def upload_environments(self, environments):
        upload_environment_results = list()
        envs_for_jenkins = set()
        self.spinner.start("Uploading Chef environments")

        for env in environments:
            chef_org = 'int'
            if env.startswith('ext'):
                chef_org = 'ext'

            if(chef_org == 'int' or (chef_org == 'ext' and self.ext_write_access)):
                upload_environment_results.append(self.pool.apply_async(
                    upload_environment, kwds = {'chef_organization': chef_org,
                                                'repo_root': self.repo_root,
                                                'environment': env}))
            else:
                envs_for_jenkins.add(env)

            if self.ttsdk_capi:
                upload_environment_results.append(self.pool.apply_async(
                    upload_environment, kwds = {'chef_organization': 'ttsdk',
                                                'repo_root': self.repo_root,
                                                'environment': env}))
            else:
                envs_for_jenkins.add(env)

        # Examine the results once they are all ready.
        finished = False if len(upload_environment_results) > 0 else True
        while not finished:
            finished = True
            for item in upload_environment_results:
                if not item.ready():
                    finished = False
                    break
            if not finished:
                time.sleep(1)

        at_least_one_failed = False
        for item in upload_environment_results:
            if not item.get():
                at_least_one_failed = True
                break

        if at_least_one_failed:
            self.spinner.fail()
        else:
            self.spinner.stop()

        self.pool.close()
        self.pool.join()
        self.pool = None

        if len(envs_for_jenkins) > 0:
            self.external_chef_upload(envs_for_jenkins)


    def perform_updates(self):
        # Check if provided a release_branch:
        release_pattern = re.compile("release_v\d+\/current")
        on_release = False
        if self.branch != 'master':
            self.spinner.start("Switching to 'master' branch to validate provided environments")
            # Validate and build list of environments
            if not self.checkout_branch('master'):
                self.spinner.fail()
                print(bcolors.get("red") + "Oops! An Error occured while trying to checkout the branch 'master' on git!\n"
                                  "for more information please check the log at /var/log/debesys/update_environment.log" + bcolors.get("endc"))
                sys.exit(1)
            self.spinner.stop()
        environment_list=self.get_environment_list()
        # Get cookbook version and update environments
        if not self.version:
            if release_pattern.match(self.branch):
                on_release = True
            self.spinner.start("Switching to '{0}' branch to get latest cookbook versions".format(self.branch))
            if not self.checkout_branch(self.branch):
                self.spinner.fail()
                print(bcolors.get("red") + "Oops! An Error occured while trying to checkout the branch {0} on git!\n"
                                  "for more information please check the log at /var/log/debesys/update_environment.log".format(self.branch) + bcolors.get("endc"))
                sys.exit(1)
            self.spinner.stop()
        cookbook_data = {}
        if self.target:
            target_cookbooks = []
            for target in self.target:
                self.spinner.start("Looking up cookbooks in target '{0}'.".format(target))
                target_lookup = CookbookTargets(self.repo_root).get_cookbooks(target)
                if not target_lookup:
                    self.spinner.fail()
                    print("\n{0}{1}Provided target '{2}' is an invalid target, aborting environment update!{3}\n".format(bcolors.get("bold"), bcolors.get("red"), target, bcolors.get("endc")))
                    sys.exit(1)
                target_cookbooks = target_cookbooks + target_lookup
                self.spinner.stop()
            if self.cookbook:
                complete_list = target_cookbooks + list(set(self.cookbook) - set(target_cookbooks))
                self.cookbook = complete_list
            else:
                self.cookbook = target_cookbooks

        # Verify Cookbook Exists on the Chef Server(s)
        int_srv=ext_srv=False
        self.environment_str=" AND ("
        for env in environment_list:
            if env.startswith('int'):
                int_srv = True
            if env.startswith('ext'):
                ext_srv = True
            self.environment_str += "chef_environment:{} OR".format(env)

            if env.startswith('ext'):
                self.chef_api=self.ext_capi
            else:
                self.chef_api=self.int_capi
            self.environment_str=self.environment_str[:-3] + ")"
            if env.startswith('ext'):
                chef_api=self.ext_capi
            else:
                chef_api=self.int_capi


        missing_in_envs = {}
        for cookbook in self.cookbook:
            if self.version:
                cb_version = self.version
            else:
                cb_version = self.get_cookbook_version(cookbook)
                if on_release and cb_version:
                    release_num = self.branch.replace("release_v", "").replace("/current", "")
                    if "." + release_num + "." not in cb_version:
                        print(bcolors.get("red") + "ERROR: The cookbook provided '{0}' is not a part of the provided release!".format(cookbook) + bcolors.get("endc"))
                        sys.exit(1)
            if cb_version:
                if int_srv:
                    self.spinner.start("Verifying version '{0}' of '{1}' exists on the Internal Chef Server".format(cb_version, cookbook))
                    if not self.check_cookbook_exists('int', cookbook, cb_version):
                        self.spinner.fail()
                        print(bcolors.get("red") + "\nERROR: Version '{0}' of the cookbook '{1}' is not on the Internal Chef Server!\n".format(cb_version, cookbook) + bcolors.get("endc"))
                        sys.exit(1)
                    self.spinner.stop()
                if ext_srv:
                    self.spinner.start("Verifying version '{0}' of '{1}' exists on the External Chef Server".format(cb_version, cookbook))
                    if not self.check_cookbook_exists('ext', cookbook, cb_version):
                        self.spinner.stop()
                        print(bcolors.get("red") + "\nERROR: Version '{0}' of the cookbook '{1}' is not on the External Chef Server!\n".format(cb_version, cookbook) + bcolors.get("endc"))
                        sys.exit(1)
                    self.spinner.stop()
                cookbook_data.update({cookbook: cb_version})
                big_data = None
                if self.support_locks:
                    big_data = self.get_version(self.cookbook, environment_list)
            cb_missing = self.check_cookbook_in_environments(cookbook, environment_list)
            if cb_missing:
                missing_in_envs.update(cb_missing)

        if not cookbook_data:
            print(bcolors.get("red") + "ERROR: No valid cookbooks found for this environment!" + bcolors.get("endc"))
            sys.exit(1)
        if self.branch != 'master':
            self.spinner.start("Switching to 'master' branch to make environment file changes")
            # Validate and build list of environments
            if not self.checkout_branch('master'):
                self.spinner.fail()
                print(bcolors.get("red") + "Oops! An Error occured while trying to checkout the branch 'master' on git!\n"
                                  "for more information please check the log at /var/log/debesys/update_environment.log" + bcolors.get("endc"))
                sys.exit(1)
            self.spinner.stop()
        environment_list=self.get_environment_list()

        if not self.skip_confirm:
            self.confirm_changes(self.branch, cookbook_data, environment_list, missing_in_envs, big_data)
        if self.support_locks:
            self.remove_lock(big_data, self.cookbook, environment_list, cookbook_data)
            self.add_lock(big_data, self.cookbook, environment_list, cookbook_data)
        if not self.only_add_missing:
            self.update_environments(environment_list, cookbook_data)
        failed_envs = []
        if missing_in_envs:
            for cb, envs in missing_in_envs.iteritems():
                self.spinner.start("Adding {0} cookbook to missing environments".format(cb))
                try:
                    cb_version = cookbook_data[cb]
                    dev_envs = []
                    ver_envs =[]
                    for e in envs:
                        if "int-dev" in e:
                            dev_envs.append(e)
                        else:
                            ver_envs.append(e)
                    environment_versions = ChefEnvironmentCookbookVersions([cb], cb_version, ver_envs)
                    environment_versions.run(stdout=False)
                    if dev_envs:
                        environment_versions = ChefEnvironmentCookbookVersions([cb], None, dev_envs)
                        environment_versions.run(stdout=False)
                except:
                    self.cleanup()
                    self.spinner.fail()
                    print(bcolors.get("red") + "Oops! An Error occured while trying to add new cookbook {0} to the environments ({1})\n".format(cb, ', '.join(environment_list)) + bcolors.get("endc"))
                    sys.exit(1)
                self.spinner.stop()
        self.spinner.start("Updating Environment Files (on git)")
        push_result = self.push_environment_changes(environment_list)
        if not push_result:
            self.spinner.fail()
            print(bcolors.get("red") + "Oops! An Error occured while trying to update the {0} environment file on git!\n"
                  "for more information please check the log at /var/log/debesys/update_environment.log".format(', '.join(environment_list)) + bcolors.get("endc"))
        else:
            self.spinner.stop()
            if push_result == "No Changes":
                print(bcolors.get("yellow") + 'Note: Environment file for {0} was already up to date!'.format(', '.join(environment_list)) + bcolors.get("endc"))
            if not self.no_upload:
                self.upload_environments(environment_list)
            else:
                print(bcolors.get("yellow") + "--no-upload was provided. The environment files will not be uploaded to the chef server.\n" + bcolors.get("endc"))


    def perform_sync(self):
        # Lookup Latest Release Versions
        environment_list=self.get_environment_list()
        release_updates = self.update_releases(environment_list)
        cb_versions_to_check = {}
        for env, release_info in release_updates.iteritems():
            for release_num, release_cbs in release_info.iteritems():
                if release_num not in cb_versions_to_check:
                    cb_versions_to_check[release_num]=[]
                for cb in release_cbs:
                    if cb not in cb_versions_to_check[release_num]:
                        cb_versions_to_check[release_num].append(cb)
        cb_versions = {}
        for branch, cb_list in cb_versions_to_check.iteritems():
            release_branch = "release_v{0}/current".format(branch)
            print("Switching to '{0}' branch to get latest cookbook versions".format(release_branch))
            if not self.checkout_branch(release_branch):
                print(bcolors.get("red") + "Oops! An Error occured while trying to checkout the branch {0} on git!\n"
                                  "for more information please check the log at /var/log/debesys/update_environment.log".format(release_branch) + bcolors.get("endc"))
                sys.exit(1)

            for cb in cb_list:
                cb_version = self.get_cookbook_version(cb)
                if cb_version:
                    if branch not in cb_versions:
                        cb_versions[branch]={}
                    cb_versions[branch].update({cb: cb_version})
        env_cookbook_updates = {}
        for env, release_info in release_updates.iteritems():
            cookbook_data = {}
            for release_num, release_cbs in release_info.iteritems():
                for cb in release_cbs:
                    if release_num in cb_versions:
                        if cb in cb_versions[release_num]:
                            cb_version = cb_versions[release_num][cb]
                            cookbook_data.update({cb: cb_version})
            if cookbook_data:
                env_cookbook_updates[env] = cookbook_data

        if not env_cookbook_updates:
            print(bcolors.get("red") + "No cookbooks on release versions found in provided environments! Will now exit." + bcolors.get("endc"))
            sys.exit(1)

        # Release Update Confirmation
        print("{0}{1}Attention: Before the release versions are updated, please confirm this is what you are expecting.\n"
              "The following cookbooks will be upgraded to the following versions in the following environments:{2}".format(bcolors.get("bold"), bcolors.get("red"), bcolors.get("endc")))
        for env, cookbook_data in env_cookbook_updates.iteritems():
            print(bcolors.get("yellow") + env + ":" + bcolors.get("endc"))
            for cookbook, cb_version in cookbook_data.iteritems():
                print(bcolors.get("blue") + "\t\t{0} => {1}".format(cookbook, cb_version) + bcolors.get("endc"))
        if not self.skip_confirm:
            input = raw_input("\nEnter 'y' if you wish to proceed: ")
            if not input.lower().startswith("y"):
                abort_msg = ("User Aborted Environment File Updates!")
                self.log.info(abort_msg)
                if not self.log.get_stdout():
                    print("\n{0}{1}{2}{3}\n".format(bcolors.get("bold"), bcolors.get("red"), abort_msg, bcolors.get("endc")))
                sys.exit(1)
            else:
                print (" ")


        # Get on master to make changes
        self.spinner.start("Switching to 'master' branch to make environment file changes")
        if not self.checkout_branch('master'):
            self.spinner.fail()
            print(bcolors.get("red") + "Oops! An Error occured while trying to checkout the branch 'master' on git!\n"
                              "for more information please check the log at /var/log/debesys/update_environment.log" + bcolors.get("endc"))
            sys.exit(1)
        self.spinner.stop()

        failed_envs = []
        # Update Environment Files
        for env, cookbook_data in env_cookbook_updates.iteritems():
            self.update_environments(env.split(), cookbook_data)

            # Push Environment File Changes
            self.spinner.start("Updating {0}.rb Environment File (on git)".format(env))
            push_result = self.push_environment_changes(environment_list)
            if not push_result:
                self.spinner.fail()
                print(bcolors.get("red") + "Oops! An Error occured while trying to update the {0} environment file on git!\n"
                      "for more information please check the log at /var/log/debesys/update_environment.log".format(env) + bcolors.get("endc"))
            else:
                if push_result == "No Changes":
                    self.spinner.stop()
                else:
                    self.spinner.stop()
                if not self.no_upload:
                    if env.startswith("ext-"):
                        try:
                            self.spinner.start("Uploading {0}.rb to external chef".format(env))
                            self.ext_capi.environment_upload(env + '.rb')
                            self.spinner.stop()
                        except:
                            if env not in failed_envs:
                                failed_envs.append(env)
                            self.spinner.fail()
                    elif env.startswith("int-"):
                        self.spinner.start("Uploading {0}.rb to internal chef".format(env))
                        self.int_capi.environment_upload(env + '.rb')
                        self.spinner.stop()
                    else:
                        print(bcolors.get("yellow") + "Unable to identify int/ext information for environment '{0}' upload will be skipped!\n".format(env) + bcolors.get("endc"))
                    if self.ttsdk_capi:
                        try:
                            self.spinner.start("Uploading {0}.rb to ttsdk chef".format(env))
                            self.ttsdk_capi.environment_upload(env + '.rb')
                            self.spinner.stop()
                        except:
                            if env not in failed_envs:
                                failed_envs.append(env)
                            self.spinner.fail()
                else:
                    print(bcolors.get("yellow") + "--no-upload was provided. The environment '{0}' will not be uploaded to the chef server.\n".format(env) + bcolors.get("endc"))
                if push_result == "No Changes":
                    print(bcolors.get("yellow") + "No git changes were made to '{0}.rb'. Current Environment Files have been uploaded.".format(env) + bcolors.get("endc"))
                else:
                    print(bcolors.get("green") + "Successfully Updated {0} Environment File!\n".format(env) + bcolors.get("endc"))
        # Kick any upload failures to Jenkins
        if failed_envs:
            self.external_chef_upload(failed_envs)

    def external_chef_upload(self, failed_envs):
        attempt = 1
        max_retry = 6
        sleep_between_retry = 2

        job = TTJenkins(user=self.jenkins_user, token=self.token,
                        verbose=False, verbose_timestamps=False,
                        logger=self.log, allow_output_to_console=False)
        parameters = {'ENVIRONMENTS': " ".join(failed_envs)}
        message = ("{}Uh no!{} {}There was a problem telling Jenkins to upload your cookbooks to the external\n"
                   "Chef server.  Please email the deployment team and provide the exact command you just ran\n"
                   "and the branch so someone can upload the cookbooks and debug why the Jenkins request failed."
                   "".format(bcolors.get("red"), bcolors.get("endc"), bcolors.get("cyan"), bcolors.get("endc")))

        while(attempt <= max_retry):
            try:
                self.spinner.start("Attempting to upload environments via Jenkins")
                parameters['GUID'] = str(uuid.uuid4())
                result = job.launch_job(job="environment-upload-external", params=parameters, wait=True)
                self.log.info("Started Jenkins job cookbook-upload-external with "
                                 "parameters: {0}, result was '{1}'.".format(parameters, result))
                if not result:
                    raise Exception("External environment upload Jenkins launch failure.")
                break # Success, leave the while loop.
            except Exception:
                self.spinner.fail()
                attempt += 1
                if attempt > max_retry:
                    return message
                self.log.warning("Failed to launch; no environment upload via Jenkins "
                                    "(attempt {} of {}).".format(attempt, max_retry), exc_info=True)
                time.sleep(sleep_between_retry)
        self.spinner.stop()
        return None


    def get_version(self, cookbooks, environment_list):
        big_data={}
        for e in environment_list:
            big_data.update({e:{}})
            for c in cookbooks:
                big_data[e].update({c:{}})
        for e in environment_list:
            if self.query:
                provided_query = self.query
                provided_nodes = self.chef_api.search_environment(e, additional_criteria=provided_query)
            else:
                provided_nodes={}
            for c in cookbooks:
                query = "deployed_cookbooks:{0} AND chef_environment:{1} AND NOT run_list:*{0}\:\:noop@0.*".format(c,e)
                nodes = self.chef_api.search_environment(e, additional_criteria=query)
                big_data[e][c]={}
                for n in nodes:
                    in_query = False
                    for p in provided_nodes:
                        if p['name'] == n['name']:
                            in_query = True
                            break
                    big_data[e][c].update({n["name"]:{}})
                    current_version = n['automatic']['cookbooks'][c]['version']
                    name = n['name']
                    version = current_version
                    is_locked = False
                    locked_ver = ""
                    for rl in n['run_list']:
                        if "{0}::noop@".format(c) in rl:
                            is_locked = True
                            locked_ver = rl.split("@")[1].replace("]","")
                    big_data[e][c][n['name']]={'is_locked': is_locked, 'version': version, 'in_query': in_query, 'locked_ver': locked_ver}
        return big_data


    def add_lock(self, big_data, cookbooks, environment_list, cookbook_data):
        for e, c in itertools.product(environment_list, cookbooks):
            for node_name, node_data in big_data[e][c].iteritems():
                if self.query and (StrictVersion(node_data['version']) != StrictVersion(cookbook_data[c])):
                    if not node_data['is_locked'] and not node_data['in_query'] and not node_data['version'] == '1000000.0.0':
                        recipe = [c + "::noop@" + node_data['version']]
                        self.chef_api.add_to_runlist(node_name = node_name, run_list = recipe)


    def remove_lock(self, big_data, cookbooks, environment_list, cookbook_data):
        for e, c in itertools.product(environment_list, cookbooks):
            for node_name, node_data in big_data[e][c].iteritems():
                if node_data['is_locked'] and not node_data['version'].startswith('0.'):
                    if StrictVersion(node_data['version']) < StrictVersion(cookbook_data[c]):
                        if (self.query and node_data['in_query']) or not self.query:
                            if node_data['locked_ver']:
                                version = node_data['locked_ver']
                            else:
                                version = node_data['version']
                            recipe = ["recipe[" + c + "::noop@" + version + "]"]
                            result=self.chef_api.remove_from_runlist(node_name, recipe)


    def get_current_version(self, cookbook, environment):
        regex_cookbook_ver = "\"{0}\" .+\".+\s(.+?)\"".format(cookbook)
        env_path = os.path.join(self.repo_root, "deploy/chef/environments")
        env_file = os.path.join(env_path, "{0}.rb".format(environment))
        with open(env_file) as env_read:
            for line in env_read:
                ver_search = re.search(regex_cookbook_ver, line)
                if ver_search and ('{' not in line):
                    cb_ver = ver_search.group(1)
                    return cb_ver
        return ""


    def check_cookbook_in_environments(self, cookbook, environment_list):
        regex_cookbook_ver = ".*\"{0}\".*".format(cookbook)
        missing_envs = []
        for environment in environment_list:
            found = False
            env_path = os.path.join(self.repo_root, "deploy/chef/environments")
            env_file = os.path.join(env_path, "{0}.rb".format(environment))
            with open(env_file) as env_read:
                for line in env_read:
                    ver_search = re.search(regex_cookbook_ver, line)
                    if ver_search:
                        found = True
            if not found:
                missing_envs.append(environment)
        if missing_envs:
            return {cookbook:missing_envs}
        else:
            return False


    def check_version(self, curr_ver, new_ver):
        try:
            if not curr_ver:
                return True
            elif tuple(map(int, (new_ver.split(".")))) < tuple(map(int, (curr_ver.split(".")))):
                return False
        except ValueError:
            pass
        return True


    def update_releases(self, environments):
        updates = {}
        version_pattern = re.compile("\".+\" .+\".+\s\d+.\d+.\d+\"")
        all_updates = {}
        for env in environments:
            env_path = os.path.join(self.repo_root, "deploy/chef/environments")
            env_file = os.path.join(env_path, "{0}.rb".format(env))
            with open(env_file) as env_read:
                for line in env_read:
                    if line.strip().startswith('cookbook_versions({'):
                        break
                for line in env_read:
                    if "> 0.0" in line.strip():
                        cookbook_name = line.strip().split('=>')[0].replace('"', '')
                        print("{0} cookbook is locked (> 0.0), this cookbook will be skipped.".format(cookbook_name))
                    elif version_pattern.match(line.replace(',', '').strip()):
                        v = re.search("\".+\" .+\".+\s(.+?)\"", line.replace(',', ''))
                        if v:
                            version_number = v.group(1)
                            second_octet = int(re.findall(r'\.([^"]*)\.', version_number)[0].replace('.', ''))
                            if second_octet > 0:
                                cookbook_name = line.strip().split(' =>')[0].replace('"', '')
                                cb_file = "{0}/deploy/chef/cookbooks/{1}/attributes/cookbook_repo_hash.rb".format(self.repo_root, cookbook_name)
                                try:
                                    git("show-branch", "remotes/origin/release_v{0}/current".format(second_octet), _env=self.env)
                                except Exception:
                                    pass
                                else:
                                    if not os.path.isfile(cb_file):
                                        pass
                                    elif second_octet in updates:
                                        updates[second_octet].append(cookbook_name)
                                    else:
                                        updates[second_octet] = [cookbook_name]
                    elif line.strip() == "},":
                        break

            all_updates[env] = updates
        return all_updates


    def cleanup(self):
        if self.repo_root != os.getcwd():
            print("Changing directory to root of repo: {0}".format(self.repo_root))
            os.chdir(self.repo_root)
        try:
            self.log.info("git reset HEAD --hard --quiet")
            git("reset", "HEAD", "--hard", "--quiet", _env=self.env)
        except:
            message = ("git reset HEAD --hard (clean up attempt) failed.")
            self.log.error(message, exc_info=True)
            return False


    def checkout_branch(self, branch):
        if self.repo_root != os.getcwd():
            print("Changing directory to root of repo: {0}".format(self.repo_root))
            os.chdir(self.repo_root)
        try:
            self.log.info("git checkout {0} --quiet".format(branch))
            git("checkout", branch, "--quiet", _env=self.env)
        except:
            message = ("git checkout {0} returned non-zero, aborting.".format(branch))
            self.log.error(message, exc_info=True)
            return False

        try:
            self.log.info("git pull origin {0} --quiet".format(branch))
            git("pull", "origin", branch, "--quiet", _env=self.env)
        except:
            message = ("git pull returned non-zero, aborting.")
            self.log.error(message, exc_info=True)
            return False

        try:
            self.log.info("git submodule update --quiet")
            git("submodule", "update", "--quiet", _env=self.env)
        except:
            message = ("git submodule update returned non-zero, aborting.")
            self.log.error(message, exc_info=True)
            return False

        return True

        print("Successfully checkout out '{0}' branch".format(branch))


    def check_cookbook_exists(self, chef_srv, cookbook, ver):
        print "\n", "#"*50
        print "ver =", ver
        print "\n", "#"*50
        if chef_srv == 'int':
            versions = self.int_capi.cookbook_show(cookbook)
        elif chef_srv == 'ext':
            versions = self.ext_capi.cookbook_show(cookbook)
        else:
            print("ERROR: check_cookbook_exists recieved bad chef_srv param. only 'int' and 'ext' are valid!")
            sys.exit(-1)
        print "\n", "#"*50
        print "versions =", versions
        print "\n", "#"*50
        if ver in versions:
            return True
        return False


    def get_cookbook_version(self, cookbook):
        # Verify Cookbook Exists
        if not os.path.isdir("deploy/chef/cookbooks/{0}".format(cookbook)):
            print("Cookbook '{0}' doesn't exist on this branch! This cookbook will be skipped.".format(cookbook))
            return False
        try:
            version_line = self.run("cat deploy/chef/cookbooks/{0}/metadata.rb | grep -w ^version | grep -oP \"(?<=').*?(?=')\"".format(cookbook))
        except:
            return False
        return version_line


    def get_environment_list(self):
        environment_list = set()
        for env in self.environment:
            if env in ['int-dev', 'int-stage', 'ext-uat', 'ext-prod', 'ext-alt', 'int', 'ext']:
                for env_name in os.listdir('deploy/chef/environments'):
                    if env_name.startswith(env) and 'broken' not in env_name:
                        env_name = env_name.replace('.rb', '')
                        environment_list.add(env_name)
            elif os.path.isfile("deploy/chef/environments/{0}.rb".format(env)):
                environment_list.add(env)
            else:
                print("Environment '{0}' doesn't exist on this branch! Verify the environment is valid and try again.".format(env))
                sys.exit(1)
        return list(environment_list)


    def confirm_changes(self, branch, cookbook_data, environment_list, missing_in_envs, big_data):
        sym_bdr = u'\u2590'.encode('utf8') + " "
        rollback_cb_data = {}
        for env in environment_list:
            for cookbook, cb_version in cookbook_data.iteritems():
                curr_cb_ver = self.get_current_version(cookbook, env)
                if not self.rollback and not self.check_version(curr_cb_ver, cb_version):
                    if env not in rollback_cb_data:
                        rollback_cb_data.update({env: [cookbook]})
                    else:
                        rollback_cb_data[env].append(cookbook)
        if rollback_cb_data:
            print(bcolors.get("red") + bcolors.get("bold") + "\nWARNING: Rollback(s) detected!\n"\
                  "By default, any changes to environments that would cause a rollback will be skipped.\n"\
                  "You may continue but the following cookbooks in these environments will be skipped:\n")
            for env, cbs in rollback_cb_data.iteritems():
                print(bcolors.get("yellow") + bcolors.get("bold") + env + ": " + bcolors.get("blue") + ", ".join(cbs) + bcolors.get("endc"))
            print(bcolors.get("red") + bcolors.get("bold") + "\nIf you intended to perform a rollback, please provide the --rollback option." + bcolors.get("endc"))
            print("Would you like to skip updating cookbooks in the environments listed above?")
            input = raw_input("\nEnter 'y' if you wish to skip these and continue:")
            if not input.lower().startswith("y"):
                abort_msg = ("User Aborted Environment File Updates!")
                self.log.info(abort_msg)
                if not self.log.get_stdout():
                    print("\n{0}{1}{2}{3}\n".format(bcolors.get("bold"), bcolors.get("red"), abort_msg, bcolors.get("endc")))
                    sys.exit(1)
        print("\n" + sym_bdr + "{0}{1}Attention: Before the environment files are changed, please confirm this is what you are expecting.{2}\n{3}{0}{1}"
              "The following cookbooks will be changed to the following versions:{2}".format(bcolors.get("bold"), bcolors.get("red"), bcolors.get("endc"), sym_bdr))
        for env in environment_list:
            print(sym_bdr + bcolors.get("yellow") + env + ": " + bcolors.get("endc"))
            for cookbook, cb_version in cookbook_data.iteritems():
                curr_cb_ver = self.get_current_version(cookbook, env)
                fmt_version = self.format_version_changes(old_ver=curr_cb_ver, new_ver=cb_version)
                if env in rollback_cb_data and cookbook in rollback_cb_data[env] and not self.rollback:
                    print(sym_bdr + bcolors.get("blue") + "\t\t" + cookbook + ": " + bcolors.get("red") + "(will not be changed due to rollback)" + bcolors.get("endc"))
                elif self.only_add_missing and not fmt_version:
                    print(sym_bdr + bcolors.get("blue") + "\t\t" + cookbook + ": " + bcolors.get("endc") + "(existing version '{0}' will not be modified)".format(curr_cb_ver))
                else:
                    print(sym_bdr + bcolors.get("blue") + "\t\t" + cookbook + ": " + bcolors.get("endc") + fmt_version)
                    if self.support_locks:
                        for node_name, node_data in big_data[env][cookbook].iteritems():
                            if self.query:
                                if self.query and node_data['is_locked'] and node_data['in_query'] and not node_data['version'].startswith('0.'):
                                    fmt_node_version = self.format_version_changes(old_ver=str(node_data['version']), new_ver=cb_version)
                                    print(sym_bdr + bcolors.get("blue") + "\t\t\t" + str(node_name) + ": " + bcolors.get("endc") + str(node_data['version']) + " => " + str(cb_version) + ' (Node in query. Noop Found. Will remove noop. Will be on the latest version )')
                                elif not node_data['is_locked'] and node_data['in_query'] and not node_data['version'].startswith('0.'):
                                    print(sym_bdr + bcolors.get("blue") + "\t\t\t" + str(node_name) + ": " + bcolors.get("endc") + str(node_data['version']) + " => " + str(cb_version) + ' (Node in query. No noop found. Node will be on the latest version)')
                                elif node_data['is_locked'] and not node_data['in_query'] and not node_data['version'].startswith('0.'):
                                    print(sym_bdr + bcolors.get("blue") + "\t\t\t" + str(node_name) + ": " + bcolors.get("endc") + str(node_data['version']) + " => " + str(cb_version) + ' (Node not in query. Noop Found.)')
                                elif not node_data['is_locked'] and not node_data['in_query'] and not node_data['version'].startswith('0.'):
                                    print(sym_bdr + bcolors.get("blue") + "\t\t\t" + str(node_name) + ": " + bcolors.get("endc") + str(node_data['version']) + " => " + str(cb_version) + ' (Node not in query. Noop not found. Noop will be added of current verison.)')
                            elif not node_data['is_locked'] and not node_data['version'].startswith('0.'):
                                print(sym_bdr + bcolors.get("blue") + "\t\t\t" + str(node_name) + ": " + bcolors.get("endc") + str(node_data['version']) + " => " + str(node_data['version']) + ' (No query provided. No lock found. Node will be deployed to latest.)')
                            else:
                                print(sym_bdr + bcolors.get("blue") + "\t\t\t" + str(node_name) + ": " + bcolors.get("endc") + str(node_data['version']) + " => " + str(node_data['version']) + ' (No query provided. Removing lock. Node will be deployed to latest.)')
        if branch:
            print(sym_bdr + "\n" + sym_bdr + "(these were the latest versions found on the tip of '{0}{1}{2}')\n".format(bcolors.get("yellow"), branch, bcolors.get("endc")) + sym_bdr)
        else:
            print(sym_bdr + "\n" + sym_bdr + "(this version was provided using the --version option.)\n".format(bcolors.get("yellow"), branch, bcolors.get("endc")) + sym_bdr)
        print(sym_bdr + "These will be updated in the following environment files:")
        for i in range(len(environment_list)/7+1):
            print(sym_bdr + bcolors.get("yellow") + ", ".join(environment_list[i*7:(i+1)*7]) + bcolors.get("endc"))
        input = raw_input("\nEnter 'y' if you wish to proceed: ")
        if not input.lower().startswith("y"):
            abort_msg = ("User Aborted Environment File Updates!")
            self.log.info(abort_msg)
            if not self.log.get_stdout():
                print("\n{0}{1}{2}{3}\n".format(bcolors.get("bold"), bcolors.get("red"), abort_msg, bcolors.get("endc")))
            sys.exit(1)
        else:
            print(" ")


    def update_environments(self, environment_list, cookbook_data):
        rollback_cb_data = {}
        for env in environment_list:
            for cookbook, cb_version in cookbook_data.iteritems():
                curr_cb_ver = self.get_current_version(cookbook, env)
                if not self.rollback and not self.check_version(curr_cb_ver, cb_version):
                    if env not in rollback_cb_data:
                        rollback_cb_data.update({env: [cookbook]})
                    else:
                        rollback_cb_data[env].append(cookbook)

        for cookbook, cb_version in cookbook_data.iteritems():
            # Set some regex to find the cookbook version line
            version_regex = re.compile(r"\"{0}\"(\s)*=>(\s)*\".*[0-9]+\.[0-9]+\.[0-9]+.*\"(\s)*".format(
                    cookbook), re.IGNORECASE)
            gt_version_regex = re.compile(r"\"{0}\"(\s)*=>(\s)*\"> 0\.0*\"(\s)*".format(
                    cookbook), re.IGNORECASE)
            cookbook_versions_regex = re.compile(r"(\s)*cookbook_versions(\s)*\((\s)*{", re.IGNORECASE)
            for environment in environment_list:
                if environment in rollback_cb_data and cookbook in rollback_cb_data[environment] and not self.rollback:
                    print(bcolors.get("yellow") + "NOTE: skipping update of {0} in {1} due to rollback.".format(cookbook, environment) + bcolors.get("endc"))
                else:
                    env_file = "deploy/chef/environments/{0}.rb".format(environment)
                    if not os.path.isfile(env_file):
                        raise Exception("Unable to find environment file {0}, aborting.\n".format(env_file))

                    # Open and read existing environment file to buffer, then delete it
                    env_fd = open(env_file, 'r')
                    lines = env_fd.readlines()
                    env_fd.close()
                    os.remove(env_file)

                    # open new version of the environment file
                    env_fd = open(env_file, 'w')
                    found_cookbook_version_map = False
                    for line in lines:
                        if re.search(cookbook_versions_regex, line) is not None:
                            found_cookbook_version_map = True

                        if found_cookbook_version_map:
                            s = re.search(version_regex, line)
                            gt = re.search(gt_version_regex, line)
                            if s is not None:
                                # This cookbook's version line was found.
                                comma = ""
                                if line.rstrip().endswith(","):
                                    comma = ","

                                env_fd.write("    \"{0}\" => \"<= {1}\"{2}\n".format(
                                    cookbook,
                                    cb_version,
                                    comma))
                                self.log.info("Set {0} cookbook to version {1} in {2}.".format(cookbook, cb_version, environment))
                            elif gt is not None:
                                print(bcolors.get("yellow") + "The cookbook '{0}' is locked in the '{1}' environment file (> 0.0), this cookbook will be skipped.\n"
                                      "If you want to set this cookbook please remove the environment file lock.\n".format(cookbook, environment) + bcolors.get("endc"))
                                self.log.info("Cookbook '{0}' is set to > 0.0 in '{1}' environment file, update skipped.".format(cookbook, environment))
                                env_fd.write(line)
                            else:
                                env_fd.write(line)
                        else:
                            env_fd.write(line)
                    env_fd.close()


    def push_environment_changes(self, environment_list):
        try:
            self.log.info("git pull --quiet")
            git("pull", "--quiet", _env=self.env)
        except ErrorReturnCode:
            message = ("git pull returned non-zero, aborting.")
            self.log.error(message, exc_info=True)
            return False

        try:
            self.log.info("git submodule update --quiet")
            git("submodule", "update", "--quiet", _env=self.env)
        except ErrorReturnCode:
            message = ("git submodule update returned non-zero, aborting.")
            self.log.error(message, exc_info=True)
            return False

        if len(git("status", "-s", "-uno", _env=self.env)) == 0:
            return "No Changes"

        for e in environment_list:
            try:
                self.log.info("git add deploy/chef/environments/{0}.rb".format(e))
                git("add", "deploy/chef/environments/{0}.rb".format(e), _env=self.env)
            except ErrorReturnCode:
                message = ("git add returned non-zero, aborting.")
                self.log.error(message, exc_info=True)
                return False

        commit_cbs = ""
        if self.target:
            commit_cbs += "Target(s): "
            commit_cbs += "\n"
            for each in izip_longest(fillvalue='', *[iter(self.target)]*4):
                commit_cbs += "\t".join(each)
                commit_cbs += "\n"

        elif self.cookbook:
            commit_cbs += "Cookbook(s): "
            commit_cbs += "\n"
            for each in izip_longest(fillvalue='', *[iter(self.cookbook)]*4):
                commit_cbs += "\t".join(each)
                commit_cbs += "\n"

        # Check the reason for a CHG###### and store it.
        if self.reason is None:
            self.reason = "No reason provided."

        commit_msg = ""
        commit_envs = ""
        all_change_numbers = []
        chg_regex = re.compile('(chg\d{7})', re.IGNORECASE)
        all_matches = re.finditer(chg_regex, self.reason)
        for m in all_matches:
            all_change_numbers.append(m.group())

        if len(all_change_numbers) < 1:
            commit_msg += "Chef Environment Change: {0}\n".format(self.reason[0:35])
            commit_msg += "\n"
        elif len(all_change_numbers) == 1:
            commit_msg += "Chef Environment Change: {0}\n".format(self.reason)
            commit_msg += "\n"
        else:
            chgs = "{0}".format(' '.join(all_change_numbers))
            commit_msg += "Chef Environment Change: {0}\n".format(chgs[0:35])
            commit_msg += "\n"

        commit_msg += "\n"
        commit_msg += "{0}\n".format(commit_cbs)
        commit_msg += "\n"

        for each in izip_longest(fillvalue='', *[iter(environment_list)]*2):
            commit_envs += "\t".join(each)
            commit_envs += "\n"

        commit_msg += "Environment(s):\n"
        commit_msg += "{0}\n".format(commit_envs)
        commit_msg += "\n"
        commit_msg += "@goodgardening\n"

        try:
            self.log.info("git commit -m '{0}' --quiet".format(commit_msg))
            git("commit", "-m", "{0}".format(commit_msg), "--quiet", _env=self.env)
        except ErrorReturnCode:
            message = ("git commit returned non-zero, aborting.")
            self.log.error(message, exc_info=True)
            return False

        for x in range(0, 5):
            try:
                self.log.info("git push origin master --quiet")
                git("push", "origin", "master", _env=self.env)
                return True
            except ErrorReturnCode:
                message = ("git push origin master returned non-zero, will rebase with master and retry. ({0}/5)".format(x+1))
                self.log.warning(message)
                self.log.info("git pull --rebase")
                git("pull", "--rebase", _env=self.env)
                self.log.info("git submodule update")
                git("submodule", "update", _env=self.env)
                pass

        return False


    def format_version_changes(self, old_ver, new_ver):
        fmt_str = ""
        change_detected = False
        old_l = old_ver.split(".")
        new_l = new_ver.split(".")
        if new_ver and not old_ver:
            return str(new_ver) + " (new cookbook)"
        if not self.only_add_missing:
            if len(new_l) != len(old_l):
                return "(cookbook will not be updated due to > 0.0 in the environment file)"
            for idx, old in enumerate(old_l):
                    if old == new_l[idx]:
                        fmt_str = fmt_str + old + "."
                    else:
                        fmt_str = fmt_str + bcolors.get("bold") + old + bcolors.get("endc") + "."
                        change_detected = True
            fmt_str = fmt_str[:-1]
            if change_detected:
                fmt_str = fmt_str + bcolors.get("blue") + " => " + bcolors.get("endc")
            else:
                fmt_str = fmt_str + bcolors.get("yellow") + " => " + bcolors.get("endc")
            for idx, new in enumerate(new_l):
                    if new == old_l[idx]:
                        fmt_str = fmt_str + new + "."
                    else:
                        fmt_str = fmt_str + bcolors.get("bold") + new + bcolors.get("endc") + "."
            fmt_str = fmt_str[:-1]
            if not change_detected:
                fmt_str = fmt_str + " (no change)"
            if StrictVersion(new_ver) < StrictVersion(old_ver):
                fmt_str = fmt_str + " (rollback)"
        return fmt_str


    def run(self, command):
        self.log.info("running '{0}'".format(command))
        output = check_output(command, shell=True)
        self.log.info(output)
        return output.rstrip()


if __name__ == '__main__':
    descr = ("This script will update the chef environment files on git and upload them.")

    parser = ArgumentParser(description=descr, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-b', '--branch', action='store', default=None,
                        help=("Specify which git branch you would like to deploy your cookbook from\n"
                              "The version of the provided cookbook on this branch will be used."))
    parser.add_argument('-e', '--environment', action='store', nargs='+', default=None,
                        help=("Specifies that the environments you would like to be updated to include\n"
                              "your cookbook. You may provide partial names of environments to hit all of them,\n"
                              "for example, providing 'ext-prod' will hit all ext-prod-* environments."))
    parser.add_argument('-c', '--cookbook', action='store', nargs='+', default=None,
                        help=("The cookbook(s) you would like to deploy from the given branch.\n"
                              "Only provide multiple cookbooks if they are expected to come from the same branch and\n"
                              "are getting deployed in the same environments.\n"))
    parser.add_argument('-t', '--target', action='store', nargs='+', default=None,
                        help=("The target(s) you would like to deploy from the given branch.\n"
                              "Only provide multiple targets if they are expected to come from the same branch and\n"
                              "are getting deployed in the same environments. You can also use target in addition to\n"
                              "cookbooks using the -c option."))
    parser.add_argument('-r', '--reason', action='store', default=None,
                        help=("Provide a reason.  Most useful will be a CHG######, but can be any string."))
    parser.add_argument('--skip-confirm', action='store_true', default=False,
                        help=("By default, the user will be prompted to confirm changes before the environment\n"
                              "files are updated on master. This option skips the confirmation in case it is being\n"
                              "executed by a script. Unless needed - IT IS HIGHLY RECOMMENDED YOU DO NOT USE THIS OPTION."))
    parser.add_argument('--support-locks', action='store_true', default=False,
                        help=("By default, the user will be prompted to confirm changes and remove/add Locks\n"
                              "files are updated on master. This option skips the adding / removing any noops."))
    parser.add_argument('--version', action='store', default=None,
                        help=("You can use this option to explicitly set a cookbook version instead of the tip of the provided\n"
                              "branch. This option is only intended to be used for rollbacks and other strange versioning cases.\n"
                              "This is not a regularly used option for this script and should only be used if you know what you\n"
                              "are doing. NOTE: This option can only be used when just one cookbook is provided"))
    parser.add_argument('--sync-release', action='store_true', default=False,
                        help=("This command must be used with the --environment option. It will find all cookbooks that appear to\n"
                              "be running off of a release branch and update those cookbooks to the versions on the tip of their\n"
                              "release branch.\n"
                              "NOTE: This option will skip any cookbooks currently set to > 0.0 in the environment file."))
    parser.add_argument('--no-upload', action='store_true', default=False,
                        help=("If provided, the environment files will be updated on git, but not uploaded to the chef server.\n"
                              "In most situations you do not want to provide this option."))
    parser.add_argument('--only-add-missing', action='store_true', default=False,
                        help=("Existing versions of the given cookbooks will not be updated, instead the cookbook will only get.\n"
                              "added to provided environment files that it is currently missing from.\n"
                              "Using this option is generally not recommended unless you have a unique use-case."))
    parser.add_argument('--rollback', action='store_true', default=False,
                        help=("If provided, the script will be allowed to downgrade cookbooks to older versions.\n"
                              "In most situations you do not want to provide this option."))
    parser.add_argument('-q','--query', action='store', default=None,
                        help=("Chef query of a subset of nodes that you wish to lock to the provided version or \n"
                              "version on the tip of provided branch"))
    parser.add_argument('--jenkins-user', action='store',
                          help=("Your intad username, which is your Jenkins user name.  If not specified, the\n"
                                "script will look for an environment variable named JENKINS_USER and\n"
                                "use its value."))
    parser.add_argument('--token', action='store',
                          help=("Your Jenkins user token.  Instructions for getting this token are available\n"
                                "at go/jenkins-setup.  If not specified, the script will look for an\n"
                                "environment variable named JENKINS_TOKEN and use its value."))
    parser.add_argument('-o', '--stdout', action='store_true', default=False,
                        help=("Write log messages to stdout instead of log file."))
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Verbose output (default false).', dest='verbose')
    parser.add_argument('--log-dir', action='store', default='/var/log/debesys',
                        help=("Directory where the update_environment.log file will be written.\n"
                              "This log is created to allow debugging when errors are happening."))


    args = parser.parse_args()

    #
    # Validate all of the provided arguments
    #
    if not args.jenkins_user:
        if 'JENKINS_USER' in os.environ:
            args.jenkins_user = os.environ['JENKINS_USER']

    if not args.token:
        if 'JENKINS_TOKEN' in os.environ:
            args.token = os.environ['JENKINS_TOKEN']

    if not args.jenkins_user or not args.token:
        print("You need to provide your Jenkins user and token.\n"
              "You can use the --jenkins-user and --token parameters, but it's recommended that you\n"
              "set the environment variables JENKINS_USER and JENKINS_TOKEN.\n"
              "Instructions for getting this token are available at go/jenkins-setup.\n"
              "Use -h for more details about how to set the environment variables.")
        sys.exit(1)

    if not args.environment:
        print("\n{0}{1} ERROR: you must provide a space seperated list of environments to update for this script to work!{2}\n"
              "".format(bcolors.get("bold"), bcolors.get("red"), bcolors.get("endc")))
        sys.exit(1)

    if not args.cookbook and not args.target and not args.sync_release:
        print("\n{0}{1} ERROR: you must provide a space seperated list of cookbooks or targets to version for this script to work!{2}\n"
              "".format(bcolors.get("bold"), bcolors.get("red"), bcolors.get("endc")))
        sys.exit(1)

    if not args.branch and not args.version and not args.sync_release:
        print("\n{0}{1} ERROR: you must provide the branch you bumped on via --branch or the cookbook version you would like to use via --version!{2}\n"
              "".format(bcolors.get("bold"), bcolors.get("red"), bcolors.get("endc")))
        sys.exit(1)

    if args.branch and args.version:
        print("\n{0}{1} ERROR: you can not use both --branch and --version!{2}\n"
              "".format(bcolors.get("bold"), bcolors.get("red"), bcolors.get("endc")))
        sys.exit(1)

    if args.cookbook and len(args.cookbook) > 1 and args.version:
        print("\n{0}{1} ERROR: the --version option only works with a single cookbook.{2}\n"
              "".format(bcolors.get("bold"), bcolors.get("red"), bcolors.get("endc")))
        sys.exit(1)

    if args.version:
        invalid_version = False
        if args.version.count('.') != 2:
            invalid_version = True
        elif '..' in args.version:
            invalid_version = True
        else:
            try:
                int(args.version.replace(".", ""))
            except:
                invalid_version = True

        if invalid_version:
            print("\n{0}{1} ERROR: invalid version provided. The cookbook version must be in the format of X.Y.Z!{2}\n"
                  "".format(bcolors.get("bold"), bcolors.get("red"), bcolors.get("endc")))
            sys.exit(1)


    UE=UpdateEnvironment(branch = args.branch,
                      environment = args.environment,
                      cookbook = args.cookbook,
                      target = args.target,
                      reason = args.reason,
                      skip_confirm = args.skip_confirm,
                      support_locks = args.support_locks,
                      version = args.version,
                      sync_release = args.sync_release,
                      stdout = args.stdout,
                      verbose = args.verbose,
                      log_dir = args.log_dir,
                      no_upload = args.no_upload,
                      rollback = args.rollback,
                      jenkins_user = args.jenkins_user,
                      token = args.token,
                      only_add_missing = args.only_add_missing,
                      query= args.query
                     )
