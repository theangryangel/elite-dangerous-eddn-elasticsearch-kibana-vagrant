# Elite:Dangerous Data Network -> Kibana
A quick VM to take data from the [EDDN](https://forums.frontier.co.uk/showthread.php?t=57986) and dump it into
elasticsearch and kibana.

## Getting started
What this will do is create a preconfigured virtual machine, running elasticsearch, kibana, elastic-curator, 
and the client.py collector. At minimum you'll require [git](http://git-scm.com/), [vagrant](https://www.vagrantup.com/), [ansible](http://www.ansible.com/) and a virtualisation platform supported by vagrant to be installed - as I'm using ansible, you'll require Linux, OSX, or to get ansible running under cygwin on Windows.

  - Open a command line interface, and cd to somewhere you can store a small amount of data
  - `git clone https://github.com/theangryangel/elite-dangerous-eddn-elasticsearch-kibana-vagrant.git`
  - `cd elite-dangerous-eddn-elasticsearch-kibana-vagrant`
  - `vagrant up` - This may take sometime as it will download, install and configure a small Debian virtual machine
  - Open a web browser and head to [http://localhost:5601/](http://localhost:5601/)
  - The first time you open kibana you'll be asked to configure what indexes for it to look at. You should only do this
    after the first set of data has come in. This may take several minutes, as it's a live feed from other users.
	Give it a few minutes and then set the index to "eddn-*" and select message.Timestamp as the timestamp field from
	the dropdown.
  - Now you can mind the data as much as you desire - i'd suggest looking up how to use Kibana (4) as a starting point,
    or just having a play around.

### Stopping and starting the VM
When in the cloned git repository:
  - To stop run `vagrant halt`
  - To restart later run `vagrant up`

The reason why you do it this way is because the collector is run directly from the git repository, allowing for easy update. When you manually start a VM through the normal management interfaces the files may not be correctly shared with the VM. Vagrant ensures that this happens everytime on start up.

### ACHTUNG!
  - Data older than 30 days will be automatically culled
  - Data is only collected whilst the VM is on, has a network internet connection, the collector and elasticsearch
    daemons are running - they will do this automatically for you - and more
	importantly as long as the EDDN receiving and passing data

## Uninstalling/Bored?
  - cd to the cloned git repository
  - `vagrant destroy`
  - If you need git or vagrant any longer, refer to their documentation to
    uninstall
