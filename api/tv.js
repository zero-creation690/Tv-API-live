import fetch from "node-fetch";

export default async function handler(req, res) {
  const search = req.query.search || "";

  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET,OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    res.status(200).end();
    return;
  }

  try {
    const response = await fetch(`https://tv-chi-eosin.vercel.app/tv?search=${encodeURIComponent(search)}`);
    const data = await response.json();

    // Enable CORS
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET,OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");

    res.status(200).json(data);
  } catch (error) {
    console.error("Error fetching upstream API:", error);
    res.status(500).json({ error: "Failed to fetch upstream API" });
  }
}
