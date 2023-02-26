import re
import os
import random
import socket
import struct

# Define regex patterns to match IP and MAC addresses
ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
mac_pattern = re.compile(r'(?:[0-9a-fA-F]:?){12}')

# Read the sample log file
with open('Sample_log.txt', 'r') as f:
    log = f.read()

# Split the log into sections using the "Display" keyword as a separator
sections = log.split('\nDisplay ')
# Ignore specified sections
sections = [section for section in sections if not section.startswith('processes')
            and not section.startswith('memory debug')
            and not section.startswith('running-config')]

# Create a new file for each section and write the contents to the file
for section in sections:
    # Get the section name
    section_name = section.split('\n')[0].replace(' ', '_')
    with open('Display ' + section_name + '.txt', 'w') as f:
        f.write(section)

# Replace IP addresses with randomly generated valid IP addresses
for match in ip_pattern.finditer(log):
    old_ip = match.group(0)
    new_ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    log = log.replace(old_ip, new_ip)

# Replace MAC addresses with randomly generated valid MAC addresses
for match in mac_pattern.finditer(log):
    old_mac = match.group(0)
    new_mac = ':'.join(['{:02x}'.format(random.randint(0x00, 0xff)) for _ in range(6)])
    log = log.replace(old_mac, new_mac)
