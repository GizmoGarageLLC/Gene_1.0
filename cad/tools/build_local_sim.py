"""Self-contained copy of the head sim for opening straight from disk: sim/head_sim.html.

All JSON the page fetches is inlined as window.__SIM, keyed by file name, and window.fetch is shimmed to serve it.
Rebuild after any export.py run or edit to web/index.html.

One page covers all four setups: battery (2S2P pack / INIU P50 power bank, battery_powerbank.py) and eye screens (2.1"
LCD / 1.75" AMOLED, eye_amoled.py), switched in the page's Setup panel. Text that differs between setups is written into
the page twice, the default version classed v-pack / v-lcd and the other v-pb / v-am, and CSS shows the one that applies.

Optional: build_local_sim.py <web dir> <out file>."""
import os, json, glob, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "web")
html = open(os.path.join(HERE, "web", "index.html"), encoding="utf-8").read()
POWER_TEXT = [   # (2S2P pack text, power bank text)
    ("~3 h battery</span>", "~2 h power bank (INIU P50)</span>"),
    ("<p>The pack sits in the dome just above the twin servos, the lowest place a horizontal 2S2P pack fits. It is held in a tray that screws to pads on top of both servo brackets. A deck on top carries the two 5&nbsp;V converters and the charger board, so the pack, deck and electronics can be built on the bench as one unit.</p>",
     "<p>A bought power bank (INIU Pocket Rocket P50) lies across the dome just above the twin servos, ports at Gene's left. Its tray screws to the same pads on top of both servo brackets. A deck on top clamps the bank down and carries the two 5&nbsp;V converters and a 15&nbsp;V USB-C PD trigger board. There are no cells, BMS or charger board: the charge port plugs straight into the bank.</p>"),
    ("<tr class=\"tot\"><td>From the pack, at 90% converter efficiency</td>", "<tr class=\"tot\"><td>From the bank, at 90% converter efficiency</td>"),
    ("<div><dt>Pack</dt><dd>2S2P 18650, 7.2&nbsp;V nominal</dd></div>", "<div><dt>Bank</dt><dd>INIU P50, 83.6 &times; 53.1 &times; 25.4&nbsp;mm, one USB-C at 15&nbsp;V 3&nbsp;A (45&nbsp;W)</dd></div>"),
    ("<div><dt>Cells</dt><dd>4 &times; 3000&ndash;3500&nbsp;mAh, rated 10&nbsp;A or more (Samsung 30Q, Molicel P28A)</dd></div>", "<div><dt>Capacity</dt><dd>10000&nbsp;mAh</dd></div>"),
    ("<dd class=\"mono\">43&ndash;50 Wh</dd>", "<dd class=\"mono\">about 37 Wh</dd>"),
    ("<dd class=\"mono\">about 3 h</dd>", "<dd class=\"mono\">about 2 h</dd>"),
    ("<dd class=\"mono\">6.2 A at 6.4 V</dd>", "<dd class=\"mono\">2.4 A at 15 V</dd>"),
    ("<div><dt>BMS</dt><dd>2S balancing, 10&nbsp;A continuous</dd></div>", "<div><dt>PD trigger</dt><dd>USB-C, fixed 15&nbsp;V, into the switch and fuse</dd></div>"),
    ("<dd class=\"mono\">about 190 g of cells</dd>", "<dd class=\"mono\">about 160 g bank</dd>"),
    ("Build the pack, tray and deck on the bench first.", "Build the bank, tray and deck on the bench first."),
    ("drive 4 &times; M3&times;12 self-tappers up through the pads from underneath.", "drive the self-tappers up through the pads from underneath: 2 &times; M3&times;12 at the rear, 2 &times; M3&times;10 at the front."),
    ("<p>The pack stays in the head. It needs a charge port through the skull, which isn't cut yet.</p>", "<p>The bank stays in the head and charges through the USB-C port in the back of the skull. Plug and unplug the charger with Gene switched off: the bank's output blips when the charger goes in or out.</p>"),
    ("<span class=\"mono\">battery_tray.stl</span> has three cradle ribs, two strap windows for 22&nbsp;mm hook-and-loop straps, and a lead exit in the rear wall.",
     "<span class=\"mono\">battery_tray_pb.stl</span> has a 6&nbsp;mm floor on the bracket pads, walls on three sides, and an open end under the bank's plugs."),
    ("<span class=\"mono\">battery_deck.stl</span> has two 30&nbsp;&times;&nbsp;46 converter bays and a 40&nbsp;&times;&nbsp;20 charger bay,",
     "<span class=\"mono\">battery_deck_pb.stl</span> has two 26.4 converter bays and a 33&nbsp;&times;&nbsp;15 PD trigger bay,"),
    ('name:"2S2P 18650 pack",', 'name:"Power bank (INIU P50)",'),
    ('name:"Bucks + charger",', 'name:"Bucks + PD trigger",'),
    ('"Converters and charger in their bays"', '"Converters and PD trigger in their bays"'),
    ('"Pack in the ribs, strapped"', '"Bank in its bay, clamped by the deck"'),
    ('battery:"Battery pack + BMS"', 'battery:"Power bank"'),
    ('boards:"Bucks + charger"', 'boards:"Bucks + PD trigger"'),
    ("\"Sit the 2S2P pack in the tray's cradle ribs and strap it down through the two strap windows.\"",
     "\"Slide the power bank into the tray, ports to the open +X end, with a 1&nbsp;mm foam pad on top.\""),
    ("\"Screw the deck onto the tray posts from above, 4 &times; M3&times;10.\"", "\"Screw the deck onto the tray posts from above, 4 &times; M3&times;10. It clamps the bank down.\""),
    ("Zip-tie the two 5&nbsp;V bucks and the USB-C charger into their bays on the deck. Set the Pi's buck to 5.1&nbsp;V. The pack leads leave through the tray's rear wall.",
     "Zip-tie the two 5&nbsp;V bucks and the 15&nbsp;V PD trigger into their bays on the deck, and plug the trigger into the bank's USB-C output."),
    ('hw:["4 &times; M3&times;10 self-tapping","2 &times; hook-and-loop strap, 20&ndash;22&nbsp;mm","zip ties"]', 'hw:["4 &times; M3&times;10 self-tapping","1&nbsp;mm foam pad","zip ties"]'),
]
EYES_TEXT = [   # (2.1" LCD text, 1.75" AMOLED text)
    ('name:"Display carriers",', 'name:"AMOLED eye harnesses",'),
    ('note:"top slot"', 'note:"eye_amoled.py"'),
    ('name:"2.1″ round LCDs",', 'name:"1.75″ AMOLED ESP32-S3 boards",'),
    ('carrier_L:"Carrier L"', 'carrier_L:"Harness L"'), ('carrier_R:"Carrier R"', 'carrier_R:"Harness R"'),
    ('display_L:"Display L"', 'display_L:"AMOLED L"'), ('display_R:"Display R"', 'display_R:"AMOLED R"'),
    ('"Aperture margin round the active area"', '"Board on the lip, two snap fingers over its back"'),
    ('twin jaw drive, eye screens and cameras', 'twin jaw drive, 1.75&Prime; AMOLED eye screens and cameras'),
    ('All 41 current parts', 'All the current parts'), ('all 15 cable runs', 'all 14 cable runs'),
    ('<tr><td>2 &times; 2.1&Prime; round LCD</td><td class="num">1.2 W</td><td class="num">1.2 W</td></tr>',
     '<tr><td>2 &times; 1.75&Prime; AMOLED + ESP32-S3 (estimate)</td><td class="num">1.2 W</td><td class="num">1.6 W</td></tr>'),
    ('and the display cables use a 6&nbsp;mm worst case sized for micro-HDMI.', 'and the eyes&rsquo; USB-C leads use a 4&nbsp;mm round cable.'),
    ('The tightest gaps are the left display cable at 0.19&nbsp;mm and the pack leads at 0.25&nbsp;mm, both assuming the full 6&nbsp;mm envelope; thinner cable gains room.',
     'The eyes&rsquo; two USB-C leads keep at least 1.2&nbsp;mm from every part; like the LCD power leads, their last few millimetres run into the Pi mock, which is a solid block, ports included.'),
    ('Displays: left to micro-HDMI&nbsp;1, right to micro-HDMI&nbsp;0, 250 each.',
     'Eyes: each board&rsquo;s 90&deg; USB-C lead to a Pi USB-A port, left 150, right 200.'),
]

CLS = {"pb": ("v-pack", "v-pb"), "am": ("v-lcd", "v-am")}
TAG = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)[^>]*?(/?)>")
VOID = {"br", "img", "input", "meta", "link", "hr", "wbr"}


def balanced(x):
    st = []
    for m in TAG.finditer(x):
        close, name, selfc = m.group(1), m.group(2).lower(), m.group(3)
        if selfc or name in VOID: continue
        if close:
            if not st or st[-1] != name: return False
            st.pop()
        else: st.append(name)
    return not st and x.count("<") == x.count(">")


def clean_cut(x, i):     # cutting x at i leaves no half tag or half entity on either side
    a = x[:i]
    return a.rfind("<") <= a.rfind(">") and a.rfind("&") <= a.rfind(";")


def dual(src, a, b, key, js):
    """Both versions of a, side by side, each shown only in its setup. js: a sits inside a JS string (no double quotes)."""
    c0, c1 = CLS[key]
    m = re.match(r"<([a-zA-Z0-9]+)([^>]*)>", a)
    if m and a.endswith("</%s>" % m.group(1)) and balanced(a) and not js:      # a whole element: class it
        def inject(x, c):
            t = re.match(r"<([a-zA-Z0-9]+)([^>]*)>", x)
            attrs = t.group(2)
            attrs = attrs.replace('class="', 'class="%s ' % c, 1) if 'class="' in attrs else attrs + ' class="%s"' % c
            return "<%s%s>" % (t.group(1), attrs) + x[t.end():]
        return src.replace(a, inject(a, c0) + inject(b, c1))
    p = 0
    while p < min(len(a), len(b)) and a[p] == b[p]: p += 1
    q = 0
    while q < min(len(a), len(b)) - p and a[-1 - q] == b[-1 - q]: q += 1

    def ok(p, q):
        ma, mb = a[p:len(a) - q], b[p:len(b) - q]
        return (clean_cut(a, p) and clean_cut(a, len(a) - q) and clean_cut(b, p) and clean_cut(b, len(b) - q)
                and balanced(ma) and balanced(mb) and not (js and ('"' in ma or '"' in mb)))
    while not ok(p, q):
        if p == 0 and q == 0: raise SystemExit("can't dual: " + a[:70])
        if p >= q: p -= 1
        else: q -= 1
    ma, mb = a[p:len(a) - q], b[p:len(b) - q]
    return src.replace(a, a[:p] + "<span class=%s>%s</span><span class=%s>%s</span>" % (c0, ma, c1, mb) + a[len(a) - q:])


JS_FROM = html.index("var PARTS=")
for key, pairs in (("pb", POWER_TEXT), ("am", EYES_TEXT)):
    for a, b in pairs:
        assert html.count(a) == 1, "setup text not found once: " + a[:70]
        html = dual(html, a, b, key, html.index(a) > JS_FROM)
data = {}
for p in sorted(glob.glob(os.path.join(WEB, "*.json"))):
    data[os.path.basename(p)] = json.load(open(p, encoding="utf-8"))
shim = ("<script>window.__SIM=" + json.dumps(data, separators=(",", ":")) + ";"
        "(function(){var f0=window.fetch;window.fetch=function(u){var k=String(u).replace(/^\\.\\//,'').split('?')[0];"
        "if(window.__SIM[k])return Promise.resolve({ok:true,status:200,json:function(){return Promise.resolve(window.__SIM[k]);}});"
        "return f0.apply(this,arguments);};})();</script>\n")
anchor = '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>'
assert html.count(anchor) == 1, "three.js tag not found"
out = '<meta charset="utf-8">\n' + html.replace(anchor, shim + anchor)
fn = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.dirname(HERE)), "sim", "head_sim.html")
open(fn, "w", encoding="utf-8").write(out)
print(f"{fn}: {len(data)} data files inlined, {os.path.getsize(fn) / 1e6:.1f} MB")
