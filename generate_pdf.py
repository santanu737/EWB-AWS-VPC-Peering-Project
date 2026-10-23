#!/usr/bin/env python3
"""
generate_pdf.py
Builds SantanuMondal_EWB_VPC_Peering.pdf (EWB AWS VPC Peering Student Project).

Usage:
    pip install reportlab
    python generate_pdf.py

Put the screenshot files (see IMAGE_FILES below) in the same folder as this
script, or change IMAGE_DIR. Any missing image is replaced by a styled
placeholder box, so the script always runs without errors.
"""

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
OUTPUT_FILE = "SantanuMondal_EWB_VPC_Peering.pdf"
IMAGE_DIR = os.path.dirname(os.path.abspath(__file__))

STUDENT = "Santanu Mondal"
PROJECT = "EWB AWS VPC Peering Student Project"
REGION = "us-west-2 (Oregon)"
EXEC_DATE = "October 23, 2026"
ENVIRONMENT = "AWS Skill Builder lab sandbox (AWSLabsUser role)"
PCX_ID = "pcx-0a53069a0b0424408"
PCX_NAME = "ewb-peering-a-to-b"

IMAGE_FILES = {
    "vpc": "vpc_details.png",
    "subnets": "subnets.png",
    "igw": "igw_attached.png",
    "peering": "peering_connection.png",
    "routes": "route_tables.png",
    "sg": "security_groups.png",
}

NAVY = colors.HexColor("#1A365D")
SLATE = colors.HexColor("#4A5568")
LIGHT = colors.HexColor("#EDF2F7")
WHITE = colors.white
AMBER = colors.HexColor("#B7791F")
AMBER_BG = colors.HexColor("#FEFCBF")
RED = colors.HexColor("#9B2C2C")

PAGE_W, PAGE_H = letter
MARGIN = 0.5 * inch
CONTENT_W = PAGE_W - 2 * MARGIN  # 7.5 inch

# --------------------------------------------------------------------------
# Styles
# --------------------------------------------------------------------------
base = getSampleStyleSheet()

S = {
    "body": ParagraphStyle(
        "body", parent=base["Normal"], fontName="Helvetica", fontSize=9.5,
        leading=13.5, textColor=colors.HexColor("#2D3748"), alignment=TA_JUSTIFY,
        spaceAfter=6,
    ),
    "bullet": ParagraphStyle(
        "bullet", parent=base["Normal"], fontName="Helvetica", fontSize=9.5,
        leading=13, textColor=colors.HexColor("#2D3748"), leftIndent=14,
        bulletIndent=3, spaceAfter=2,
    ),
    "h1": ParagraphStyle(
        "h1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=15,
        leading=19, textColor=NAVY, spaceBefore=10, spaceAfter=2,
    ),
    "h2": ParagraphStyle(
        "h2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=11.5,
        leading=15, textColor=NAVY, spaceBefore=9, spaceAfter=4,
    ),
    "h3": ParagraphStyle(
        "h3", parent=base["Heading3"], fontName="Helvetica-Bold", fontSize=10,
        leading=13, textColor=SLATE, spaceBefore=6, spaceAfter=3,
    ),
    "cell": ParagraphStyle(
        "cell", parent=base["Normal"], fontName="Helvetica", fontSize=8.3,
        leading=10.8, textColor=colors.HexColor("#2D3748"), alignment=TA_LEFT,
    ),
    "cellh": ParagraphStyle(
        "cellh", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=8.3,
        leading=10.8, textColor=WHITE, alignment=TA_LEFT,
    ),
    "caption": ParagraphStyle(
        "caption", parent=base["Normal"], fontName="Helvetica-Oblique",
        fontSize=8, leading=10.5, textColor=SLATE, alignment=TA_CENTER,
        spaceBefore=3, spaceAfter=8,
    ),
    "code": ParagraphStyle(
        "code", parent=base["Code"], fontName="Courier", fontSize=8, leading=10.5,
        textColor=colors.HexColor("#1A202C"), backColor=LIGHT, borderPadding=(5, 6, 5, 6),
        leftIndent=6, rightIndent=6, spaceBefore=4, spaceAfter=9,
    ),
    "note": ParagraphStyle(
        "note", parent=base["Normal"], fontName="Helvetica", fontSize=9,
        leading=12.5, textColor=colors.HexColor("#2D3748"), alignment=TA_LEFT,
    ),
    "title": ParagraphStyle(
        "title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=24,
        leading=29, textColor=WHITE, alignment=TA_LEFT,
    ),
    "subtitle": ParagraphStyle(
        "subtitle", parent=base["Normal"], fontName="Helvetica", fontSize=12,
        leading=16, textColor=colors.HexColor("#CBD5E0"), alignment=TA_LEFT,
    ),
}


# --------------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------------
def P(text, style="body"):
    return Paragraph(text, S[style])


def H1(text):
    return KeepTogether([
        Paragraph(text, S["h1"]),
        HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=6),
    ])


def H2(text):
    return Paragraph(text, S["h2"])


def H3(text):
    return Paragraph(text, S["h3"])


def bullets(items):
    return [Paragraph(t, S["bullet"], bulletText="\u2022") for t in items]


def code(text):
    return Preformatted(text.strip("\n"), S["code"])


def table(rows, col_widths, header=True, zebra=True):
    """Build a styled table. Strings are wrapped in Paragraphs for wrapping."""
    data = []
    for r_idx, row in enumerate(rows):
        style = "cellh" if (header and r_idx == 0) else "cell"
        data.append([c if not isinstance(c, str) else Paragraph(c, S[style]) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]
    if header:
        cmds.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    if zebra:
        start = 1 if header else 0
        for i in range(start, len(data)):
            if (i - start) % 2 == 1:
                cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
    t.setStyle(TableStyle(cmds))
    return t


def callout(title, body_html, bg=AMBER_BG, border=AMBER):
    inner = [Paragraph("<b>%s</b>" % title, S["note"]), Spacer(1, 2), Paragraph(body_html, S["note"])]
    t = Table([[inner]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.8, border),
        ("LINEBEFORE", (0, 0), (0, -1), 4, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def figure(filename, caption, max_w=6.9 * inch, max_h=4.0 * inch):
    """Embed a local image; fall back to a styled placeholder on any problem."""
    path = os.path.join(IMAGE_DIR, filename)
    try:
        if not os.path.isfile(path):
            raise FileNotFoundError(path)
        iw, ih = ImageReader(path).getSize()
        scale = min(max_w / float(iw), max_h / float(ih))
        img = Image(path, width=iw * scale, height=ih * scale)
        img.hAlign = "CENTER"
        box = Table([[img]], colWidths=[CONTENT_W])
        box.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#CBD5E0")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
    except Exception:
        ph = Paragraph(
            "<b>[ Screenshot placeholder ]</b><br/>File not found or unreadable: "
            "<font face='Courier'>%s</font><br/>Place the image next to this script "
            "and re-run to embed it." % filename,
            ParagraphStyle("ph", parent=S["note"], alignment=TA_CENTER, textColor=SLATE),
        )
        box = Table([[ph]], colWidths=[CONTENT_W], rowHeights=[1.5 * inch])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
            ("BOX", (0, 0), (-1, -1), 1, SLATE, None, (4, 3)),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
    return KeepTogether([box, Paragraph(caption, S["caption"])])


def test_block(title, purpose, preconditions, procedure, expected, conclusion):
    """Layout for one test: summary table + procedure code block."""
    rows = [
        [Paragraph("<b>Purpose</b>", S["cell"]), Paragraph(purpose, S["cell"])],
        [Paragraph("<b>Preconditions</b>", S["cell"]), Paragraph(preconditions, S["cell"])],
        [Paragraph("<b>Expected result</b>", S["cell"]), Paragraph(expected, S["cell"])],
        [Paragraph("<b>Conclusion</b>", S["cell"]), Paragraph(conclusion, S["cell"])],
    ]
    t = Table(rows, colWidths=[1.3 * inch, CONTENT_W - 1.3 * inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, -1), LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]))
    return [H3(title), t, Paragraph("<b>Procedure</b>", S["cell"]), code(procedure), Spacer(1, 4)]


# --------------------------------------------------------------------------
# Page chrome (running header / footer with "Page X of Y")
# --------------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_pages = []

    def showPage(self):
        self._saved_pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_pages)
        for state in self._saved_pages:
            self.__dict__.update(state)
            self._draw_chrome(total)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def _draw_chrome(self, total):
        page = self._pageNumber
        self.saveState()
        # Header (skipped on the first page, which has the title banner)
        if page > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(NAVY)
            self.drawString(MARGIN, PAGE_H - MARGIN + 6, "EWB AWS VPC Peering Student Project")
            self.setFont("Helvetica", 8)
            self.setFillColor(SLATE)
            self.drawRightString(PAGE_W - MARGIN, PAGE_H - MARGIN + 6, "Region: us-west-2 (Oregon)")
            self.setStrokeColor(NAVY)
            self.setLineWidth(0.8)
            self.line(MARGIN, PAGE_H - MARGIN + 2, PAGE_W - MARGIN, PAGE_H - MARGIN + 2)
        # Footer
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.6)
        self.line(MARGIN, MARGIN - 6, PAGE_W - MARGIN, MARGIN - 6)
        self.setFont("Helvetica", 8)
        self.setFillColor(SLATE)
        self.drawString(MARGIN, MARGIN - 18, "%s  |  %s" % (STUDENT, EXEC_DATE))
        self.drawRightString(PAGE_W - MARGIN, MARGIN - 18, "Page %d of %d" % (page, total))
        self.restoreState()


# --------------------------------------------------------------------------
# Document content
# --------------------------------------------------------------------------
def build_story():
    st = []

    # ---- Title banner -----------------------------------------------------
    banner = Table(
        [[[
            Paragraph("EWB AWS VPC Peering<br/>Student Project", S["title"]),
            Spacer(1, 6),
            Paragraph("Connect two VPCs. Prove private connectivity.", S["subtitle"]),
        ]]],
        colWidths=[CONTENT_W],
    )
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 18),
        ("RIGHTPADDING", (0, 0), (-1, -1), 18),
        ("TOPPADDING", (0, 0), (-1, -1), 22),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 22),
    ]))
    st += [banner, Spacer(1, 10)]

    meta = [
        ["Student", STUDENT],
        ["Project", PROJECT],
        ["AWS Region", REGION],
        ["Execution date", EXEC_DATE],
        ["Environment", ENVIRONMENT],
        ["Account / role", "AWSLabsUser (managed lab sandbox)"],
    ]
    mt = Table([[Paragraph("<b>%s</b>" % a, S["cell"]), Paragraph(b, S["cell"])] for a, b in meta],
               colWidths=[1.5 * inch, CONTENT_W - 1.5 * inch])
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E0")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    st += [mt, Spacer(1, 8)]

    # ---- 1. Executive summary --------------------------------------------
    st.append(H1("1. Executive Summary"))
    st.append(H2("1.1 Objective"))
    st.append(P(
        "This project builds the network foundation for private connectivity between two isolated "
        "Amazon VPCs using a <b>VPC Peering Connection</b>, and defines a verification plan that proves: "
        "(a) workloads in separate VPCs communicate over private IP addresses without crossing the public "
        "internet; (b) administrative access to private instances is possible only through a hardened "
        "bastion host; and (c) reachability depends on routing in <i>both</i> VPCs plus correct security "
        "group rules, not on the peering state alone."))
    st.append(H2("1.2 Architecture overview"))
    st += bullets([
        "<b>VPC A (ewb-vpc-a)</b> contains a public subnet (planned bastion host, internet-facing through an "
        "Internet Gateway) and a private subnet (planned App-A).",
        "<b>VPC B (ewb-vpc-b)</b> contains a single private subnet (planned App-B) with no Internet Gateway "
        "and no public addressing.",
        "A <b>peering connection</b> links the two VPCs. Static routes in each VPC direct traffic for the "
        "remote CIDR through the peering connection.",
    ])
    st.append(Spacer(1, 4))
    st.append(H2("1.3 Non-overlapping CIDR plan and IP design rationale"))
    st.append(table([
        ["Network", "CIDR", "Role", "Usable IPs*"],
        ["VPC A", "10.10.0.0/16", "Bastion + App-A", "65,531"],
        ["&nbsp;&nbsp;ewb-a-public", "10.10.1.0/24", "Bastion host", "251"],
        ["&nbsp;&nbsp;ewb-a-private", "10.10.2.0/24", "App-A", "251"],
        ["VPC B", "10.20.0.0/16", "App-B", "65,531"],
        ["&nbsp;&nbsp;ewb-b-private", "10.20.1.0/24", "App-B", "251"],
    ], [2.2 * inch, 1.6 * inch, 2.4 * inch, 1.3 * inch]))
    st.append(P("<font size=7.5 color='#4A5568'>*AWS reserves 5 addresses per subnet (network address, VPC router, "
                "DNS, reserved for future use, broadcast).</font>"))
    st += bullets([
        "<b>Non-overlapping ranges are mandatory.</b> AWS refuses to peer VPCs with overlapping CIDRs, and "
        "routing would be ambiguous. 10.10.0.0/16 and 10.20.0.0/16 share no addresses.",
        "<b>RFC 1918 private space</b> keeps all traffic non-routable on the public internet.",
        "<b>Readable octet scheme:</b> the second octet identifies the VPC (10 = A, 20 = B) and the third "
        "identifies the tier (1 = public, 2 = private in A; 1 = private in B), making route tables and "
        "security rules easy to audit.",
        "<b>/16 VPCs with /24 subnets</b> leave room for more tiers or Availability Zones without renumbering.",
    ])

    # ---- 2. Inventory & evidence -----------------------------------------
    st.append(PageBreak())
    st.append(H1("2. Resource Inventory and Evidence"))
    st.append(H2("2.1 VPCs, subnets, gateways and peering"))
    st.append(table([
        ["Resource", "Name", "ID", "CIDR / Detail"],
        ["VPC", "ewb-vpc-a", "vpc-00595e2a2cfb858dd", "10.10.0.0/16; State: Available; DNS resolution enabled"],
        ["VPC", "ewb-vpc-b", "vpc-0d558ceae7d6a326c", "10.20.0.0/16"],
        ["Subnet", "ewb-a-public", "subnet-0fee352033ec319c6", "10.10.1.0/24"],
        ["Subnet", "ewb-a-private", "subnet-0a000387dc83a4d12", "10.10.2.0/24"],
        ["Subnet", "ewb-b-private", "subnet-05debd941ed0e600a", "10.20.1.0/24"],
        ["Internet Gateway", "ewb-igw-a", "igw-0a44f93c2902ce0ee", "Attached to ewb-vpc-a"],
        ["Peering Connection", PCX_NAME, PCX_ID,
         "Requester: ewb-vpc-a (10.10.0.0/16); Accepter: ewb-vpc-b; "
         "<b>Status: Pending acceptance</b> (expires Oct 29, 2026)"],
    ], [1.2 * inch, 1.3 * inch, 2.0 * inch, 3.0 * inch]))
    st.append(Spacer(1, 6))

    st.append(H2("2.2 Route tables"))
    st.append(table([
        ["Route table", "ID", "Associated subnet", "Routes as configured"],
        ["ewb-rt-a-public", "rtb-0b9a24627a866393f", "ewb-a-public",
         "10.10.0.0/16 -&gt; local (Active)<br/>0.0.0.0/0 -&gt; igw-0a44f93c2902ce0ee (Active)<br/>"
         "<i>Peering route for 10.20.0.0/16 required, see Section 3.3</i>"],
        ["ewb-rt-a-private", "rtb-0a1e8f41cdd77a5d6", "ewb-a-private",
         "10.10.0.0/16 -&gt; local (Active)<br/>10.20.0.0/16 -&gt; " + PCX_ID + " (<b>Blackhole</b>)"],
        ["ewb-rt-b-private", "rtb-026be207ac9b3a54c", "ewb-b-private",
         "10.20.0.0/16 -&gt; local (Active)<br/>10.10.0.0/16 -&gt; " + PCX_ID + " (<b>Blackhole</b>)"],
        ["Main (VPC A)", "rtb-066ad9197c76fd172", "None explicit", "10.10.0.0/16 -&gt; local"],
    ], [1.25 * inch, 1.6 * inch, 1.2 * inch, 3.45 * inch]))
    st.append(P("<font size=7.5 color='#4A5568'>Blackhole is the expected status of a peering route while the "
                "connection has not been accepted. It changes to Active once the accepter side accepts the "
                "request.</font>"))

    st.append(H2("2.3 Security groups"))
    st.append(table([
        ["Security group", "ID", "VPC", "Inbound rules"],
        ["ewb-sg-bastion", "sg-0cb096ef048164789", "VPC A", "TCP 22 from Admin public IP /32"],
        ["ewb-sg-app-a", "(record from console)", "VPC A",
         "TCP 22 from 10.10.1.10/32 (bastion)<br/>ICMP Echo Request from 10.20.1.10/32 (App-B)"],
        ["ewb-sg-app-b", "sg-02f97011ae2d414a4", "VPC B",
         "TCP 22 from 10.10.1.10/32 (bastion)<br/>ICMP Echo Request from 10.10.2.10/32 (App-A)"],
    ], [1.3 * inch, 1.7 * inch, 0.7 * inch, 3.8 * inch]))
    st.append(Spacer(1, 6))

    st.append(H2("2.4 Planned compute (not launched, see Section 5)"))
    st.append(table([
        ["Instance", "Subnet", "Private IP", "Security group", "Public IP"],
        ["Bastion", "ewb-a-public", "10.10.1.10", "ewb-sg-bastion", "Yes"],
        ["App-A", "ewb-a-private", "10.10.2.10", "ewb-sg-app-a", "No"],
        ["App-B", "ewb-b-private", "10.20.1.10", "ewb-sg-app-b", "No"],
    ], [1.2 * inch, 1.5 * inch, 1.3 * inch, 2.1 * inch, 1.4 * inch]))

    st.append(H2("2.5 Screenshot evidence"))
    st.append(figure(IMAGE_FILES["vpc"],
                     "Figure 1. VPC A (ewb-vpc-a, vpc-00595e2a2cfb858dd) created and in the Available state."))
    st.append(figure(IMAGE_FILES["subnets"],
                     "Figure 2. Public (ewb-a-public) and private (ewb-a-private) subnets created in VPC A."))
    st.append(figure(IMAGE_FILES["igw"],
                     "Figure 3. Internet gateway ewb-igw-a (igw-0a44f93c2902ce0ee) attached to ewb-vpc-a."))
    st.append(figure(IMAGE_FILES["peering"],
                     "Figure 4. Peering connection %s (%s) showing <b>Pending acceptance</b>." % (PCX_NAME, PCX_ID)))

    # ---- 3. Analysis ------------------------------------------------------
    st.append(PageBreak())
    st.append(H1("3. Network Routing and Security Architecture Analysis"))
    st.append(H2("3.1 Route table target evaluation (longest-prefix match)"))
    st.append(P(
        "A VPC route table selects the <b>most specific</b> matching destination (longest prefix). Every table "
        "contains an immutable <font face='Courier'>local</font> route for its own VPC CIDR. If no route matches, "
        "the packet is dropped. A route whose target is a peering connection that is not Active is shown as "
        "<b>Blackhole</b> and matching traffic is silently discarded."))
    st.append(table([
        ["Source -&gt; destination", "Table consulted", "Matching route", "Outcome"],
        ["App-A -&gt; App-B (10.20.1.10)", "ewb-rt-a-private", "10.20.0.0/16 -&gt; pcx", "Forwarded over peering (once Active)"],
        ["App-B -&gt; App-A (10.10.2.10)", "ewb-rt-b-private", "10.10.0.0/16 -&gt; pcx", "Forwarded over peering (once Active)"],
        ["Bastion -&gt; App-B", "ewb-rt-a-public", "10.20.0.0/16 -&gt; pcx (/16 beats 0.0.0.0/0)", "Forwarded over peering (requires the route)"],
        ["Bastion -&gt; Internet", "ewb-rt-a-public", "0.0.0.0/0 -&gt; igw", "Exits through IGW"],
        ["App-A -&gt; Internet", "ewb-rt-a-private", "No match", "Dropped (no NAT, by design)"],
        ["App-B -&gt; Internet", "ewb-rt-b-private", "No match", "Dropped (no IGW in VPC B)"],
    ], [1.9 * inch, 1.3 * inch, 2.3 * inch, 2.0 * inch]))
    st.append(Spacer(1, 4))

    st.append(H2("3.2 Stateful security group mechanics"))
    st.append(P(
        "Security groups are <b>stateful</b>: when traffic is permitted in one direction, the response is "
        "automatically permitted regardless of outbound rules. App-B therefore needs only an inbound ICMP "
        "<i>Echo Request</i> rule for App-A; the Echo Reply is allowed automatically. Rules are allow-only with "
        "an implicit deny, and each source is scoped to a single host (/32) following least privilege. "
        "Security groups filter packets but do not create paths, so <b>routing and filtering are independent "
        "controls</b>, and both must permit traffic. (Network ACLs, by contrast, are stateless and need rules "
        "in both directions; the default ACL allows all.)"))

    st.append(H2("3.3 Bastion, ProxyJump and the public route table"))
    st.append(P(
        "App-A and App-B have no public IP addresses and cannot be reached from the internet. All "
        "administration flows through one hardened entry point, the bastion in the public subnet, whose "
        "security group accepts SSH only from the administrator's /32."))
    st.append(code(
        "Laptop --SSH/22--> Bastion (10.10.1.10, public subnet, Admin /32 only)\n"
        "                     |--SSH/22, private IP--------> App-A (10.10.2.10)\n"
        "                     |--SSH/22, over peering------> App-B (10.20.1.10)"))
    st.append(P(
        "With SSH <b>ProxyJump</b> (<font face='Courier'>-J</font>) the laptop opens one end-to-end encrypted "
        "session whose transport hops through the bastion. The private key never leaves the laptop."))
    st.append(code(
        "ssh -i ewb-key.pem -J ec2-user@<BASTION_PUBLIC_IP> ec2-user@10.20.1.10\n"
        "\n"
        "# ~/.ssh/config equivalent\n"
        "Host ewb-bastion\n"
        "    HostName <BASTION_PUBLIC_IP>\n"
        "    User ec2-user\n"
        "    IdentityFile ~/ewb-key.pem\n"
        "Host ewb-app-b\n"
        "    HostName 10.20.1.10\n"
        "    User ec2-user\n"
        "    IdentityFile ~/ewb-key.pem\n"
        "    ProxyJump ewb-bastion"))
    st.append(P(
        "<b>Why the public route table needs a route for 10.20.0.0/16.</b> The second SSH hop is initiated by "
        "the bastion, so the route table of <i>its</i> subnet (ewb-rt-a-public) decides where the packet goes. "
        "Without <font face='Courier'>10.20.0.0/16 -&gt; %s</font>, traffic to 10.20.1.10 matches only "
        "<font face='Courier'>0.0.0.0/0 -&gt; igw</font> and is sent to the Internet Gateway, which cannot deliver "
        "to a private address, so the hop fails. Adding the more specific /16 peering route wins by "
        "longest-prefix match while all other traffic still uses the IGW." % PCX_ID))
    st.append(callout(
        "Configuration status",
        "In the captured evidence, ewb-rt-a-public contains only the local route and the IGW default route. "
        "The <font face='Courier'>10.20.0.0/16 -&gt; %s</font> entry is documented here as a <b>required "
        "addition</b> to be applied before Test 04, since it is mandatory for the bastion-to-App-B path." % PCX_ID))
    st.append(Spacer(1, 8))
    st.append(H2("3.4 Properties of VPC peering relevant to this design"))
    st += bullets([
        "<b>Non-transitive:</b> peering gives access only to the peer VPC's own resources, never to its "
        "IGW, NAT gateway, VPN or Direct Connect.",
        "<b>Private path:</b> traffic stays on the AWS backbone without NAT, so original source IPs are preserved.",
        "<b>Both sides must route, and the request must be accepted</b> by the accepter before it becomes Active.",
    ])
    st.append(Spacer(1, 6))
    st.append(H2("3.5 Screenshot evidence"))
    st.append(figure(IMAGE_FILES["routes"],
                     "Figure 5. Route tables (top left to bottom right): ewb-rt-a-public routes, ewb-rt-a-private routes, "
                     "ewb-rt-b-private routes and ewb-rt-a-public subnet associations. Peering routes show "
                     "Blackhole while the connection is pending.", max_h=5.2 * inch))
    st.append(figure(IMAGE_FILES["sg"],
                     "Figure 6. Inbound rules for ewb-sg-bastion (left) and ewb-sg-app-b (right). "
                     "The ewb-sg-app-a screenshot was not captured.", max_h=3.0 * inch))

    # ---- 4. Tests ---------------------------------------------------------
    st.append(PageBreak())
    st.append(H1("4. Testing and Verification Mechanics (Tests 01 to 05)"))
    st.append(callout(
        "Status of this section",
        "Tests 01 to 05 are specified as a validation procedure with <b>expected results derived from the "
        "configured routing and security state</b>. They were <b>not executed</b> on live instances because the "
        "sandbox denied compute launch and peering acceptance (Section 5). No terminal output is presented "
        "as observed."))
    st.append(Spacer(1, 6))

    st += test_block(
        "Test 01: Baseline failure (no usable peering path)",
        "Prove that the two VPCs are isolated by default.",
        "No active peering route between the VPCs (peering absent, pending or route not yet added). "
        "App-A and App-B running.",
        "# On App-A\nping -c 4 10.20.1.10",
        "<font face='Courier'>4 packets transmitted, 0 received, 100% packet loss</font>. "
        "The route for 10.20.0.0/16 is missing or Blackhole, so packets never leave VPC A.",
        "Separate VPCs cannot communicate until peering is Active and routes exist. The current Pending/Blackhole "
        "state is exactly this baseline.")

    st += test_block(
        "Test 02: App-A to App-B ping across the peering connection",
        "Show private connectivity from VPC A to VPC B.",
        "Peering Active; routes present on both sides; ewb-sg-app-b allows ICMP Echo Request from 10.10.2.10/32.",
        "# On App-A\nping -c 4 10.20.1.10",
        "<font face='Courier'>4 packets transmitted, 4 received, 0% packet loss</font>.",
        "Forward path (App-A route + peering + App-B security group) is functional.")

    st += test_block(
        "Test 03: App-B to App-A ping (reverse direction)",
        "Show that connectivity is bidirectional and the return route works.",
        "As Test 02, plus ewb-sg-app-a allows ICMP Echo Request from 10.20.1.10/32.",
        "# On App-B\nping -c 4 10.10.2.10",
        "<font face='Courier'>4 packets transmitted, 4 received, 0% packet loss</font>.",
        "Both route tables and both security groups are correctly configured.")

    st += test_block(
        "Test 04: Private SSH via ProxyJump (Laptop -> Bastion -> App-B)",
        "Prove that App-B is reachable for administration only through the bastion.",
        "Instances running; ewb-rt-a-public has the 10.20.0.0/16 peering route; App-B SG allows TCP 22 from "
        "10.10.1.10/32; bastion SG allows TCP 22 from the Admin /32.",
        "# Allowed: via bastion\n"
        "ssh -i ewb-key.pem -J ec2-user@<BASTION_PUBLIC_IP> ec2-user@10.20.1.10\n"
        "hostname -I            # expect 10.20.1.10\n"
        "\n"
        "# Must fail: direct from laptop\n"
        "ssh -i ewb-key.pem ec2-user@10.20.1.10",
        "Jump login succeeds and App-B sees the connection from 10.10.1.10. The direct attempt times out "
        "because 10.20.1.10 is not routable from the internet.",
        "Single controlled entry point confirmed; private instances are not exposed.")

    st += test_block(
        "Test 05: Controlled ICMP failure and recovery",
        "Show that the security group, not the route, controls ICMP, and that the fault is reversible.",
        "Test 02 passing.",
        "1) ping -c 4 10.20.1.10        # App-A: 0% loss\n"
        "2) Delete the ICMP rule from ewb-sg-app-b\n"
        "3) ping -c 4 10.20.1.10        # App-A: 100% loss (timeouts)\n"
        "4) SSH via bastion to App-B    # still works (only ICMP removed)\n"
        "5) Re-add ICMP Echo Request from 10.10.2.10/32\n"
        "6) ping -c 4 10.20.1.10        # App-A: 0% loss",
        "0% loss, then 100% loss after rule removal (silent drop, not 'unreachable'), then 0% loss after restore.",
        "Routing and peering remained healthy throughout; only filtering changed. This separates routing "
        "faults from security group faults when troubleshooting.")

    # ---- 5. Sandbox constraint -------------------------------------------
    st.append(PageBreak())
    st.append(H1("5. Sandbox Environmental Constraint Notice"))
    st.append(P(
        "This project was executed in a managed AWS Skill Builder sandbox under the IAM role "
        "<b>AWSLabsUser</b>. The role's policy <b>explicitly denies</b> two actions required to complete the "
        "end-to-end validation:"))
    st += bullets([
        "<font face='Courier'>ec2:RunInstances</font>: no EC2 instance (bastion, App-A, App-B) could be launched.",
        "<font face='Courier'>ec2:AcceptVpcPeeringConnection</font>: the peering request created from VPC A "
        "could not be accepted on the VPC B side, so it remains in <b>Pending acceptance</b>.",
    ])
    st.append(Spacer(1, 4))
    st.append(P(
        "In IAM policy evaluation an explicit deny overrides any allow, so neither action can be performed "
        "in this account regardless of other permissions. The Blackhole status on both peering routes is the "
        "expected consequence of the connection not being Active, and is consistent with the console evidence "
        "in Figures 4 and 5."))
    st.append(table([
        ["Layer", "Status"],
        ["VPCs, subnets, Internet Gateway", "Built and verified"],
        ["Route tables and subnet associations", "Built and verified"],
        ["Peering connection request and static routes", "Built; connection <b>Pending acceptance</b> "
         "(acceptance denied by IAM); routes Blackhole"],
        ["Security groups and rules", "Built and verified"],
        ["Peering route in ewb-rt-a-public (10.20.0.0/16)", "Documented as required; not present in captured evidence"],
        ["EC2 instances (Bastion, App-A, App-B)", "<b>Not launched</b>: ec2:RunInstances explicitly denied"],
        ["Live ping and SSH tests (01 to 05)", "<b>Not executable</b> without compute and an Active peering"],
    ], [3.3 * inch, 4.2 * inch]))
    st.append(Spacer(1, 6))
    st.append(P(
        "All network and security infrastructure that the tests depend on was configured, so validation can "
        "run as soon as the peering is accepted and compute permissions exist. Expected outcomes in Section 4 "
        "follow deterministically from longest-prefix route evaluation, stateful security group behaviour and "
        "the non-transitive nature of peering."))

    # ---- 6. Viva ----------------------------------------------------------
    st.append(H1("6. Technical Viva and Evaluation Questions"))

    st.append(H3("Q1. Why is a return route required in VPC B?"))
    st.append(P(
        "Peering routing is neither automatic nor symmetric. When App-A pings App-B, the Echo Reply from "
        "10.20.1.10 is addressed to 10.10.2.10. App-B's subnet consults ewb-rt-b-private; with only "
        "<font face='Courier'>10.20.0.0/16 -&gt; local</font> there is no match for 10.10.0.0/16 and the reply is "
        "dropped. Stateful security groups permit the reply <i>logically</i>, but statefulness does not create "
        "a <i>path</i>. Each VPC needs a route to the other's CIDR via the peering connection."))

    st.append(H3("Q2. Why is the SSH source for App-B the bastion's private IP?"))
    st.append(P(
        "With ProxyJump the TCP connection arriving at App-B originates from the bastion instance, not the "
        "laptop. It crosses the peering connection using private addressing with no NAT, so App-B sees source "
        "10.10.1.10. The bastion's public IP never appears on this path. Using 10.10.1.10/32 also applies least "
        "privilege: only that host can open SSH sessions to App-B, and no internet-routable address is trusted. "
        "(A production alternative is referencing the bastion's security group as the source, which survives "
        "IP changes.)"))

    st.append(H3("Q3. Why does Active peering state alone not guarantee ICMP reachability?"))
    st.append(P(
        "Active only means both sides agreed to the link (control plane). Data-plane reachability also "
        "requires: (1) routes in <b>both</b> subnets' route tables to the remote CIDR via the peering "
        "connection; (2) security groups that permit ICMP; (3) network ACLs that allow it in both directions "
        "(they are stateless); (4) non-overlapping CIDRs; and (5) no OS-level firewall blocking ICMP. A failure "
        "at any one layer produces silent drops, as demonstrated in Test 05."))

    st.append(H3("Q4. Why can VPC B not access the Internet via VPC A's Internet Gateway?"))
    st.append(P(
        "VPC peering is <b>non-transitive</b> and does not support edge-to-edge routing. Traffic arriving over "
        "a peering connection can only be delivered to resources inside the peer VPC; it is never forwarded "
        "onward to the peer's IGW, NAT gateway, VPN or Direct Connect. In addition, App-B has no public IP "
        "and VPC B has no IGW. Internet access for VPC B would need its own IGW with public addressing, or a "
        "NAT gateway in VPC B."))

    # ---- 7. Cleanup & conclusion -----------------------------------------
    st.append(Spacer(1, 6))
    st.append(H1("7. Resource Cleanup Plan"))
    st.append(P("Delete in dependency order to avoid 'has dependencies' errors, then verify nothing tagged "
                "<font face='Courier'>Project = EWB-VPC-Peering</font> remains."))
    st.append(table([
        ["Order", "Action"],
        ["1", "Terminate any EC2 instances and release Elastic IPs (none were launched in this lab)."],
        ["2", "Delete the peering connection %s (or let the pending request expire on Oct 29, 2026)." % PCX_ID],
        ["3", "Delete the peering routes from ewb-rt-a-public (if added), ewb-rt-a-private and ewb-rt-b-private."],
        ["4", "Disassociate subnets, then delete the custom route tables."],
        ["5", "Detach ewb-igw-a from ewb-vpc-a, then delete it."],
        ["6", "Delete security groups ewb-sg-bastion, ewb-sg-app-a, ewb-sg-app-b (remove cross-references first)."],
        ["7", "Delete subnets ewb-a-public, ewb-a-private, ewb-b-private."],
        ["8", "Delete ewb-vpc-a and ewb-vpc-b."],
        ["9", "Confirm no VPCs, IGWs or peering connections with the project tag remain."],
    ], [0.7 * inch, 6.8 * inch]))

    st.append(Spacer(1, 6))
    st.append(H1("8. Final Conclusion"))
    st.append(P(
        "This project designed and built a two-VPC architecture with non-overlapping RFC 1918 ranges "
        "(10.10.0.0/16 and 10.20.0.0/16), an internet-facing bastion tier, private application tiers, a "
        "peering connection request, bidirectional static routes and least-privilege security groups using "
        "/32 sources. The configuration illustrates the core principles of VPC peering: isolation by default, "
        "routes required on both sides, stateful security group behaviour and non-transitivity."))
    st.append(P(
        "End-to-end validation was prevented by explicit IAM denies in the lab sandbox on "
        "<font face='Courier'>ec2:RunInstances</font> and <font face='Courier'>ec2:AcceptVpcPeeringConnection</font>. "
        "The connection therefore remains Pending acceptance and the peering routes show Blackhole. The "
        "documented test plan gives deterministic expected results that can be executed directly once the "
        "peering is accepted, the bastion's peering route is added and compute is permitted."))
    st.append(callout(
        "Key takeaway",
        "Peering provides a <i>possible</i> path. Route tables, security groups and network ACLs decide whether "
        "packets actually take it.", bg=LIGHT, border=NAVY))
    return st


def main():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN + 0.2 * inch, bottomMargin=MARGIN + 0.2 * inch,
        title="%s - %s" % (PROJECT, STUDENT),
        author=STUDENT,
        subject="VPC Peering lab report, %s" % REGION,
    )
    doc.build(build_story(), canvasmaker=NumberedCanvas)
    print("Created %s" % os.path.abspath(OUTPUT_FILE))


if __name__ == "__main__":
    main()
