#!/usr/bin/env python

import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory, Host, Group
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor


class MyInventory(Inventory):  
    def __init__(self, resource, loader, variable_manager):  
        self.resource = resource  
        self.inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=[])  
        self.dynamic_inventory()  

    def add_dynamic_group(self, hosts, groupname, groupvars=None):   
        my_group = Group(name=groupname)   
        if groupvars:  
            for key, value in groupvars.items():  
                my_group.set_variable(key, value)  
        for host in hosts:  
            # set connection variables  
            hostname = host.get("hostname")  
            hostip = host.get('ip', hostname)  
            hostport = host.get("port")  
            username = host.get("username")  
            password = host.get("password")  
            ssh_key = host.get("ssh_key")  
            my_host = Host(name=hostname, port=hostport)  
            my_host.set_variable('ansible_ssh_host', hostip)  
            my_host.set_variable('ansible_ssh_port', hostport)  
            my_host.set_variable('ansible_ssh_user', username)  
            my_host.set_variable('ansible_ssh_pass', password)  
            my_host.set_variable('ansible_ssh_private_key_file', ssh_key)   
            for key, value in host.items():  
                if key not in ["hostname", "port", "username", "password"]:  
                    my_host.set_variable(key, value)  
            my_group.add_host(my_host)  

        self.inventory.add_group(my_group)  

    def dynamic_inventory(self):  
        if isinstance(self.resource, list):  
            self.add_dynamic_group(self.resource, 'default_group')  
        elif isinstance(self.resource, dict):  
            for groupname, hosts_and_vars in self.resource.items():  
                self.add_dynamic_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars")) 


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))


class MyRunner:

    def __init__(self, resource, *args, **kwargs):
        self.resource = resource
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.results_callback = ResultCallback()
        self.inventory = None
        self._initialize_data()


    def _initialize_data(self):  
        Options = namedtuple('Options', ['connection','module_path', 'forks', 'timeout',  'remote_user',  
                'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',  
                'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass', 'verbosity',  
                'check', 'listhosts', 'listtasks', 'listtags', 'syntax'])  

        self.variable_manager = VariableManager()  
        self.loader = DataLoader()  
        self.options = Options(connection='smart', module_path=None, forks=100, timeout=10,  
                remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None, ssh_extra_args=None,  
                sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,  
                become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,  
                listtasks=False, listtags=False, syntax=False)  

        self.passwords = dict(sshpass=None, becomepass=None)  
        self.inventory = MyInventory(self.resource, self.loader, self.variable_manager).inventory
        self.variable_manager.set_inventory(self.inventory) 

    # def _initialize_data(self):
    #     Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check'])
    #     # initialize needed objects
    #     self.variable_manager = VariableManager()
    #     self.loader = DataLoader()
    #     self.options = Options(connection='local', module_path='/path/to/mymodules', forks=100, become=None, become_method=None, become_user=None, check=False)
    #     self.passwords = dict(vault_pass=None)

    #     # Instantiate our ResultCallback for handling results as they come in
    #     self.results_callback = ResultCallback()

    #     # create inventory and pass to var manager
    #     # inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='localhost')
    #     self.inventory = MyInventory(self.resource, self.loader, self.variable_manager).inventory
    #     self.variable_manager.set_inventory(self.inventory)

    def run_module(self, hosts, module_name, module_args):
        # create play with tasks
        play_source =  dict(
                name = "Ansible Play",
                hosts = hosts,
                gather_facts = 'no',
                tasks = [
                    dict(action=dict(module=module_name, args=module_args))
                ]
            )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        # actually run it
        tqm = None
        try:
            tqm = TaskQueueManager(
                    inventory=self.inventory,
                    variable_manager=self.variable_manager,
                    loader=self.loader,
                    options=self.options,
                    passwords=self.passwords,
                    stdout_callback=self.results_callback,  # Use our custom callback instead of the ``default`` callback plugin
                )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
    
    def run_playbook(self, playbook_path): 
        """ 
        run ansible palybook 
        """
        try:
            executor = PlaybookExecutor(  
                playbooks=[playbook_path], inventory=self.inventory, variable_manager=self.variable_manager, loader=self.loader,  
                options=self.options, passwords=self.passwords
            )  
            executor._tqm._stdout_callback = self.results_callback
            executor.run()  
        except Exception as e: 
            print(e)
            return False

