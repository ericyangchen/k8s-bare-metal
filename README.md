# Provisioning local cluster using kubespray

<img src="https://skillicons.dev/icons?i=kubernetes,ansible" />

This tool helps setting up a local kubernetes cluster in a manageable and reproducible way using kubespray and Ansible.

### Definition 📟

- **`Provisioning Machine`**: the machine used to config the cluster (need not to be one of the cluster node)
- **`Hosts`**: all the cluster nodes (master, workers)
  - **`Master`**: master node
  - **`Worker`**: worker nodes

## Pre-installation ⚙️

1. Clone this repository (with [kubespray](https://github.com/kubernetes-sigs/kubespray.git) submodule) using
   ```bash
   git clone --recurse-submodules https://github.com/ericyangchen/k8s-bare-metal.git
   ```
2. Create a python virtual environment using conda
   ```bash
   conda create python=3.8 -n k8s-cluster
   conda activate k8s-cluster
   ```
3. Install kubespray dependencies (including ansible package)
   ```bash
   pip install -r kubespray/requirements.txt
   ```
4. Ensure **`Provisioning Machine`** have SSH access to all **`Hosts`** without password (using public-key based SSH): refer to [Copy SSH key to multiple hosts](#Copy-SSH-key-to-multiple-hosts)

## Provisioning the cluster 🚀

1. Modify `inventory/hosts.yml` to configure your cluster nodes.
2. Check if every node is accessible from **`Provisioning Machine`** by running

   ```bash
   ansible -i inventory/hosts.yml -m ping all
   ```

3. Then, provision the cluster by running

   ```bash
   ansible-playbook -i inventory/hosts.yml --become --become-user=root \
   --private-key=${PATH_TO_SSH_PRIVATE_KEY} kubespray/cluster.yml
   ```

   > 💡 Note: You might need to provide ansible the sudo password of the cluster machine by adding \
   > `--extra-vars "ansible_sudo_pass=${SUDO_PASSWORD}"` if you encounter \
   > `fatal: [node]: FAILED! => {"msg": "Missing sudo password"}` during the setup.

4. Once the installation is complete, you will see the following output

   <img src="https://i.imgur.com/XkzM36w.png"/>

5. Now, to use commands like `kubectl`, you will need a kube config file. The config file will be located in the **`Master`** machine in `/etc/kubernetes/admin.conf`. Copy it to your local machine to access the cluster.
6. After acquiring the config file to your local machine, edit the config file and
   change the IP address to **`Master`**'s public ip `server: https://${CONTROL_PLANE_IP}:6443`
7. run
   ```bash
   kubectl get nodes --kubeconfig=${PATH_TO_CONFIG_FILE}
   ```
   to verify the status of all nodes.

## Copy SSH key to multiple hosts 💡

To make all **`Hosts`** accessible from **`Provisioning Machine`**, we create a SSH key in **`Provisioning Machine`** and copy them to all **`Hosts`**.

1. Enter `ssh-keygen`, create a pair of keys
2. Use `scripts/sh-copy-id.py` script to copy keys to multiple servers

   - Create a `scripts/secrets.py` file using `scripts/secrets.py.template`

     ```bash
     cp scripts/secrets.py.template scripts/secrets.py
     ```

   - Modify the `secrets.py` file to include your servers
     ```bash
     # secrets template
     PUBLICKEY_FILE = "<path to your public key file>"
     SERVER_INFO = {
         "<hostname>@<ip-address>:<port>": "<password>",
         "<hostname>@<ip-address>:<port>": "<password>",
     		..
     }
     ```
   - run `python scripts/ssh-copy-id.py` to copy keys.

## Add new node to cluster 💡

1. Modify `inventory/hosts.yml` by adding new nodes
2. Run ansible-playbook with `kubespray/scale.yml`

## Remove node from cluster 💡

1. Modify `inventory/hosts.yml` by removing the unwanted nodes
2. Run ansible-playbook with `kubespray/remove-node.yml`

## Troubleshooting 😈

Contact [@ericyangchen](https://github.com/ericyangchen) for more info.
