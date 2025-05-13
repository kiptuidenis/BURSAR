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
