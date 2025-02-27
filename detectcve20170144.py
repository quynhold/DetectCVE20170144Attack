import pyshark, csv, sys, os, binascii, hashlib
from datetime import datetime
import os
from pathlib import Path

def getTCPPayload(packet):
	if 'tcp' in packet:
		if 'tcp.payload' in packet.tcp._all_fields:
			a=str(packet.tcp.payload)
			tcpPayload = a.replace(':','')
			data = bytes.fromhex(tcpPayload)
			return data.decode('utf-8', 'replace').encode('cp850','replace').decode('cp850')\
				.replace('\n','').replace('\t','')\
				.replace('\r','').replace('\\x', '')\
				.replace(',', '|')
	return ''

def getSMBnt_status(pkt):
	if "SMB" in pkt:
		if "smb.nt_status" in pkt.smb._all_fields:
			a = str(pkt.smb.nt_status)
			return a
	return ""

def get_packet_details(packet):
	try:
		protocol = packet.highest_layer
		source_address = packet.ip.src
		source_port = packet[packet.transport_layer].srcport
		destination_address = packet.ip.dst
		destination_port = packet[packet.transport_layer].dstport
		packet_time = packet.sniff_time
		packet_data = str(getSMBnt_status(packet))
		f = open('bcd.csv', 'a')
		writer = csv.writer(f, delimiter=',',lineterminator='\n')
		row = [protocol, source_address, source_port, destination_address, destination_port, packet_time, packet_data]
		writer.writerow(row)
		return {
			"protocol":protocol, 
			"source_address":source_address, 
			"source_port":source_port, 
			"destination_address":destination_address, 
			"destination_port":destination_port, 
			"packet_time":packet_time, 
			"packet_data":packet_data
		}
	except Exception:
		print(Exception)

def capture_live_packets(network_interface):
	capture = pyshark.LiveCapture(interface=network_interface)
	for raw_packet in capture.sniff_continuously():
		if "SMB" in raw_packet:
			p = get_packet_details(raw_packet)
			if isAttackPacket(p) == 1:
				time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				string = time+" [Warning: Phat hien tan cong CVE 2017 0144] IP:"+p['source_address']+" remote code by IP:"+p['destination_address']\
				+""
				print(string,"\n")
				#Write Log
				with open('log.txt', 'a') as log:
					log.write(string)
					log.write("\n")


def isAttackPacket(p):
	if p['packet_data'] is None:
		return False
	data = str(p['packet_data'])
	if "0xc000000d"  in data: #signature của EternalBlue
		return True
	return False

print('-- Restart Capture --')
try:
	capture_live_packets('Ethernet0')
except Exception as e:
	print(e)
