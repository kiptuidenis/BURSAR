const fs = require('fs');
const path = require('path');

console.log("Starting Vercel build process...");

// Create required directories
const dirs = ['staticfiles'];
dirs.forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`Created ${dir} directory`);
  }
});

try {
  // Source and destination directories
  const sourceDir = path.join(process.cwd(), 'app', 'static');
  const destDir = path.join(process.cwd(), 'staticfiles');

  // Ensure favicon.ico exists
  const faviconSource = path.join(sourceDir, 'favicon.ico');
  const faviconDest = path.join(destDir, 'favicon.ico');
  if (!fs.existsSync(faviconSource)) {
    console.log('Creating default favicon.ico...');
    // Create a simple 16x16 transparent ICO file
    const icoHeader = Buffer.from([
      0x00, 0x00,             // Reserved
      0x01, 0x00,             // ICO format
      0x01, 0x00,             // 1 image
      0x10, 0x10,             // 16x16 pixels
      0x00,                   // No color palette
      0x00,                   // Reserved
      0x01, 0x00,             // 1 color plane
      0x20, 0x00,             // 32 bits per pixel
      0x28, 0x00, 0x00, 0x00, // Size of bitmap data
      0x16, 0x00, 0x00, 0x00, // Offset to bitmap data
      0x28, 0x00, 0x00, 0x00  // BITMAPINFOHEADER size
    ]);
    // Create 16x16 transparent pixels (all zeros)
    const pixels = Buffer.alloc(16 * 16 * 4, 0);
    fs.writeFileSync(faviconSource, Buffer.concat([icoHeader, pixels]));
  }

  // Copy static files if source directory exists
  if (fs.existsSync(sourceDir)) {
    console.log('Copying static files...');
    copyRecursive(sourceDir, destDir);
  } else {
    console.log('No static directory found, creating default files...');
  }

  // Create default index.html if it doesn't exist
  const indexPath = path.join(destDir, 'index.html');
  if (!fs.existsSync(indexPath)) {
    fs.writeFileSync(
      indexPath,
      '<html><body>Static files will be served here</body></html>'
    );
    console.log('Created default index.html');
  }

  console.log('Build completed successfully');
} catch (error) {
  console.error('Build failed:', error.message);
  process.exit(1);
}

// Helper function to copy files recursively
function copyRecursive(src, dest) {
  if (fs.statSync(src).isDirectory()) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    const files = fs.readdirSync(src);
    for (const file of files) {
      const srcPath = path.join(src, file);
      const destPath = path.join(dest, file);
      copyRecursive(srcPath, destPath);
    }
  } else {
    fs.copyFileSync(src, dest);
    console.log(`Copied: ${path.relative(process.cwd(), dest)}`);
  }
}
