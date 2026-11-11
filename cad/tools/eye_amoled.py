# Eye harness for an all-in-one round display board, the Waveshare ESP32-S3-Touch-AMOLED-1.75 (466 x 466 AMOLED, touch,
# ESP32-S3 on the back, one USB-C for power + data). ALTERNATIVE to the 2.1" TekGroAml LCD + separate driver board: no LCD
# flex, no driver board, no HDMI. One part per eye replaces the carrier + cradle pair.
#
# The board is smaller than the 2.1" LCD (48.96 dia x 10.40 deep against 56.18 x 2.3 + a 57 mm board 19 mm behind it), so the
# harness is a cup with the old carrier's OUTSIDE (OD 60.50, front face Y -96.10 on the barrel ridge's rear face, glued the
# same way) and a smaller INSIDE. Same part both eyes. Eye axis along Y, axis at X 0, Z 0 in this file (parts.py places it
# like the carrier). Front to back:
#   front lip   Y -96.10..-94.10, aperture AP (mask over the module's black border, so only lit pixels show); its front face
#               bears on the ridge like the old carrier
#   outer tube  r 28.25..30.25 (front) / ..29.90 behind the old carrier's back face (Y -84.10), as the cradle's cage did:
#               the slip fit in the barrel bore and what the CA goes on
#   seat        bore SEAT for the module, from the lip's rear face (glass front at Y -94.10, the plane the LCD sat in, so the
#               camera bezel and pupil are unchanged) back past the module
#   ribs        6 radial ribs tie the seat sleeve to the outer tube (weight: hollow between)
#   snaps       two fingers at +/-X click over the module's back edge, so it presses in from behind and stays without glue
#   cable       the bottom is open (+/-35 deg) behind the lip for the USB-C lead; a tie tab below with two slots takes a 2.5 mm
#               zip tie round the lead, so a tug stops at the harness, not the board's socket
# ASSUMED (check against the board in hand; all are parameters below): module OD 48.96, depth 10.40 (Core Electronics listing),
# active area 1.75 in (44.45), USB-C on the rear face. Print in black PETG, lip down, no supports.
import trimesh, numpy as np, os, manifold3d as mf
OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MOD_D, MOD_T = 48.96, 10.40          # module outer dia, glass front to tallest rear part
ACTIVE = 44.45                       # 1.75 in round active area
AP = 45.20                           # lip aperture: active + 0.375 a side
SEAT = MOD_D+0.44                    # 0.22 a side, as the eased LCD seat
Y_FRONT, Y_LIP = -96.10, -94.10      # carrier front face / lip rear face = glass front
Y_OLD_BACK = -84.10                  # the old carrier's back face
Y_MOD_BACK = Y_LIP+MOD_T             # -83.70
Y_BACK = Y_MOD_BACK+2.40             # -81.30: snap barbs sit just behind the module
R_OUT_F, R_OUT_B, T_OUT = 30.25, 29.90, 1.6
R_SEAT = SEAT/2
T_SLEEVE = 1.4
CABLE_HALF = 35.0                    # deg, bottom opening

def to_tm(m): g=m.to_mesh(); return trimesh.Trimesh(g.vert_properties[:,:3],g.tri_verts)
def at_y(m,y0): return m.transform([[1,0,0,0],[0,0,1,y0],[0,1,0,0]])
def tube(r0,r1,y0,y1,n=192):
    return at_y(mf.Manifold.cylinder(y1-y0,r1,r1,n)-mf.Manifold.cylinder(y1-y0,r0,r0,n),y0)
def cone(ra,rb,y0,y1,n=192): return at_y(mf.Manifold.cylinder(y1-y0,ra,rb,n),y0)
def wedge(centre_deg,half_deg,y0,y1,R=60):
    a=np.radians(np.linspace(centre_deg-half_deg,centre_deg+half_deg,48))
    pts=np.vstack([[0,0],np.c_[R*np.cos(a),R*np.sin(a)]])
    return at_y(mf.CrossSection([pts]).extrude(y1-y0),y0)
def box(x0,x1,y0,y1,z0,z1): return mf.Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])

def harness():
    c=tube(AP/2,R_OUT_F,Y_FRONT,Y_LIP)                                   # front lip
    c+=tube(R_OUT_F-T_OUT,R_OUT_F,Y_LIP,Y_OLD_BACK)                       # outer tube, old carrier's OD
    c+=tube(R_OUT_B-T_OUT,R_OUT_B,Y_OLD_BACK,Y_BACK)                      # behind it, the cradle cage's OD
    c+=tube(R_SEAT,R_SEAT+T_SLEEVE,Y_LIP,Y_BACK)                          # seat sleeve
    for a in np.radians(np.arange(30,360,60)):                            # 6 ribs at 30, 90, ... (none at the bottom)
        r0,r1=R_SEAT+T_SLEEVE-0.3,R_OUT_B-T_OUT+0.3
        rib=mf.Manifold.cube([r1-r0,1.6,Y_BACK-Y_LIP]).translate([r0,-0.8,0]).rotate([0,0,np.degrees(a)])
        c+=at_y(rib,Y_LIP)                                                # local z = eye axis
    c-=wedge(270,CABLE_HALF,Y_LIP+0.6,Y_BACK+1)-tube(R_OUT_B-T_OUT,40,Y_LIP,Y_BACK+1)   # USB-C lead: bottom of the seat sleeve open
    # snap fingers at +/-X (rib-free there: ribs are at 30/90/150...; +X = 0 deg, -X = 180 deg)
    FW,SL=8.0,0.7
    for sx in (1,-1):
        x0,x1=(R_SEAT-0.1,R_OUT_F+1) if sx>0 else (-R_OUT_F-1,-R_SEAT+0.1)
        for z0 in (FW/2,-FW/2-SL):
            c-=box(x0,x1,Y_OLD_BACK-3.0,Y_BACK+1,z0,z0+SL)               # slits in both sleeves
        f=box(x0,x1,Y_OLD_BACK-3.0,Y_BACK+1,-FW/2,FW/2)
        c-=f^tube(R_SEAT+T_SLEEVE,R_OUT_B+1,Y_OLD_BACK-3.0,Y_BACK+1)      # finger = inner sleeve only, free of the tube
        barb=(cone(R_SEAT+0.1,R_SEAT+0.1,Y_MOD_BACK+0.1,Y_BACK)-cone(R_SEAT-0.6,R_SEAT,Y_MOD_BACK+0.1,Y_BACK))^f
        c+=barb                                                            # 0.6 catch, ramped on the way in
    c-=cone(R_SEAT,R_SEAT+0.5,Y_BACK-0.5,Y_BACK+0.01)                     # lead-in at the mouth
    c-=at_y(mf.Manifold.cylinder(0.61,40,40,192),Y_FRONT-0.01)-cone(R_OUT_F-0.6,R_OUT_F,Y_FRONT-0.01,Y_FRONT+0.6)  # 0.6 chamfer
    # zip-tie tongue: runs back from the bottom of the outer tube, 2 thick, with two slots across it. The lead leaves the
    # module's back, bends down over the tongue and is tied to it, so a tug stops here and not at the board's USB-C socket
    TY0,TY1=Y_BACK-3.0,Y_BACK+8.0
    tab=box(-8,8,TY0,TY1,-R_OUT_B,-R_OUT_B+2.0)^cone(R_OUT_B,R_OUT_B,TY0-1,TY1+1)
    for y in (Y_BACK+2.5,Y_BACK+5.8):
        tab-=box(-6.4,-3.2,y-0.8,y+0.8,-40,0)+box(3.2,6.4,y-0.8,y+0.8,-40,0)
    c+=tab
    comps=sorted(c.decompose(),key=lambda k:-k.volume())
    assert all(k.volume()<1 for k in comps[1:])
    return to_tm(comps[0])

# USB-C lead: a 90 deg plug in the module's rear socket (ASSUMED centred on the back face, plug body pointing down), its
# overmould 12 x 6.5 mm and reaching 22 mm below the axis; the cable leaves its lower end and is tied to the tongue
PLUG=(-6.0,6.0,Y_MOD_BACK,Y_MOD_BACK+6.5,-22.0,-4.0)
def module_mock():
    # glass + board as one disc plus the USB-C plug, glass front at Y -94.10 (placed in parts.py at the axis with no Y shift)
    return to_tm(cone(MOD_D/2,MOD_D/2,Y_LIP,Y_MOD_BACK,128)+box(*PLUG))

def write_print(h):
    # print/parts/25 (lip on the bed, as the carrier in printprep.py) and Plate 12 with the two harnesses, 8 mm apart, centred
    from threemf import write_3mf
    from trimesh.transformations import rotation_matrix as rot
    PR=os.path.join(os.path.dirname(OUT),"print")
    p=h.copy(); p.apply_transform(rot(np.radians(90),[1,0,0])); p.apply_translation(-p.bounds[0])
    assert abs(p.bounds[0][2])<1e-6 and p.is_watertight
    p.export(os.path.join(PR,"parts","25_eye_amoled_harness_x2.stl"))
    objs=[]
    for i in range(2):
        m=p.copy(); m.apply_translation([i*(p.extents[0]+8.0),0,0]); objs.append((f"amoled_harness_{i+1}",m))
    W=2*p.extents[0]+8.0; H=p.extents[1]
    for _,m in objs: m.apply_translation([-W/2,-H/2,0])
    write_3mf(os.path.join(PR,"plates","Plate12_amoled_harnesses.3mf"),objs)
    print(f"  print/parts/25_eye_amoled_harness_x2.stl and Plate12_amoled_harnesses.3mf ({W:.0f} x {H:.0f} mm, {p.extents[2]:.1f} tall) written")

if __name__=="__main__":
    h=harness(); assert h.is_watertight
    h.export(os.path.join(OUT,"eye_amoled_harness.stl"))
    m=module_mock(); m.export(os.path.join(OUT,"mocks","display_amoled175.stl"))
    print(f"harness: {h.volume/1000:.2f} cm3, bounds {np.round(h.bounds,2).tolist()}")
    print(f"module mock: {np.round(m.bounds,2).tolist()}")
    write_print(h)
