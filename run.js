#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// Get the directory where the script is located
const scriptDir = __dirname;

// Path to the Python script
const pythonScript = path.join(scriptDir, 'mcp_server.py');

// Spawn Python process
const pythonProcess = spawn('python', [pythonScript], {
  stdio: ['pipe', 'pipe', 'pipe']
});

// Forward stdin to Python process
process.stdin.pipe(pythonProcess.stdin);

// Forward Python stdout to process stdout
pythonProcess.stdout.pipe(process.stdout);

// Forward Python stderr to process stderr
pythonProcess.stderr.pipe(process.stderr);

// Handle process termination
pythonProcess.on('close', (code) => {
  process.exit(code);
});

// Handle errors
pythonProcess.on('error', (err) => {
  console.error('Failed to start Python process:', err);
  process.exit(1);
}); 