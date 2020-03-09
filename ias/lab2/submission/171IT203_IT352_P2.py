import os
import pandas as pd
import numpy as numpy
import math

dirname = os.path.dirname(__file__)
input_filename = os.path.join(dirname, 'input.txt')
output_filename = os.path.join(dirname, '171IT203_IT352_P2_Output_TC5.txt')
acl_rules_filename = os.path.join(dirname, 'ACL-File.xlsx')


def main():
    input_file = open(input_filename, "r")
    output = open(output_filename, "a")
    dump = input_file.readline()

    # To read the ACL file
    acl_rules = pd.read_excel(
        acl_rules_filename, na_values=[]).fillna(-1).values

    num_rules = 0
    num_cols = acl_rules.shape[1]

    for i in range(acl_rules.shape[0]):
        flag = 1
        for j in range(acl_rules.shape[1]):
            if acl_rules[i][j] == -1:
                flag = 0
                break

        if flag == 1:
            num_rules = num_rules + 1

    acl_rules = acl_rules[:num_rules, :]

    # print(acl_rules)

    # To get ethernet header details
    data = list(map(lambda x: int(x, 16), dump.split()))
    mac_addr = dict()
    mac_addr['dest'] = dump.split()[0:6]
    mac_addr['src'] = dump.split()[6:12]

    print('MAC Address (Source):\t\t', ":".join(
        map(str, mac_addr['src'])), file=open(output_filename, "a+"))
    print('MAC Address (Source):\t\t', ":".join(
        map(str, mac_addr['src'])))
    print('MAC Address (Destination):\t', ":".join(
        map(str, mac_addr['dest'])), file=open(output_filename, "a+"))
    print('MAC Address (Destination):\t', ":".join(
        map(str, mac_addr['dest'])))

    ethernet_protocol_type = data[12:14]

    packet_type = ""

    # if it is IP version 4 packet
    if ethernet_protocol_type[0] == 8 and ethernet_protocol_type[1] == 0:

        print('Packet Type:\t\t\t\t IPv4', file=open(output_filename, "a+"))
        print('Packet Type:\t\t\t IPv4')

        # To get IP header details
        ipVersion = data[14] > 4

        protocol_num = data[23]
        protocol = ''

        # Standard Codes
        if protocol_num == 6:
            protocol = 'TCP'
        elif protocol_num == 17:
            protocol = 'UDP'

        print('IPv4 Packet Protocol:\t\t', protocol,
              file=open(output_filename, "a+"))
        print('IPv4 Packet Protocol:\t\t', protocol)

        ip_addr = dict()

        ip_addr['src'] = data[26:30]
        ip_addr['dest'] = data[30:34]

        port_num = dict()
        port_num['src'] = (data[34] << 8) + data[35]
        port_num['dest'] = (data[36] << 8) + data[37]

        print('IP Address (Source):\t\t', ".".join(
            map(str, ip_addr['src'])) + ":" + str(port_num['src']), file=open(output_filename, "a+"))
        print('IP Address (Destination):\t', ".".join(
            map(str, ip_addr['dest'])) + ":" + str(port_num['dest']), file=open(output_filename, "a+"))
        print('IP Address (Source):\t\t', ".".join(
            map(str, ip_addr['src'])) + ":" + str(port_num['src']))
        print('IP Address (Destination):\t', ".".join(
            map(str, ip_addr['dest'])) + ":" + str(port_num['dest']))

        rule_matched = False

        for rule in acl_rules:
            agreements = 0

            if rule[0] != 'Any':
                flag = True
                ip_addr_check = rule[0].split('.')
                for i in range(4):
                    if (ip_addr_check[i] != '*') and (ip_addr['src'][i] != int(ip_addr_check[i])):
                        flag = False
                        break
                if flag:
                    agreements = agreements + 1
            else:
                agreements = agreements + 1

            if rule[1] != 'Any':
                port_num_check = rule[1]
                if (port_num_check == port_num['src']):
                    agreements = agreements + 1
            else:
                agreements = agreements + 1

            if rule[2] != 'Any':
                flag = True
                ip_addr_check = rule[2].split('.')
                for i in range(4):
                    if (ip_addr_check[i] != '*') and (ip_addr['dest'][i] != int(ip_addr_check[i])):
                        flag = False
                        break
                if flag:
                    agreements = agreements + 1
            else:
                agreements = agreements + 1

            if rule[3] != 'Any':
                port_num_check = rule[3]
                if (port_num_check == port_num['dest']):
                    agreements = agreements + 1
            else:
                agreements = agreements + 1

            if (agreements == 4):
                print('Action:\t\t\t\t\t\t',
                      rule[4], file=open(output_filename, "a+"))
                print('Action:\t\t\t\t',
                      rule[4])
                rule_matched = True

            if rule_matched == True:
                break

    # ARP Packet
    elif ethernet_protocol_type[0] == 8 and ethernet_protocol_type[1] == 6:

        print('Packet Type:\t\t\t\t\t ARP', file=open(output_filename, "a+"))
        print('Packet Type:\t\t\t ARP')

        ip_addr = dict()

        ip_addr['src'] = data[28:32]
        ip_addr['dest'] = data[38:42]

        port_num = dict()
        port_num['src'] = (data[34] << 8) + data[35]
        port_num['dest'] = (data[36] << 8) + data[37]

        print('IP Address (Source):\t\t', ".".join(
            map(str, ip_addr['src'])), file=open(output_filename, "a+"))
        print('IP Address (Destination):\t', ".".join(
            map(str, ip_addr['dest'])), file=open(output_filename, "a+"))
        print('IP Address (Source):\t\t', ".".join(
            map(str, ip_addr['src'])))
        print('IP Address (Destination):\t', ".".join(
            map(str, ip_addr['dest'])))

        print('Action:\t\t\t\t\t\t Deny', file=open(output_filename, "a+"))
        print('Action:\t\t\t\t Deny')
    print('------------------------------------------------',
          file=open(output_filename, "a+"))


main()
