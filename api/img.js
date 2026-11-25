/* Serves the site's photography. The GitHub write path used for this
   repo is text-only, so the photo bytes live in _imgdata.js as base64
   string chunks (array-join format) and are decoded here — the same
   pattern the flagship uses for its embedded image modules.
   Usage: /api/img?n=hero-kitchen · /api/img?n=city-van            */
const DATA = require('./_imgdata');

module.exports = function (req, res) {
  const name = (req.query && req.query.n) || '';
  const item = DATA[name];
  if (!item) {
    res.statusCode = 404;
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.end('image not found');
    return;
  }
  const buf = Buffer.from(item.b64, 'base64');
  res.statusCode = 200;
  res.setHeader('Content-Type', item.type);
  res.setHeader('Content-Length', buf.length);
  res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
  res.end(buf);
};
