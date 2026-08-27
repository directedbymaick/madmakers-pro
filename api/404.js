const fs = require('fs');
const path = require('path');

module.exports = function handler(request, response) {
  const page = fs.readFileSync(path.join(process.cwd(), 'carnet-plein', 'site', '404.html'), 'utf8');
  response.statusCode = 404;
  response.setHeader('Content-Type', 'text/html; charset=utf-8');
  response.end(page);
};
