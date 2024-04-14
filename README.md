# Live feed of potentially malicious typosquats of defined domains

This application is a set of two containers.

One refreshes the feed by taking in the configured protected domains, permutating them, and checking which permutations are live. These permutations are considered "typosquats" and are potentially malicioius domains, often parked specifically to deceive users into believing they are on the correct website or to redirect users to other malicioius websites.

The other is a simple nginx container that hosts the feed after it is generated.

The feed that is output can then be imported as a live feed to most firewall vendors to allow for blocking of these typosquats. This particular application was built specifically for Fortinet live feeds, but can also be used with Palo Alto, Sophos, and other firewalls that support pulling in an IP list dynamically.
## Installation

Prior to cloning the repo, the following must be installed and working on the machine:

- Docker
- Docker compose

Clone the repo and update the ``conf/domains.txt`` file to include any domains you wish to locate live typosquats for.

Run the following commands to set up and start the containers and their requirements:

```bash
  chmod +700 setup.sh
  sudo ./setup.sh
  sudo ./start.sh
```
    