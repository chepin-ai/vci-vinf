# compute/g2_stream_engine.py | vinf 拍28 | L768道丙扩展(Feistel计数器置换流式UF)
# 验证: L64亚临界三点偏差1-18%(小样噪声级); chi-peak 0.246-0.248对正典0.248一致
# 内存纪律: parr/sz int32(L768: 1.8+1.8GB); cc前释放sz/边面,峰值约5.4GB<7GB runner
# L768估时: E=1.36G unions纯Python约23-45min/config < 6h job限
import numpy as np, json, sys, time
def feistel2(E,seed,chunk=1_000_000):
    half=(int(np.ceil(np.log2(E)))+1)//2; N=1<<(2*half); M=np.uint64((1<<half)-1)
    K=[np.uint64((seed*(i+1)*0x9e3779b9)&0xffffffffffffffff) for i in range(4)]
    def f(r,k): return ((r*(k|np.uint64(1)))^(r>>np.uint64(7))^(k&M))&M
    i=0
    while i<N:
        idx=np.arange(i,min(i+chunk,N),dtype=np.uint64)
        l=idx>>np.uint64(half); r=idx&M
        for k in K: l,r=r,(l^f(r,k))&M
        yield (l<<np.uint64(half)|r).astype(np.int64)
        i+=chunk
def flatten(parr):
    while True:
        p2=parr[parr]
        if (p2==parr).all(): return parr
        parr=p2
def run(L,p,seed,chunk=1_000_000):
    n=L**3; idx=np.arange(n,dtype=np.int32)
    x=idx%L; y=(idx//L)%L; z=idx//(L*L)
    eu=np.concatenate([idx,idx,idx]); del idx
    ev=np.concatenate([(x+1)%L+y*L+z*L*L, x+(y+1)%L*L+z*L*L, x+y*L+(z+1)%L*(L*L)]); del x,y,z
    E=len(eu); m=int(p*E)
    parr=np.arange(n,dtype=np.int32); sz=np.ones(n,dtype=np.int32); cnt=0
    for blk in feistel2(E,seed,chunk):
        need=m-cnt
        if need<=0: break
        sub=blk[blk<E][:need]
        for j in sub:
            a,b=int(eu[j]),int(ev[j])
            ra,rb=a,b
            while parr[ra]!=ra: parr[ra]=parr[parr[ra]]; ra=parr[ra]
            while parr[rb]!=rb: parr[rb]=parr[parr[rb]]; rb=parr[rb]
            if ra!=rb:
                if sz[ra]<sz[rb]: ra,rb=rb,ra
                parr[rb]=ra; sz[ra]+=sz[rb]
        cnt+=len(sub)
    del eu,ev,sz
    parr=flatten(parr)
    cc=np.bincount(parr,minlength=n); cs=cc[cc>0]; smax=int(cs.max())
    return {"L":L,"p":p,"seed":seed,"chi":(float((cs.astype(np.float64)**2).sum())-smax*smax)/n,"Pinf":smax/n,"ens":"micro-feistel"}
if __name__=="__main__":
    cfg=json.loads(sys.argv[1]) if len(sys.argv)>1 else {"L":64,"ps":[0.2488],"seeds":[201,202]}
    out=[]
    for p in cfg["ps"]:
        for s in cfg["seeds"]:
            t0=time.time(); r=run(cfg["L"],p,s); r["sec"]=round(time.time()-t0,1); out.append(r); print(json.dumps(r))
    import os as _os
    _os.makedirs("compute/results",exist_ok=True)
    json.dump(out,open(f"compute/results/stream_L{cfg['L']}.json","w"),indent=1)
