# 🌐 Computer Networks — Interview Prep

> The "what happens when you type a URL?" subject. Master the layered models and key protocols.

---

## THE SYLLABUS (interview-relevant)
1. **OSI Model** (7 layers) & **TCP/IP Model** (4-5 layers)
2. **TCP vs UDP** — reliability, ordering, use cases
3. **IP Addressing** — IPv4/IPv6, subnetting, CIDR, public/private
4. **DNS** — resolution process, record types
5. **HTTP/HTTPS** — methods, status codes, TLS handshake
6. **Routing** — routers, switches, protocols (RIP, OSPF, BGP basics)
7. **TCP mechanics** — 3-way handshake, congestion control, flow control
8. **Application protocols** — HTTP, FTP, SMTP, DHCP, ARP
9. **Network devices** — hub, switch, router, gateway

---

## THE TOP 20 INTERVIEW QUESTIONS
1. Explain the OSI model (7 layers).
2. TCP vs UDP?
3. **What happens when you type a URL and press Enter?** ⭐ (the classic)
4. Explain the TCP 3-way handshake.
5. What is DNS? How does resolution work?
6. HTTP vs HTTPS? How does TLS work?
7. Hub vs Switch vs Router?
8. What is an IP address? IPv4 vs IPv6?
9. What is subnetting? CIDR?
10. What is ARP? DHCP?
11. Common HTTP status codes? (200, 301, 404, 500, etc.)
12. What is congestion control? (slow start, AIMD)
13. What is flow control? (sliding window)
14. Public vs private IP? NAT?
15. What is a socket?
16. GET vs POST?
17. What is latency vs bandwidth vs throughput?
18. What is a MAC address vs IP address?
19. What are common ports? (80, 443, 22, 21, 25, 53)
20. What is a firewall? VPN?

---

## THE "URL" ANSWER (memorize this flow)
1. Browser checks cache; if miss, **DNS resolution** (recursive: resolver → root → TLD → authoritative) returns the IP
2. **TCP connection** established (3-way handshake: SYN, SYN-ACK, ACK)
3. If HTTPS, **TLS handshake** (negotiate keys, verify certificate)
4. Browser sends **HTTP request** (GET /)
5. Server processes, returns **HTTP response** (status + HTML)
6. Browser **renders** (parses HTML, fetches CSS/JS/images, builds DOM, paints)
7. Connection closed (or kept alive)

---

## RESOURCES
### YouTube ⭐
- **[Gate Smashers](https://www.youtube.com/@GateSmashers)** — complete CN playlist
- **[Neso Academy](https://www.youtube.com/@nesoacademy)** — CN (detailed)
- **[Knowledge Gate](https://www.youtube.com/@KnowledgeGate.in)** — CN

### Written
- **[GeeksforGeeks](https://www.geeksforgeeks.org)** — CN Last Minute Notes + interview questions ⭐

### Books / Free
- **Computer Networking: A Top-Down Approach** (Kurose & Ross) ⭐
- **Computer Networks** (Tanenbaum)

---

## PREP PLAN (5 days)
- Day 1: OSI/TCP-IP models
- Day 2: TCP/UDP, 3-way handshake, congestion/flow control
- Day 3: IP addressing, subnetting, NAT, DNS
- Day 4: HTTP/HTTPS, TLS, application protocols
- Day 5: Devices, routing + the "URL" flow + revise top 20

---

**→ Next:** [`04-OOP.md`](./04-OOP.md)
