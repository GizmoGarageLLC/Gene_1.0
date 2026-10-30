# Crown insert post-step: the GPIO ribbon's male plug clicks into the insert, no glue.
# The ribbon bought is the UCTRONICS U6033 (Amazon B07D991KMR), 40-pin male-to-female, 20 cm. Its male end is a standard
# shrouded 2.54 mm male IDC plug (same outline as Wurth WR-BHD 612 040 258 21): 61.10 long over the cover's end arms,
# 8.40 wide, 13.0 tall assembled, shroud cavity 56.10 x 6.30 and 6.30 deep. The ribbon is clamped across its underside
# and leaves one long side horizontally ~3 mm above the bottom, so nothing may wall in the sides below that.
# Changes, all inside the head (the visible top is untouched except the opening over the pins, now 56.2 long):
#   - the old sleeve below the dome is removed and the old 56.6 x 9.5 pocket filled;
#   - new pocket 61.5 x 8.8 (0.2 a side), moved 1 mm forward to Y -47.5 so the crown keeps >= 1.2 mm over the plug's ends;
#     its roof is a lip over the shroud walls (the top stop), with a 6.45 x 56.2 opening over the cavity;
#   - side walls down to 7.5 mm below the shroud top only, clear of the ribbon;
#   - a cantilever finger at each end (7.2 wide, 1.6 thick, ~13 long, rooted 1.2 mm under the crown surface) with a hook
#     that snaps under the plug's ends, past the ribbon's edges. Push the plug up from below until both click; release by
#     pushing the fingers outward from below with a small screwdriver.
# Old file kept as tools/retired/crown_insert_before_idc_snap.stl. Rewrites crown_meta.json for gpio_mocks.py and
# gpio_flashlight.py (rerun both after this), print/parts/13 and Plate 5.
import trimesh, numpy as np, os, io, re, json, shutil, zipfile, manifold3d as mf
from trimesh.transformations import rotation_matrix as rot
from threemf import write_3mf
OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PR=os.path.join(os.path.dirname(OUT),"print")

PL_L,PL_W,PL_H=61.10,8.40,13.0          # plug outline, assembled
CAV_L,CAV_W,CAV_D=56.10,6.30,6.30       # shroud cavity
PIN_H=6.0                               # pins above the cavity floor
CLR=0.2                                 # pocket clearance per side
OP_L,OP_W=56.2,6.45                     # opening over the cavity (6.45: off the old 6.4 well's walls, which leave a pinch)
CX,GYC=1.25,-47.5                       # was -46.5: the ends of the longer plug need the crown's height
PT=84.7                                 # shroud top: crown >= 1.2 mm over it at the pocket's ends
PB=PT-PL_H
WALL_BOT=PT-7.5                         # side walls stop here, clear of the ribbon leaving the plug ~PB+3
F_W,F_T,F_GAP,F_SIDE=7.2,1.6,1.4,1.0    # finger width (X), thickness, room behind it to flex, side gaps
ROOT=83.5                               # finger root: slot behind it stops 1.2 mm under the crown
HOOK,HOOK_FLAT,LEAD=0.8,0.3,1.4         # hook reach under the plug, flat at the tip, lead-in chamfer height
CATCH=PB-0.1                            # hook top: 0.1 mm play under the plug
OLD_GYC,OLD_PW,OLD_PL,OLD_BB,OLD_BT=-46.5,9.5,56.6,71.89926767659958,79.49926767659957

def to_mf(t): return mf.Manifold(mf.Mesh(vert_properties=np.asarray(t.vertices,np.float32),tri_verts=np.asarray(t.faces,np.uint32)))
def to_tm(m): g=m.to_mesh(); return trimesh.Trimesh(g.vert_properties[:,:3],g.tri_verts)
def bx(x0,x1,y0,y1,z0,z1): return mf.Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])

def finger(s):
    """End finger with its hook; s=-1 front end, +1 rear end. Built as a YZ profile extruded along X."""
    yi=GYC+s*(PL_L/2+CLR)                               # pocket end face = finger's inner face
    yo=yi+s*F_T; yt=yi-s*HOOK                           # outer face, hook tip
    zb=CATCH-HOOK_FLAT-LEAD
    pts=[(yo,zb),(yo,ROOT+0.5),(yi,ROOT+0.5),(yi,CATCH),(yt,CATCH),(yt,CATCH-HOOK_FLAT),(yi,zb)]
    if s<0: pts=pts[::-1]                               # keep the outline counter-clockwise
    sec=mf.CrossSection([np.array(pts)])
    return sec.extrude(F_W).transform([[0,0,1,CX-F_W/2],[1,0,0,0],[0,1,0,0]])

def build():
    fn=os.path.join(OUT,"crown_insert.stl")
    bak=os.path.join(OUT,"tools","retired","crown_insert_before_idc_snap.stl")
    if not os.path.exists(bak): shutil.copy(fn,bak)
    ins=trimesh.load(bak); A=to_mf(ins)
    inner=json.load(open("sphere_inner.json")); IC,IR=np.array(inner["c"]),inner["r"]
    # the dome underside is crown.py's sphere: cut 0.3 past it either way (on it exactly leaves zero-thickness slivers)
    dome=lambda r: to_mf(trimesh.creation.icosphere(subdivisions=6,radius=r)).translate(IC.tolist())
    # 1. old sleeve off (all of it below the dome), old pocket filled back up into the dome's solid
    old=bx(CX-OLD_PW/2-1.7,CX+OLD_PW/2+1.7,OLD_GYC-OLD_PL/2-1.7,OLD_GYC+OLD_PL/2+1.7,OLD_BB-1.5,95.0)   # 0.1 past its faces
    B=(A-(old^dome(IR+0.3)))+(bx(CX-OLD_PW/2,CX+OLD_PW/2,OLD_GYC-OLD_PL/2,OLD_GYC+OLD_PL/2,OLD_BB-2,OLD_BT+0.01)-dome(IR-0.3))
    # 2. side walls round the shroud, down to WALL_BOT
    hw,hl=PL_W/2+CLR,PL_L/2+CLR
    B=B+bx(CX-hw-1.6,CX+hw+1.6,GYC-hl,GYC+hl,WALL_BOT,85.0)   # up into the dome solid: its underside is 83.6..84.0 over the plug, the crown >= 85.9
    # 3. pocket (open below, roof at the shroud top), opening over the cavity, a slot round each finger
    cut=bx(CX-hw,CX+hw,GYC-hl,GYC+hl,50.0,PT)+bx(CX-OP_W/2,CX+OP_W/2,GYC-OP_L/2,GYC+OP_L/2,PT-0.5,120.0)
    for s in (-1,1):
        y0,y1=sorted((GYC+s*hl,GYC+s*(hl+F_T+F_GAP)))
        cut+=bx(CX-F_W/2-F_SIDE,CX+F_W/2+F_SIDE,y0,y1,50.0,ROOT)
    C=(B-cut)+finger(-1)+finger(1)
    comps=sorted([c for c in C.decompose() if c.volume()>0.01],key=lambda c:-c.volume())
    assert len(comps)==1,[round(c.volume(),2) for c in comps]
    def reloads_ok(t):
        b=io.BytesIO(); t.export(b,file_type="stl"); b.seek(0); r=trimesh.load(b,file_type="stl")
        return r.is_watertight and r.body_count==1
    for tol in (0,0.002,0.005,0.01,0.02):
        t=to_tm(comps[0] if tol==0 else comps[0].simplify(tol))
        if reloads_ok(t): break
    else: raise AssertionError("does not reload watertight")
    t.export(fn)
    meta=json.load(open("crown_meta.json"))
    meta.update({"GYC":GYC,"CX":CX,"BODY_TOP":PT-CAV_D,"BODY_BOT":PB,"PLUG_TOP":PT,"IDC":[PL_L,PL_W,PL_H,PIN_H],
                 "CAVITY":[CAV_L,CAV_W,CAV_D],"OPENING":[OP_L,OP_W]})
    json.dump(meta,open("crown_meta.json","w"))
    # crown surface over the plug's ends and over the finger slots
    top=lambda y: t.ray.intersects_location([[CX,y,200.0]],[[0,0,-1.0]],multiple_hits=False)[0][0][2]
    print(f"crown insert: {ins.volume/1000:.2f} -> {t.volume/1000:.2f} cm3, watertight on reload (tol {tol}), bounds {np.round(t.bounds,1).tolist()}")
    print(f"   plug Z {PB:.1f}..{PT:.1f}, Y {GYC-PL_L/2:.2f}..{GYC+PL_L/2:.2f}; hooks catch at Z {CATCH:.1f}, finger bottoms Z {CATCH-HOOK_FLAT-LEAD:.1f}")
    for s in (-1,1):
        yp=GYC+s*hl; ys=GYC+s*(hl+F_T+F_GAP)
        print(f"   {'front' if s<0 else 'rear '} end: crown over the pocket end {top(yp-s*0.3)-PT:.2f} mm, over the finger slot {top(ys-s*0.3)-ROOT:.2f} mm")
    L=ROOT-(CATCH-HOOK_FLAT); print(f"   finger: free length {L:.1f}, bending strain at full hook deflection {1.5*F_T*HOOK/L**2*100:.2f} %")
    return t

def reprint(t):
    # printed on its side like printprep.py does (-90 deg about Y): same bounds as before, so it drops into place on Plate 5
    p=t.copy(); p.apply_transform(rot(np.radians(-90),[0,1,0])); p.apply_translation(-p.bounds[0])
    old=trimesh.load(os.path.join(PR,"parts","13_crown_insert_x1.stl"))
    assert np.allclose(old.extents,p.extents,atol=0.05),(old.extents,p.extents)
    p.export(os.path.join(PR,"parts","13_crown_insert_x1.stl"))
    fn=os.path.join(PR,"plates","Plate5_crown_insert_handle.3mf"); x=zipfile.ZipFile(fn).read("3D/3dmodel.model").decode(); objs=[]
    for name,body in re.findall(r'<object id="\d+" name="([^"]*)"[^>]*>(.*?)</object>',x,re.S):
        v=np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"',body),float)
        f=np.array(re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"',body),int)
        m=trimesh.Trimesh(v,f,process=False)
        if name.startswith("crown_insert"):
            m2=p.copy(); m2.apply_translation(m.bounds[0]); m=m2
        objs.append((name,m))
    write_3mf(fn,objs); print("  Plate5: crown insert replaced in place")

if __name__=="__main__":
    reprint(build())
