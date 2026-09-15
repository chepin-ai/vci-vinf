#!/usr/bin/env python3
"""VINF-Q02-G2XI v3-candidate engine (Actions rail)
koujing v3: pool=occupied sites(>=1 open bond); G2(r)=P(same cluster|both occupied,r)
dr=1, min-image torus, fit window [3,14], rmax=16 (L<=64) else 22, 1M-pair chunks.
Label: PROVISIONAL v3 — NOT declared anchor-compatible (see TH-L384-RESOURCE-01-APP-A)."""
import sys, json, time
import numpy as np
from scipy.spatial import cKDTree

def edges_sc32(L):
    idx = np.arange(L**3, dtype=np.int32).reshape(L, L, L)
    src = idx.ravel()
    eu = np.concatenate([src, src, src])
    ev = np.concatenate([np.roll(idx, -1, axis=a).ravel() for a in range(3)])
    return eu, ev

def clusters_at_p(eu, ev, n, p, seed):
    rng = np.random.default_rng(seed)
    E = eu.shape[0]; m = int(p * E)
    order = rng.permutation(E)[:m]
    parent = np.arange(n, dtype=np.int32)
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for e in order:
        ra, rb = find(int(eu[e])), find(int(ev[e]))
        if ra != rb: parent[ra] = rb
    lab = np.empty(n, dtype=np.int32)
    for i in range(n): lab[i] = find(i)
    # occupied = endpoint of >=1 selected edge
    occ = np.zeros(n, dtype=bool)
    oe = order
    occ[eu[oe]] = True; occ[ev[oe]] = True
    return lab, occ

def G2_occupied(lab, occ, L, rmax, dr=1.0, nsamp=30000, seed=7, chunk=1_000_000):
    pool = np.nonzero(occ)[0]
    rng = np.random.default_rng(seed)
    if len(pool) > nsamp:
        pool = rng.choice(pool, size=nsamp, replace=False)
    pts = np.stack([pool // (L * L), (pool // L) % L, pool % L], axis=1).astype(np.float32)
    slab = lab[pool]
    pairs = cKDTree(pts, boxsize=np.float32(L)).query_pairs(float(rmax), output_type='ndarray')
    nb = int(round(rmax / dr))
    cnt = np.zeros(nb, dtype=np.int64); s = np.zeros(nb, dtype=np.float64)
    Lf = np.float32(L)
    for i0 in range(0, len(pairs), chunk):
        P = pairs[i0:i0 + chunk]
        d = pts[P[:, 0]] - pts[P[:, 1]]
        d -= Lf * np.round(d / Lf)
        r = np.sqrt((d.astype(np.float64) ** 2).sum(axis=1))
        inds = np.floor(r / dr).astype(np.int64)
        m = (inds >= 0) & (inds < nb)
        cnt += np.bincount(inds[m], minlength=nb)
        s += np.bincount(inds[m], weights=(slab[P[:, 0]] == slab[P[:, 1]])[m], minlength=nb)
        del P, d, r, inds, m
    G = np.full(nb, np.nan); ok = cnt > 0; G[ok] = s[ok] / cnt[ok]
    return (np.arange(nb) + 0.5) * dr, G, len(pool), len(pairs)

def xi_from_G(rc, G, win=(3, 14)):
    m = (rc >= win[0]) & (rc <= win[1]) & np.isfinite(G) & (G > 0)
    if m.sum() < 3: return float('nan'), float('nan')
    slope, _ = np.polyfit(rc[m], np.log(G[m]), 1)
    return -1.0 / slope, slope

def run(L, p, seed):
    t0 = time.time()
    eu, ev = edges_sc32(L)
    lab, occ = clusters_at_p(eu, ev, L**3, p, seed)
    rmax = 16 if L <= 64 else 22
    rc, G, pooln, npairs = G2_occupied(lab, occ, L, rmax, 1.0, 30000, 7)
    xi, slope = xi_from_G(rc, G, (3, 14))
    return {"L": L, "p": p, "seed": seed, "koujing": "v3-occupied-cond",
            "rmax": rmax, "win": [3, 14], "pool": pooln, "pairs": npairs,
            "xi": round(float(xi), 3), "slope": round(float(slope), 4),
            "G_at": {str(round(float(r),1)): (None if not np.isfinite(g) else round(float(g),5)) for r, g in zip(rc, G)},
            "secs": round(time.time() - t0, 1)}

if __name__ == '__main__':
    L = int(sys.argv[1]); jobs = json.loads(sys.argv[2])  # [[p,seed],...]
    out = [run(L, p, s) for p, s in jobs]
    print(json.dumps(out, ensure_ascii=False, indent=1))
