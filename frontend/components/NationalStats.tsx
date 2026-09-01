"use client";

import { useEffect, useState } from "react";
import { apiJson } from "../lib/api";

type PublicLand = { ok?: boolean; totalHectares?: number };
type Vdl = { ok?: boolean; totalHectares?: number };
type Gaps = { live?: unknown[]; gaps?: unknown[] };

function formatHa(value: number | undefined): string {
  if (value == null || Number.isNaN(value)) return "—";
  if (value >= 1000) {
    return `${(value / 1000).toLocaleString("en-GB", {
      maximumFractionDigits: 0,
    })}k ha`;
  }
  return `${value.toLocaleString("en-GB", { maximumFractionDigits: 0 })} ha`;
}

export default function NationalStats() {
  const [pub, setPub] = useState<PublicLand | null>(null);
  const [vdl, setVdl] = useState<Vdl | null>(null);
  const [live, setLive] = useState<number | null>(null);
  const [gap, setGap] = useState<number | null>(null);

  useEffect(() => {
    let cancelled = false;
    void Promise.all([
      apiJson<PublicLand>("/api/public-land.json"),
      apiJson<Vdl>("/api/vdl.json"),
      apiJson<Gaps>("/platform/gaps"),
    ])
      .then(([p, v, g]) => {
        if (cancelled) return;
        setPub(p);
        setVdl(v);
        setLive((g.live || []).length);
        setGap((g.gaps || []).length);
      })
      .catch(() => {
        /* strip stays empty if stats fail */
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (pub == null && vdl == null) return null;

  return (
    <div className="national-strip">
      <div className="national-strip-title">Open land snapshot</div>
      <div className="national-strip-grid">
        <div>
          <span className="fd-label">Public / Crown</span>
          <span className="fd-value">{formatHa(pub?.totalHectares)}</span>
        </div>
        <div>
          <span className="fd-label">Vacant (SVDLS)</span>
          <span className="fd-value">{formatHa(vdl?.totalHectares)}</span>
        </div>
        <div>
          <span className="fd-label">Coverage</span>
          <span className="fd-value">
            {live ?? "—"} live / {gap ?? "—"} gap
          </span>
        </div>
      </div>
      <p className="national-strip-note">
        Five national bodies only · survey vacant ha · not a rates bill ·{" "}
        <a href="/api/roll.json">AGR roll</a>
        {" · "}
        <a href="/downloads">Downloads</a>
        {" · "}
        <a href="/open-api">API</a>
      </p>
    </div>
  );
}
