# 🌐 How The Internet Works

> *"The internet is not a cloud. It's cables, computers, and a remarkably clever set of agreements about how they talk."*

Before HTTP, before HTML, there's the network itself. This chapter explains how a message gets from your computer to a server on the other side of the planet and back — and what actually happens in the seconds between pressing Enter on a URL and seeing a page.

---

## I. THE INTERNET IS A NETWORK OF NETWORKS

The word "internet" literally means *inter-network* — a network of networks. Your home Wi-Fi is a small network. Your ISP runs a bigger one. Universities, companies, and data centers run their own. The internet is all of them interconnected, agreeing to pass each other's traffic.

```
   Your laptop ── Home router ── ISP ── Regional network ── Backbone ── ... ── Server's data center
                                                (undersea cables, fiber, routers)
```

No one "owns" the internet. It works because everyone agrees on the same **protocols** — shared rules for how to format and route messages. The internet is, at heart, a set of agreements.

> **Key idea:** every device on the internet is identified by an **IP address** and communicates by breaking messages into **packets** that are routed independently across many networks to their destination.

---

## II. IP ADDRESSES — EVERY DEVICE HAS A NUMBER

An **IP address** (Internet Protocol address) is the unique number identifying a device on a network — like a postal address for computers.

### Two versions
- **IPv4** — four numbers 0–255, e.g. `93.184.216.34`. About 4.3 billion addresses. We've essentially run out.
- **IPv6** — much longer, e.g. `2606:2800:220:1:248:1893:25c8:1946`. Effectively unlimited (enough for every grain of sand to have trillions).

### Public vs private
- Your **public IP** is what the world sees (assigned by your ISP, often shared).
- Your **private IP** (like `192.168.x.x`) identifies your device *inside* your home network. Your router translates between them using **NAT** (Network Address Translation) — which is why many devices at home share one public IP.

```bash
# See your machine's IP info
# Windows:
ipconfig
# macOS / Linux:
ifconfig        # or:  ip addr

# Find the public IP of a domain
nslookup example.com
ping example.com          # shows the resolved IP and round-trip time
```

---

## III. DNS — THE INTERNET'S PHONE BOOK

Humans remember `google.com`; computers need `142.250.190.78`. **DNS** (Domain Name System) is the distributed directory that translates **domain names → IP addresses**.

### How a DNS lookup works

```
You request "example.com"
      │
      ▼
1. Browser cache?      ── "Have I looked this up recently?" If yes, done.
      │ no
      ▼
2. OS cache?           ── Operating system checks its own cache / hosts file.
      │ no
      ▼
3. Recursive resolver  ── Usually your ISP's (or 1.1.1.1 / 8.8.8.8). It does the legwork:
      │
      ├─▶ Root nameserver:  "Who handles .com?"        → "Ask the .com TLD servers."
      ├─▶ TLD nameserver:   "Who handles example.com?" → "Ask example.com's authoritative server."
      └─▶ Authoritative:    "What's example.com's IP?" → "93.184.216.34"
      │
      ▼
4. IP returned and CACHED (per the record's TTL) so next time is instant.
```

This whole hierarchy resolves in milliseconds. Results are **cached** at every level with a **TTL** (time-to-live) so the internet doesn't melt under repeated lookups.

### Common DNS record types

| Record | Maps... | Example |
|---|---|---|
| **A** | Domain → IPv4 | `example.com → 93.184.216.34` |
| **AAAA** | Domain → IPv6 | `example.com → 2606:2800:...` |
| **CNAME** | Domain → another domain (alias) | `www.example.com → example.com` |
| **MX** | Domain → mail server | routes email |
| **TXT** | Arbitrary text | verification, SPF/DKIM |
| **NS** | Domain → its nameservers | delegation |

```bash
# Inspect DNS records yourself
nslookup -type=A example.com
dig example.com           # macOS/Linux, more detailed
dig example.com MX        # see mail servers
```

> **Gotcha:** When you change a DNS record (e.g. point a domain to a new server), the change isn't instant everywhere — caches around the world hold the old value until their TTL expires. This is "DNS propagation," and it's why a new site sometimes works for some people but not others for a while.

---

## IV. PACKETS — MESSAGES BROKEN INTO PIECES

Data doesn't travel as one big blob. It's chopped into small **packets**, each sent independently and reassembled at the destination.

Each packet carries:
- **Payload** — a chunk of the actual data.
- **Header** — source IP, destination IP, sequence number (so they can be reordered), and more.

```
Big message:  "GET /index.html ... <all the data>"
                       │ split
                       ▼
   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
   │packet 1│ │packet 2│ │packet 3│ │packet 4│   each routed independently,
   │ seq=1  │ │ seq=2  │ │ seq=3  │ │ seq=4  │   possibly via different paths
   └────────┘ └────────┘ └────────┘ └────────┘
                       │ reassembled in order at the destination
                       ▼
              "GET /index.html ... <all the data>"
```

**Why packets?** Resilience and sharing. If one packet is lost, only that small piece is resent. Many conversations can share the same cables by interleaving packets. Packets can route around damage — the internet was designed to survive partial failure.

---

## V. THE TCP/IP MODEL — LAYERS OF RESPONSIBILITY

The internet's protocols are organized in **layers**, each handling one concern and trusting the layer below. This is the **TCP/IP model**:

| Layer | Job | Examples |
|---|---|---|
| **Application** | What the app actually wants to do | HTTP, HTTPS, DNS, SMTP, FTP |
| **Transport** | Reliable (or fast) delivery between programs | **TCP**, **UDP** |
| **Internet** | Routing packets across networks by IP | **IP**, ICMP |
| **Link** | Physical transmission on the local medium | Ethernet, Wi-Fi |

When you send data, it travels *down* the layers (each wraps the data with its own header), across the wire, then *up* the layers on the other side (each unwraps its header). This is **encapsulation**.

```
Your HTTP request
   ▼ Application : HTTP message
   ▼ Transport   : + TCP header (ports, sequence)        → "segment"
   ▼ Internet    : + IP header (source/dest IP)           → "packet"
   ▼ Link        : + Ethernet/Wi-Fi header                → "frame"
   ════ travels across the physical network ════
   ▲ each layer strips its header on the way up, on the server
```

### TCP vs UDP — the two transport choices

| | **TCP** | **UDP** |
|---|---|---|
| Reliability | Guaranteed, ordered delivery (retransmits lost packets) | Best-effort, no guarantees |
| Connection | Connection-based (handshake first) | Connectionless (just send) |
| Speed | Slower (overhead of acknowledgments) | Faster (no overhead) |
| Used by | HTTP, HTTPS, email, file transfer | Video calls, gaming, live streams, DNS queries |

**The TCP handshake** establishes a connection before data flows:

```
Client ──── SYN ───────▶ Server      "Let's talk?"
Client ◀─── SYN-ACK ──── Server      "Sure, ready?"
Client ──── ACK ───────▶ Server      "Ready. Go."
            (now data can flow reliably)
```

> **Why it matters:** HTTP runs over TCP, so every web request pays the cost of this handshake (plus a TLS handshake for HTTPS). This is why *connection reuse* and protocols like HTTP/2 and HTTP/3 matter for performance — they avoid repeating setup.

---

## VI. PORTS — MANY DOORS ON ONE ADDRESS

An IP address identifies a *machine*; a **port** identifies a specific *program* on that machine. One server can run a website (port 443), a mail server (port 25), and a database (port 5432) at once — the port says which one a packet is for.

| Port | Service |
|---|---|
| 80 | HTTP (unencrypted web) |
| 443 | HTTPS (encrypted web) |
| 22 | SSH (secure remote login) |
| 25 / 587 | Email (SMTP) |
| 5432 | PostgreSQL |
| 27017 | MongoDB |
| 3000 / 8080 | Common dev servers (you'll see these constantly) |

So `https://example.com` really means *"connect to example.com's IP, on port 443, speaking HTTP over TLS."*

---

## VII. PUTTING IT ALL TOGETHER — A URL BECOMES A PAGE

Let's trace the *entire* network journey for `https://example.com/page`:

```
1. PARSE URL      Browser splits it: scheme=https, host=example.com, port=443, path=/page
2. DNS LOOKUP     example.com → 93.184.216.34  (browser → OS → resolver → root → TLD → authoritative)
3. TCP HANDSHAKE  SYN / SYN-ACK / ACK with 93.184.216.34 on port 443
4. TLS HANDSHAKE  Negotiate encryption keys, verify the server's certificate (because https)
5. HTTP REQUEST   "GET /page HTTP/1.1, Host: example.com" sent (as packets, over TCP, over IP)
6. ROUTING        Packets hop router-to-router across many networks to the server
7. SERVER WORKS   Server receives, runs code, maybe queries a DB, builds a response
8. HTTP RESPONSE  "200 OK" + HTML travels back (as packets, reassembled in order)
9. BROWSER RENDERS Parses HTML; for each <link>/<script>/<img>, repeats steps 2–8
10. PAGE APPEARS   You see it. Connections may be kept alive for follow-up requests.
```

Steps 2–8 are pure networking — this chapter. Step 9 (rendering) is `03-Browsers-And-Rendering.md`. Steps 5/8 (the HTTP language) are the next chapter.

---

## VIII. ISPs AND THE PHYSICAL INTERNET

- **ISP (Internet Service Provider)** — the company that connects you to the rest of the internet (your home/mobile provider). They route your traffic toward its destination and assign your public IP.
- **Backbone** — high-capacity long-haul networks (run by large telecoms) that carry traffic between regions and countries.
- **Undersea cables** — the internet between continents is mostly physical fiber-optic cables on the ocean floor. "The cloud" is, ultimately, cables and buildings full of computers.
- **IXPs (Internet Exchange Points)** — physical locations where different networks interconnect to hand off traffic efficiently.

This physical reality explains **latency**: a request to a server on another continent is fundamentally limited by the speed of light through fiber plus router hops. You can't beat physics — which is exactly why **CDNs** put copies of content geographically close to users (see `06-Web-Performance-And-Security-Basics.md`).

---

## IX. COMMON PITFALLS / GOTCHAS

- **"DNS changes are instant."** No — caching and TTLs mean changes propagate gradually. Lower a record's TTL *before* a planned migration.
- **Confusing IP and DNS.** DNS *translates* names to IPs; it doesn't transport your data. The transport is TCP/IP.
- **Forgetting localhost is special.** `localhost` / `127.0.0.1` is your own machine — it never touches the network or DNS. Great for dev, but it hides every real-world networking issue.
- **Assuming HTTPS hides everything.** TLS encrypts the *content* and *path*, but the *destination IP* and (often) the domain name are still observable. It protects the message, not the fact you're talking.
- **Ignoring latency vs bandwidth.** Bandwidth is how *much* data per second; latency is how *long* until the first byte. Many "slow site" problems are latency (round trips), not bandwidth — and physics sets a floor.
- **"The internet" = "the web."** The web (HTTP/HTML) is *one* application running on the internet. Email, video calls, and games are others, on the same network.

---

## ✅ KEY TAKEAWAYS

- The internet is a **network of networks** held together by shared **protocols**, not owned by anyone.
- Every device has an **IP address**; **DNS** translates human domain names into those addresses via a cached, hierarchical lookup (root → TLD → authoritative).
- Data travels as independently-routed **packets**, organized by the layered **TCP/IP model** (Application → Transport → Internet → Link), each layer adding/stripping its own header.
- **TCP** gives reliable, ordered delivery (used by HTTP) via a handshake; **UDP** trades guarantees for speed.
- **Ports** distinguish programs on one machine (80=HTTP, 443=HTTPS, 22=SSH...).
- A URL becomes a page through: parse → DNS → TCP → TLS → HTTP request → routing → server → response → render. Hold this whole journey in your head.
- Latency is bounded by physical distance and router hops — the reason CDNs exist.

---

**→ Next:** [`02-HTTP-And-HTTPS.md`](./02-HTTP-And-HTTPS.md) — the language clients and servers speak
**← Prev:** [`00-Index.md`](./00-Index.md)
**🗺️ Index:** [`00-Index.md`](./00-Index.md)
