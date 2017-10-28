# -*- mode: ruby -*-
# vi: set ft=ruby sw=2 :
#
#################################################################
# title:      Vagrantfile                                       #
# desciption: Bootstrap development environment with Vagrant    #
#             and Virtualbox. All configuration is done through #
#             ./vagrant.yml file in the same folder. Please DO  #
#             NOT EDIT Vagrantfile unless you really-really     #
#             need to do so. Instead edit ./vagrant.yml and     #
#             all the changes will be fetched by Vagrant on     #
#             next provision or up.                             #
# developer:  ddnomad                                           #
# version:    0.1.2                                             #
#################################################################

require 'yaml' # to parse config file

# load configuration file and sub-sections
VCONF = YAML.load_file('./vagrant.yml').freeze
VB_PROPS = VCONF['vb_props'].freeze
ANS_PROPS = VCONF['ansible_props'].freeze

# generic properties
BASE_BOX = VCONF['base_box'].freeze
VC_VERSION = VCONF['vc_version'].freeze

# virtualbox properties
VB_NAME = VB_PROPS['name'].freeze
VB_CPUS = VB_PROPS['cpus'].freeze
VB_CAP = VB_PROPS['cpu_cap'].freeze
VB_RAM = VB_PROPS['ram'].freeze

# ansible properties
ANS_BP = ANS_PROPS['base_path'].freeze
ANS_CM = ANS_PROPS['comp_mode'].freeze
ANS_PB = ANS_PROPS['playbook'].freeze
ANS_CFG = ANS_PROPS['config'].freeze
ANS_REQ = ANS_PROPS['requirements_path'].freeze

# on-call commands to execute
ON_CALL_CMDS = VCONF['exec_on_call'].freeze

# ports to forward
FORW_PORTS = VCONF['forward_ports'].freeze

# actual Vagrant configuration block
Vagrant.configure(VC_VERSION) do |config|
  # specifying base box
  config.vm.box = BASE_BOX

  # configuring Virtualbox provider
  config.vm.provider :virtualbox do |vb|
    vb.name = VB_NAME
    vb.cpus = VB_CPUS
    vb.memory = VB_RAM
    vb.customize ['modifyvm', :id, '--cpuexecutioncap', VB_CAP]
  end

  # provision the guest with Ansible
  config.vm.provision 'ansible_local' do |ansible|
    ansible.compatibility_mode = ANS_CM
    ansible.provisioning_path = ANS_BP
    ansible.playbook = ANS_PB
    ansible.config_file = ANS_CFG
  end

  # forwarding ports
  FORW_PORTS.each do |guest_port, host_port|
    config.vm.network 'forwarded_port', guest: guest_port, host: host_port
  end
end
