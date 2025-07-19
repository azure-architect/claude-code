#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');

function formatJavaScriptFile(filePath) {
    try {
        // Check if prettier is available
        try {
            execSync('which prettier', { stdio: 'ignore' });
        } catch {
            return 'Prettier not found. Install with: npm install -g prettier';
        }
        
        // Run prettier formatter
        execSync(`prettier --write "${filePath}"`, { stdio: 'pipe' });
        
        // Check if ESLint is available for linting
        try {
            execSync('which eslint', { stdio: 'ignore' });
            const eslintResult = execSync(`eslint "${filePath}"`, { 
                encoding: 'utf8',
                stdio: 'pipe' 
            });
            
            if (eslintResult.trim()) {
                return `ESLint issues:\n${eslintResult}`;
            }
        } catch (eslintError) {
            // ESLint found issues or not installed
            if (eslintError.status === 1) {
                return `ESLint issues:\n${eslintError.stdout}`;
            }
            // ESLint not installed - that's ok, just skip
        }
        
        return null;
    } catch (error) {
        return `Error formatting ${filePath}: ${error.message}`;
    }
}

function processFile(filePath) {
    const ext = filePath.split('.').pop().toLowerCase();
    
    if (ext === 'js' || ext === 'jsx') {
        return formatJavaScriptFile(filePath);
    }
    
    return null;
}

try {
    let input = '';
    process.stdin.on('data', chunk => input += chunk);
    process.stdin.on('end', () => {
        const inputData = JSON.parse(input);
        const toolName = inputData.tool_name || '';
        const toolInput = inputData.tool_input || {};
        
        let filePath = '';
        
        if (toolName === 'Write') {
            filePath = toolInput.file_path || '';
        } else if (toolName === 'Edit') {
            filePath = toolInput.file_path || '';
        } else if (toolName === 'MultiEdit') {
            const edits = toolInput.edits || [];
            if (edits.length > 0 && edits[0].file_path) {
                filePath = edits[0].file_path;
            }
        }
        
        if (filePath) {
            const issues = processFile(filePath);
            if (issues) {
                const jsonResponse = {
                    decision: 'block',
                    reason: `JavaScript file formatting issues detected:\n${issues}\nPlease fix these issues before proceeding.`
                };
                console.log(JSON.stringify(jsonResponse));
                process.exit(0); // Use exit code 0 with JSON response
            }
        }
        
        process.exit(0); // No issues
    });
} catch (error) {
    console.error(`Hook error: ${error.message}`);
    process.exit(1); // Non-blocking error
}