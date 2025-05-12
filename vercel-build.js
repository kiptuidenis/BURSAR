const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log("Starting Vercel build process...");

// Create required directories
const dirs = ['staticfiles', 'public'];
dirs.forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`Created ${dir} directory`);
  }
});

try {
  // Install Python dependencies
  console.log("Installing Python dependencies...");
  execSync('pip install -r requirements.txt', { stdio: 'inherit' });
  
  // Run static file collection
  console.log("Collecting static files...");
  execSync('python collect_static.py', { stdio: 'inherit' });
  
  // Try to copy index.html as fallback
  try {
    if (fs.existsSync('public/index.html')) {
      fs.copyFileSync('public/index.html', 'staticfiles/index.html');
      console.log("Copied public/index.html to staticfiles/index.html");
    }
  } catch (copyError) {
    console.log("No public/index.html to copy or copy failed:", copyError.message);
    
    // Create a default index.html if it doesn't exist
    if (!fs.existsSync('staticfiles/index.html')) {
      fs.writeFileSync(
        'staticfiles/index.html', 
        '<html><body>Static files will be served here</body></html>'
      );
      console.log("Created default index.html in staticfiles directory");
    }
  }
  
  console.log("Build completed successfully");
} catch (error) {
  console.error("Build failed:", error.message);
  process.exit(1);
}
