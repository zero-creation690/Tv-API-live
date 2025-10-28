export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS, POST');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    const { search, url } = req.query;

    // If no search parameter, return usage info
    if (!search && !url) {
      return res.status(200).json({
        message: 'TV Proxy API is running',
        usage: {
          search: '/api/tv?search=ChannelName',
          direct: '/api/proxy?url=https://original-api-url'
        },
        endpoints: {
          tv_search: '/api/tv?search=YourSearchTerm',
          direct_proxy: '/api/proxy?url=EncodedURL'
        }
      });
    }

    let targetUrl;
    
    if (url) {
      // Direct URL proxy
      targetUrl = decodeURIComponent(url);
    } else {
      // TV API proxy
      targetUrl = `https://tv-chi-eosin.vercel.app/tv?search=${encodeURIComponent(search)}`;
    }

    // Fetch from target API with timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

    const response = await fetch(targetUrl, {
      signal: controller.signal,
      headers: {
        'User-Agent': 'TV-Proxy-API/1.0'
      }
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      return res.status(response.status).json({
        error: 'Upstream API error',
        status: response.status,
        statusText: response.statusText
      });
    }

    const data = await response.json();

    // Success response
    res.status(200).json({
      success: true,
      data: data,
      proxy_metadata: {
        timestamp: new Date().toISOString(),
        cors_enabled: true
      }
    });

  } catch (error) {
    console.error('Proxy Error:', error);

    if (error.name === 'AbortError') {
      return res.status(504).json({
        error: 'Gateway Timeout',
        message: 'Request to upstream API timed out'
      });
    }

    res.status(500).json({
      error: 'Proxy Error',
      message: error.message
    });
  }
}
