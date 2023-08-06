set -ex
alias sudo='sudo env "PATH=$PATH" '

sudo apt-get update
sudo apt-get upgrade -y

sudo apt install -y tldr tmux
sudo apt install -y vim-gtk  # vim with +clipboard, so vim can use os's clipboard

sudo apt install -y gdb cgdb

sudo apt install -y nsight-systems-2021.2.4 nsight-compute-2021.3.1
sudo ln -s /opt/nvidia/nsight-compute/2021.3.1/ncu /usr/local/bin

currentver="$(lsb_release -sr)" # get the current Ubuntu version
requiredver="20.10" # set the required version

if [ "$(printf '%s\n' "$requiredver" "$currentver" | sort -V | head -n1)" = "$requiredver" ]; then 
    echo "Current version is greater than or equal to $requiredver, will install exa"
    sudo apt install -y exa
else
    echo "Current version is less than $requiredver, exa wouldn't be installed"
fi

sudo apt install peco mlocate bat python3-pip tig fzf fd-find ripgrep duf zip unzip httpie
# wget -O /tmp/bat.deb https://github.com/sharkdp/bat/releases/download/v0.21.0/bat-musl_0.21.0_amd64.deb && sudo dpkg -i /tmp/bat.deb


sudo pip install  py-spy python3.8-dbg viztracer glances pre-commit

sudo pip install cmake==3.21.4

curl -LSfs https://raw.githubusercontent.com/cantino/mcfly/master/ci/install.sh | sudo sh -s -- --git cantino/mcfly
echo "eval "$(mcfly init zsh)"" >> ~/.zshrc
# tab complete of git
# curl https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -o ~/.git-completion.bash
# echo "source ~/.git-completion.bash" >> ~/.zshrc
# install tool to outuput c++ call graph, class grpah
sudo  apt-get install -y silversearcher-ag
(
cd /tmp
wget https://raw.githubusercontent.com/satanson/cpp_etudes/master/calltree.pl
wget https://raw.githubusercontent.com/satanson/cpp_etudes/master/cpptree.pl
chmod 777 calltree.pl cpptree.pl
sudo mv calltree.pl /usr/local/bin/calltree
sudo mv cpptree.pl /usr/local/bin/cpptree
)
sudo pip install gdbgui
