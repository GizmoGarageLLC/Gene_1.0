# Eye cradle install path check: the cradle + driver board + plug ends (not the flexible ribbons) moved along the found way in,
# densified to 0.25 mm / 0.25 deg, against what is in the head at that build step (skull, carrier, LCD, bezel, camera), both eyes
# (left mirrored), plus the rise from 90 mm below the start pose. Way in, reversed from the search in plan: start behind the eye,
# 10 mm toward the nose, front turned 11 deg toward the nose; slide forward, ease out to the axis, straighten at 8 mm out, push home.
# Writes eye_cradle_path_L.json / _R.json (far -> seated: yaw deg, toward the nose mm, back mm, up mm). Run: python eye_cradle_path.py .
import sys, json; sys.path.insert(0,'.')
from parts import *
P=load_all()
pathR=[(0,0,8,0)]+[(-t,0,8,0) for t in range(1,11)]+[(-10,0,9,0),(-11,0,9,0),(-11,0,10,0),(-11,0,11,0),(-11,0,12,0),(-11,1,12,0),(-11,1,13,0),(-11,1,14,0),(-11,2,14,0),(-11,3,14,0),(-11,3,15,0)]+[(-11,d,15,0) for d in range(4,7)]+[(-11,7,15,0),(-11,7,16,0)]+[(-11,d,16,0) for d in range(8,11)]+[(-11,10,y,0) for y in range(17,46)]
for s in "RL":
    ax=AXR if s=="R" else AXL
    clip=mf.Manifold.cube([400,400,400]).translate([-200,-462,-200])
    mod=(to_mf(trimesh.util.concatenate([P["cradle_"+s],P["dboard_"+s]]))^clip).translate([-ax,0,-ZC])
    O=mf.Manifold()
    for k in ("shell","carrier_"+s,"display_"+s,"bezel_"+s,"camera_"+s): O+=to_mf(P[k])
    O=O.translate([-ax,0,-ZC])
    sx=1 if s=="R" else -1          # mirror X for the left eye (outboard is -X there)
    def M(th,dx,dy,dz):
        th=th*sx; c,sn=np.cos(np.radians(th)),np.sin(np.radians(th)); piv=np.array([0,-80,0.])
        R=np.array([[c,-sn,0],[sn,c,0],[0,0,1.]]); t=piv-R@piv+np.array([-sx*dx,dy,dz])
        return [list(R[0])+[t[0]],list(R[1])+[t[1]],list(R[2])+[t[2]]]
    def ov(n): return (mod.transform(M(*n))^O).volume()
    # densify: 0.25 steps between waypoints
    bad=[]
    full=[(0,0,y,0) for y in np.arange(0,8,0.25)]
    for a,b in zip(pathR,pathR[1:]):
        for f in np.linspace(0,1,5)[:-1]: full.append(tuple(np.array(a)+(np.array(b)-np.array(a))*f))
    full.append(pathR[-1])
    for n in full:
        if ov(n)>1e-3: bad.append(n)
    # come up from below at the start pose
    up=[(-11,10,45,z) for z in np.arange(-90,0.01,1.0)]
    badup=[n[3] for n in up if ov(n)>1e-3]
    # alternatives if straight up is blocked: from behind (more +Y) at z 0
    print(s, "path poses checked",len(full),"collisions",len(bad), bad[:3], "| rise from below at the start pose:", "clear" if not badup else f"blocked at z {min(badup):.0f}..{max(badup):.0f}")
    json.dump({"path":[list(map(float,n)) for n in full[::-1]]},open(f"{sys.argv[1]}/eye_cradle_path_{s}.json","w"))
