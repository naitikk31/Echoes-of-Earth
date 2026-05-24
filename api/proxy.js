/**
 * Vercel Serverless Proxy for NewsAPI
 *
 * Proxies requests from /api/news/* to https://newsapi.org/*
 * This solves two problems:
 *   1. CORS — NewsAPI doesn't allow browser-origin requests on the free plan
 *   2. Key security — The API key stays server-side, never exposed to the client
 *
 * Environment variable required on Vercel:
 *   NEWS_API_KEY — Your NewsAPI.org API key (do NOT prefix with VITE_)
 */

export default async function handler(req, res) {
  // Only allow GET requests
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const apiKey = process.env.NEWS_API_KEY;
  if (!apiKey) {
    return res.status(500).json({
      error: 'NEWS_API_KEY environment variable is not configured on the server.',
    });
  }

  try {
    // Reconstruct the original path from the request URL
    // The Vercel rewrite sends /api/news/v2/everything?q=... → /api/proxy
    // The original URL is available via the referer or x-vercel-forwarded-for headers,
    // but the simplest approach is to pass the path via query params from the rewrite.
    //
    // Since vercel.json rewrites /api/news/(.*) → /api/proxy,
    // we need to extract the original path. Vercel sets req.url to the rewritten URL
    // but we can also read the x-matched-path header, or we reconstruct from query params.

    // Parse the original URL from the request headers
    const originalUrl = req.headers['x-invoke-path'] || req.url;

    // Get query parameters from the original request
    const url = new URL(req.url, `https://${req.headers.host}`);
    const params = url.searchParams;

    // The client sends the full path like /api/news/v2/everything?q=...&apiKey=CLIENT_KEY
    // We need to rebuild this as: https://newsapi.org/v2/everything?q=...&apiKey=SERVER_KEY

    // Extract the path after /api/news from the forwarded URL
    const forwardedUrl = req.headers['x-forwarded-url'] || req.headers['x-original-url'] || '';
    let newsApiPath = '/v2/everything'; // default fallback

    if (forwardedUrl) {
      const match = forwardedUrl.match(/\/api\/news(\/.*?)(\?|$)/);
      if (match) {
        newsApiPath = match[1];
      }
    }

    // Build the NewsAPI URL with all query params
    const targetUrl = new URL(`https://newsapi.org${newsApiPath}`);

    // Copy all query params from the original request
    for (const [key, value] of params.entries()) {
      if (key === 'apiKey') continue; // Remove client-sent API key
      targetUrl.searchParams.set(key, value);
    }

    // Inject the server-side API key
    targetUrl.searchParams.set('apiKey', apiKey);

    // Make the request to NewsAPI
    const response = await fetch(targetUrl.toString(), {
      headers: {
        'User-Agent': 'EchoesOfEarth/1.0',
      },
    });

    const data = await response.json();

    // Set caching headers (cache for 5 minutes)
    res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate=600');
    res.setHeader('Access-Control-Allow-Origin', '*');

    return res.status(response.status).json(data);
  } catch (error) {
    console.error('[API Proxy] Error:', error.message);
    return res.status(500).json({
      error: 'Failed to fetch from NewsAPI',
      message: error.message,
    });
  }
}
