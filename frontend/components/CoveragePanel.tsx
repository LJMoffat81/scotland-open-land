"use client";

export type CoverageLayer = {
  id: string;
  label: string;
  status: "live" | "linked" | "gap" | string;
  description?: string;
  source_url?: string;
  endpoint?: string;
};

type Props = {
  live: CoverageLayer[];
  gaps: CoverageLayer[];
  open: boolean;
  onToggleOpen: () => void;
  onToggleLayer?: (id: string) => void;
  activeLayerIds?: string[];
};

export default function CoveragePanel({
  live,
  gaps,
  open,
  onToggleOpen,
  onToggleLayer,
  activeLayerIds = [],
}: Props) {
  const liveCount = live.length;
  const gapCount = gaps.length;

  return (
    <div className="coverage-panel">
      <button
        type="button"
        className="coverage-summary"
        onClick={onToggleOpen}
        aria-expanded={open}
      >
        <span className="layer-select-label" style={{ marginBottom: 0 }}>
          Coverage
        </span>
        <span className="coverage-counts">
          <span className="flag public">{liveCount} live</span>
          <span className="flag gap">{gapCount} linked / gap</span>
        </span>
      </button>
      {open && (
        <ul className="coverage-list">
          {live.map((layer) => (
            <li key={layer.id} className="coverage-item">
              {onToggleLayer &&
              ["vdl", "public_crown", "boundaries", "cell_grid"].includes(
                layer.id,
              ) ? (
                <button
                  type="button"
                  className={
                    activeLayerIds.includes(layer.id)
                      ? "coverage-name toggle on"
                      : "coverage-name toggle"
                  }
                  onClick={() => onToggleLayer(layer.id)}
                  title={layer.description}
                >
                  {layer.label}
                </button>
              ) : (
                <span className="coverage-name" title={layer.description}>
                  {layer.label}
                </span>
              )}
              <span className="flag public">live</span>
              {layer.source_url && (
                <a
                  href={layer.source_url}
                  target="_blank"
                  rel="noreferrer"
                  className="coverage-src"
                >
                  source
                </a>
              )}
            </li>
          ))}
          {gaps.map((layer) => (
            <li key={layer.id} className="coverage-item">
              <span className="coverage-name" title={layer.description}>
                {layer.label}
              </span>
              <span className={layer.status === "linked" ? "flag band-mid" : "flag gap"}>
                {layer.status}
              </span>
              {layer.source_url && (
                <a
                  href={layer.source_url}
                  target="_blank"
                  rel="noreferrer"
                  className="coverage-src"
                >
                  source
                </a>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
