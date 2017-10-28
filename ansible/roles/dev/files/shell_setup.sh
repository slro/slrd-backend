# ddnomad-specific setup
# remove if it bothers
set -o vi
bind -m vi-insert "\C-l":clear-screen

# cd to a project folder and cleanup
cd /vagrant || exit 1
mv ./ubuntu-xenial*.log log/"$(date +%F%T)"_vagrant_boot.log &> /dev/null
