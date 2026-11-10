# Skull v7 post-step: everything in the eye barrels comes 15 mm forward (EYE_DY in parts.py).
# In front of the pupil rings (front face Y -107.6) the barrel was empty for 30.0 mm to its front face (Y -137.6); the
# eye stack (camera, bezel, pupil, display, carrier and cradle / AMOLED harness) moves forward half of that. In each barrel:
#   ridge      the 56.80 ridge the bezel sits on (front face) and the carrier butts on (rear face), Y -99.60..-96.10, moves to
#              Y -114.60..-111.10
#   bore       from the new ridge's rear face back to the old one the bore was the 59.3 front tube and the old ridge; it opens to
#              the rear bore's 60.60 so the carrier (OD 60.50) and cradle slide the extra 15 mm in
#   ledge      the relief in the top of the barrel for the LCD's flex ledge starts 15 mm further forward (same section)
#   slot       the inboard camera-ribbon slot starts at Y -124.5 instead of -114.0 (the camera's rigid tail goes out through
#              it); the face skin's inner surface is at Y -127 or further forward there, so it stays inside the head
# Nothing may change from outside: checked with depth maps from 13 directions (none looking up through the open bottom) before and after.
# Run after skull_v7_ledge_relief.py. Old file kept as tools/retired/GeneTop_v7_before_eyes_forward.stl.
# Also updates print/parts/01 and Plates 1 and 8.
import trimesh, numpy as np, os, io, shutil, manifold3d as mf
from skull_v7_eye_plate_window import reprint
import skull_v7_ledge_relief as LR
OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHIFT=np.array([-64.8,-61.4,-35.0])
AXL,AXR,ZC=-60.96,60.95,-0.32
EYE_DY=-15.0
RIDGE_OLD=(-99.60,-96.10)
RIDGE_NEW=(RIDGE_OLD[0]+EYE_DY,RIDGE_OLD[1]+EYE_DY)
R_RIDGE=28.40                       # 56.80
R_TUBE=29.62                        # front tube as measured (59.24)
R_BORE=30.30                        # rear bore 60.60
SLOT_Y0,SLOT_Y1=-124.5,-114.0       # the new length of slot, added to the old -114.0..-87.5
SLOT_H,SLOT_R0,SLOT_R1=7.5,27.0,40.0

def to_mf(t): return mf.Manifold(mf.Mesh(vert_properties=np.asarray(t.vertices,np.float32),tri_verts=np.asarray(t.faces,np.uint32)))
def to_tm(m): g=m.to_mesh(); return trimesh.Trimesh(g.vert_properties[:,:3],g.tri_verts)
def ring(ax,r0,r1,y0,y1,n=256):
    m=mf.Manifold.cylinder(y1-y0,r1,r1,n)
    if r0>0: m-=mf.Manifold.cylinder(y1-y0,r0,r0,n)
    return m.transform([[1,0,0,ax],[0,0,1,y0],[0,1,0,ZC]])
def box(x0,x1,y0,y1,z0,z1): return mf.Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])

def ledge_cutter(ax):
    y0=LR.Y0+EYE_DY                  # -109.5, to the old relief's start
    w=LR.LEDGE_W/2+LR.CLEAR-0.01      # 0.01 inside the old relief where they overlap, so no faces coincide
    sec=(mf.CrossSection.square([2*w,LR.LEDGE_R+LR.CLEAR-0.01]).translate([-w,0])
         ^(mf.CrossSection.circle(LR.R1-0.01,256)-mf.CrossSection.circle(LR.R0,256)))
    return sec.extrude(LR.Y0-y0+0.5).transform([[1,0,0,ax],[0,0,1,y0],[0,1,0,ZC]])

def depth_maps(t):
    # first-hit distance on a 1 mm grid over the face, from 14 directions: the outside surface as seen from outside.
    # Rays that end inside an eye bore (looking down the open barrel at the ridge) are left out: those are meant to change.
    # No direction looks up (+Z): through the open bottom those see the inside of the head. The grid is offset off round
    # numbers so no ray runs exactly along a mesh seam
    c=np.array([0.0,-100.0,0.0]); out=[]
    dirs=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,-1)]+[(sx,sy,-1) for sx in (1,-1) for sy in (1,-1)]+[(sx,sy,0) for sx in (1,-1) for sy in (1,-1)]
    for d in dirs:
        d=np.array(d,float); d/=np.linalg.norm(d)
        u=np.cross(d,[0,0,1.0]) if abs(d[2])<0.9 else np.cross(d,[1.0,0,0]); u/=np.linalg.norm(u); v=np.cross(d,u)
        g=np.arange(-100,100.1,1.0)+0.373; U,V=np.meshgrid(g,g)
        O=c-d*300+U.reshape(-1,1)*u+V.reshape(-1,1)*v
        loc,idx,_=t.ray.intersects_location(O,np.tile(d,(len(O),1)),multiple_hits=False)
        r=np.full(len(O),np.inf); r[idx]=np.linalg.norm(loc-O[idx],axis=1)
        inbore=np.zeros(len(O),bool)
        for ax in (AXL,AXR):
            q=loc-[ax,0,ZC]; inbore[idx[(np.hypot(q[:,0],q[:,2])<R_BORE+0.6)&(loc[:,1]>-138.0)]]=True
        out.append((r,inbore))
    return out

def build():
    fn=os.path.join(OUT,"skull.stl")
    bak=os.path.join(OUT,"tools","retired","GeneTop_v7_before_eyes_forward.stl")
    if not os.path.exists(bak): shutil.copy(fn,bak)
    sh=trimesh.load(bak); sh.apply_translation(SHIFT); A=to_mf(sh)
    new=A
    for ax in (AXL,AXR):
        inb=1 if ax<0 else -1
        new=new+ring(ax,R_RIDGE,R_TUBE+0.3,*RIDGE_NEW)                     # new ridge, fused into the barrel wall
        new=new-ring(ax,0,R_BORE+0.05,RIDGE_NEW[1],RIDGE_OLD[1]+0.1)      # bore opened to 60.70, old ridge gone (0.05 over
                                                                           # the rear bore: a cut flush with it doesn't reload watertight)
        new=new-ledge_cutter(ax)
        x0,x1=sorted([ax+inb*SLOT_R0,ax+inb*SLOT_R1])
        new=new-box(x0,x1,SLOT_Y0,SLOT_Y1+0.5,ZC-SLOT_H/2+0.01,ZC+SLOT_H/2-0.01)     # the ribbon slot runs forward, notching the new ridge
    comps=sorted([c for c in new.decompose() if c.volume()>0.01],key=lambda c:-c.volume())
    assert len(comps)==1, [round(c.volume(),2) for c in comps]
    def reloads_ok(t):
        b=io.BytesIO(); t.export(b,file_type="stl"); b.seek(0); r=trimesh.load(b,file_type="stl")
        return r.is_watertight and r.body_count==1
    for tol in (0,0.002,0.005,0.01,0.02):
        t=to_tm(comps[0] if tol==0 else comps[0].simplify(tol))
        if reloads_ok(t): break
    else: raise AssertionError("does not reload watertight")
    before,after=depth_maps(sh),depth_maps(t)
    moved,flips,skipped=0.0,0,0
    for (a,ia),(b,ib) in zip(before,after):
        keep=~(ia|ib); skipped+=int((ia|ib).sum())
        both=keep&np.isfinite(a)&np.isfinite(b)
        if both.any(): moved=max(moved,float(np.abs(a[both]-b[both]).max()))
        flips+=int(np.sum(keep&(np.isfinite(a)!=np.isfinite(b))))
    print(f"  ({skipped} rays ending inside the eye bores left out)")
    print(f"outside seen from 13 directions: largest depth change {moved:.3f} mm, {flips} rays changed hit/miss")
    assert moved<0.05 and flips==0, "the outside changed"
    dv=(comps[0].volume()-A.volume())/1000
    t.apply_translation(-SHIFT); t.export(fn)
    print(f"skull v7: eyes forward {-EYE_DY:.1f} mm, {dv:+.2f} cm3, vol {t.volume/1000:.2f} cm3, watertight on reload (tol {tol})")
    return t

if __name__=="__main__":
    reprint(build())
