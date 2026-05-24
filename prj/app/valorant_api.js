import HenrikDevValorantAPI from "unofficial-valorant-api";

const api = new HenrikDevValorantAPI(process.env.HENRIKDEV_KEY);

/**
 * Only inputs: Riot ID (name#tag).
 * Everything else is derived automatically.
 */
export async function getValorantProfile({ name, tag }) {
  // 1) Account lookup (gives you region + puuid)
  const { data: acc } = await api.getAccount({ name, tag });

  // 2) MMR lookup (by puuid + region)
  const mmrRes = await api.getMMRByPUUID({
    version: "v1",
    region: acc.region,
    puuid: acc.puuid,
  });

  // 3) Return a single normalized object (easy for your app to consume)
  return {
    riot_id: `${acc.name}#${acc.tag}`,
    region: acc.region,
    puuid: acc.puuid,
    account_level: acc.account_level,
    card: acc.card,
    last_update: mmrRes?.data?.last_update, // depends on endpoint response
    mmr: mmrRes?.data,
    raw: {
      account: acc,
      mmr: mmrRes,
    },
  };
}

async function pushToDjango(profile) {
  const res = await fetch("http://127.0.0.1:8000/api/upsert_player/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });

  if (!res.ok) {
    throw new Error(`Django upsert failed: ${res.status} ${await res.text()}`);
  }
  return res.json();
}

// example usage:
const profile = await getValorantProfile({ name: "ibreedfemboys", tag: "069" });
try {
  const upsertRes = await pushToDjango(profile);
  console.log("Upsert result:", upsertRes);
} catch (err) {
  console.error("Upsert failed:", err);
}
console.dir(profile, { depth: null });