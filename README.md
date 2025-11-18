Advanced Computer Networks – Multi-Client Chat System & DNS Tools

This repository contains several advanced networking projects developed as part of an Advanced Computer Networks course.
The work demonstrates hands-on experience with:


-TCP socket programming

-Multi-client server architecture

-Custom application-layer protocol design

-Event-driven I/O using select()

-Server-side state management

-DNS queries and packet analysis using Scapy



Project Structure
HW1/
├── server.py          # Multi-client TCP chat server
├── client.py          # Interactive TCP client
├── protocol.py        # Custom length-prefixed protocol
├── myDNSapp.py        # DNS query tool
├── nslookup_DNS.py    # DNS resolver (A / PTR / CNAME)
└── README.md


1. Multi-Client Chat System (TCP)

A fully implemented multi-client chat application built with Python sockets.
The system includes a server capable of handling multiple clients simultaneously and a client interface for sending commands and messages.


Features:

    -User registration: NAME <username>
    
    -List connected users: GET_NAMES
    
    -Direct messaging: MSG <user> <message>
    
    -Broadcast messaging: MSG BROADCAST <message>
    
    -Blocking users: BLOCK <username>
    
    -Graceful disconnection: EXIT

Server Maintains:

    -Active client sockets
    
    -Username ↔ socket mappings
    
    -Per-user block lists

Technologies Used:

    -Python TCP sockets (socket.AF_INET, socket.SOCK_STREAM)
    
    -Event-driven server with select.select()
    
    -Custom 3-byte length-prefixed protocol
    
    -Modular architecture (server/client/protocol separation)
    
    -Server – server.py

The server implements:

    -Client connection management
    
    -Command parsing
    
    -Message routing (direct & broadcast)
    
    -Block rule enforcement
    
    -State tracking for all connected clients
    
    -Non-blocking I/O using select()
    
    -Client – client.py

The client provides:

    -Non-blocking keyboard input (msvcrt)
    
    -Concurrent message reception
    
    -Support for all chat commands
    
    -Automatic use of the custom protocol for message framing
    
    -Protocol – protocol.py

Implements the application protocol:

-<LENGTH:3><DATA>






Includes:

    
    -create_msg(data) – wraps outgoing messages with a 3-digit length field
    
    -get_message(sock) – reads a complete framed message safely
    
    -Ensures correct message boundaries over TCP.
    
    -2. DNS Query Tools (Scapy)
    
    -Two utilities demonstrating understanding of DNS internals and Scapy-based packet crafting.
    
    -myDNSapp.py
    
    -Experimental Scapy-based DNS tool with raw packet crafting and response inspection.
    
    -nslookup_DNS.py

A functional DNS resolver supporting:

    -A records (IPv4)
    
    -PTR (reverse DNS)
    
    -CNAME extraction
    
    Structured, readable output









Skills Demonstrated:

    -Networking & Protocols
    
    -TCP socket development
    
    -Message framing & parsing
    
    -Multi-client communication
    
    -Event-driven architecture
    
    -DNS record types & resolver logic
    
    Software Engineering
    
    Clean modular structure
    
    Documentation & readability
    
    Defensive input handling
    
    Git version control workflow
    
    Security
    
    Input sanitization
    
    Blocking and filtering logic
    
    Handling malformed data




How to Run!!-
    Start the server
    python server.py


Start a client
    python client.py


Supported chat commands
    -NAME <your_name>
    -GET_NAMES
    -MSG <target> <message>
    -MSG BROADCAST <message>
    -BLOCK <name>
    -EXIT

Run DNS resolver
    python nslookup_DNS.py



Author,
Liel Kriheli
Software Engineering Student
Advanced Computer Networks Track
