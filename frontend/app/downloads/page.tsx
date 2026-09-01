"use client";

import { useEffect, useState } from "react";
import { apiJson, getApiBaseUrl } from "../../lib/api";

type DownloadItem = {
  id: string;
  label: string;
  licence?: string;
  url?: string;
  endpoint?: string;
  note?: string;
};

type Downloads = { note?: string; items?: DownloadItem[] };

const OPEN_JSON = [
  { href: "/api/roll.json", label: "32-council AGR roll (JSON)" },
  { href: "/api/roll.csv", label: "32-council AGR roll (CSV)" },
  { href: "/api/public-land.json", label: "Public / Crown hectares by body" },
  { href: "/api/vdl.json", label: "SVDLS vacant land by owner class" },
  { href: "/api/vdl-councils.json", label: "Vacant hectares × illustrative AGR" },
  { href: "/api/place.json?pc=EH1+1YZ", label: "Place card example (Edinburgh)" },
  { href: "/api/catalog.json", label: "Live / linked / gap catalog" },
  { href: "/api/registers.json", label: "Official register landing pages" },
];

export default function DownloadsPage() {
  const [data, setData] = useState<Downloads | null>(null);

  useEffect(() => {
    void apiJson<Downloads>("/downloads")
      .then(setData)
      .catch(() => setData({ items: [] }));
  }, []);

  return (
    <main className="downloads-page">
      <p className="downloads-nav">
        <a href="/">Map</a>
        {" · "}
        <a href="/methodology">About</a>
      </p>
      <h1>Open downloads</h1>
      <p>
        Freely licensed statistics and official source links. Research AGR
        figures are not a rates bill. Public/Crown polygons are a viewport
        overlay, not a bulk dump.
      </p>
      {data?.note && <p className="downloads-note">{data.note}</p>}

      <h2>This API</h2>
      <p className="downloads-note">
        Interactive docs:{" "}
        <a href={`${getApiBaseUrl()}/docs`}>OpenAPI /docs</a>. Assessment is{" "}
        <code>/square</code>; open
        layers are <code>/layers/open/vdl</code> and{" "}
        <code>/layers/open/public-land</code>. Stats below are JSON/CSV only —
        not a bulk polygon dump.
      </p>
      <ul>
        {OPEN_JSON.map((item) => (
          <li key={item.href}>
            <a href={item.href}>{item.label}</a>
          </li>
        ))}
      </ul>

      <h2>Official sources</h2>
      <ul>
        {(data?.items || [])
          .filter((item) => item.url)
          .map((item) => (
            <li key={item.id}>
              <a href={item.url} target="_blank" rel="noreferrer">
                {item.label}
              </a>
              {item.licence ? ` · ${item.licence}` : ""}
              {item.note ? ` — ${item.note}` : ""}
            </li>
          ))}
      </ul>
    </main>
  );
}
