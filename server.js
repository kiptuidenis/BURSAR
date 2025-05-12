// Server to help route traffic
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.get('*', (req, res) => {
  res.send('Welcome to the BURSAR application');
});

app.listen(port, () => {
  console.log(`Express server listening on port ${port}`);
});
