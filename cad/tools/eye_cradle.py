# Eye board cradle: one printed part per eye that holds the LCD and its round driver board rigidly together, so the
# LCD's 40-pin flex is bent once at assembly and never moves again. Before this the driver board hung on the flex and
# the HDMI / USB leads, so every tug on a lead and every head turn worked the flex until it broke.
#
# The cradle replaces the retainer ring. Front to back (eye axis along Y, axis at X 0, Z 0 in this file):
#   front ring   r 23.0..28.1, Y -91.6..-84.1. Sits in the carrier's 56.60 seat just behind the LCD (back of the glass at
#                -91.8, so 0.2 clear: it stops the panel falling back without pressing it) and is glued to the carrier's
#                two side walls like the retainer was.
#   shoulder     r 28.1..29.1 at Y -84.1: butts on the carrier's back face (side walls r 28.3..30.25), so pushing the
#                cradle home sets the LCD gap by itself.
#   cage         r 27.0..29.9, Y -84.1..-76.0, open at the top (+/-42 deg) for the flex to fold down to the board.
#   board seat   r 28.7..29.9 (57.4 bore for the 57 mm PCB), Y -76.0..-72.4. The PCB's front face rests on the cage's end
#                (r 27.0..28.7) at Y -76.0, and two snap fingers at the sides (+/-X) click over its back face. Open at the
#                top for the FPC connector and at the bottom (+/-40 deg) for the mini-HDMI / micro-USB plugs.
#   tie plate    33 x 13.5 x 2 under the plugs (0.5 below them, so they can't drop out), on two side webs, with two pairs of
#                zip-tie slots: tie both leads to it and a pull on a lead stops at the plate instead of the board or flex.
# Driver board: TekGroAml, 57 mm round, parts facing back, mounted turned 180 deg (flex connector at the top, plugs at the
# bottom) as in the current build. Its 4 x M2.5 holes are not used, so the hole positions don't need to be known.
# Same part for both eyes. Also writes the real LCD outline (R28.09 circle + the flex ledge at the top, 2.3 thick) to
# mocks/display.stl and the board mock turned 180 deg with its PCB front face at Y -76 to mocks/display_driver_board.stl.
import trimesh, numpy as np, os, manifold3d as mf
OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AXL,AXR,ZC=-60.96,60.95,-0.32
LCD_FRONT,LCD_T=-94.10,2.30          # glass sits on the carrier lip's rear face
Y_F=LCD_FRONT+LCD_T+0.20             # -91.6 cradle front face
Y_C=-84.10                           # carrier back face
Y_B=-76.00                           # PCB front face
PCB_T=1.60
Y_E=-72.40                           # back end of the seat
R_RING_I,R_RING_O=23.0,28.10
R_SHOULDER=29.10
R_CAGE_I,R_CAGE_O=27.0,29.90
R_SEAT=28.70                         # 57.4 bore
TOP_HALF,BOT_HALF=42.0,40.0          # window half-angles (deg) about +Z / -Z
FING_W,FING_ROOT,SLIT=9.0,-83.0,0.8
BARB_Y0,BARB_Y1,BARB_R=Y_B+PCB_T+0.1,-72.6,28.15
PLATE_U,PLATE_V,PLATE_T,PLATE_Y0,PLATE_Y1=17.8,-33.4,2.0,-73.5,-60.0   # plate top 0.5 under the flat plug-end boards
WEB_U0,WEB_U1=16.5,18.0

def to_tm(m): g=m.to_mesh(); return trimesh.Trimesh(g.vert_properties[:,:3],g.tri_verts)
Y_ALONG=[[1,0,0,0],[0,0,1,0],[0,1,0,0]]              # local (x, y, z) -> head (x, z, y): extrude along Y
def at_y(m,y0): return m.transform([[1,0,0,0],[0,0,1,y0],[0,1,0,0]])
def tube(r0,r1,y0,y1,n=192):
    return at_y(mf.Manifold.cylinder(y1-y0,r1,r1,n)-mf.Manifold.cylinder(y1-y0,r0,r0,n),y0)
def cone(ra,rb,y0,y1,n=192): return at_y(mf.Manifold.cylinder(y1-y0,ra,rb,n),y0)
def wedge(centre_deg,half_deg,y0,y1,R=60):
    a=np.radians(np.linspace(centre_deg-half_deg,centre_deg+half_deg,48))
    pts=np.vstack([[0,0],np.c_[R*np.cos(a),R*np.sin(a)]])
    return at_y(mf.CrossSection([pts]).extrude(y1-y0),y0)
def box(x0,x1,y0,y1,z0,z1): return mf.Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])

def skull_keepout(side,clear=1.0):
    # the skull round one eye in the cradle's frame, grown by `clear` (union of shifted copies). The cradles are handed: the
    # plug ends need the tie-plate webs at |u| 16.5-18, where the barrel's lower outboard wall is, so each cradle is cut against
    # its own eye only. The inboard web (towards the nose) stays whole and carries the plate; the outboard one is trimmed
    sk=trimesh.load(os.path.join(OUT,"skull.stl")); sk.apply_translation([-64.8,-61.4,-35.0])
    S=mf.Manifold(mf.Mesh(vert_properties=np.asarray(sk.vertices,np.float32),tri_verts=np.asarray(sk.faces,np.uint32)))
    win=box(-45,45,-92,-55,-50,40)
    eyes=[S.translate([-(AXR if side=='R' else AXL),0,-ZC])^win]
    k=mf.Manifold()
    for e in eyes:
        for dx,dz in [(0,0)]+[(clear*np.cos(a),clear*np.sin(a)) for a in np.radians(np.arange(0,360,45))]:
            for dy in (-clear,0,clear):
                k+=e.translate([dx,dy,dz])
    return k

def cradle(side):
    c=tube(R_RING_I,R_RING_O,Y_F,Y_C)
    c+=tube(R_RING_I+2,R_SHOULDER,Y_C,Y_C+1.0)                       # shoulder onto the carrier's back face
    c+=tube(R_CAGE_I,R_CAGE_O,Y_C,Y_B)
    c+=tube(R_SEAT,R_CAGE_O,Y_B,Y_E)
    c-=wedge(90,TOP_HALF,Y_C+1.0,Y_E+1)                            # flex window (keeps the shoulder ring whole)
    c-=wedge(270,BOT_HALF,Y_B-0.01,Y_E+1)                          # plug window in the seat
    # lead-ins, so it slides home without catching: 0.8 x 45 deg on the front ring's outer edge (into the carrier seat),
    # 1.0 x 45 deg on the cage's front outer edge (into the barrel; the shoulder keeps r 28.3-28.9 on the carrier),
    # 0.6 x 45 deg inside the board seat's mouth (the board starts square before the fingers take it)
    c-=at_y(mf.Manifold.cylinder(0.81,32,32,192),Y_F-0.01)-cone(R_RING_O-0.8,R_RING_O,Y_F-0.01,Y_F+0.8)
    c-=at_y(mf.Manifold.cylinder(1.0,32,32,192),Y_C)-cone(R_CAGE_O-1.0,R_CAGE_O,Y_C,Y_C+1.0)
    c-=cone(R_SEAT,R_SEAT+0.6,Y_E-0.6,Y_E+0.01)
    # snap fingers at +X and -X: slits either side, inner wall thinned to the seat bore, barb at the tip
    h=FING_W/2
    for sx in (1,-1):
        x0,x1=(24,32) if sx>0 else (-32,-24)
        for z0 in (h,-h-SLIT):
            c-=box(x0,x1,FING_ROOT,Y_E+1,z0,z0+SLIT)
        fz=box(x0,x1,FING_ROOT,Y_E+1,-h,h)
        c-=fz^cone(R_SEAT,R_SEAT,FING_ROOT,Y_E+1)                  # inner wall back to r 28.7 along the finger
        c+=(cone(R_CAGE_O-0.3,R_CAGE_O-0.3,BARB_Y0,BARB_Y1)-cone(BARB_R,R_SEAT,BARB_Y0,BARB_Y1))^fz
    # cable tie plate under the plugs, on two side webs with a 45 deg lower edge (prints without supports)
    v0,v1=PLATE_V-PLATE_T,PLATE_V
    c+=box(-PLATE_U,PLATE_U,PLATE_Y0,PLATE_Y1,v0,v1)
    for s in (1,-1):
        u0,u1=sorted((s*WEB_U0,s*WEB_U1))
        # web: from the cage (v -24) down to the plate, Y from the cage front to the plate's end; lower-front corner cut at 45
        yw=Y_C+0.5
        prof=np.array([[yw,-22.0],[Y_B-0.3,-22.0],[Y_B-0.3,-25.5],[PLATE_Y1-0.2,-25.5],[PLATE_Y1-0.2,v0+0.2],[PLATE_Y0+0.3,v0+0.2],[yw,max(v0+0.2+(PLATE_Y0+0.3-yw),-29.0)]])   # top runs into the cage wall in front of the board
        x_,y_=prof[:,0],prof[:,1]
        if np.dot(x_,np.roll(y_,-1))-np.dot(y_,np.roll(x_,-1))<0: prof=prof[::-1]   # make it CCW
        web=mf.CrossSection([prof]).extrude(u1-u0).transform([[0,0,1,u0],[1,0,0,0],[0,1,0,0]])
        web-=mf.Manifold.cylinder(80,R_CAGE_I,R_CAGE_I,192).transform([[1,0,0,0],[0,0,1,Y_C-1],[0,1,0,0]])  # stay outside the cage bore
        c+=web
    # zip-tie slots: 2 pairs, 3.2 x 1.6, across the plate
    for u in (-9.5,9.5):
        for y in (-68.5,-63.0):
            c-=box(u-1.6,u+1.6,y-0.8,y+0.8,v0-1,v1+1)
    for i in range(1 if side=="L" else 2):                         # 1 dimple under the plate = L, 2 = R
        c-=mf.Manifold.cylinder(0.8,1.2,1.2,32).translate([-4.0+8.0*i,-64.0,v0-0.01])
    c-=skull_keepout(side)
    comps=sorted(c.decompose(),key=lambda k:-k.volume())
    for k in comps[1:]:
        print(f"  dropped a {k.volume():.2f} mm3 sliver the skull clearance cut off")
        assert k.volume()<5
    assert comps[0].volume()>9000
    return to_tm(comps[0])

def display_mock():
    # TTC021XRS-02 outline: R28.09 circle + ledge 31.40 wide to 31.62 from the centre (corners eased 1.5), ledge at +Z
    a=np.radians(np.linspace(0,360,193)[:-1]); circ=np.c_[28.09*np.cos(a),28.09*np.sin(a)]
    cs=mf.CrossSection([circ])
    led=mf.CrossSection.square([31.4-3.0,31.62-1.5-20.0]).translate([-15.7+1.5,20.0])
    led=led.offset(1.5,mf.JoinType.Round)
    m=(cs+led).extrude(LCD_T).transform(Y_ALONG)                 # front face at y 0, like the old mock
    return to_tm(m)

# The bought leads (Amazon, 2026-09/10): chenyang CYFPV micro-HDMI to mini-HDMI FPC (0.5 m) and chenyang micro-USB flat ribbon
# (0.5 m). Each board end is a 90 deg plug on a small flat PCB with a ZIF latch for the 0.1 mm FPC: the plug goes up into the
# board's edge connector and the PCB lies flat under it, the ribbon leaving its far edge along Y. Both ribbons run back
# into the head (+Y): the micro-USB end is 'UP angled' and the mini-HDMI end must then be the 'UP angled' one too (NGFF
# CN-017-UP, bought 2026-11-10; the chenyang 'Down angled' end sends the HDMI ribbon forward, at the LCD). Sizes from the
# listing photos, rounded up: HDMI end 16 x 15.5 x 4 mm, USB end 12 x 13.5 x 3.5 mm; ribbons 13 and 8 mm wide.
PLUGS=(  # name, u centre, width, Y front, Y back, thickness, ribbon width
    ("hdmi", 5.9,16.0,-75.5,-60.0,4.0,13.0),
    ("usb", -8.9,12.0,-75.5,-62.0,3.5, 8.0))
RIB_Y1=-59.5                         # ribbons drawn to the tie plate's end; route.py carries them on to the Pi
def board_mock():
    old=os.path.join(OUT,"tools","retired","display_driver_board_flexdown.stl")
    fn=os.path.join(OUT,"mocks","display_driver_board.stl")
    if not os.path.exists(old) and os.path.exists(fn): os.replace(fn,old)
    src=open(os.path.join(OUT,"tools","dboard_mock.py")).read().replace("PCB_Y=-73","PCB_Y=%.2f"%Y_B)
    src=src.replace('m.export(os.path.join(OUT,"mocks/display_driver_board.stl"))','')
    g={"__file__":os.path.join(OUT,"tools","dboard_mock.py")}; exec(src,g)
    parts=[]
    for ax in (AXL,AXR):
        y0=Y_B+PCB_T
        b=trimesh.util.concatenate([g["cylinder"](radius=28.5,height=1.6,sections=96).apply_transform(
              trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0])).apply_translation([ax,Y_B+0.8,ZC]),
            g["bx"](ax-8,ax+8,y0,y0+1.4,ZC-8,ZC+8),
            g["bx"](ax-5.9-5.75,ax-5.9+5.75,y0,y0+3.2,ZC+21.0,ZC+28.9),      # mini-HDMI receptacle (flex-down frame)
            g["bx"](ax+8.9-4.0,ax+8.9+4.0,y0,y0+3.0,ZC+23.0,ZC+28.9)])       # micro-USB receptacle
        T=np.eye(4); T[0,0]=-1; T[2,2]=-1; T[0,3]=2*ax; T[2,3]=2*ZC; b.apply_transform(T)   # turned 180 deg: plugs at the bottom
        ends=[]
        for nm,uc,w,ya,yb,t,rw in PLUGS:
            ends.append(g["bx"](ax+uc-w/2,ax+uc+w/2,ya,yb,ZC-28.9-t,ZC-28.9))                  # flat end board under the plug
            ends.append(g["bx"](ax+uc-rw/2,ax+uc+rw/2,yb,RIB_Y1,ZC-28.9-t/2-0.15,ZC-28.9-t/2+0.15))  # ribbon, back into the head
        parts.append(trimesh.util.concatenate([b]+ends))
    return trimesh.util.concatenate(parts)

def write_print(cs):
    # print/parts/24 L and R (front ring on the bed, as printprep.py) and Plate 11 with the two cradles, 8 mm apart, centred
    from threemf import write_3mf
    from trimesh.transformations import rotation_matrix as rot
    PR=os.path.join(os.path.dirname(OUT),"print")
    old=os.path.join(PR,"parts","24_eye_display_cradle_x2.stl")
    if os.path.exists(old): os.remove(old)
    objs=[]; x=0
    for side,c in cs:
        p=c.copy(); p.apply_transform(rot(np.radians(90),[1,0,0])); p.apply_translation(-p.bounds[0])
        p.export(os.path.join(PR,"parts",f"24_eye_display_cradle_{side}_x1.stl"))
        m=p.copy(); m.apply_translation([x,0,0]); objs.append((f"cradle_{side}",m)); x+=p.extents[0]+8.0
    W=x-8.0; H=max(m.extents[1] for _,m in objs)
    for _,m in objs: m.apply_translation([-W/2,-H/2,0])
    write_3mf(os.path.join(PR,"plates","Plate11_eye_cradles.3mf"),objs)
    print(f"  print/parts/24_eye_display_cradle_L_x1.stl, _R_x1.stl and Plate11_eye_cradles.3mf ({W:.0f} x {H:.0f} mm) written")

if __name__=="__main__":
    cs=[]
    for side in ("L","R"):
        c=cradle(side); assert c.is_watertight; cs.append((side,c))
        c.export(os.path.join(OUT,f"eye_display_cradle_{side}.stl"))
        print(f"cradle {side}: {c.volume/1000:.2f} cm3, bounds {np.round(c.bounds,2).tolist()}")
    old=os.path.join(OUT,"eye_display_cradle.stl")
    if os.path.exists(old): os.remove(old)
    write_print(cs)
    d=display_mock(); d.export(os.path.join(OUT,"mocks","display.stl")); print(f"display mock: {np.round(d.bounds,2).tolist()}")
    b=board_mock(); b.export(os.path.join(OUT,"mocks","display_driver_board.stl")); print(f"board mock: {np.round(b.bounds,2).tolist()}")
