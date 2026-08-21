const number = new Intl.NumberFormat("en-US");
const percent = value => `${(value * 100).toFixed(1)}%`;

function escapeHtml(value = "") {
  return value.replace(/[&<>'"]/g, character => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  })[character]);
}

function displayTime(value) {
  if (!value) return "unavailable";
  return new Date(value).toLocaleString([], {dateStyle: "medium", timeStyle: "short"});
}

function latestContent(platform, predicate = () => true) {
  return platform.content.filter(predicate).sort((a, b) =>
    new Date(b.published_at || 0) - new Date(a.published_at || 0)
  )[0];
}

function audienceCards(data) {
  const container = document.querySelector("#platform-grid");
  container.innerHTML = data.platforms.map(platform => {
    const history = data.audience_history[platform.platform] || [];
    const first = history[0]?.followers;
    const delta = platform.followers == null || first == null ? null : platform.followers - first;
    const count = platform.followers == null ? "—" : number.format(platform.followers);
    const deltaText = delta == null ? "No history yet" : `${delta >= 0 ? "+" : ""}${number.format(delta)} since first snapshot`;
    const points = history.map((point, index) => {
      const values = history.map(item => item.followers);
      const min = Math.min(...values);
      const max = Math.max(...values);
      const x = history.length === 1 ? 50 : index * 100 / (history.length - 1);
      const y = max === min ? 50 : 90 - ((point.followers - min) / (max - min)) * 80;
      return `${x},${y}`;
    }).join(" ");
    return `
      <article class="platform-card">
        <div class="card-top"><span>${platform.platform}</span><span class="status ${platform.followers == null ? "missing" : "live"}">${platform.followers == null ? "manual needed" : "tracked"}</span></div>
        <strong>${count}</strong>
        <p>${deltaText}</p>
        <svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
          ${points ? `<polyline points="${points}" />` : ""}
        </svg>
        <small>Updated ${displayTime(platform.captured_at)}</small>
      </article>`;
  }).join("");
}

function funnelCards(data) {
  const youtube = latestContent(data.platforms.find(item => item.platform === "YouTube"));
  const x = latestContent(
    data.platforms.find(item => item.platform === "X"),
    item => item.media?.type === "video"
  );
  const instagram = latestContent(data.platforms.find(item => item.platform === "Instagram"));
  const tiktok = latestContent(data.platforms.find(item => item.platform === "TikTok"));
  const xMedia = x?.media;
  const xStarts = xMedia?.non_public_metrics?.playback_0_count;
  const xComplete = xMedia?.non_public_metrics?.playback_100_count;
  const cards = [
    {
      title: "YouTube Short",
      metrics: [
        ["Public starts", youtube?.public_views],
        ["Engaged views", youtube?.analytics?.engagedViews],
        ["Avg viewed", youtube?.analytics?.averageViewPercentage == null ? null : `${youtube.analytics.averageViewPercentage.toFixed(1)}%`],
        ["Subscribers", youtube?.analytics?.subscribersGained]
      ],
      note: youtube?.analytics ? "Processed Analytics data" : "Watch behavior has not processed yet"
    },
    {
      title: "X native video",
      metrics: [
        ["Impressions", x?.metrics?.impression_count],
        ["Video views", xMedia?.organic_metrics?.view_count],
        ["Starts", xStarts],
        ["Completed", xComplete == null ? null : `${number.format(xComplete)} (${percent(xComplete / xStarts)})`]
      ],
      note: "Starts and qualified views use different definitions"
    },
    {
      title: "Instagram Reel",
      metrics: [
        ["Plays", instagram?.metrics?.views],
        ["Reach", instagram?.metrics?.reach],
        ["Avg watch", instagram?.metrics?.ig_reels_avg_watch_time == null ? null : `${(instagram.metrics.ig_reels_avg_watch_time / 1000).toFixed(1)}s`],
        ["Interactions", instagram?.metrics?.total_interactions]
      ],
      note: "Reach is accounts; plays can include repeats"
    },
    {
      title: "TikTok video",
      metrics: [
        ["Views", tiktok?.metrics?.views],
        ["Likes", tiktok?.metrics?.likes],
        ["Comments", tiktok?.metrics?.comments],
        ["Shares", tiktok?.metrics?.shares]
      ],
      note: "Manually recorded — no working API access for this account yet"
    }
  ];
  document.querySelector("#funnel-grid").innerHTML = cards.map(card => `
    <article class="funnel-card">
      <h3>${card.title}</h3>
      <div class="metric-grid">
        ${card.metrics.map(([label, value]) => `<div><span>${label}</span><strong>${value == null ? "—" : typeof value === "number" ? number.format(value) : value}</strong></div>`).join("")}
      </div>
      <p>${card.note}</p>
    </article>`).join("");
}

function rowMetrics(platform, item) {
  if (platform === "YouTube") {
    const analytics = item.analytics;
    return {
      reach: `${number.format(item.public_views)} public views`,
      consumption: analytics ? `${analytics.averageViewDuration}s avg · ${analytics.averageViewPercentage.toFixed(1)}%` : "processing",
      engagement: `${item.likes} likes · ${item.comments} comments`,
      conversion: analytics ? `${analytics.subscribersGained} subscribers` : "—"
    };
  }
  if (platform === "X") {
    const media = item.media;
    return {
      reach: `${number.format(item.metrics.impression_count || 0)} impressions`,
      consumption: media?.organic_metrics?.view_count == null ? "—" : `${number.format(media.organic_metrics.view_count)} video views`,
      engagement: `${number.format(item.metrics.engagements || 0)} engagements`,
      conversion: `${number.format(item.metrics.user_profile_clicks || 0)} profile clicks`
    };
  }
  if (platform === "TikTok") {
    const m = item.metrics;
    return {
      reach: m.views == null ? "— (manual, not yet recorded)" : `${number.format(m.views)} views`,
      consumption: "—",
      engagement: [
        m.likes == null ? null : `${number.format(m.likes)} likes`,
        m.comments == null ? null : `${number.format(m.comments)} comments`,
        m.shares == null ? null : `${number.format(m.shares)} shares`
      ].filter(Boolean).join(" · ") || "—",
      conversion: "—"
    };
  }
  return {
    reach: `${number.format(item.metrics.reach || 0)} reached · ${number.format(item.metrics.views || 0)} plays`,
    consumption: item.metrics.ig_reels_avg_watch_time == null ? "—" : `${(item.metrics.ig_reels_avg_watch_time / 1000).toFixed(1)}s avg`,
    engagement: `${number.format(item.metrics.total_interactions || 0)} interactions`,
    conversion: "—"
  };
}

function contentTable(data, selected = "All") {
  const rows = data.platforms.flatMap(platform =>
    platform.content.map(item => ({platform: platform.platform, ...item}))
  ).filter(item => selected === "All" || item.platform === selected)
   .sort((a, b) => new Date(b.published_at || 0) - new Date(a.published_at || 0));
  document.querySelector("#content-table").innerHTML = rows.map(item => {
    const metrics = rowMetrics(item.platform, item);
    return `<tr>
      <td><span class="platform-pill">${item.platform}</span></td>
      <td>${displayTime(item.published_at)}</td>
      <td><a href="${item.url}" target="_blank" rel="noreferrer">${escapeHtml(item.title.slice(0, 110))}</a></td>
      <td>${metrics.reach}</td>
      <td>${metrics.consumption}</td>
      <td>${metrics.engagement}</td>
      <td>${metrics.conversion}</td>
    </tr>`;
  }).join("");
}

async function main() {
  const response = await fetch("/api/dashboard", {cache: "no-store"});
  const data = await response.json();
  document.querySelector("#freshness").textContent = `Rendered ${displayTime(data.generated_at)}`;
  audienceCards(data);
  funnelCards(data);
  const names = ["All", ...data.platforms.filter(item => item.content.length).map(item => item.platform)];
  const filters = document.querySelector("#filters");
  filters.innerHTML = names.map((name, index) => `<button class="${index === 0 ? "active" : ""}" data-platform="${name}">${name}</button>`).join("");
  filters.addEventListener("click", event => {
    const button = event.target.closest("button");
    if (!button) return;
    filters.querySelectorAll("button").forEach(item => item.classList.remove("active"));
    button.classList.add("active");
    contentTable(data, button.dataset.platform);
  });
  contentTable(data);
}

main().catch(error => {
  document.querySelector("#freshness").textContent = `Unable to load snapshots: ${error.message}`;
});
