from scapy.all import sniff
import tkinter as tk
from scapy.all import sniff, IP, TCP
from threading import Thread
from scapy.all import sniff, IP, TCP

# Function to analyze and filter the packets
def packet_callback(packet):
    print(f"Packet Captured: {packet.summary()}")
    
    # Analyzing HTTP packets
    if packet.haslayer('TCP') and packet.haslayer('Raw'):
        payload = packet.getlayer('Raw').load
        if b"HTTP" in payload:
            print("HTTP Packet Detected:")
            print(payload)

    # Analyzing HTTPS packets
    if packet.haslayer('TCP') and packet.haslayer('Raw'):
        payload = packet.getlayer('Raw').load
        if b"HTTP/1.1" in payload or b"HTTP/2" in payload:
            print("HTTPS Packet Detected:")
            print(payload)

# Start sniffing the network
sniff(prn=packet_callback, store=0, filter="tcp", count=10)


# Function to analyze and filter the packets
def packet_callback(packet):
    if packet.haslayer(IP):
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        print(f"Source IP: {ip_src}, Destination IP: {ip_dst}")
        
        if packet.haslayer(TCP):
            tcp_sport = packet[TCP].sport
            tcp_dport = packet[TCP].dport
            
            # Detecting FTP traffic (port 21)
            if tcp_dport == 21:
                print(f"FTP Detected: {ip_src} -> {ip_dst} (Port 21)")
            
            # Detecting HTTP traffic (port 80)
            if tcp_dport == 80:
                print(f"HTTP Detected: {ip_src} -> {ip_dst} (Port 80)")
            
            # Detecting HTTPS traffic (port 443)
            if tcp_dport == 443:
                print(f"HTTPS Detected: {ip_src} -> {ip_dst} (Port 443)")

# Start sniffing the network with a filter on TCP packets
sniff(prn=packet_callback, store=0, filter="tcp", count=10)


# Function to update the GUI with captured packet data
def update_gui(packet_data):
    text_box.insert(tk.END, packet_data + "\n")
    text_box.yview(tk.END)

# Function to analyze and filter the packets
def packet_callback(packet):
    packet_info = f"Packet Captured: {packet.summary()}"
    update_gui(packet_info)
    
    if packet.haslayer(IP):
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        
        if packet.haslayer(TCP):
            tcp_sport = packet[TCP].sport
            tcp_dport = packet[TCP].dport
            
            if tcp_dport == 21:
                packet_info = f"FTP Traffic Detected: {ip_src} -> {ip_dst} (Port 21)"
                update_gui(packet_info)
            elif tcp_dport == 80:
                packet_info = f"HTTP Traffic Detected: {ip_src} -> {ip_dst} (Port 80)"
                update_gui(packet_info)
            elif tcp_dport == 443:
                packet_info = f"HTTPS Traffic Detected: {ip_src} -> {ip_dst} (Port 443)"
                update_gui(packet_info)

# Function to start packet sniffing in a separate thread
def start_sniffing():
    sniff(prn=packet_callback, store=0, filter="tcp", count=10)

# Creating the Tkinter window for GUI
root = tk.Tk()
root.title("Network Traffic Sniffer")

# Creating a scrollable text box to display packet information
text_box = tk.Text(root, height=20, width=100)
text_box.pack()

# Start the sniffing in a separate thread
sniffing_thread = Thread(target=start_sniffing)
sniffing_thread.start()

# Running the Tkinter main loop
root.mainloop()
